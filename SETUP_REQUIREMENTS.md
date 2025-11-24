# 📋 Wellness Companion - Complete Setup Requirements

## 🎯 What You Need

### 1. API Keys (Already Have ✅)
- ✅ Google API Key (Gemini)
- ✅ Murf API Key (TTS)
- ✅ Deepgram API Key (STT)
- ✅ LiveKit (Running locally)

### 2. Notion Setup (Need to Do 📝)
- [ ] Notion Integration Token
- [ ] Notion Database ID

---

## 📓 Notion Setup - Step by Step

### Step 1: Create Notion Integration (5 minutes)

1. **Go to Notion Integrations**
   - Open: https://www.notion.so/my-integrations
   - Click **"+ New integration"**

2. **Fill in Details**
   ```
   Name: Wellness Companion
   Associated workspace: [Select your workspace]
   Type: Internal integration
   ```

3. **Submit and Copy Token**
   - Click **"Submit"**
   - You'll see: `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **COPY THIS TOKEN** - you'll need it!

---

### Step 2: Create Wellness Database (5 minutes)

1. **Create New Page in Notion**
   - Open Notion
   - Click **"+ New page"**
   - Name it: **"Daily Wellness Journal"**

2. **Add Database**
   - Type `/database` and select **"Table - Inline"**
   - Or click **"Table"** from the blocks menu

3. **Create These Columns** (Properties)

   | Column Name | Type | How to Add |
   |-------------|------|------------|
   | **Date** | Date | Click "+", select "Date" |
   | **Mood** | Text | Click "+", select "Text" |
   | **Objectives** | Text | Click "+", select "Text" |
   | **Summary** | Text | Click "+", select "Text" |

4. **Your Database Should Look Like This:**
   ```
   ┌──────────────┬─────────────┬──────────────────┬─────────────┐
   │ Date         │ Mood        │ Objectives       │ Summary     │
   ├──────────────┼─────────────┼──────────────────┼─────────────┤
   │ (empty rows) │             │                  │             │
   └──────────────┴─────────────┴──────────────────┴─────────────┘
   ```

---

### Step 3: Share Database with Integration (2 minutes)

1. **Open Your Database**
   - Go to your "Daily Wellness Journal" page

2. **Click the "..." Menu**
   - Top right corner of the page
   - Click the three dots (...)

3. **Add Connection**
   - Scroll down to **"Connections"**
   - Click **"Add connections"**
   - Find and select **"Wellness Companion"** (your integration)
   - Click **"Confirm"**

---

### Step 4: Get Database ID (2 minutes)

1. **Open Database in Browser**
   - Make sure you're viewing the database page
   - Look at the URL in your browser

2. **Copy Database ID from URL**
   ```
   URL Format:
   https://www.notion.so/workspace/DATABASE_ID?v=VIEW_ID
                                   ↑
                                   This part!
   
   Example:
   https://www.notion.so/myworkspace/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6?v=...
                                     ↑─────────────────────────────↑
                                     Copy this 32-character ID
   ```

3. **The Database ID is:**
   - 32 characters long
   - Mix of letters and numbers
   - No dashes or spaces
   - Example: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

---

### Step 5: Add Keys to .env File (1 minute)

1. **Open** `backend/.env`

2. **Add Your Keys:**
   ```env
   NOTION_API_TOKEN=secret_your_actual_token_here
   NOTION_DATABASE_ID=your_actual_database_id_here
   ```

