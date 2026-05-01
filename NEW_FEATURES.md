# New Admin Features

Three powerful new features have been added to help you manage multiple elections and maintain security.

---

## 🔑 1. Change Admin Password

**Location:** Admin Panel → Change Password

### What it does:
- Allows you to update the admin password from within the app
- No need to reset the database or edit config files

### How to use:

1. Login to admin panel
2. Click **"Change Password"** in the sidebar
3. Enter:
   - Current password
   - New password (minimum 8 characters)
   - Confirm new password
4. Click **"Change Password"**

### Security Features:
- Requires current password for verification
- Minimum 8 character requirement
- Password confirmation to prevent typos
- Bcrypt hashing for secure storage

### When to use:
- ✅ After initial setup (change from default `admin123`)
- ✅ Periodically for security (every 3-6 months)
- ✅ If you suspect password has been compromised
- ✅ When transferring admin responsibilities

---

## 📦 2. Archive Elections (Stash Results)

**Location:** Admin Panel → Archives → Archive Election

### What it does:
- Saves complete election data permanently
- Preserves historical records
- Allows you to reference past elections

### What gets archived:
✅ All wings and their details
✅ All nominees and their information
✅ All votes (anonymized with counter numbers)
✅ Complete results with winners
✅ Vote counts and rankings
✅ Timestamps

### How to use:

**Step 1: Archive Current Election**
1. Login to admin panel
2. Click **"Archives"** in sidebar
3. Click **"Archive Current Election"**
4. Give it a memorable name (e.g., "2026 Wing Representatives Election")
5. Click **"Archive Election"**

**Step 2: View Archived Elections**
1. Go to **"Archives"**
2. See list of all archived elections
3. Click **"View"** to see detailed results
4. Click **"Delete"** to remove an archive (if needed)

### Archive Details Include:
- Election name and date
- Total votes, nominees, and wings
- Winners by wing and gender
- Full voting statistics

### When to use:
- ✅ Before starting a new election
- ✅ At the end of each election cycle
- ✅ For compliance/record-keeping requirements
- ✅ To compare results across years

### Important Notes:
⚠️ **Archiving does NOT delete current data**
→ Use "New Election" feature to clear data after archiving

💡 **Best Practice:**
1. Archive current election
2. Export Excel files (anonymous + detailed)
3. Then start new election

---

## 🆕 3. Start New Election

**Location:** Admin Panel → New Election

### What it does:
- Clears old election data
- Prepares system for a fresh election
- Offers flexible reset options

### Three Reset Options:

#### Option 1: Keep Nominees & Wings (Recommended)
**Use when:** Running another election with same candidates

**Deletes:**
- ✅ All votes
- ✅ All results

**Keeps:**
- ✅ Wings
- ✅ Nominees
- ✅ All nominee details

**Perfect for:**
- Re-election or runoff with same nominees
- Quick reset between voting rounds

---

#### Option 2: Keep Wings Only
**Use when:** New election with different nominees, same building structure

**Deletes:**
- ✅ All votes
- ✅ All results
- ✅ All nominees

**Keeps:**
- ✅ Wings structure

**Perfect for:**
- Annual elections with new candidates
- Same wings, different people

---

#### Option 3: Complete Reset
**Use when:** Complete fresh start

**Deletes:**
- ✅ All votes
- ✅ All results
- ✅ All nominees
- ✅ All wings

**Keeps:**
- ✅ Admin account
- ✅ System settings
- ✅ Archived elections (if any)

**Perfect for:**
- Testing purposes
- Major restructuring
- Building expansion/changes

---

### How to use:

1. **Archive First (Recommended!)**
   - Go to Archives → Archive Current Election
   - Save your data before deleting

2. **Start New Election**
   - Go to **"New Election"**
   - Review current data summary
   - Choose reset option
   - Check the confirmation box
   - Click **"Start New Election"**

3. **Set Up New Election**
   - Add/update wings (if needed)
   - Add new nominees (if needed)
   - Enable voting in Settings
   - Start accepting votes!

### Safety Features:
- 🔒 Requires explicit confirmation checkbox
- ⚠️ Shows warning about data deletion
- 💡 Reminds you to archive first
- 📊 Displays current data before deletion

---

## 🎯 Complete Workflow Example

Here's how to manage multiple election cycles:

### End of Current Election:

1. **Declare Results**
   - Dashboard → Declare Results
   - Results become visible

2. **Export Data**
   - Download Anonymous Excel
   - Download Detailed Excel
   - Download Results Excel
   - Store files securely

3. **Archive Election**
   - Archives → Archive Current Election
   - Name: "2026 Wing Representatives"
   - Save permanently

4. **Start New Election**
   - New Election → Choose reset option
   - Recommended: "Keep Wings Only"
   - Confirm and clear data

5. **Set Up Next Election**
   - Add new nominees
   - Configure settings
   - Enable voting
   - Announce to residents

---

## 📍 Quick Access

All new features are in the admin sidebar:

```
Admin Panel
├── Dashboard
├── Manage Wings
├── Manage Nominees
├── Voting Progress
├── Settings
├── ─────────────
├── Change Password  ← NEW
├── Archives         ← NEW
└── New Election     ← NEW
```

Also accessible from Dashboard action cards!

---

## 🔐 Security Best Practices

1. **Change Default Password Immediately**
   ```
   Default: admin / admin123
   → Change to: YourSecurePassword123!
   ```

2. **Use Strong Passwords**
   - Minimum 8 characters (enforced)
   - Mix letters, numbers, symbols
   - Don't reuse passwords
   - Store securely (password manager)

3. **Archive Regularly**
   - After each election
   - Before major changes
   - Keep permanent records

4. **Backup Archive Data**
   - Export Excel files
   - Store in multiple locations
   - Keep for required duration

---

## 💡 Pro Tips

1. **Before New Election:**
   - ✅ Archive current data
   - ✅ Export all Excel files
   - ✅ Verify archives are saved
   - ✅ Then reset

2. **Password Management:**
   - Change every 3-6 months
   - Use password manager
   - Don't share credentials
   - Different from personal passwords

3. **Archive Naming:**
   - Include year: "2026 Election"
   - Be specific: "April 2026 Wing Rep Election"
   - Consistent format helps searching

4. **Reset Strategy:**
   - Same nominees? → Keep Nominees & Wings
   - New nominees? → Keep Wings Only
   - Testing/Major change? → Complete Reset

---

## 📞 Need Help?

### Common Questions:

**Q: Can I undo "New Election"?**
A: No, deletion is permanent. That's why archiving first is crucial!

**Q: How many elections can I archive?**
A: Unlimited! Each archive is stored in the database.

**Q: Will archiving slow down my system?**
A: No. Archives are stored as compressed JSON. Very efficient.

**Q: Can I export archived data?**
A: Yes! View archive details to see all information. You can also manually query the database.

**Q: What if I forget my new password?**
A: Delete `instance/voting.db` and restart app. This resets everything to defaults (admin/admin123).

**Q: Can I change admin username?**
A: Currently only password change is supported. Username change requires database modification.

---

## ✅ Testing Checklist

Before using in production:

- [ ] Test password change with strong password
- [ ] Create test election data
- [ ] Archive the test election
- [ ] Verify archive appears in list
- [ ] View archived election details
- [ ] Test all three reset options
- [ ] Verify correct data is deleted/kept
- [ ] Delete test archive
- [ ] Set up production election

---

**Ready to use these features!** They make managing multiple elections safe and easy. 🎉
