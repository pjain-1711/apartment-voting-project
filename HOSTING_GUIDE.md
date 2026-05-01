# Hosting Guide - Free & Paid Options

## 🌐 Can I host on GitHub?

**GitHub Pages:** ❌ No - only for static sites (HTML/CSS/JS)
**GitHub (as code repository):** ✅ Yes - use it to store your code
**GitHub + Cloud Hosting:** ✅ Yes - best approach!

---

## 🆓 FREE Hosting Options (Recommended)

### Option 1: Render.com (EASIEST - Recommended)

**Cost:** FREE (500 hrs/month, sleeps after 15min inactivity)
**Perfect for:** Small elections, occasional use

#### Steps:

1. **Push to GitHub:**
   ```bash
   cd voting-system
   git remote add origin https://github.com/YOUR_USERNAME/voting-system.git
   git push -u origin main
   ```

2. **Create `render.yaml`:**
   ```bash
   cat > render.yaml << 'EOF'
   services:
     - type: web
       name: voting-system
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn run:app
       envVars:
         - key: FLASK_ENV
           value: production
         - key: SECRET_KEY
           generateValue: true
         - key: ADMIN_USERNAME
           value: admin
         - key: ADMIN_PASSWORD
           value: ChangeThisPassword123!

   databases:
     - name: voting-db
       databaseName: voting
       user: voting
   EOF
   ```

3. **Add gunicorn to requirements.txt:**
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push
   ```

5. **Deploy on Render:**
   - Go to https://render.com
   - Sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - It auto-detects render.yaml
   - Click "Create Web Service"

6. **Done!** Your URL: `https://voting-system-xyz.onrender.com`

**Note:** Free tier sleeps after 15min. First request takes 30s to wake up.

---

### Option 2: Railway.app (Easy + Always On)

**Cost:** $5/month (500 hours free, then paid)
**Perfect for:** Active elections needing 24/7 uptime

#### Steps:

1. **Push to GitHub** (same as above)

2. **Add railway.toml:**
   ```bash
   cat > railway.toml << 'EOF'
   [build]
   builder = "nixpacks"

   [deploy]
   startCommand = "gunicorn run:app"
   EOF
   ```

3. **Deploy:**
   - Go to https://railway.app
   - Sign up with GitHub
   - "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Add environment variables:
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-secret-key`
     - `ADMIN_USERNAME=admin`
     - `ADMIN_PASSWORD=SecurePass123!`
   - Deploy!

4. **Get URL:** `https://voting-system.up.railway.app`

---

### Option 3: PythonAnywhere (Simple Setup)

**Cost:** FREE tier available, $5/month for custom domain
**Perfect for:** Beginners, simple deployments

#### Steps:

1. **Sign up:** https://www.pythonanywhere.com

2. **Upload code:**
   - Dashboard → "Files"
   - Upload your folder or clone from GitHub

3. **Setup virtual env:**
   ```bash
   mkvirtualenv voting --python=/usr/bin/python3.10
   cd voting-system
   pip install -r requirements.txt
   ```

4. **Configure Web App:**
   - "Web" tab → "Add new web app"
   - Select "Manual configuration" → Python 3.10
   - Configure WSGI file (see detailed guide below)
   - Set virtualenv: `/home/yourusername/.virtualenvs/voting`

5. **Add environment variables in WSGI file:**

   ```python
   import os
   os.environ['SECRET_KEY'] = 'your-secret-key'
   os.environ['ADMIN_USERNAME'] = 'admin'
   os.environ['ADMIN_PASSWORD'] = 'SecurePassword123!'
   ```

   **📖 DETAILED GUIDE:** See [PYTHONANYWHERE_SETUP.md](PYTHONANYWHERE_SETUP.md) for complete WSGI configuration with templates!

6. **Reload** and your app is live!

**URL:** `https://yourusername.pythonanywhere.com`

---

### Option 4: Fly.io (Modern Platform)

**Cost:** FREE tier (3GB RAM, 160GB/month bandwidth)
**Perfect for:** Modern deployments

#### Quick Deploy:

1. **Install flyctl:**
   ```bash
   # macOS
   brew install flyctl

   # Linux
   curl -L https://fly.io/install.sh | sh

   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login:**
   ```bash
   flyctl auth login
   ```

3. **Initialize:**
   ```bash
   cd voting-system
   flyctl launch
   ```

4. **Follow prompts:**
   - App name: voting-system
   - Region: Choose closest
   - PostgreSQL: Yes (optional)
   - Deploy: Yes

5. **Set secrets:**
   ```bash
   flyctl secrets set SECRET_KEY=your-secret-key
   flyctl secrets set ADMIN_PASSWORD=SecurePass123!
   ```

6. **Done!** URL: `https://voting-system.fly.dev`

