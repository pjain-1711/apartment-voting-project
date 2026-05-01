# PythonAnywhere Deployment Guide

Complete step-by-step guide for deploying the voting system on PythonAnywhere.

---

## 📋 Prerequisites

- PythonAnywhere account (free or paid)
- Your code ready (on GitHub or local)

---

## 🚀 Step-by-Step Deployment

### Step 1: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Click **"Pricing & signup"**
3. Choose plan:
   - **Beginner (Free)** - Good for testing
   - **Hacker ($5/month)** - Recommended for production
4. Create account and verify email

---

### Step 2: Upload Your Code

#### Option A: From GitHub (Recommended)

1. Open **Bash Console** in PythonAnywhere
2. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/voting-system.git
   cd voting-system
   ```

#### Option B: Upload Files

1. Go to **"Files"** tab
2. Click **"Upload a file"**
3. Upload your project as ZIP
4. Extract: `unzip voting-system.zip`

---

### Step 3: Create Virtual Environment

In the **Bash console**:

```bash
# Navigate to your project
cd ~/voting-system

# Create virtual environment with Python 3.10
mkvirtualenv voting-env --python=/usr/bin/python3.10

# Activate it (should auto-activate)
workon voting-env

# Install dependencies
pip install -r requirements.txt
```

**Note:** The virtual environment path will be:
```
/home/YOUR_USERNAME/.virtualenvs/voting-env
```

---

### Step 4: Configure WSGI File

This is where you **add environment variables**!

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10**
5. Click on **WSGI configuration file** link (e.g., `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`)

6. **Replace the entire content** with this:

```python
# +++++++++++ FLASK APP +++++++++++
# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import sys
import os

# ========================================
# 1. ADD YOUR PROJECT PATH
# ========================================
# Update YOUR_USERNAME with your actual username
path = '/home/YOUR_USERNAME/voting-system'
if path not in sys.path:
    sys.path.append(path)

# ========================================
# 2. SET ENVIRONMENT VARIABLES (IMPORTANT!)
# ========================================
# These are your app's configuration settings
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-very-long-random-secret-key-change-this'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'YourSecurePassword123!'

# Optional: If using PostgreSQL instead of SQLite
# os.environ['DATABASE_URL'] = 'postgresql://user:password@host/database'

# ========================================
# 3. IMPORT AND CREATE APP
# ========================================
from app import create_app

application = create_app()

# ========================================
# 4. INITIALIZE DATABASE (First time only)
# ========================================
# This will create tables and default admin user
with application.app_context():
    from app import db
    from app.models import AdminUser, ConfigSetting

    # Create all tables
    db.create_all()

    # Seed default admin user if not exists
    if not AdminUser.query.first():
        admin_user = AdminUser(username=os.environ.get('ADMIN_USERNAME', 'admin'))
        admin_user.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
        db.session.add(admin_user)
        db.session.commit()

    # Seed default config settings
    default_settings = {
        'voting_enabled': 'true',
        'results_visible': 'false',
        'winners_per_gender': '2'
    }
    for key, value in default_settings.items():
        if not ConfigSetting.query.filter_by(key=key).first():
            setting = ConfigSetting(key=key, value=value)
            db.session.add(setting)
    db.session.commit()
```

7. **Update the following in the WSGI file:**

   - Line 16: Replace `YOUR_USERNAME` with your PythonAnywhere username
   - Line 24: Generate a secret key (see below)
   - Line 26: Change admin password to something secure

8. **Save the file** (Ctrl+S or click Save button)

---

### Step 5: Generate Secret Key

Run this in **Bash console**:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output (looks like: `a1b2c3d4e5f6...`) and paste it in the WSGI file at line 24.

Example:
```python
os.environ['SECRET_KEY'] = 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456'
```

---

### Step 6: Configure Virtual Environment Path

1. Still in **"Web"** tab
2. Scroll to **"Virtualenv"** section
3. Enter the path:
   ```
   /home/YOUR_USERNAME/.virtualenvs/voting-env
   ```
   (Replace `YOUR_USERNAME` with your actual username)

4. Click the checkmark to save

---

### Step 7: Set Static Files Path

1. In **"Web"** tab, scroll to **"Static files"** section
2. Add this mapping:

   **URL:** `/static/`
   **Directory:** `/home/YOUR_USERNAME/voting-system/app/static`

3. Click checkmark to save

---

### Step 8: Reload Web App

1. Scroll to top of **"Web"** tab
2. Click big green **"Reload YOUR_USERNAME.pythonanywhere.com"** button
3. Wait for confirmation message

---

### Step 9: Test Your App

1. Click the link: `https://YOUR_USERNAME.pythonanywhere.com`
2. You should see the voting system home page!
3. Go to admin: `https://YOUR_USERNAME.pythonanywhere.com/admin/login`
4. Login with credentials from WSGI file

---

## 🔐 Environment Variables Explained

In the WSGI file, these environment variables configure your app:

### Required Variables:

```python
# Flask environment (development or production)
os.environ['FLASK_ENV'] = 'production'

# Secret key for session encryption (MUST BE RANDOM!)
os.environ['SECRET_KEY'] = 'your-random-secret-key'

# Admin login credentials
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'SecurePassword123!'
```

### Optional Variables:

```python
# Database URL (if using PostgreSQL instead of SQLite)
os.environ['DATABASE_URL'] = 'postgresql://user:pass@host/db'

# Custom settings
os.environ['WINNERS_PER_GENDER'] = '2'
```

