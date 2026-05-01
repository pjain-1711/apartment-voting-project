# Additional admin routes for password change, archiving, and new elections
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import AdminUser, Wing, Nominee, Voter, Vote, Result, ArchivedElection
import json
from datetime import datetime

bp = Blueprint('admin_extra', __name__, url_prefix='/admin')


@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change admin password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin_extra.change_password'))

        # Check current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('admin_extra.change_password'))

        # Check new password match
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('admin_extra.change_password'))

        # Check password strength
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long', 'error')
            return redirect(url_for('admin_extra.change_password'))

        # Update password
        current_user.set_password(new_password)
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/change_password.html')


@bp.route('/archive-election', methods=['GET', 'POST'])
@login_required
def archive_election():
    """Archive current election results"""
    if request.method == 'POST':
        election_name = request.form.get('election_name', '').strip()

        if not election_name:
            flash('Election name is required', 'error')
            return redirect(url_for('admin_extra.archive_election'))

        # Check if there's data to archive
        total_votes = Voter.query.count()
        if total_votes == 0:
            flash('No voting data to archive', 'error')
            return redirect(url_for('admin_extra.archive_election'))

        # Collect all election data
        election_data = {
            'election_name': election_name,
            'archived_at': datetime.utcnow().isoformat(),
            'wings': [],
            'nominees': [],
            'votes': [],
            'results': []
        }

        # Collect wings
        for wing in Wing.query.all():
            election_data['wings'].append({
                'id': wing.id,
                'name': wing.name,
                'is_active': wing.is_active
            })

        # Collect nominees
        for nominee in Nominee.query.all():
            election_data['nominees'].append({
                'id': nominee.id,
                'name': nominee.name,
                'gender': nominee.gender,
                'flat_number': nominee.flat_number,
                'phone_number': nominee.phone_number,
                'wing_id': nominee.wing_id
            })

        # Collect votes (anonymized for storage)
        for voter in Voter.query.all():
            voter_votes = Vote.query.filter_by(voter_id=voter.id).all()
            election_data['votes'].append({
                'counter_number': voter.counter_number,
                'flat_number': voter.flat_number,
                'wing_id': voter.wing_id,
                'voted_at': voter.voted_at.isoformat(),
                'nominees_voted': [vote.nominee_id for vote in voter_votes]
            })

        # Collect results
        for result in Result.query.all():
            election_data['results'].append({
                'wing_id': result.wing_id,
                'nominee_id': result.nominee_id,
                'gender': result.gender,
                'vote_count': result.vote_count,
                'rank': result.rank,
                'is_winner': result.is_winner
            })

        # Save to database
        total_nominees = Nominee.query.count()
        archive = ArchivedElection(
            election_name=election_name,
            election_data=json.dumps(election_data),
            total_votes=total_votes,
            total_nominees=total_nominees
        )
        db.session.add(archive)
        db.session.commit()

        flash(f'Election "{election_name}" archived successfully!', 'success')
        return redirect(url_for('admin_extra.view_archives'))

    # Show preview of current data
    total_votes = Voter.query.count()
    total_nominees = Nominee.query.count()
    total_wings = Wing.query.count()

    return render_template('admin/archive_election.html',
                           total_votes=total_votes,
                           total_nominees=total_nominees,
                           total_wings=total_wings)


@bp.route('/archives')
@login_required
def view_archives():
    """View all archived elections"""
    archives = ArchivedElection.query.order_by(ArchivedElection.archived_at.desc()).all()
    return render_template('admin/archives.html', archives=archives)


@bp.route('/archives/<int:archive_id>')
@login_required
def view_archive_detail(archive_id):
    """View details of a specific archived election"""
    archive = ArchivedElection.query.get_or_404(archive_id)
    election_data = json.loads(archive.election_data)

    return render_template('admin/archive_detail.html',
                           archive=archive,
                           election_data=election_data)


@bp.route('/archives/<int:archive_id>/delete', methods=['POST'])
@login_required
def delete_archive(archive_id):
    """Delete an archived election"""
    archive = ArchivedElection.query.get_or_404(archive_id)
    election_name = archive.election_name

    db.session.delete(archive)
    db.session.commit()

    flash(f'Archived election "{election_name}" deleted successfully', 'success')
    return redirect(url_for('admin_extra.view_archives'))


@bp.route('/new-election', methods=['GET', 'POST'])
@login_required
def new_election():
    """Start a new election"""
    if request.method == 'POST':
        reset_option = request.form.get('reset_option')
        confirm = request.form.get('confirm') == 'yes'

        if not confirm:
            flash('Please confirm to start a new election', 'error')
            return redirect(url_for('admin_extra.new_election'))

        if reset_option == 'keep_nominees':
            # Delete only votes and results, keep wings and nominees
            Vote.query.delete()
            Voter.query.delete()
            Result.query.delete()

            flash('New election started! Votes cleared, nominees and wings retained.', 'success')

        elif reset_option == 'keep_wings':
            # Delete votes, results, and nominees, keep only wings
            Vote.query.delete()
            Voter.query.delete()
            Result.query.delete()
            Nominee.query.delete()

            flash('New election started! All data cleared except wings.', 'success')

        elif reset_option == 'full_reset':
            # Delete everything except admin users and config
            Vote.query.delete()
            Voter.query.delete()
            Result.query.delete()
            Nominee.query.delete()
            Wing.query.delete()

            flash('New election started! All election data cleared.', 'success')

        else:
            flash('Invalid reset option', 'error')
            return redirect(url_for('admin_extra.new_election'))

        # Reset configuration
        from app.models import ConfigSetting
        ConfigSetting.set_value('voting_enabled', 'true')
        ConfigSetting.set_value('results_visible', 'false')

        db.session.commit()

        return redirect(url_for('admin.dashboard'))

    # Show current data before reset
    total_votes = Voter.query.count()
    total_nominees = Nominee.query.count()
    total_wings = Wing.query.count()

    return render_template('admin/new_election.html',
                           total_votes=total_votes,
                           total_nominees=total_nominees,
                           total_wings=total_wings)
