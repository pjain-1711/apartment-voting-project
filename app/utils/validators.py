from app.models import Voter, Nominee, Wing


def extract_wing_from_flat(flat_number):
    """
    Extract wing from flat number (first digit indicates wing)
    Returns: (wing_id, error_message)
    """
    # Validate flat number format
    if not flat_number or len(flat_number) != 4:
        return None, "Flat number must be exactly 4 digits"

    if not flat_number.isdigit():
        return None, "Flat number must contain only digits"

    # Get first digit (wing number)
    wing_number = int(flat_number[0])

    if wing_number == 0:
        return None, "Flat number cannot start with 0"

    # Try multiple wing name formats
    possible_wing_names = [
        str(wing_number),              # "1", "2", "3"
        f"WING {wing_number}",         # "WING 1", "WING 2", "WING 3"
        f"Wing {wing_number}",         # "Wing 1", "Wing 2", "Wing 3"
        f"wing {wing_number}",         # "wing 1", "wing 2", "wing 3"
    ]

    # Also add letter mapping (1=A, 2=B, etc.)
    wing_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}
    wing_letter = wing_map.get(wing_number)
    if wing_letter:
        possible_wing_names.extend([
            wing_letter,                   # "A", "B", "C"
            f"WING {wing_letter}",         # "WING A", "WING B"
            f"Wing {wing_letter}",         # "Wing A", "Wing B"
        ])

    # Try to find wing with any of these names
    wing = None
    for wing_name in possible_wing_names:
        wing = Wing.query.filter_by(name=wing_name).first()
        if wing:
            break

    if not wing:
        return None, f"Wing for flat starting with {wing_number} does not exist in the system. Please add a wing named 'WING {wing_number}' or '{wing_number}' in admin panel."

    if not wing.is_active:
        return None, f"Wing {wing.name} is not active"

    return wing.id, None


def has_already_voted(flat_number, wing_id):
    """Check if a flat has already voted"""
    existing_voter = Voter.query.filter_by(
        flat_number=flat_number,
        wing_id=wing_id
    ).first()
    return existing_voter is not None


def get_nominees_by_wing_and_gender(wing_id):
    """Get nominees grouped by gender for a specific wing"""
    male_nominees = Nominee.query.filter_by(
        wing_id=wing_id,
        gender='male'
    ).order_by(Nominee.name).all()

    female_nominees = Nominee.query.filter_by(
        wing_id=wing_id,
        gender='female'
    ).order_by(Nominee.name).all()

    return {
        'male': male_nominees,
        'female': female_nominees
    }


def get_next_counter_number():
    """Generate next sequential counter number"""
    last_voter = Voter.query.order_by(Voter.counter_number.desc()).first()
    return (last_voter.counter_number + 1) if last_voter else 1


def validate_vote_selection(male_nominee_ids, female_nominee_ids, wing_id):
    """
    Validate vote selection (now supports multiple selections - up to 2 each)
    Returns: (is_valid, error_message)
    """
    nominees = get_nominees_by_wing_and_gender(wing_id)
    MAX_SELECTIONS = 2

    # Validate male nominees
    if len(nominees['male']) > 0:
        if not male_nominee_ids or len(male_nominee_ids) == 0:
            return False, "Please select at least one male nominee"

        if len(male_nominee_ids) > MAX_SELECTIONS:
            return False, f"You can select a maximum of {MAX_SELECTIONS} male nominees"

        # Verify each male nominee exists and belongs to correct wing
        for male_nominee_id in male_nominee_ids:
            male_nominee = Nominee.query.get(male_nominee_id)
            if not male_nominee or male_nominee.wing_id != wing_id or male_nominee.gender != 'male':
                return False, "Invalid male nominee selection"

    # Validate female nominees
    if len(nominees['female']) > 0:
        if not female_nominee_ids or len(female_nominee_ids) == 0:
            return False, "Please select at least one female nominee"

        if len(female_nominee_ids) > MAX_SELECTIONS:
            return False, f"You can select a maximum of {MAX_SELECTIONS} female nominees"

        # Verify each female nominee exists and belongs to correct wing
        for female_nominee_id in female_nominee_ids:
            female_nominee = Nominee.query.get(female_nominee_id)
            if not female_nominee or female_nominee.wing_id != wing_id or female_nominee.gender != 'female':
                return False, "Invalid female nominee selection"

    # Edge case: if no nominees at all
    if len(nominees['male']) == 0 and len(nominees['female']) == 0:
        return False, "No nominees available for your wing"

    return True, None
