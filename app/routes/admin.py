from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import AdminUser, Wing, Nominee, Voter, Vote, Result, ConfigSetting, ArchivedElection
import json
from sqlalchemy import func

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin/login.html')


@bp.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('voting.landing'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics
    total_voters = Voter.query.count()
    total_nominees = Nominee.query.count()
    total_wings = Wing.query.filter_by(is_active=True).count()

    # Voting progress by wing
    wing_stats = db.session.query(
        Wing.name,
        func.count(Voter.id).label('votes_cast')
    ).outerjoin(Voter).group_by(Wing.id, Wing.name).all()

    # Nominee count by gender
    male_nominees = Nominee.query.filter_by(gender='male').count()
    female_nominees = Nominee.query.filter_by(gender='female').count()

    # Recent voters
    recent_voters = Voter.query.order_by(Voter.voted_at.desc()).limit(10).all()

    # Check if results declared
    results_declared = Result.query.first() is not None

    return render_template('admin/dashboard.html',
                           total_voters=total_voters,
                           total_nominees=total_nominees,
                           total_wings=total_wings,
                           wing_stats=wing_stats,
                           male_nominees=male_nominees,
                           female_nominees=female_nominees,
                           recent_voters=recent_voters,
                           results_declared=results_declared)


@bp.route('/wings')
@login_required
def wings():
    """Manage wings"""
    all_wings = Wing.query.order_by(Wing.name).all()
    return render_template('admin/wings.html', wings=all_wings)


@bp.route('/wings/add', methods=['POST'])
@login_required
def add_wing():
    """Add new wing"""
    wing_name = request.form.get('wing_name', '').strip()

    if not wing_name:
        flash('Wing name is required', 'error')
        return redirect(url_for('admin.wings'))

    # Check if wing already exists
    existing = Wing.query.filter_by(name=wing_name).first()
    if existing:
        flash(f'Wing "{wing_name}" already exists', 'error')
        return redirect(url_for('admin.wings'))

    new_wing = Wing(name=wing_name)
    db.session.add(new_wing)
    db.session.commit()

    flash(f'Wing "{wing_name}" added successfully', 'success')
    return redirect(url_for('admin.wings'))


@bp.route('/wings/<int:wing_id>/delete', methods=['POST'])
@login_required
def delete_wing(wing_id):
    """Delete a wing"""
    wing = Wing.query.get_or_404(wing_id)

    # Check if wing has nominees
    if wing.nominees:
        flash(f'Cannot delete wing "{wing.name}" because it has nominees. Delete nominees first.', 'error')
        return redirect(url_for('admin.wings'))

    # Check if wing has voters
    if wing.voters:
        flash(f'Cannot delete wing "{wing.name}" because it has voting records.', 'error')
        return redirect(url_for('admin.wings'))

    wing_name = wing.name
    db.session.delete(wing)
    db.session.commit()

    flash(f'Wing "{wing_name}" deleted successfully', 'success')
    return redirect(url_for('admin.wings'))


@bp.route('/nominees')
@login_required
def nominees():
    """Manage nominees"""
    wing_filter = request.args.get('wing', type=int)

    query = Nominee.query.join(Wing)

    if wing_filter:
        query = query.filter(Nominee.wing_id == wing_filter)

    all_nominees = query.order_by(Wing.name, Nominee.gender, Nominee.name).all()
    all_wings = Wing.query.filter_by(is_active=True).order_by(Wing.name).all()

    return render_template('admin/nominees.html',
                           nominees=all_nominees,
                           wings=all_wings,
                           selected_wing=wing_filter)


@bp.route('/nominees/add', methods=['POST'])
@login_required
def add_nominee():
    """Add new nominee"""
    name = request.form.get('name', '').strip()
    gender = request.form.get('gender')
    flat_number = request.form.get('flat_number', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    wing_id = request.form.get('wing_id', type=int)

    # Validation
    if not all([name, gender, flat_number, phone_number, wing_id]):
        flash('All fields are required', 'error')
        return redirect(url_for('admin.nominees'))

    if gender not in ['male', 'female']:
        flash('Invalid gender', 'error')
        return redirect(url_for('admin.nominees'))

    # Check if wing exists
    wing = Wing.query.get(wing_id)
    if not wing:
        flash('Invalid wing selected', 'error')
        return redirect(url_for('admin.nominees'))

    new_nominee = Nominee(
        name=name,
        gender=gender,
        flat_number=flat_number,
        phone_number=phone_number,
        wing_id=wing_id
    )

    db.session.add(new_nominee)
    db.session.commit()

    flash(f'Nominee "{name}" added successfully', 'success')
    return redirect(url_for('admin.nominees'))


@bp.route('/nominees/<int:nominee_id>/delete', methods=['POST'])
@login_required
def delete_nominee(nominee_id):
    """Delete a nominee"""
    nominee = Nominee.query.get_or_404(nominee_id)

    # Check if nominee has votes
    if nominee.votes:
        flash(f'Cannot delete nominee "{nominee.name}" because votes have been cast for them.', 'error')
        return redirect(url_for('admin.nominees'))

    nominee_name = nominee.name
    db.session.delete(nominee)
    db.session.commit()

    flash(f'Nominee "{nominee_name}" deleted successfully', 'success')
    return redirect(url_for('admin.nominees'))


@bp.route('/nominees/upload', methods=['GET', 'POST'])
@login_required
def upload_nominees():
    """Upload nominees from Excel file"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('admin.upload_nominees'))

        file = request.files['file']

        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('admin.upload_nominees'))

        # Validate file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            flash('Please upload an Excel file (.xlsx or .xls)', 'error')
            return redirect(url_for('admin.upload_nominees'))

        # Process file
        from app.utils.excel_import import import_nominees_from_excel

        try:
            success_count, error_count, errors = import_nominees_from_excel(file)

            # Show results
            if success_count > 0:
                flash(f'Successfully imported {success_count} nominee(s)', 'success')

            if error_count > 0:
                flash(f'{error_count} error(s) occurred during import', 'warning')

                # Show first 5 errors
                for error in errors[:5]:
                    flash(error, 'error')

                if len(errors) > 5:
                    flash(f'... and {len(errors) - 5} more error(s)', 'error')

            return redirect(url_for('admin.nominees'))

        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('admin.upload_nominees'))

    # GET request - show upload form
    return render_template('admin/upload_nominees.html')


@bp.route('/progress')
@login_required
def progress():
    """View voting progress"""
    # Get all wings with their voting stats
    wing_progress = []

    for wing in Wing.query.filter_by(is_active=True).order_by(Wing.name).all():
        male_nominees = Nominee.query.filter_by(wing_id=wing.id, gender='male').count()
        female_nominees = Nominee.query.filter_by(wing_id=wing.id, gender='female').count()
        votes_cast = Voter.query.filter_by(wing_id=wing.id).count()

        wing_progress.append({
            'wing': wing,
            'male_nominees': male_nominees,
            'female_nominees': female_nominees,
            'votes_cast': votes_cast
        })

    return render_template('admin/progress.html', wing_progress=wing_progress)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Manage configuration settings"""
    if request.method == 'POST':
        voting_enabled = request.form.get('voting_enabled') == 'on'
        results_visible = request.form.get('results_visible') == 'on'
        winners_per_gender = request.form.get('winners_per_gender', '2')

        ConfigSetting.set_value('voting_enabled', 'true' if voting_enabled else 'false')
        ConfigSetting.set_value('results_visible', 'true' if results_visible else 'false')
        ConfigSetting.set_value('winners_per_gender', winners_per_gender)

        flash('Settings updated successfully', 'success')
        return redirect(url_for('admin.settings'))

    # Get current settings
    current_settings = {
        'voting_enabled': ConfigSetting.is_voting_enabled(),
        'results_visible': ConfigSetting.are_results_visible(),
        'winners_per_gender': ConfigSetting.get_winners_per_gender()
    }

    return render_template('admin/config.html', settings=current_settings)


@bp.route('/declare-results', methods=['POST'])
@login_required
def declare_results():
    """Calculate and declare results"""
    from app.models import Result
    from sqlalchemy import func

    # Clear previous results
    Result.query.delete()

    # Calculate results for each wing and gender
    wings = Wing.query.filter_by(is_active=True).all()
    winners_per_gender = ConfigSetting.get_winners_per_gender()

    for wing in wings:
        for gender in ['male', 'female']:
            # Get all nominees for this wing and gender
            nominees = Nominee.query.filter_by(wing_id=wing.id, gender=gender).all()
            nominee_count = len(nominees)

            # Handle edge case: no nominees
            if nominee_count == 0:
                # No nominees - seat remains empty, nothing to record
                continue

            # Handle edge case: fewer nominees than winner slots
            if nominee_count <= winners_per_gender:
                # Auto-select all nominees as winners
                for rank, nominee in enumerate(nominees, 1):
                    # Get actual vote count (even if they auto-win)
                    vote_count = Vote.query.filter_by(nominee_id=nominee.id).count()

                    result = Result(
                        wing_id=wing.id,
                        nominee_id=nominee.id,
                        gender=gender,
                        vote_count=vote_count,
                        rank=rank,
                        is_winner=True  # All are winners when not enough nominees
                    )
                    db.session.add(result)
            else:
                # Normal case: more nominees than winner slots
                # Count votes for each nominee
                vote_counts = db.session.query(
                    Nominee.id,
                    Nominee.name,
                    func.count(Vote.id).label('vote_count')
                ).outerjoin(Vote).filter(
                    Nominee.wing_id == wing.id,
                    Nominee.gender == gender
                ).group_by(Nominee.id, Nominee.name).order_by(
                    func.count(Vote.id).desc(),
                    Nominee.name
                ).all()

                # Create result records - top N are winners
                for rank, (nominee_id, name, vote_count) in enumerate(vote_counts, 1):
                    result = Result(
                        wing_id=wing.id,
                        nominee_id=nominee_id,
                        gender=gender,
                        vote_count=vote_count,
                        rank=rank,
                        is_winner=(rank <= winners_per_gender)
                    )
                    db.session.add(result)

    db.session.commit()

    # Make results visible
    ConfigSetting.set_value('results_visible', 'true')

    flash('Results declared successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
