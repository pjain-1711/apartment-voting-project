# Deployment Checklist

Use this checklist when deploying to production (AWS or any cloud platform).

## Pre-Deployment Checklist

### Security
- [ ] Change admin username from default `admin`
- [ ] Change admin password from default `admin123`
- [ ] Generate strong SECRET_KEY (use `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Review and update `.env` with production values
- [ ] Never commit `.env` file to git
- [ ] Enable HTTPS/SSL certificate
- [ ] Set `SESSION_COOKIE_SECURE=True` in production config

### Database
- [ ] Set up PostgreSQL database (AWS RDS recommended)
- [ ] Note down database connection URL
- [ ] Set DATABASE_URL environment variable
- [ ] Test database connection
- [ ] Plan backup strategy

### Application Configuration
- [ ] Set `FLASK_ENV=production`
- [ ] Add your logo at `app/static/images/logo.png`
- [ ] Test all features locally before deployment
- [ ] Review rate limiting settings (currently 5 votes/hour per IP)
- [ ] Decide on configurable settings defaults:
  - Voting enabled: true/false
  - Results visible: true/false
  - Winners per gender: 2 (or your preference)

### AWS Specific (if using AWS)
- [ ] Create AWS account
- [ ] Set up IAM user with appropriate permissions
- [ ] Choose deployment method:
  - [ ] Elastic Beanstalk (easier, recommended)
  - [ ] EC2 + Nginx + Gunicorn (more control)
- [ ] Set up RDS PostgreSQL instance (t3.micro for free tier)
- [ ] Configure security groups (allow port 80, 443)
- [ ] Set up billing alerts

## Deployment Steps

### Option A: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init -p python-3.11 assetz-voting-system
   ```

3. **Create EB Environment**
   ```bash
   eb create assetz-voting-env
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv \
     FLASK_ENV=production \
     SECRET_KEY=your-secret-key \
     ADMIN_USERNAME=your-admin \
     ADMIN_PASSWORD=strong-password \
     DATABASE_URL=postgresql://user:pass@host/db
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

6. **Open Application**
   ```bash
   eb open
   ```

### Option B: EC2 Manual Deployment

1. **Launch EC2 Instance**
   - Instance type: t2.micro (free tier)
   - OS: Ubuntu 22.04 LTS
   - Security group: Allow ports 22, 80, 443

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip

   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and dependencies
   sudo apt install python3-pip python3-venv nginx -y

   # Clone your repository
   git clone <your-repo-url>
   cd voting-system

   # Set up virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Create Environment File**
   ```bash
   nano .env
   # Add all production environment variables
   ```

4. **Set up Gunicorn Service**
   ```bash
   sudo nano /etc/systemd/system/voting.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Voting System Gunicorn
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/voting-system
   Environment="PATH=/home/ubuntu/voting-system/venv/bin"
   ExecStart=/home/ubuntu/voting-system/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 run:app

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable voting
   sudo systemctl start voting
   ```

5. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/voting
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /home/ubuntu/voting-system/app/static;
       }
   }
   ```

   Enable and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/voting /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Post-Deployment Checklist

### Verification
- [ ] Application loads at your URL
- [ ] Admin login works
- [ ] Can add wings
- [ ] Can add nominees
- [ ] Voting process works end-to-end
- [ ] Results declaration works
- [ ] Excel exports download correctly
- [ ] Logo displays correctly
- [ ] Mobile responsiveness works
- [ ] HTTPS is working (if configured)

### Initial Setup
- [ ] Login as admin
- [ ] Change admin password immediately
- [ ] Add all wings for your apartment
- [ ] Configure settings (voting enabled, winner count)
- [ ] Test with one sample vote
- [ ] Delete test data if needed

### Monitoring
- [ ] Set up AWS CloudWatch (if using AWS)
- [ ] Configure billing alerts
- [ ] Set up database backups
- [ ] Monitor application logs
- [ ] Check disk space usage
- [ ] Monitor database connections

### Communication
- [ ] Share voting URL with residents
- [ ] Provide admin contact information
- [ ] Announce voting period
- [ ] Set deadline for voting
- [ ] Plan result declaration timing

## Maintenance Tasks

### During Voting Period
- [ ] Monitor voting progress daily
- [ ] Check for any errors in logs
- [ ] Be available for technical support
- [ ] Keep backups of database

### After Election
- [ ] Declare results at scheduled time
- [ ] Export all data (anonymous + detailed)
- [ ] Store exports securely
- [ ] Optionally disable voting
- [ ] Make results visible

### Database Backup
- [ ] Set up automated daily backups
- [ ] Test restore process
- [ ] Store backups securely
- [ ] Keep backups for required duration

## Rollback Plan

If something goes wrong:

1. **AWS EB:**
   ```bash
   eb deploy --version <previous-version>
   ```

2. **Manual:**
   - Restore database from backup
   - Revert to previous git commit
   - Restart application

## Cost Optimization

### AWS Free Tier (12 months)
- EC2 t2.micro: 750 hours/month
- RDS t3.micro: 750 hours/month
- 20GB storage

**Estimated monthly cost after free tier:**
- EC2 t2.micro: ~$8-10/month
- RDS t3.micro: ~$15-20/month
- Total: ~$25-30/month

### Tips to Reduce Costs
- [ ] Use SQLite for very small deployments (< 50 flats)
- [ ] Stop instances when not in use (if election is time-bound)
- [ ] Use single EC2 with SQLite instead of RDS
- [ ] Set up billing alerts at $1, $5, $10

## Emergency Contacts

**Technical Issues:**
- AWS Support (if subscribed)
- Development team contact
- Database administrator

**Important URLs:**
- Production URL: _______________
- Admin panel: _______________/admin/login
- AWS Console: https://console.aws.amazon.com

## Backup Admin Credentials

**Store these SECURELY (password manager recommended):**
- Admin Username: _______________
- Admin Password: _______________
- Database URL: _______________
- AWS Access Key: _______________

---

## Quick Reference Commands

### Check application status
```bash
# Gunicorn service
sudo systemctl status voting

# Nginx
sudo systemctl status nginx

# View logs
sudo journalctl -u voting -f
```

### Restart application
```bash
sudo systemctl restart voting
sudo systemctl restart nginx
```

### Update application
```bash
cd voting-system
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart voting
```

### Database backup (manual)
```bash
# PostgreSQL
pg_dump -h localhost -U username dbname > backup_$(date +%Y%m%d).sql

# SQLite
cp instance/voting.db backups/voting_$(date +%Y%m%d).db
```

---

**Remember:** Always test changes in a staging environment before deploying to production!
