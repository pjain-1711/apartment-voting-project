from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask_login import login_required
from app.models import Result, Wing, ConfigSetting
from app.utils.excel_export import create_anonymous_export, create_detailed_export, create_results_export
import io
from datetime import datetime

bp = Blueprint('results', __name__, url_prefix='/results')


@bp.route('/')
def view_results():
    """View election results"""
    # Check if results are visible
    if not ConfigSetting.are_results_visible():
        return render_template('results/results.html',
                               results_available=False,
                               wing_results=[])

    # Get results grouped by wing
    wings = Wing.query.filter_by(is_active=True).order_by(Wing.name).all()
    wing_results = []

    for wing in wings:
        male_results = Result.query.filter_by(
            wing_id=wing.id,
            gender='male'
        ).order_by(Result.rank).all()

        female_results = Result.query.filter_by(
            wing_id=wing.id,
            gender='female'
        ).order_by(Result.rank).all()

        wing_results.append({
            'wing': wing,
            'male_results': male_results,
            'female_results': female_results
        })

    return render_template('results/results.html',
                           results_available=True,
                           wing_results=wing_results)


@bp.route('/export/anonymous')
@login_required
def export_anonymous():
    """Export anonymous votes to Excel"""
    try:
        workbook = create_anonymous_export()

        # Save to BytesIO object
        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)

        filename = f'anonymous_votes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        flash('Error generating export file', 'error')
        return redirect(url_for('admin.dashboard'))


@bp.route('/export/detailed')
@login_required
def export_detailed():
    """Export detailed votes to Excel (includes voter information)"""
    try:
        workbook = create_detailed_export()

        # Save to BytesIO object
        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)

        filename = f'detailed_votes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        flash('Error generating export file', 'error')
        return redirect(url_for('admin.dashboard'))


@bp.route('/export/results')
@login_required
def export_results():
    """Export election results to Excel"""
    if not ConfigSetting.are_results_visible():
        flash('Results have not been declared yet', 'error')
        return redirect(url_for('admin.dashboard'))

    try:
        workbook = create_results_export()

        # Save to BytesIO object
        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)

        filename = f'election_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        flash('Error generating export file', 'error')
        return redirect(url_for('admin.dashboard'))
