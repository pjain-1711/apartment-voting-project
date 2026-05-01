from app import create_app, db
from app.models import AdminUser, Wing, Nominee, Voter, Vote, Result, ConfigSetting, ArchivedElection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'AdminUser': AdminUser,
        'Wing': Wing,
        'Nominee': Nominee,
        'Voter': Voter,
        'Vote': Vote,
        'Result': Result,
        'ConfigSetting': ConfigSetting,
        'ArchivedElection': ArchivedElection
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
