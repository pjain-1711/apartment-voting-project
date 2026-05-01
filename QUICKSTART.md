# Quick Start Guide

## Get Started in 5 Minutes!

### 1. Install Dependencies
```bash
cd voting-system
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

The application will start at: **http://localhost:5000**

### 3. Login as Admin
- Navigate to: **http://localhost:5000/admin/login**
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANT:** Change these credentials immediately in production!

### 4. Set Up Your Election

#### Step 1: Add Wings
1. Go to "Manage Wings" in admin panel
2. Click "Add Wing"
3. Add wings like: A, B, C, Tower 1, etc.

#### Step 2: Add Nominees
1. Go to "Manage Nominees"
2. Click "Add Nominee"
3. Fill in details:
   - Name
   - Gender (Male/Female)
   - Flat Number
   - Phone Number
   - Wing

#### Step 3: Enable Voting
1. Go to "Settings"
2. Toggle "Enable Voting" ON
3. Save settings

### 5. Start Voting!
- Share the home URL with residents: **http://localhost:5000**
- Each flat enters their details and votes
- System prevents duplicate votes automatically

### 6. Monitor Progress
- Check "Dashboard" for real-time statistics
- View "Voting Progress" for wing-wise details

### 7. Declare Results
1. When voting is complete, go to Dashboard
2. Click "Declare Results"
3. Winners are automatically calculated
4. Results become visible on the results page

### 8. Export Data
Download vote records:
- **Anonymous Export:** Vote data without voter names
- **Detailed Export:** Complete voter information
- **Results Export:** Election results with winners

## Accessing the System

### For Voters (Residents)
- **Home Page:** http://localhost:5000
- Enter flat details and vote

### For Administrators
- **Admin Login:** http://localhost:5000/admin/login
- **Dashboard:** http://localhost:5000/admin/dashboard

### View Results
- **Results Page:** http://localhost:5000/results
- (Only visible after admin declares results)

## Common Tasks

### Change Admin Password
Edit `.env` file:
```env
ADMIN_USERNAME=newadmin
ADMIN_PASSWORD=newsecurepassword123
```
Then restart the app.

### Reset Everything
```bash
# Delete database
rm instance/voting.db

# Restart app (database will be recreated)
python run.py
```

### Add Your Logo
1. Place your PNG logo file at: `app/static/images/logo.png`
2. Recommended size: 200x60 pixels
3. Refresh the page

## Production Deployment

### AWS Free Tier
See [README.md](README.md#aws-deployment) for detailed AWS deployment instructions.

### Environment Variables for Production
```bash
export SECRET_KEY="your-very-secret-random-key-here"
export ADMIN_USERNAME="your_admin"
export ADMIN_PASSWORD="strong_password"
export DATABASE_URL="postgresql://user:pass@host/db"
export FLASK_ENV="production"
```

## Troubleshooting

**Problem:** Can't access the app
- **Solution:** Make sure it's running on http://localhost:5000
- Check if another process is using port 5000

**Problem:** Forgot admin password
- **Solution:** Delete `instance/voting.db` and restart (this resets everything!)

**Problem:** Vote not submitting
- **Solution:** Check if voting is enabled in Settings

**Problem:** Results not showing
- **Solution:**
  1. Declare results from admin dashboard
  2. Make sure "Show Results" is enabled in Settings

## Need Help?

1. Check the full [README.md](README.md)
2. Review error messages in the terminal
3. Contact your development team

---

**🎉 You're ready to run your apartment elections!**