3. **Example (with fake keys):**
   ```env
   NOTION_API_TOKEN=secret_abc123def456ghi789jkl012mno345pqr678
   NOTION_DATABASE_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

---

## ✅ Verification Checklist

### Before Starting
- [ ] I have a Notion account
- [ ] I can access https://www.notion.so/my-integrations
- [ ] I have the backend/.env file open

### After Setup
- [ ] Created Notion integration
- [ ] Copied integration token
- [ ] Created "Daily Wellness Journal" database
- [ ] Added 4 columns: Date, Mood, Objectives, Summary
- [ ] Shared database with integration
- [ ] Copied database ID from URL
- [ ] Added both keys to backend/.env
- [ ] Saved the .env file

---

## 🧪 Testing Your Setup

### Step 1: Restart Backend
```bash
cd backend
uv run python src/agent.py dev
```

### Step 2: Start Frontend (if not running)
```bash
cd frontend
pnpm dev
```

### Step 3: Have a Conversation
1. Open http://localhost:3000
2. Click "Begin Check-in"
3. Talk about your mood and goals
4. Complete the conversation

### Step 4: Check Notion
1. Go to your "Daily Wellness Journal" in Notion
2. You should see a new entry with:
   - Today's date
   - Your mood
   - Your objectives
   - Summary

---

## 🎯 What You'll Get

### Notion Database View
```
┌──────────────┬─────────────────────────┬──────────────────────────────┬─────────────────────┐
│ Date         │ Mood                    │ Objectives                   │ Summary             │
├──────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────┤
│ Nov 24, 2025 │ Feeling energized       │ Complete project, Walk,      │ User is in good     │
│ 2:45 PM      │ and optimistic          │ Meditate                     │ spirits             │
├──────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────┤
│ Nov 25, 2025 │ A bit tired but         │ Finish report, Call mom,     │ User needs rest     │
│ 9:30 AM      │ motivated               │ Yoga session                 │ but staying focused │
└──────────────┴─────────────────────────┴──────────────────────────────┴─────────────────────┘
```

---

## 🔧 Troubleshooting

### "Failed to save to Notion"

**Check 1: Integration Token**
```env
# Make sure it starts with "secret_"
NOTION_API_TOKEN=secret_abc123...
```

**Check 2: Database ID**
```env
# Should be 32 characters, no dashes
NOTION_DATABASE_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Check 3: Database Shared**
- Go to database in Notion
- Click "..." menu
- Check "Connections"
- Your integration should be listed

**Check 4: Column Names**
- Must be exactly: `Date`, `Mood`, `Objectives`, `Summary`
- Case-sensitive!

### "Notion API error: 401"
- Your token is wrong or expired
- Create a new integration and get a new token

### "Notion API error: 404"
- Database ID is wrong
- Double-check the ID from the URL
- Make sure you copied the right part

### Still Not Working?
Check the backend terminal for detailed errors:
```
ERROR agent Error saving to Notion: [detailed error message]
```

---

## 📱 Bonus: Notion Mobile Access

### On Your Phone
1. Download Notion app (iOS/Android)
2. Sign in to your account
3. Find "Daily Wellness Journal"
4. View and edit entries on the go!

### Share with Others
1. Open database in Notion
2. Click "Share" (top right)
3. Invite people or create a link
4. Set permissions (view-only or edit)

---

## 🎨 Customization Ideas

### Add More Columns
- **Energy Level** (Select: Low, Medium, High)
- **Stress Level** (Number: 1-10)
- **Sleep Hours** (Number)
- **Exercise** (Checkbox)
- **Tags** (Multi-select: Work, Personal, Health)

### Create Views
- **Calendar View**: See entries by date
- **Gallery View**: Visual cards
- **This Week**: Filter to show only this week
- **By Mood**: Group entries by mood

### Add Formulas
- Days since last check-in
- Average mood this week
- Goal completion rate

---

## 📊 Summary

### Time Required
- **Total Setup Time**: ~15 minutes
- **Per Check-in**: Automatic (0 minutes)

### What You Get
- ✅ Automatic wellness journal in Notion
- ✅ Searchable and filterable entries
- ✅ Access from any device
- ✅ Beautiful visual interface
- ✅ Shareable with others
- ✅ Local backup in JSON

### Next Steps
1. ✅ Follow steps above to set up Notion
2. ✅ Add keys to .env file
3. ✅ Restart backend
4. ✅ Test with a check-in
5. ✅ Enjoy your wellness journey!

---

**Need Help?** Check the detailed guide in `NOTION_SETUP_GUIDE.md` 🌿✨
