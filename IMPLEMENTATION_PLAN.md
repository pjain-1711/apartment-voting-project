# Implementation Plan for Requested Changes

## Status: 5/7 Complete

**Completed:**
1. ✅ Remove view results from home page
2. ✅ Auto-select nominees when not enough candidates
3. ✅ Download archived reports
4. ✅ Limit archives to 12
5. ✅ Remove phone number from voting form
6. ✅ Auto-deduce wing from flat number

**Remaining:**
7. ⏳ Excel upload for nominees

---

## ✅ 1. Remove View Results from Home Page (COMPLETED)

**Changes Made:**
- Removed "View Results" from landing page
- Moved Results link to admin-only navigation
- Only authenticated admins can see results link

**Files Modified:**
- `app/templates/landing.html`
- `app/templates/base.html`

---

## ⏳ 2. Results Visible Only After Declaration

**Status:** Already Implemented ✅

**How it Works:**
- `ConfigSetting.are_results_visible()` checks if results should be shown
- Admin declares results via dashboard
- Sets `results_visible` config to `true`
- Public can only see results after admin enables visibility

**No changes needed** - feature already exists!

---

## 🔄 3. Auto-Select Default if Not Enough Nominees

**Requirement:** If there are fewer nominees than winner slots, automatically select them as winners.

**Implementation Plan:**

### Files to Modify:
- `app/routes/admin.py` - Update `declare_results()` function

### Logic:
```python
# In declare_results()
for wing in wings:
    for gender in ['male', 'female']:
        nominees = Nominee.query.filter_by(wing_id=wing.id, gender=gender).all()

        if len(nominees) == 0:
            # No nominees - seat remains empty
            continue
        elif len(nominees) <= winners_per_gender:
            # Auto-select all as winners
            for rank, nominee in enumerate(nominees, 1):
                result = Result(
                    wing_id=wing.id,
                    nominee_id=nominee.id,
                    gender=gender,
                    vote_count=0,  # Or actual vote count
                    rank=rank,
                    is_winner=True  # All are winners
                )
        else:
            # Normal voting - top N win
            # Existing logic
```

---

## 📥 4. Download Archived Reports + Limit to 12 Archives

**Requirements:**
- Allow downloading Excel reports for archived elections
- Limit total archives to 12 (delete oldest when adding 13th)

### Part A: Download Archived Report

**Files to Modify:**
- `app/routes/admin_new_features.py` - Add download route
- `app/templates/admin/archives.html` - Add download button
- `app/utils/excel_export.py` - Add archive export function

**New Route:**
```python
@bp.route('/archives/<int:archive_id>/download')
@login_required
def download_archive(archive_id):
    archive = ArchivedElection.query.get_or_404(archive_id)
    workbook = create_archive_export(archive)
    # ... return Excel file
```

### Part B: Limit to 12 Archives

**Files to Modify:**
- `app/routes/admin_new_features.py` - Update `archive_election()` function

**Logic:**
```python
# Before creating new archive
archive_count = ArchivedElection.query.count()
if archive_count >= 12:
    # Delete oldest archive
    oldest = ArchivedElection.query.order_by(ArchivedElection.archived_at).first()
    db.session.delete(oldest)
    flash('Oldest archive was automatically deleted (limit: 12)', 'warning')

# Then create new archive
```

---

## 📱 5. Remove Phone Number from Voting Form

**Files to Modify:**
1. `app/templates/voting/voter_info.html` - Remove phone input
2. `app/routes/voting.py` - Remove phone from processing
3. `app/models.py` - Make phone_number optional in Voter model

### voter_info.html:
```html
<!-- REMOVE THIS:
<div class="mb-3">
    <label for="phone_number">Phone Number</label>
    <input type="tel" name="phone_number" required>
</div>
-->
```

### voting.py:
```python
# Remove from vote() function:
# phone_number = request.form.get('phone_number', '').strip()

# Update session:
session['voter_info'] = {
    'name': voter_name,
    'flat_number': flat_number,
    'wing_id': wing_id
    # Remove phone_number
}

# Update Voter creation:
voter = Voter(
    name=voter_info['name'],
    flat_number=voter_info['flat_number'],
    wing_id=voter_info['wing_id'],
    # Remove phone_number line
    counter_number=counter_number
)
```

