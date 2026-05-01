# Troubleshooting Guide - "Hello from Flask!" Issue

## 🔴 Problem: Getting "Hello from Flask!" on PythonAnywhere

This means the default Flask template is running instead of your app.

---

## ✅ Solution: Fix Your WSGI File

### Step 1: Open Your WSGI Configuration

1. Go to PythonAnywhere **"Web"** tab
2. Find the **"Code:"** section
3. Click on the WSGI configuration file link
   - It will be something like: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

### Step 2: Replace ENTIRE Content

**Delete everything** in the WSGI file and replace with this:

```python
# +++++++++++ VOTING SYSTEM WSGI CONFIGURATION +++++++++++
import sys
import os

# ========================================
# 1. UPDATE YOUR USERNAME HERE
# ========================================
USERNAME = 'YOUR_PYTHONANYWHERE_USERNAME'  # ← CHANGE THIS!

# ========================================
# 2. SET YOUR SECRET KEY AND CREDENTIALS
# ========================================
# Generate secret key: python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = 'PASTE_YOUR_GENERATED_SECRET_KEY_HERE'  # ← CHANGE THIS!
ADMIN_USERNAME = 'admin'                              # ← CHANGE THIS!
ADMIN_PASSWORD = 'YourSecurePassword123!'             # ← CHANGE THIS!

# ========================================
# 3. ADD PROJECT TO PYTHON PATH
# ========================================
project_path = f'/home/{USERNAME}/voting-system'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# ========================================
# 4. SET ENVIRONMENT VARIABLES
# ========================================
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = SECRET_KEY
os.environ['ADMIN_USERNAME'] = ADMIN_USERNAME
os.environ['ADMIN_PASSWORD'] = ADMIN_PASSWORD

# ========================================
# 5. IMPORT YOUR APP (THIS IS THE KEY PART!)
# ========================================
from app import create_app

# Create the Flask application
application = create_app()

# ========================================
# 6. INITIALIZE DATABASE ON FIRST RUN
# ========================================
with application.app_context():
    from app import db
    from app.models import AdminUser, ConfigSetting

    # Create tables
    db.create_all()

    # Create default admin user
    if not AdminUser.query.first():
        admin = AdminUser(username=ADMIN_USERNAME)
        admin.set_password(ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Admin user created: {ADMIN_USERNAME}")

    # Create default settings
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
    print("✓ Database initialized")

print("✓ Voting system loaded successfully!")
```

### Step 3: Update the Variables

In the WSGI file you just pasted, update these lines:

1. **Line 8:** Replace with your PythonAnywhere username
   ```python
   USERNAME = 'john123'  # Your actual username
   ```

2. **Line 13:** Generate and paste secret key
   ```bash
   # Run this in Bash console:
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it:
   ```python
   SECRET_KEY = 'a1b2c3d4e5f6...'  # The generated key
   ```

3. **Lines 14-15:** Set your admin credentials
   ```python
   ADMIN_USERNAME = 'myadmin'           # Your choice
   ADMIN_PASSWORD = 'SecurePass123!'    # Strong password
   ```

### Step 4: Verify Project Path

Make sure your project is actually at this location:
```
/home/YOUR_USERNAME/voting-system
```

To check, run in **Bash console**:
```bash
ls -la ~/voting-system
```

You should see:
```
app/
instance/
config.py
run.py
requirements.txt
...
```

If files are in a different location, update line 18 in WSGI:
```python
project_path = f'/home/{USERNAME}/your-actual-folder-name'
```

### Step 5: Save and Reload

1. **Save** the WSGI file (Ctrl+S or click Save)
2. Go back to **"Web"** tab
3. Click the big green **"Reload"** button
4. Wait for confirmation

### Step 6: Test

Visit: `https://yourusername.pythonanywhere.com`

✅ **You should now see your voting system home page!**

---

## 🔍 Still Seeing "Hello from Flask!"?

### Check #1: Verify Import Path

In **Bash console**:
```bash
cd ~/voting-system
python3
```

