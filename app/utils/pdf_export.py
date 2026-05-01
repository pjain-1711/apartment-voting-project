from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from app.models import Result, Wing
import io


def create_results_pdf():
    """Generate PDF of election results"""
    # Create BytesIO buffer
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)

    # Container for PDF elements
    elements = []

    # Get styles
    styles = getSampleStyleSheet()

    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    # Subtitle style
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    # Wing header style
    wing_style = ParagraphStyle(
        'WingHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )

    # Gender header style
    gender_style = ParagraphStyle(
        'GenderHeader',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    # Add title
    elements.append(Paragraph("Election Results", title_style))
    elements.append(Paragraph("Wing Representative Elections", subtitle_style))
    elements.append(Paragraph("Assetz Sun and Sanctum", subtitle_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
                             styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Get all active wings
    wings = Wing.query.filter_by(is_active=True).order_by(Wing.name).all()

    for wing_idx, wing in enumerate(wings):
        # Wing header
        elements.append(Paragraph(f"Wing {wing.name}", wing_style))

        # Male representatives
        male_results = Result.query.filter_by(
            wing_id=wing.id,
            gender='male'
        ).order_by(Result.rank).all()

        if male_results:
            elements.append(Paragraph("Male Representatives", gender_style))

            # Create table data
            male_data = [['Rank', 'Name', 'Flat Number', 'Votes', 'Status']]
            for result in male_results:
                status = 'WINNER ★' if result.is_winner else 'Candidate'
                male_data.append([
                    str(result.rank),
                    result.nominee.name,
                    result.nominee.flat_number,
                    str(result.vote_count),
                    status
                ])

            # Create table
            male_table = Table(male_data, colWidths=[0.8*inch, 2.2*inch, 1.3*inch, 1*inch, 1.2*inch])
            male_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))

            # Highlight winners
            for idx, result in enumerate(male_results, start=1):
                if result.is_winner:
                    male_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#fff3cd')),
                        ('TEXTCOLOR', (4, idx), (4, idx), colors.HexColor('#ffc107')),
                        ('FONTNAME', (4, idx), (4, idx), 'Helvetica-Bold'),
                    ]))

            elements.append(male_table)
            elements.append(Spacer(1, 0.2*inch))

        # Female representatives
        female_results = Result.query.filter_by(
            wing_id=wing.id,
            gender='female'
        ).order_by(Result.rank).all()

        if female_results:
            elements.append(Paragraph("Female Representatives", gender_style))

            # Create table data
            female_data = [['Rank', 'Name', 'Flat Number', 'Votes', 'Status']]
            for result in female_results:
                status = 'WINNER ★' if result.is_winner else 'Candidate'
                female_data.append([
                    str(result.rank),
                    result.nominee.name,
                    result.nominee.flat_number,
                    str(result.vote_count),
                    status
                ])

            # Create table
            female_table = Table(female_data, colWidths=[0.8*inch, 2.2*inch, 1.3*inch, 1*inch, 1.2*inch])
            female_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff69b4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))

            # Highlight winners
            for idx, result in enumerate(female_results, start=1):
                if result.is_winner:
                    female_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#fff3cd')),
                        ('TEXTCOLOR', (4, idx), (4, idx), colors.HexColor('#ffc107')),
                        ('FONTNAME', (4, idx), (4, idx), 'Helvetica-Bold'),
                    ]))

            elements.append(female_table)
            elements.append(Spacer(1, 0.2*inch))

        # Add page break after each wing except the last one
        if wing_idx < len(wings) - 1:
            elements.append(PageBreak())

    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=0
    )
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Developed by Priyanka Jain", footer_style))

    # Build PDF
    doc.build(elements)

    # Get PDF from buffer
    buffer.seek(0)
    return buffer
