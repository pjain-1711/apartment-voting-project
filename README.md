# Assetz Sun and Sanctum - Voting System

A secure, wing-based electronic voting system for apartment complex wing representative elections. Built with Flask, this system allows residents to vote for male and female representatives from their specific wings.

## Features

### For Voters
- ✅ Wing-specific voting (voters only see nominees from their wing)
- ✅ Vote for one male and one female representative
- ✅ Duplicate vote prevention (one vote per flat)
- ✅ Sequential counter number for vote tracking
- ✅ Mobile-responsive interface
- ✅ Confirmation step before final submission

### For Administrators
- ✅ Secure admin authentication
- ✅ Wing management (add/remove wings)
- ✅ Nominee management (add/delete nominees with details)
- ✅ Real-time voting progress tracking
- ✅ Result declaration with automatic winner calculation
- ✅ Excel export (anonymous and detailed)
- ✅ Configurable settings (voting enable/disable, winner count, results visibility)

### Technical Features
- ✅ SQLite database (development) / PostgreSQL (production)
- ✅ Flask-Login for authentication
- ✅ Rate limiting on voting endpoint
- ✅ CSRF protection
- ✅ Bootstrap 5 responsive UI
- ✅ Edge case handling (0/1/2+ nominees per gender)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd voting-system
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and set your configuration
   ```

5. **Initialize the database:**
   ```bash
   python run.py
   ```
   The database will be created automatically on first run with a default admin user.

6. **Run the application:**
   ```bash
   python run.py
   ```
   The application will be available at `http://localhost:5000`

## Default Admin Credentials

**IMPORTANT:** Change these immediately after first login!

- **Username:** `admin`
- **Password:** `admin123`

You can change these by setting environment variables:
```bash
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_password
```

## Usage Guide

### For Administrators

1. **Login:** Navigate to `/admin/login` and use admin credentials

2. **Add Wings:**
   - Go to "Manage Wings"
   - Click "Add Wing"
   - Enter wing name (e.g., "A", "B", "Tower 1")

3. **Add Nominees:**
   - Go to "Manage Nominees"
   - Click "Add Nominee"
   - Fill in: Name, Gender, Flat Number, Phone, Wing

4. **Monitor Progress:**
   - Dashboard shows real-time statistics
   - "Voting Progress" shows wing-wise details

5. **Declare Results:**
   - Go to Dashboard
   - Click "Declare Results" when voting is complete
   - Winners are automatically calculated (top 2 per gender per wing)

6. **Export Data:**
   - Anonymous Export: Vote records without voter names
   - Detailed Export: Complete voter and vote information
   - Results Export: Election results with winners

### For Voters

1. **Navigate to the voting page** (home page)

2. **Enter your details:**
   - Name
   - Flat Number
   - Wing
   - Phone Number

3. **Select nominees:**
   - Choose ONE male representative (if available)
   - Choose ONE female representative (if available)

4. **Confirm and submit:**
   - Review your selections
   - Submit your vote
   - Save your counter number for reference

## Configuration

### System Settings (Admin Panel → Settings)

- **Voting Enabled:** Toggle voting on/off
- **Results Visible:** Show/hide results to public
- **Winners Per Gender:** Number of winners per gender per wing (default: 2)

### Environment Variables

Create a `.env` file with:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# For production
DATABASE_URL=postgresql://user:password@host/dbname
```

## AWS Deployment

### Option 1: Elastic Beanstalk (Recommended)

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and deploy:**
   ```bash
   eb init -p python-3.11 voting-system
   eb create voting-system-env
   eb open
   ```

3. **Set environment variables:**
   ```bash
   eb setenv SECRET_KEY=your-secret-key ADMIN_PASSWORD=secure-password
   ```

### Option 2: EC2 + Gunicorn

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

3. **Set up Nginx as reverse proxy** (recommended for production)

### Database for Production

Use PostgreSQL on AWS RDS:

1. Create RDS instance (PostgreSQL, t3.micro for free tier)
2. Set `DATABASE_URL` environment variable:
   ```
   postgresql://username:password@rds-endpoint:5432/votingdb
   ```

## Project Structure

```
voting-system/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes/              # Route blueprints
│   │   ├── admin.py         # Admin panel
│   │   ├── voting.py        # Voting interface
│   │   └── results.py       # Results & exports
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   └── utils/               # Helper functions
├── instance/                # SQLite database (gitignored)
├── config.py                # Configuration
├── requirements.txt         # Dependencies
├── run.py                   # Entry point
└── README.md                # This file
```

## Security Features

- ✅ Bcrypt password hashing
- ✅ Flask-Login session management
- ✅ CSRF protection on all forms
- ✅ Rate limiting (5 votes per hour per IP)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Duplicate vote prevention
- ✅ Secure cookie settings

## Troubleshooting

### Database Issues

**Problem:** Database not created
```bash
# Solution: Create instance directory manually
mkdir instance
python run.py
```

### Import Errors

**Problem:** Module not found
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

**Problem:** Port 5000 already in use
```bash
# Solution: Use a different port
python run.py --port 5001
```

Or kill the process using port 5000:
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Logo

Place your "Assetz Sun and Sanctum" logo at:
```
app/static/images/logo.png
```
Recommended size: 200x60 pixels (PNG format)

## License

This project is created for Assetz Sun and Sanctum apartment complex.

## Support

For issues or questions:
1. Check this README
2. Review error logs
3. Contact the development team

## Version History

- **v1.0.0** - Initial release
  - Wing-based voting system
  - Admin panel
  - Results declaration
  - Excel exports
  - Configurable settings