### models.py:
```python
class Voter(db.Model):
    # ...
    phone_number = db.Column(db.String(20), nullable=True)  # Make optional
```

---

## 🏢 6. Auto-Deduce Wing from Flat Number

**Requirement:**
- Flat numbers are 4 digits
- First digit = wing number
- Validate flat number format
- Auto-select wing based on first digit

### Files to Modify:
1. `app/templates/voting/voter_info.html` - Remove wing dropdown, add validation
2. `app/routes/voting.py` - Extract wing from flat number
3. `app/utils/validators.py` - Add flat number validation

### voter_info.html:
```html
<!-- REMOVE wing dropdown -->
<!-- ADD flat number help text -->
<div class="mb-3">
    <label for="flat_number">Flat Number</label>
    <input type="text" name="flat_number" pattern="[0-9]{4}"
           placeholder="e.g., 1001, 2305" required>
    <small class="text-muted">
        4-digit number (First digit indicates wing: 1=A, 2=B, etc.)
    </small>
</div>
```

### validators.py - Add new function:
```python
def extract_wing_from_flat(flat_number):
    """Extract wing from flat number (first digit)"""
    if not flat_number or len(flat_number) != 4 or not flat_number.isdigit():
        return None, "Flat number must be exactly 4 digits"

    wing_number = int(flat_number[0])

    if wing_number == 0:
        return None, "Flat number cannot start with 0"

    # Map wing number to wing name (1=A, 2=B, etc.)
    wing_map = {
        1: 'A', 2: 'B', 3: 'C', 4: 'D',
        5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'
    }

    wing_name = wing_map.get(wing_number)
    if not wing_name:
        return None, f"Invalid wing number: {wing_number}"

    # Find wing in database
    wing = Wing.query.filter_by(name=wing_name).first()
    if not wing:
        return None, f"Wing {wing_name} does not exist"

    return wing.id, None
```

### voting.py:
```python
def vote():
    flat_number = request.form.get('flat_number', '').strip()

    # Extract wing from flat number
    wing_id, error = extract_wing_from_flat(flat_number)
    if error:
        flash(error, 'error')
        return redirect(url_for('voting.index'))

    # Continue with rest of logic...
```

---

## 📊 7. Excel Upload for Nominees

**Requirements:**
- Upload Excel with columns: Timestamp, Email, Name, Apartment number, Wing, Gender, Active status
- Skip nominees with Active status = "withdrawn"
- Validate data before importing

### Files to Create/Modify:
1. `app/routes/admin.py` - Add upload route
2. `app/templates/admin/nominees.html` - Add upload button/form
3. `app/utils/excel_import.py` - NEW FILE for import logic
4. `requirements.txt` - Add `pandas` and `openpyxl` (already have openpyxl)

### New Route in admin.py:
```python
@bp.route('/nominees/upload', methods=['GET', 'POST'])
@login_required
def upload_nominees():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('admin.nominees'))

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('admin.nominees'))

        if not file.filename.endswith(('.xlsx', '.xls')):
            flash('Please upload an Excel file (.xlsx or .xls)', 'error')
            return redirect(url_for('admin.nominees'))

        # Process file
        from app.utils.excel_import import import_nominees_from_excel
        success_count, error_count, errors = import_nominees_from_excel(file)

        flash(f'Imported {success_count} nominees. {error_count} errors.', 'success')
        if errors:
            for error in errors[:5]:  # Show first 5 errors
                flash(error, 'warning')

        return redirect(url_for('admin.nominees'))

    return render_template('admin/upload_nominees.html')
```