---

## 📝 Complete WSGI File Template

Save this as your WSGI configuration:

```python
import sys
import os

# ========================================
# CONFIGURATION - UPDATE THESE VALUES
# ========================================
USERNAME = 'YOUR_PYTHONANYWHERE_USERNAME'  # e.g., 'john123'
SECRET_KEY = 'GENERATE_RANDOM_KEY_HERE'     # Use: python3 -c "import secrets; print(secrets.token_hex(32))"
ADMIN_USERNAME = 'admin'                    # Change this
ADMIN_PASSWORD = 'YourSecurePassword123!'   # Change this too!

# ========================================
# PATH SETUP
# ========================================
path = f'/home/{USERNAME}/voting-system'
if path not in sys.path:
    sys.path.append(path)

# ========================================
# ENVIRONMENT VARIABLES
# ========================================
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = SECRET_KEY
os.environ['ADMIN_USERNAME'] = ADMIN_USERNAME
os.environ['ADMIN_PASSWORD'] = ADMIN_PASSWORD

# ========================================
# FLASK APP
# ========================================
from app import create_app
application = create_app()

# ========================================
# DATABASE INITIALIZATION
# ========================================
with application.app_context():
    from app import db
    from app.models import AdminUser, ConfigSetting

    db.create_all()

    if not AdminUser.query.first():
        admin_user = AdminUser(username=ADMIN_USERNAME)
        admin_user.set_password(ADMIN_PASSWORD)
        db.session.add(admin_user)
        db.session.commit()

    default_settings = {
        'voting_enabled': 'true',
        'results_visible': 'false',
        'winners_per_gender': '2'
    }
    for key, value in default_settings.items():
        if not ConfigSetting.query.filter_by(key=key).first():
            setting = ConfigSetting(key=key, value=value)
            db.session.add(setting)
    db.session.commit()
```

---

## 🐛 Troubleshooting

### Error: "No module named 'app'"

**Solution:** Check the path in WSGI file matches your project location
```python
path = '/home/YOUR_USERNAME/voting-system'  # Must be correct!
```

### Error: "Database is locked"

**Solution:** SQLite has limitations on PythonAnywhere. For production, use PostgreSQL:

1. Set up database on PythonAnywhere
2. Add to WSGI file:
```python
os.environ['DATABASE_URL'] = 'postgresql://user:pass@host/db'
```

### Error: "Application failed to start"

**Solution:** Check error log in **"Web"** tab → **"Error log"** link

Common fixes:
- Verify virtual environment path is correct
- Check all dependencies are installed
- Look for typos in WSGI file

### Static files not loading (CSS/images missing)

**Solution:**
1. Check static files mapping in "Web" tab
2. URL: `/static/`
3. Directory: `/home/YOUR_USERNAME/voting-system/app/static`
4. Reload web app

### Can't access admin panel

**Solution:**
1. Check WSGI file has correct admin credentials
2. Try default: `admin` / `admin123` (if not changed)
3. Check error log for clues

---

## 🔄 Updating Your App

When you make changes:

1. **Update code** (in Bash console):
   ```bash
   cd ~/voting-system
   git pull  # If using Git
   ```

2. **Update dependencies** (if requirements changed):
   ```bash
   workon voting-env
   pip install -r requirements.txt
   ```

3. **Reload web app** (in "Web" tab):
   - Click green "Reload" button

---

## 💾 Database Location

On PythonAnywhere, your SQLite database is at:
```
/home/YOUR_USERNAME/voting-system/instance/voting.db
```

To backup:
```bash
cd ~/voting-system/instance
cp voting.db voting_backup_$(date +%Y%m%d).db
```

To download:
1. Go to **"Files"** tab
2. Navigate to `/home/YOUR_USERNAME/voting-system/instance/`
3. Click on `voting.db`
4. Click **"Download"** button

---

## 🎯 Quick Start Checklist

- [ ] Create PythonAnywhere account
- [ ] Upload code (Git or manual)
- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Configure WSGI file with environment variables
- [ ] Generate and set SECRET_KEY
- [ ] Set ADMIN_USERNAME and ADMIN_PASSWORD
- [ ] Set virtual environment path in Web tab
- [ ] Configure static files mapping
- [ ] Reload web app
- [ ] Test at your-username.pythonanywhere.com
- [ ] Login to admin panel
- [ ] Change admin password (from admin panel)

---

## 🔗 Important URLs

After deployment:

- **Home:** https://YOUR_USERNAME.pythonanywhere.com
- **Admin:** https://YOUR_USERNAME.pythonanywhere.com/admin/login
- **Results:** https://YOUR_USERNAME.pythonanywhere.com/results

---

## 💡 Pro Tips

1. **Free Account Limitations:**
   - Your app sleeps after inactivity
   - First request takes longer (wakes up)
   - Limited to one web app

2. **Security:**
   - Always change default admin password
   - Use strong SECRET_KEY
   - Keep WSGI file credentials secure

3. **Performance:**
   - Paid account removes sleep limitation
   - Consider PostgreSQL for better performance
   - Enable compression for static files

4. **Monitoring:**
   - Check error log regularly
   - Monitor server log for issues
   - Set up email notifications (paid accounts)

---

## 📞 Need Help?

- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Help Pages: https://help.pythonanywhere.com/
- Your error log: Web tab → Error log link

---

**You're all set! Your voting system is now live on PythonAnywhere!** 🎉