Then in Python:
```python
import sys
sys.path.insert(0, '/home/YOUR_USERNAME/voting-system')
from app import create_app
app = create_app()
print("Success!")
```

If you get an error, there's a problem with your app structure.

### Check #2: Look at Error Log

1. Go to **"Web"** tab
2. Click **"Error log"** link
3. Check for errors

Common errors:
- `ModuleNotFoundError: No module named 'app'` → Path issue
- `ModuleNotFoundError: No module named 'flask'` → Virtual environment not set
- `Database is locked` → SQLite issue (use PostgreSQL)

### Check #3: Virtual Environment

1. In **"Web"** tab, find **"Virtualenv"** section
2. Make sure it's set to:
   ```
   /home/YOUR_USERNAME/.virtualenvs/voting-env
   ```
3. If empty or wrong, update it
4. Reload web app

### Check #4: Dependencies Installed

In **Bash console**:
```bash
workon voting-env
cd ~/voting-system
pip install -r requirements.txt
```

### Check #5: Static Files

In **"Web"** tab, **"Static files"** section:

**URL:** `/static/`
**Directory:** `/home/YOUR_USERNAME/voting-system/app/static`

---

## 🐛 Common WSGI File Mistakes

### ❌ WRONG (Default Template):
```python
from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello():
    return 'Hello from Flask!'  # ← This is what you're seeing!
```

### ✅ CORRECT (Your App):
```python
from app import create_app
application = create_app()  # ← This loads your voting system
```

---

## 📝 Quick Fix Checklist

- [ ] Replaced entire WSGI file content
- [ ] Updated USERNAME to your PythonAnywhere username
- [ ] Generated and set SECRET_KEY
- [ ] Set ADMIN_USERNAME and ADMIN_PASSWORD
- [ ] Verified project path exists (`~/voting-system`)
- [ ] Set virtual environment path in Web tab
- [ ] Installed dependencies in virtual environment
- [ ] Clicked "Reload" button
- [ ] Checked error log for issues

---

## 💡 Working WSGI File Example

Here's a minimal working version:

```python
import sys
import os

# Update this to YOUR username!
sys.path.insert(0, '/home/priyankajain/voting-system')

# Environment variables
os.environ['SECRET_KEY'] = 'your-secret-here'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'admin123'

# Import and create app
from app import create_app
application = create_app()

# Initialize database
with application.app_context():
    from app import db
    db.create_all()
```

**Key points:**
1. `sys.path.insert(0, ...)` adds your project to Python path
2. `from app import create_app` imports YOUR app (not Flask template)
3. `application = create_app()` creates your voting system instance

---

## 🆘 Still Not Working?

### Option 1: Manual Test

SSH into PythonAnywhere bash and test:

```bash
cd ~/voting-system
workon voting-env
python3
```

Then:
```python
from app import create_app
app = create_app()
print("If you see this, your app works!")
```

If this works but WSGI doesn't, it's a path/import issue in WSGI.

### Option 2: Check Logs

```bash
# View error log
tail -50 /var/log/yourusername.pythonanywhere.com.error.log

# View server log
tail -50 /var/log/yourusername.pythonanywhere.com.server.log
```

### Option 3: Start Fresh

If completely stuck:

1. Delete web app in "Web" tab
2. Create new one: "Manual configuration" → Python 3.10
3. Follow PYTHONANYWHERE_SETUP.md from scratch
4. Use the WSGI template above

---

## ✅ Success Indicators

When it works, you should see:

- **Home page:** Voting system interface with "Assetz Sun and Sanctum"
- **Admin page:** Login form (not "Hello from Flask!")
- **No errors** in error log

---

## 📞 Quick Help Commands

**Check if app imports:**
```bash
python3 -c "from app import create_app; print('OK')"
```

**Check if dependencies installed:**
```bash
pip list | grep -i flask
```

**View last 20 lines of error log:**
```bash
tail -20 /var/log/*.error.log
```

---

**After fixing, you should see your voting system, not "Hello from Flask!"** 🎉