### New File: app/utils/excel_import.py:
```python
import pandas as pd
from app import db
from app.models import Nominee, Wing

def import_nominees_from_excel(file):
    """Import nominees from Excel file"""
    success_count = 0
    error_count = 0
    errors = []

    try:
        # Read Excel file
        df = pd.read_excel(file)

        # Expected columns
        required_cols = ['Name', 'Apartment number', 'Wing', 'Gender', 'Active status']

        # Check columns exist
        for col in required_cols:
            if col not in df.columns:
                return 0, 1, [f'Missing required column: {col}']

        # Process each row
        for idx, row in df.iterrows():
            try:
                # Skip if withdrawn
                if str(row['Active status']).lower() == 'withdrawn':
                    continue

                # Validate data
                name = str(row['Name']).strip()
                flat_number = str(row['Apartment number']).strip()
                wing_name = str(row['Wing']).strip()
                gender = str(row['Gender']).lower().strip()

                if not name or not flat_number or not wing_name:
                    errors.append(f'Row {idx+2}: Missing required data')
                    error_count += 1
                    continue

                if gender not in ['male', 'female']:
                    errors.append(f'Row {idx+2}: Invalid gender: {gender}')
                    error_count += 1
                    continue

                # Find wing
                wing = Wing.query.filter_by(name=wing_name).first()
                if not wing:
                    errors.append(f'Row {idx+2}: Wing not found: {wing_name}')
                    error_count += 1
                    continue

                # Check if nominee already exists
                existing = Nominee.query.filter_by(
                    name=name,
                    flat_number=flat_number,
                    wing_id=wing.id
                ).first()

                if existing:
                    errors.append(f'Row {idx+2}: Nominee already exists: {name}')
                    error_count += 1
                    continue

                # Create nominee
                nominee = Nominee(
                    name=name,
                    gender=gender,
                    flat_number=flat_number,
                    phone_number='',  # Not in Excel
                    wing_id=wing.id
                )
                db.session.add(nominee)
                success_count += 1

            except Exception as e:
                errors.append(f'Row {idx+2}: {str(e)}')
                error_count += 1

        # Commit all at once
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return 0, 1, [f'Error reading Excel file: {str(e)}']

    return success_count, error_count, errors
```

### Add to nominees.html:
```html
<a href="{{ url_for('admin.upload_nominees') }}" class="btn btn-success">
    <i class="bi bi-upload"></i> Upload Excel
</a>
```

---

## 📋 Implementation Order (Recommended)

1. ✅ **Remove phone number** (Easiest, independent)
2. ✅ **Auto-deduce wing from flat** (Medium, changes user flow)
3. ✅ **Auto-select default nominees** (Easy, backend only)
4. ✅ **Limit archives to 12** (Easy, backend only)
5. ✅ **Download archived reports** (Medium, new feature)
6. ✅ **Excel upload for nominees** (Complex, new feature with validation)

---

## 🧪 Testing Checklist

After implementing each change:

### Change 3: Auto-select defaults
- [ ] Create wing with 0 nominees - check empty seats
- [ ] Create wing with 1 male nominee - check auto-winner
- [ ] Create wing with 2 male nominees - check both win
- [ ] Create wing with 3+ nominees - check voting works

### Change 4: Archive limits
- [ ] Create 12 archives - verify all saved
- [ ] Create 13th archive - verify oldest deleted
- [ ] Download archived report - verify Excel generated

### Change 5: Remove phone
- [ ] Voting form no longer asks for phone
- [ ] Vote submission works without phone
- [ ] Voter record created without phone

### Change 6: Wing deduction
- [ ] Flat 1001 → Wing A
- [ ] Flat 2305 → Wing B
- [ ] Flat 9999 → Wing I
- [ ] Flat 123 → Error (not 4 digits)
- [ ] Flat abcd → Error (not numeric)

### Change 7: Excel upload
- [ ] Upload valid Excel - nominees created
- [ ] Upload with withdrawn - skipped correctly
- [ ] Upload with invalid data - errors shown
- [ ] Upload duplicate - error shown
- [ ] Download sample template - works

---

## 📦 Dependencies to Add

```txt
# Add to requirements.txt if not present:
pandas==2.0.0
```

---

## 🔄 Migration Notes

### Database Changes Needed:

```python
# Make phone_number optional in Voter model
# Run after updating models.py:
flask db migrate -m "Make phone number optional"
flask db upgrade
```

Or manually:
```sql
ALTER TABLE voters ALTER COLUMN phone_number DROP NOT NULL;
```

---

## 📝 Summary

**Total Changes:** 7
**Completed:** 1
**Remaining:** 6
**Estimated Time:** 4-6 hours for all changes
**Complexity:** Medium to High

**Next Steps:**
1. Implement changes 5 & 6 together (remove phone + wing deduction)
2. Implement change 3 (auto-select)
3. Implement change 4 (archive limits + download)
4. Implement change 7 (Excel upload) - most complex

Would you like me to implement these one by one? Let me know which to tackle next!
