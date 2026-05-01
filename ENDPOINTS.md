# Application Endpoints

Clear separation between voting and admin functions.

---

## 🏠 Main Endpoints

### **Landing Page**
- **URL:** `/`
- **Purpose:** Welcome page with two options
- **Access:** Public
- **Description:** Beautiful landing page with two cards:
  - **Vote** → Takes residents to voting interface
  - **Admin** → Takes admin to login page

---

### **Voting Interface**
- **URL:** `/vote`
- **Purpose:** Residents cast their votes
- **Access:** Public (when voting is enabled)
- **Flow:**
  1. Enter voter details (name, flat, wing, phone)
  2. See nominees from your wing only
  3. Select one male and one female representative
  4. Confirm and submit
  5. Receive counter number

**Related URLs:**
- `/vote` - Voter information form
- `/confirm` - Vote confirmation page
- `/submit` - Final submission (POST)

---

### **Admin Console**
- **URL:** `/admin`
- **Purpose:** Election management
- **Access:** Requires login (admin credentials)
- **Features:**
  - Dashboard with statistics
  - Wing management
  - Nominee management
  - Voting progress tracking
  - Result declaration
  - Excel exports
  - Password change
  - Archive elections
  - Start new election

**Admin URLs:**
- `/admin/login` - Admin login page
- `/admin/dashboard` - Main dashboard
- `/admin/wings` - Manage wings
- `/admin/nominees` - Manage nominees
- `/admin/progress` - View voting progress
- `/admin/settings` - Configure system
- `/admin/change-password` - Change admin password
- `/admin/archives` - View archived elections
- `/admin/archive-election` - Archive current election
- `/admin/new-election` - Start new election
- `/admin/declare-results` - Declare election results
- `/admin/logout` - Logout

---

### **Results Page**
- **URL:** `/results`
- **Purpose:** View election results
- **Access:** Public (when results are visible)
- **Shows:**
  - Winners by wing and gender
  - Vote counts
  - Rankings

**Related URLs:**
- `/results` - Public results page
- `/results/export/anonymous` - Export anonymous votes (admin only)
- `/results/export/detailed` - Export detailed votes (admin only)
- `/results/export/results` - Export results (admin only)

---

## 📊 Complete URL Structure

```
Your Website
│
├── / (Landing Page)
│   ├── Button: "Cast Your Vote" → /vote
│   └── Button: "Admin Login" → /admin/login
│
├── /vote (Voting Interface)
│   ├── /vote (Voter info form)
│   ├── /confirm (Confirmation page)
│   └── /submit (Submit vote)
│
├── /admin (Admin Console)
│   ├── /admin/login (Login page)
│   ├── /admin/dashboard (Dashboard)
│   ├── /admin/wings (Wing management)
│   ├── /admin/nominees (Nominee management)
│   ├── /admin/progress (Voting progress)
│   ├── /admin/settings (System settings)
│   ├── /admin/change-password (Change password)
│   ├── /admin/archives (View archives)
│   ├── /admin/archive-election (Archive current)
│   ├── /admin/new-election (Start new)
│   ├── /admin/declare-results (Declare results)
│   └── /admin/logout (Logout)
│
└── /results (Results Page)
    ├── /results (Public view)
    ├── /results/export/anonymous (Admin export)
    ├── /results/export/detailed (Admin export)
    └── /results/export/results (Admin export)
```

---

## 🔐 Access Control

### Public Access (No Login Required)
✅ `/` - Landing page
✅ `/vote` - Voting interface (when enabled)
✅ `/results` - Results (when visible)

### Admin Access (Login Required)
🔒 All `/admin/*` routes except `/admin/login`
🔒 All `/results/export/*` routes

---

## 🌐 For Residents

Share this URL with residents:
```
https://your-website.com
```

They'll see:
1. **Landing page** with two clear options
2. Click **"Cast Your Vote"** to start voting
3. Or click **"View Results"** to see election results

---

## 👤 For Administrators

Admin access:
```
https://your-website.com/admin
```

Or:
```
https://your-website.com/admin/login
```

Default credentials (change immediately!):
- Username: `admin`
- Password: `admin123`

---

## 📱 Mobile-Friendly

All endpoints are fully responsive and work on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones

---

## 🎨 Navigation Bar

The navigation bar at the top shows:

**For Everyone:**
- Home → Landing page
- Vote → Voting interface
- Results → Election results

**For Logged-in Admins:**
- Admin → Dashboard
- Logout → Logout and return to landing page

---

## 🔄 User Flow Examples

### Resident Voting:
1. Visit `/` (landing page)
2. Click "Cast Your Vote"
3. Redirected to `/vote`
4. Fill in voter details
5. See nominees from their wing
6. Select representatives
7. Confirm at `/confirm`
8. Submit vote
9. Receive counter number

### Admin Managing Election:
1. Visit `/admin` or `/admin/login`
2. Enter credentials
3. Redirected to `/admin/dashboard`
4. Add wings: `/admin/wings`
5. Add nominees: `/admin/nominees`
6. Monitor progress: `/admin/progress`
7. Declare results: Click button on dashboard
8. Export data: Download Excel files
9. Logout: Returns to landing page

---

## 📖 Quick Reference

| I want to... | Go to... |
|-------------|----------|
| See the main page | `/` |
| Vote | `/vote` |
| Login as admin | `/admin` or `/admin/login` |
| View results | `/results` |
| Manage election | `/admin/dashboard` (after login) |
| Add nominees | `/admin/nominees` (after login) |
| Change password | `/admin/change-password` (after login) |
| Archive election | `/admin/archives` (after login) |
| Start new election | `/admin/new-election` (after login) |

---

## 🚀 For PythonAnywhere or Other Hosting

When deployed, your URLs will be:

**PythonAnywhere:**
- Landing: `https://yourusername.pythonanywhere.com/`
- Voting: `https://yourusername.pythonanywhere.com/vote`
- Admin: `https://yourusername.pythonanywhere.com/admin`

**Custom Domain:**
- Landing: `https://yoursite.com/`
- Voting: `https://yoursite.com/vote`
- Admin: `https://yoursite.com/admin`

---

**Clean, simple, and easy to remember!** 🎉
