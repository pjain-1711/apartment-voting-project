# How to Run the Voting System

Complete step-by-step guide to get your voting system up and running.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.8 or higher** installed
  - Check: `python3 --version` or `python --version`
  - Download from: https://www.python.org/downloads/
- **pip** (Python package manager) - comes with Python
- **Terminal/Command Prompt** access
- **Web browser** (Chrome, Firefox, Safari, Edge)

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Project Directory

Open your terminal and navigate to the voting system folder:

```bash
cd /Users/priyankajain/claude-learning/voting-system
```

Or use your file path:
```bash
cd path/to/voting-system
```

### Step 2: Create Virtual Environment

Create an isolated Python environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
```

**On Windows:**
```cmd
python -m venv venv
```

✅ **What this does:** Creates a folder called `venv` that contains an isolated Python installation.

### Step 3: Activate Virtual Environment

Activate the environment you just created:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

✅ **Success indicator:** Your terminal prompt should now start with `(venv)`

Example:
```
(venv) user@computer:~/voting-system$
```

### Step 4: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

⏱️ **Time:** This takes 1-3 minutes depending on your internet speed.

✅ **Success:** You should see messages about successfully installing Flask, SQLAlchemy, and other packages.

### Step 5: Run the Application

Start the Flask development server:

```bash
python run.py
```

**Alternative command:**
```bash
python3 run.py
```

✅ **Success indicators:**
- You see: `Default admin user created: admin`
- You see: `WARNING` about in-memory storage (this is OK for development)
- You see: `Running on http://127.0.0.1:5000` or `Running on http://0.0.0.0:5000`
- You see: `Press CTRL+C to quit`

**Example output:**
```
Default admin user created: admin
 * Serving Flask app 'run'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 6: Open in Browser

Open your web browser and go to:

**Main URL:** http://localhost:5000

**Or try:** http://127.0.0.1:5000

✅ **Success:** You should see the voting system home page with the Assetz Sun and Sanctum title.

---

## 🔐 Access the Admin Panel

### Step 1: Navigate to Admin Login

In your browser, go to:

http://localhost:5000/admin/login

### Step 2: Login with Default Credentials

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change these credentials immediately!

### Step 3: You're In!

After login, you'll see the admin dashboard with statistics and management options.

---

## 🎯 Set Up Your First Election

### 1. Add Wings

From the admin dashboard:

1. Click **"Manage Wings"** in the sidebar
2. Click **"Add Wing"** button
3. Enter wing name (e.g., "A", "B", "Tower 1")
4. Click **"Add Wing"**
5. Repeat for all wings in your apartment

**Example wings:**
- A
- B
- C
- Tower 1
- Tower 2

### 2. Add Nominees

1. Click **"Manage Nominees"** in sidebar
2. Click **"Add Nominee"** button
3. Fill in the form:
   - **Name:** Full name of nominee
   - **Gender:** Select Male or Female
   - **Flat Number:** e.g., "101", "A-205"
   - **Wing:** Select from dropdown
   - **Phone Number:** 10-digit number
4. Click **"Add Nominee"**
5. Repeat for all nominees

**Example nominee:**
- Name: John Doe
- Gender: Male
- Flat Number: A-101
- Wing: A
- Phone: 9876543210

### 3. Configure Settings

1. Click **"Settings"** in sidebar
2. Configure:
   - ✅ **Enable Voting** - Turn this ON
   - **Show Results** - Keep OFF until voting completes
   - **Winners Per Gender** - Default is 2 (or set your preference)
3. Click **"Save Settings"**

### 4. Test Voting

1. Open a new browser tab (or incognito window)
2. Go to: http://localhost:5000
3. Fill in voter details:
   - Your Name
   - Flat Number
   - Select Wing
   - Phone Number
4. Click **"Proceed to Vote"**
5. Select one male and one female nominee
6. Review and confirm
7. Submit vote
8. Note your counter number!

### 5. Monitor Progress

Back in admin panel:
1. Go to **Dashboard** to see vote count
2. Go to **"Voting Progress"** to see wing-wise stats

### 6. Declare Results

When voting is complete:
1. Go to **Dashboard**
2. Click **"Declare Results"** button
3. Confirm the action
4. Go to **Settings** and toggle **"Show Results"** ON
5. Save settings

### 7. View Results

Anyone can now view results at:
http://localhost:5000/results

Winners are highlighted in gold!

### 8. Export Data

From Dashboard, click:
- **"Anonymous"** - Vote data without voter names
- **"Detailed"** - Complete voter information
- **"Export Results"** - Election results

Files download as Excel (.xlsx) format.

---

## 🛑 Stop the Application

To stop the server:

1. Go to the terminal where the app is running
2. Press: **CTRL + C**

✅ The server will shut down gracefully.

---

## 🔄 Restart the Application

To run it again later:

```bash
# Navigate to project folder
cd /Users/priyankajain/claude-learning/voting-system

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run the app
python run.py
```

---

## 🌐 Access from Other Devices (Same Network)

To allow other people on your network to vote:

### Step 1: Find Your IP Address

**On macOS:**
```bash
ipconfig getifaddr en0
```
Or: System Settings → Network → Look for your IP

**On Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address"

**On Linux:**
```bash
hostname -I
```

### Step 2: Share the URL

If your IP is `192.168.1.100`, share:
```
http://192.168.1.100:5000
```

⚠️ **Note:** Other devices must be on the same WiFi network!

---

## 📱 Test on Mobile

1. Find your computer's IP address (see above)
2. On your phone, connect to same WiFi
3. Open browser and go to: `http://YOUR-IP:5000`
4. The interface is mobile-responsive!

