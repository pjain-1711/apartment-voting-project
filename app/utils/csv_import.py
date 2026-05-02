import csv
import io
from app import db
from app.models import Nominee, Wing


def import_nominees_from_csv(file):
    """
    Import nominees from CSV file

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
        # Read CSV file
        file_content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(file_content))

        # Expected columns (flexible with naming)
        required_cols = ['Name', 'Apartment number', 'Wing', 'Gender', 'Active status']

        # Check if required columns exist
        if not csv_reader.fieldnames:
            return 0, 1, ['CSV file is empty or improperly formatted']

        missing_cols = []
        for col in required_cols:
            if col not in csv_reader.fieldnames:
                missing_cols.append(col)

        if missing_cols:
            return 0, 1, [f'Missing required columns: {", ".join(missing_cols)}']

        # Process each row
        for idx, row in enumerate(csv_reader, start=2):  # Start at 2 because row 1 is header
            try:
                # Skip if withdrawn
                active_status = str(row.get('Active status', '')).strip().lower()
                if active_status == 'withdrawn':
                    continue  # Skip this nominee

                # Validate and extract data
                name = str(row.get('Name', '')).strip()
                flat_number = str(row.get('Apartment number', '')).strip()
                wing_name = str(row.get('Wing', '')).strip().upper()
                gender = str(row.get('Gender', '')).strip().lower()

                # Validation checks
                if not name or not flat_number or not wing_name:
                    errors.append(f'Row {idx}: Missing required data (Name, Apartment, or Wing)')
                    error_count += 1
                    continue

                # Validate gender
                if gender not in ['male', 'female']:
                    errors.append(f'Row {idx}: Invalid gender "{row.get("Gender")}" - must be "male" or "female"')
                    error_count += 1
                    continue

                # Find or create wing in database
                wing = Wing.query.filter_by(name=wing_name).first()
                if not wing:
                    # Auto-create wing if it doesn't exist
                    wing = Wing(name=wing_name, is_active=True)
                    db.session.add(wing)
                    db.session.flush()  # Get the wing ID without committing

                if not wing.is_active:
                    errors.append(f'Row {idx}: Wing "{wing_name}" is not active')
                    error_count += 1
                    continue

                # Check if nominee already exists
                existing = Nominee.query.filter_by(
                    name=name,
                    flat_number=flat_number,
                    wing_id=wing.id
                ).first()

                if existing:
                    errors.append(f'Row {idx}: Nominee "{name}" from flat {flat_number} already exists')
                    error_count += 1
                    continue

                # Create nominee
                nominee = Nominee(
                    name=name,
                    gender=gender,
                    flat_number=flat_number,
                    phone_number='',  # Not collected
                    wing_id=wing.id
                )
                db.session.add(nominee)
                success_count += 1

            except Exception as e:
                errors.append(f'Row {idx}: {str(e)}')
                error_count += 1

        # Commit all nominees at once
        if success_count > 0:
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        return 0, 1, [f'Error reading CSV file: {str(e)}']

    return success_count, error_count, errors


def validate_csv_file(file):
    """
    Validate CSV file before import
    Returns: (is_valid, error_message)
    """
    try:
        # Check file extension
        if not file.filename.endswith('.csv'):
            return False, 'File must be a CSV file (.csv)'

        # Try to read file
        file_content = file.read().decode('utf-8')
        file.seek(0)  # Reset file pointer

        csv_reader = csv.DictReader(io.StringIO(file_content))

        # Check if empty
        fieldnames = csv_reader.fieldnames
        if not fieldnames:
            return False, 'CSV file is empty'

        # Check for required columns
        required_cols = ['Name', 'Apartment number', 'Wing', 'Gender', 'Active status']
        missing_cols = [col for col in required_cols if col not in fieldnames]

        if missing_cols:
            return False, f'Missing required columns: {", ".join(missing_cols)}'

        return True, None

    except Exception as e:
        return False, f'Invalid CSV file: {str(e)}'