---

## 💰 Paid Options (Better Performance)

### AWS Elastic Beanstalk

**Cost:** ~$15-30/month
**Best for:** Production use, scalability

See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for full AWS guide.

### DigitalOcean App Platform

**Cost:** $5/month
**Setup:** Connect GitHub, deploy automatically

### Heroku

**Cost:** $7/month (Eco plan)
**Note:** No free tier anymore

---

## 📝 Pre-Deployment Checklist

Before hosting anywhere:

```bash
# 1. Add gunicorn
echo "gunicorn==21.2.0" >> requirements.txt

# 2. Update config.py for production
# Already done! Your config.py handles production automatically

# 3. Create .env file (don't commit this!)
cat > .env << 'EOF'
SECRET_KEY=your-very-long-random-secret-key-here
ADMIN_USERNAME=youradmin
ADMIN_PASSWORD=VeryStrongPassword123!
DATABASE_URL=postgresql://user:pass@host/db  # if using PostgreSQL
EOF

# 4. Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output to .env SECRET_KEY

# 5. Test locally with gunicorn
source venv/bin/activate
pip install gunicorn
gunicorn run:app
# Visit http://localhost:8000

# 6. Commit and push
git add .
git commit -m "Prepare for deployment"
git push
```

---

## 🎯 Recommended Approach

**For your apartment election:**

1. **Test locally first** with sqlite
2. **Deploy to Render.com FREE** for initial testing
3. **If election is active (multiple days):**
   - Upgrade to Railway ($5/month) for always-on
   - Or use AWS free tier (12 months)

---

## 🔄 GitHub Setup

### Create GitHub Repository:

1. **Create repo on GitHub:**
   - Go to https://github.com/new
   - Name: `voting-system` or `apartment-voting`
   - Keep it private (recommended) or public
   - Don't initialize with README (you already have one)

2. **Push your code:**
   ```bash
   cd voting-system
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Your code is now on GitHub!**

---

## 🚀 Quick Deploy Commands

### For Render.com:

```bash
# 1. Add deployment files
echo "gunicorn==21.2.0" >> requirements.txt
cat > render.yaml << 'EOF'
services:
  - type: web
    name: voting-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -b 0.0.0.0:$PORT run:app
EOF

# 2. Commit and push
git add .
git commit -m "Add Render deployment"
git push

# 3. Deploy on Render.com dashboard
```

### For Railway.app:

```bash
# 1. Add railway config
echo "gunicorn==21.2.0" >> requirements.txt
cat > Procfile << 'EOF'
web: gunicorn run:app
EOF

# 2. Commit and push
git add .
git commit -m "Add Railway deployment"
git push

# 3. Deploy on Railway.app dashboard
```

---

## 📱 Access Your Hosted App

Once deployed, share these URLs:

- **Voting:** `https://your-app-url.com`
- **Admin:** `https://your-app-url.com/admin/login`
- **Results:** `https://your-app-url.com/results`

---

## 💡 Cost Comparison

| Platform | Cost | Best For |
|----------|------|----------|
| Render.com | FREE | Testing, occasional use |
| Railway.app | $5/mo | Active elections |
| PythonAnywhere | FREE-$5/mo | Beginners |
| Fly.io | FREE | Modern stack |
| AWS | $15-30/mo | Production |
| DigitalOcean | $5/mo | Simplicity |

---

## 🔒 Security Notes

When hosting publicly:

1. **Change admin password immediately**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS** (most platforms do this automatically)
4. **Don't share admin credentials**
5. **Backup database regularly**

---

## ⚡ Quick Start: Deploy to Render in 5 Minutes

```bash
# 1. Prepare
cd voting-system
echo "gunicorn==21.2.0" >> requirements.txt

# 2. Create Procfile
echo "web: gunicorn run:app" > Procfile

# 3. Commit
git add .
git commit -m "Deploy to Render"

# 4. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/voting-system.git
git push -u origin main

# 5. Deploy
# Go to render.com → New Web Service → Connect GitHub → Deploy!
```

**Done! Your app is live in 5 minutes!** 🎉

---

Need help? Check specific platform docs:
- Render: https://render.com/docs/deploy-flask
- Railway: https://docs.railway.app/getting-started
- PythonAnywhere: https://help.pythonanywhere.com/pages/Flask/
