# Voting Timer Feature

## ⏱️ Overview

Each voter has **2 minutes** to complete their vote selection. This ensures fair access and prevents voters from holding the voting page open indefinitely.

---

## 🎯 How It Works

### For Voters:

1. **Start Voting**
   - Enter your details on the voting page
   - Click "Proceed to Vote"
   - Timer starts automatically

2. **Timer Display**
   - Shows at the top of the vote selection page
   - Format: `2:00` (minutes:seconds)
   - Progress bar shows remaining time visually

3. **Color Indicators**
   - 🟢 **Green** (2:00 - 0:31): Plenty of time
   - 🟡 **Yellow** (0:30 - 0:11): Time running low
   - 🔴 **Red** (0:10 - 0:00): Warning - almost expired!

4. **10-Second Warning**
   - Alert box flashes
   - Timer text pulses
   - Alert sound plays (beep)

5. **Time Expired**
   - Form becomes disabled
   - "Start Over" button appears
   - Must begin voting process again

---

## 🔒 Security Features

### Cannot Be Bypassed:

✅ **Server-side validation**
- Timer start time stored in session
- Backend checks elapsed time
- Refreshing page doesn't reset timer

✅ **Multiple checkpoints**
- Validated when reviewing selections
- Validated when submitting vote
- Session cleared if expired

✅ **Fair for everyone**
- Same 2-minute limit for all voters
- Prevents monopolizing the system

---

## 📱 Visual Indicators

### Timer Alert Box

```
┌─────────────────────────────────────┐
│ 🕐 Time Remaining:         2:00    │
│ ████████████████████████ 100%      │
└─────────────────────────────────────┘
```

**States:**

**Normal (Green):**
```
┌─────────────────────────────────────┐
│ 🕐 Time Remaining:         1:45    │
│ ████████████████████░░░░░░ 87%     │
└─────────────────────────────────────┘
```

**Warning (Yellow - 30 seconds):**
```
┌─────────────────────────────────────┐
│ 🕐 Time Remaining:         0:25    │
│ ██████░░░░░░░░░░░░░░░░░░░░ 20%     │
└─────────────────────────────────────┘
```

**Critical (Red - 10 seconds, FLASHING):**
```
┌─────────────────────────────────────┐
│ 🕐 Time Remaining:         0:07    │
│ ██░░░░░░░░░░░░░░░░░░░░░░░░ 5%      │
└─────────────────────────────────────┘
** FLASHING **
```

**Expired:**
```
┌─────────────────────────────────────┐
│        ⏰ Time Expired!             │
│  Your voting time has expired.      │
│  Please start over.                 │
│                                     │
│  [🔄 Start Over]                    │
└─────────────────────────────────────┘
```

---

## 💡 User Experience

### What Happens When Time Runs Out:

1. **Alert Sound** plays (subtle beep)
2. **Form Disabled**
   - Submit button shows "Time Expired"
   - All nominee selections disabled
   - Cannot proceed with vote
3. **Clear Message**
   - "Time Expired!" in red
   - "Start Over" button provided
4. **Session Cleared**
   - Must re-enter voter details
   - Fresh 2-minute timer starts

---

## 🔧 Technical Details

### Frontend (JavaScript)

**Timer Update:** Every 1 second
```javascript
const TOTAL_TIME = 120;  // 2 minutes
const WARNING_TIME = 10; // Flash at 10 seconds
```

**Functions:**
- `updateTimer()` - Updates display and progress bar
- `handleTimeExpired()` - Disables form when time is up
- `playAlertSound()` - Beep notification

**Animations:**
- Flash effect on alert box (0.5s intervals)
- Pulse effect on timer text
- Smooth progress bar transitions

### Backend (Python/Flask)

**Session Storage:**
```python
session['timer_start'] = datetime.utcnow().timestamp()
```

**Validation Points:**
1. `/confirm` route - Checks before showing confirmation
2. `/submit` route - Final check before recording vote

**Validation Logic:**
```python
elapsed_time = datetime.utcnow().timestamp() - timer_start
if elapsed_time > 120:
    session.clear()
    flash('Voting time expired')
    return redirect(url_for('voting.index'))
```

