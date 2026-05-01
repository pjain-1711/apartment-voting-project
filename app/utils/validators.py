from app.models import Voter, Nominee


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


def validate_vote_selection(male_nominee_id, female_nominee_id, wing_id):
    """
    Validate vote selection
    Returns: (is_valid, error_message)
    """
    nominees = get_nominees_by_wing_and_gender(wing_id)

    # Check if male vote is required and provided
    if len(nominees['male']) > 0:
        if not male_nominee_id:
            return False, "Please select a male nominee"

        # Verify male nominee exists and belongs to correct wing
        male_nominee = Nominee.query.get(male_nominee_id)
        if not male_nominee or male_nominee.wing_id != wing_id or male_nominee.gender != 'male':
            return False, "Invalid male nominee selection"

    # Check if female vote is required and provided
    if len(nominees['female']) > 0:
        if not female_nominee_id:
            return False, "Please select a female nominee"

        # Verify female nominee exists and belongs to correct wing
        female_nominee = Nominee.query.get(female_nominee_id)
        if not female_nominee or female_nominee.wing_id != wing_id or female_nominee.gender != 'female':
            return False, "Invalid female nominee selection"

    # Edge case: if no nominees at all
    if len(nominees['male']) == 0 and len(nominees['female']) == 0:
        return False, "No nominees available for your wing"

    return True, None