---

## 🐛 Troubleshooting

### Problem: "Command not found: python3"

**Solution:** Try `python` instead:
```bash
python run.py
```

### Problem: "Port 5000 already in use"

**Solution 1 - Kill the process:**

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Windows:**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Solution 2 - Use different port:**
```bash
# Edit run.py and change port to 5001
python run.py
```

### Problem: "Module not found" errors

**Solution:** Make sure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Can't access from other devices

**Solutions:**
1. Check firewall settings - allow port 5000
2. Make sure both devices on same network
3. Verify IP address is correct
4. Try: `python run.py` (it binds to 0.0.0.0 by default)

### Problem: "Database locked" error

**Solution:** Stop any other instances of the app:
```bash
# macOS/Linux
pkill -f "python run.py"

# Windows
# Close all Python processes from Task Manager
```

### Problem: Changes not showing up

**Solution:** Hard refresh the browser:
- **Chrome/Firefox:** CTRL + SHIFT + R (Windows/Linux) or CMD + SHIFT + R (Mac)
- **Safari:** CMD + OPTION + R

### Problem: Forgot admin password

**Solution:** Reset the database:
```bash
# Stop the app (CTRL+C)
rm instance/voting.db
python run.py
# Default credentials restored: admin/admin123
```

⚠️ **Warning:** This deletes ALL data (wings, nominees, votes)!

---

## 📊 Viewing Database

To inspect the database directly:

```bash
# Install SQLite browser (optional)
# macOS
brew install --cask db-browser-for-sqlite

# Or use command line
sqlite3 instance/voting.db

# Once in sqlite3:
.tables                    # List all tables
SELECT * FROM wings;       # View wings
SELECT * FROM nominees;    # View nominees
SELECT * FROM voters;      # View voters
.exit                      # Exit
```

---

## 🔧 Advanced Configuration

### Change Default Port

Edit `run.py`, line 26:
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Changed to 8080
```

### Change Admin Credentials

Create/edit `.env` file:
```env
ADMIN_USERNAME=myadmin
ADMIN_PASSWORD=MySecurePassword123!
```

Delete database and restart:
```bash
rm instance/voting.db
python run.py
```

### Enable Debug Mode

Already enabled in development! You'll see detailed error messages.

### Disable Debug Mode

Edit `run.py`, line 26:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

---

## 📂 File Locations

- **Database:** `instance/voting.db`
- **Logs:** Appear in terminal
- **Templates:** `app/templates/`
- **Static files:** `app/static/`
- **Configuration:** `config.py`

---

## 🎓 Quick Reference

### Essential Commands

| Action | Command |
|--------|---------|
| Activate venv | `source venv/bin/activate` (Mac/Linux)<br>`venv\Scripts\activate` (Windows) |
| Install deps | `pip install -r requirements.txt` |
| Run app | `python run.py` |
| Stop app | Press `CTRL + C` |
| Reset database | `rm instance/voting.db` (then restart) |

### Important URLs

| Page | URL |
|------|-----|
| Home (Voting) | http://localhost:5000 |
| Admin Login | http://localhost:5000/admin/login |
| Dashboard | http://localhost:5000/admin/dashboard |
| Results | http://localhost:5000/results |

### Default Credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

---

## 💡 Tips for Running Elections

1. **Test First:** Run through the complete process with test data before real election
2. **Backup Data:** Copy `instance/voting.db` before declaring results
3. **Monitor Progress:** Check dashboard regularly during voting period
4. **Announce Clearly:** Share the voting URL and deadline with all residents
5. **Technical Support:** Be available to help residents who face issues
6. **Export Early:** Download anonymous and detailed exports before making changes
7. **Verify Results:** Review results carefully before declaring them public

---

## 📞 Need More Help?

- Check [README.md](README.md) for detailed documentation
- Review [QUICKSTART.md](QUICKSTART.md) for setup overview
- See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for production deployment
- Read [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt) for complete feature list

---

## ✅ Success Checklist

Before starting your real election:

- [ ] Application runs without errors
- [ ] You can login to admin panel
- [ ] All wings are added
- [ ] All nominees are added correctly
- [ ] Settings configured (voting enabled, winner count set)
- [ ] Tested voting process end-to-end
- [ ] Verified duplicate vote prevention works
- [ ] Tested on mobile device
- [ ] Checked results page works
- [ ] Tested Excel exports
- [ ] Changed admin password (for production)
- [ ] Backed up empty database as template

---

**You're all set! Good luck with your election! 🗳️**