---

## ⚙️ Configuration

### Changing Timer Duration

Edit `app/templates/voting/vote_selection.html`:

```javascript
// Change this value (in seconds)
const TOTAL_TIME = 120;  // 2 minutes

// Change warning threshold
const WARNING_TIME = 10;  // Flash at 10 seconds
```

**Examples:**
- 1 minute: `const TOTAL_TIME = 60;`
- 3 minutes: `const TOTAL_TIME = 180;`
- 5 minutes: `const TOTAL_TIME = 300;`

**Don't forget to update backend validation:**

Edit `app/routes/voting.py`:
```python
# Change 120 to your desired time in seconds
if elapsed_time > 120:
```

---

## 🎨 Customization

### Change Warning Time

To flash warning at different time (e.g., 20 seconds):

```javascript
const WARNING_TIME = 20;  // Flash at 20 seconds
```

### Disable Sound

Comment out the sound function call:

```javascript
function handleTimeExpired() {
    // ... other code ...
    // playAlertSound();  // ← Comment this out
}
```

### Change Alert Sound

Modify the `playAlertSound()` function:

```javascript
function playAlertSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = 1000;  // ← Change frequency (higher = higher pitch)
    oscillator.type = 'sine';           // ← Change type: 'sine', 'square', 'sawtooth', 'triangle'

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}
```

---

## 📊 Timer States Flow

```
Start Voting
    ↓
Timer Starts (2:00)
    ↓
    ├─→ [Green Progress Bar] (2:00 - 0:31)
    │   - Normal voting
    │   - No alerts
    │
    ├─→ [Yellow Progress Bar] (0:30 - 0:11)
    │   - Warning: Time running low
    │   - Alert box turns yellow
    │
    ├─→ [Red Progress Bar + FLASH] (0:10 - 0:00)
    │   - Critical warning
    │   - Flashing alert
    │   - Pulsing timer
    │
    └─→ [Time Expired] (0:00)
        - Form disabled
        - Alert sound
        - Start over button
```

---

## 🐛 Troubleshooting

### Timer Not Starting

**Check:** JavaScript console for errors
```
Press F12 → Console tab
```

**Solution:** Ensure page fully loaded before timer starts

### Timer Resets on Refresh

**Expected Behavior:** Timer does NOT reset - backend tracks start time

**If it resets:** Check that session is working properly

### No Sound on Timeout

**Cause:** Browser may block autoplay audio

**Solution:** This is normal - sound is a bonus, visual indicators are primary

### Time Seems Off

**Cause:** Server and client time difference

**Solution:** Server-side validation is authoritative

---

## ✅ Testing Checklist

- [ ] Timer displays correctly (2:00)
- [ ] Progress bar updates every second
- [ ] Color changes at 30 seconds (yellow)
- [ ] Flashing starts at 10 seconds (red)
- [ ] Alert sound plays at 0:00
- [ ] Form disables after timeout
- [ ] "Start Over" button appears
- [ ] Refreshing page doesn't reset timer
- [ ] Backend validation prevents expired submissions
- [ ] Session cleared after timeout

---

## 💬 User Instructions

Add this to your voting instructions:

> **⏱️ Important: You have 2 minutes to cast your vote**
>
> - A timer will appear at the top of the page
> - The timer will turn yellow when you have 30 seconds left
> - The timer will flash red when you have 10 seconds left
> - If time runs out, you'll need to start over
> - Take your time, but don't leave the page open too long!

---

## 📈 Why This Feature?

**Benefits:**

1. ✅ **Fair Access**
   - Prevents voters from holding the page indefinitely
   - Ensures everyone gets equal opportunity

2. ✅ **Prevents Session Issues**
   - Forces completion within reasonable time
   - Reduces abandoned sessions

3. ✅ **Creates Urgency**
   - Encourages focused decision-making
   - Reduces indecision

4. ✅ **System Efficiency**
   - Frees up resources
   - Better session management

5. ✅ **Security**
   - Reduces risk of interference
   - Limits session hijacking window

---

**The timer makes voting more efficient while keeping it fair for everyone!** ⏰
