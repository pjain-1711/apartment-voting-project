from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db, limiter
from app.models import Wing, Nominee, Voter, Vote, ConfigSetting
from app.utils.validators import (
    has_already_voted,
    get_nominees_by_wing_and_gender,
    get_next_counter_number,
    validate_vote_selection,
    extract_wing_from_flat
)

bp = Blueprint('voting', __name__)


@bp.route('/')
def landing():
    """Landing page with options for Voting or Admin"""
    return render_template('landing.html')


@bp.route('/vote')
def index():
    """Voting page - voter information form"""
    voting_enabled = ConfigSetting.is_voting_enabled()

    return render_template('voting/voter_info.html',
                           voting_enabled=voting_enabled)


@bp.route('/vote', methods=['POST'])
@limiter.limit("5 per hour")
def vote():
    """Handle voter information and show nominees"""
    # Check if voting is enabled
    if not ConfigSetting.is_voting_enabled():
        flash('Voting is currently disabled', 'error')
        return redirect(url_for('voting.index'))

    # Get voter information
    voter_name = request.form.get('voter_name', '').strip()
    flat_number = request.form.get('flat_number', '').strip()

    # Validation
    if not all([voter_name, flat_number]):
        flash('All fields are required', 'error')
        return redirect(url_for('voting.index'))

    # Extract wing from flat number
    wing_id, error = extract_wing_from_flat(flat_number)
    if error:
        flash(error, 'error')
        return redirect(url_for('voting.index'))

    # Check if wing exists (already validated in extract_wing_from_flat)
    wing = Wing.query.get(wing_id)

    # Check if flat has already voted
    if has_already_voted(flat_number, wing_id):
        return render_template('voting/already_voted.html',
                               flat_number=flat_number,
                               wing_name=wing.name)

    # Get nominees for this wing
    nominees = get_nominees_by_wing_and_gender(wing_id)

    # Check if there are any nominees
    if len(nominees['male']) == 0 and len(nominees['female']) == 0:
        flash('There are no nominees for your wing. Please contact the admin.', 'error')
        return redirect(url_for('voting.index'))

    # Store voter info and timer start time in session
    from datetime import datetime
    session['voter_info'] = {
        'name': voter_name,
        'flat_number': flat_number,
        'wing_id': wing_id
    }
    session['timer_start'] = datetime.utcnow().timestamp()

    return render_template('voting/vote_selection.html',
                           voter_name=voter_name,
                           wing_name=wing.name,
                           male_nominees=nominees['male'],
                           female_nominees=nominees['female'])


@bp.route('/confirm', methods=['POST'])
def confirm():
    """Show confirmation page before final submission"""
    # Check session
    voter_info = session.get('voter_info')
    timer_start = session.get('timer_start')

    if not voter_info or not timer_start:
        flash('Session expired. Please start again.', 'error')
        return redirect(url_for('voting.index'))

    # Check if timer has expired (2 minutes = 120 seconds)
    from datetime import datetime
    elapsed_time = datetime.utcnow().timestamp() - timer_start
    if elapsed_time > 120:
        session.clear()
        flash('Voting time expired. Please start again.', 'error')
        return redirect(url_for('voting.index'))

    # Get selected nominees (now multiple selections allowed)
    male_nominee_ids = request.form.getlist('male_nominee_ids', type=int)
    female_nominee_ids = request.form.getlist('female_nominee_ids', type=int)

    wing_id = voter_info['wing_id']

    # Validate selection
    is_valid, error_message = validate_vote_selection(male_nominee_ids, female_nominee_ids, wing_id)
    if not is_valid:
        flash(error_message, 'error')
        return redirect(url_for('voting.index'))

    # Get nominee details for confirmation
    male_nominees = [Nominee.query.get(nid) for nid in male_nominee_ids] if male_nominee_ids else []
    female_nominees = [Nominee.query.get(nid) for nid in female_nominee_ids] if female_nominee_ids else []

    # Store selections in session
    session['vote_selection'] = {
        'male_nominee_ids': male_nominee_ids,
        'female_nominee_ids': female_nominee_ids
    }

    return render_template('voting/confirmation.html',
                           voter_info=voter_info,
                           male_nominees=male_nominees,
                           female_nominees=female_nominees)


@bp.route('/submit', methods=['POST'])
def submit():
    """Final vote submission"""
    # Check if voting is enabled
    if not ConfigSetting.is_voting_enabled():
        flash('Voting is currently disabled', 'error')
        return redirect(url_for('voting.index'))

    # Get voter info and selection from session
    voter_info = session.get('voter_info')
    vote_selection = session.get('vote_selection')
    timer_start = session.get('timer_start')

    if not voter_info or not vote_selection or not timer_start:
        flash('Session expired. Please start again.', 'error')
        return redirect(url_for('voting.index'))

    # Final timer check before submission
    from datetime import datetime
    elapsed_time = datetime.utcnow().timestamp() - timer_start
    if elapsed_time > 120:
        session.clear()
        flash('Voting time expired. Your vote was not recorded.', 'error')
        return redirect(url_for('voting.index'))

    # Double-check for duplicate vote (in case of multiple tabs)
    if has_already_voted(voter_info['flat_number'], voter_info['wing_id']):
        flash('This flat has already voted.', 'error')
        session.clear()
        return redirect(url_for('voting.index'))

    try:
        # Create voter record
        counter_number = get_next_counter_number()

        voter = Voter(
            name=voter_info['name'],
            flat_number=voter_info['flat_number'],
            wing_id=voter_info['wing_id'],
            phone_number='',  # No longer collected
            counter_number=counter_number
        )
        db.session.add(voter)
        db.session.flush()  # Get voter ID

        # Create vote records (multiple votes now supported)
        for male_nominee_id in vote_selection.get('male_nominee_ids', []):
            if male_nominee_id:
                male_vote = Vote(
                    voter_id=voter.id,
                    nominee_id=male_nominee_id
                )
                db.session.add(male_vote)

        for female_nominee_id in vote_selection.get('female_nominee_ids', []):
            if female_nominee_id:
                female_vote = Vote(
                    voter_id=voter.id,
                    nominee_id=female_nominee_id
                )
                db.session.add(female_vote)

        db.session.commit()

        # Clear session
        session.pop('voter_info', None)
        session.pop('vote_selection', None)

        # Show success page with counter number
        return render_template('voting/success.html', counter_number=counter_number)

    except Exception as e:
        db.session.rollback()
        flash('An error occurred while recording your vote. Please try again.', 'error')
        return redirect(url_for('voting.index'))
