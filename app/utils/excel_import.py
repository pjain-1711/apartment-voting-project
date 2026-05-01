import pandas as pd
from app import db
from app.models import Nominee, Wing


def import_nominees_from_excel(file):
    """
    Import nominees from Excel file

    Expected columns:
    - Timestamp (optional)
    - Email Address (optional)
    - Name
    - Apartment number
    - Wing
    - Gender
    - Active status

    Returns: (success_count, error_count, errors)
    """
    success_count = 0
    error_count = 0
    errors = []

    try:
        # Read Excel file
        df = pd.read_excel(file)

        # Expected columns (flexible with naming)
        required_cols = ['Name', 'Apartment number', 'Wing', 'Gender', 'Active status']

        # Check if required columns exist
        missing_cols = []
        for col in required_cols:
            if col not in df.columns:
                missing_cols.append(col)

        if missing_cols:
            return 0, 1, [f'Missing required columns: {", ".join(missing_cols)}']

        # Process each row
        for idx, row in df.iterrows():
            try:
                # Skip if withdrawn
                active_status = str(row['Active status']).strip().lower()
                if active_status == 'withdrawn':
                    continue  # Skip this nominee

                # Validate and extract data
                name = str(row['Name']).strip()
                flat_number = str(row['Apartment number']).strip()
                wing_name = str(row['Wing']).strip().upper()
                gender = str(row['Gender']).strip().lower()

                # Validation checks
                if not name or not flat_number or not wing_name:
                    errors.append(f'Row {idx+2}: Missing required data (Name, Apartment, or Wing)')
                    error_count += 1
                    continue

                # Validate gender
                if gender not in ['male', 'female']:
                    errors.append(f'Row {idx+2}: Invalid gender "{row["Gender"]}" - must be "male" or "female"')
                    error_count += 1
                    continue

                # Find wing in database
                wing = Wing.query.filter_by(name=wing_name).first()
                if not wing:
                    errors.append(f'Row {idx+2}: Wing "{wing_name}" does not exist in system')
                    error_count += 1
                    continue

                if not wing.is_active:
                    errors.append(f'Row {idx+2}: Wing "{wing_name}" is not active')
                    error_count += 1
                    continue

                # Check if nominee already exists
                existing = Nominee.query.filter_by(
                    name=name,
                    flat_number=flat_number,
                    wing_id=wing.id
                ).first()

                if existing:
                    errors.append(f'Row {idx+2}: Nominee "{name}" from flat {flat_number} already exists')
                    error_count += 1
                    continue

                # Create nominee
                nominee = Nominee(
                    name=name,
                    gender=gender,
                    flat_number=flat_number,
                    phone_number='',  # Not provided in Excel
                    wing_id=wing.id
                )
                db.session.add(nominee)
                success_count += 1

            except Exception as e:
                errors.append(f'Row {idx+2}: {str(e)}')
                error_count += 1

        # Commit all nominees at once
        if success_count > 0:
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        return 0, 1, [f'Error reading Excel file: {str(e)}']

    return success_count, error_count, errors


def validate_excel_file(file):
    """
    Validate Excel file before import
    Returns: (is_valid, error_message)
    """
    try:
        # Check file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            return False, 'File must be an Excel file (.xlsx or .xls)'

        # Try to read file
        df = pd.read_excel(file)

        # Check if empty
        if df.empty:
            return False, 'Excel file is empty'

        # Check for required columns
        required_cols = ['Name', 'Apartment number', 'Wing', 'Gender', 'Active status']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            return False, f'Missing required columns: {", ".join(missing_cols)}'

        return True, None

    except Exception as e:
        return False, f'Invalid Excel file: {str(e)}'
