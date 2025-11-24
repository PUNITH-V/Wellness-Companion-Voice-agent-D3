# 📓 Notion Integration Setup Guide

## Overview
Your wellness companion will automatically save each check-in to a Notion database, creating a beautiful wellness journal you can access anytime.

---

## 🔧 Setup Steps

### Step 1: Create a Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Fill in the details:
   - **Name**: "Wellness Companion" (or any name you like)
   - **Associated workspace**: Select your workspace
   - **Type**: Internal integration
4. Click **"Submit"**
5. **Copy the "Internal Integration Token"** - you'll need this!

### Step 2: Create a Wellness Database in Notion

1. Open Notion and create a new page
2. Name it **"Daily Wellness Journal"** (or your preferred name)
3. Add a **Database** (Table view)
4. Create these properties/columns:
   - **Date** (Date type) - When the check-in happened
   - **Mood** (Text type) - User's mood and energy level
   - **Objectives** (Text type) - Goals for the day
   - **Summary** (Text type) - Brief summary of the conversation

### Step 3: Share Database with Integration

1. Open your "Daily Wellness Journal" database
2. Click the **"..."** menu (top right)
3. Scroll down and click **"Add connections"**
4. Select your **"Wellness Companion"** integration
5. Click **"Confirm"**

### Step 4: Get Database ID

1. Open your database in Notion
2. Look at the URL in your browser:
   ```
   https://www.notion.so/workspace/DATABASE_ID?v=...
   ```
3. Copy the **DATABASE_ID** part (32 characters, mix of letters and numbers)
   - Example: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### Step 5: Add Keys to .env File

Open `backend/.env` and add your keys:

```env
NOTION_API_TOKEN=secret_your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

---

## ✅ Testing

1. Restart your backend agent:
   ```bash
   cd backend
   uv run python src/agent.py dev
   ```

2. Have a conversation with your wellness companion

3. After the check-in, go to your Notion database

4. You should see a new entry with:
   - Today's date
   - Your mood
   - Your objectives
   - Summary of the conversation

---

## 📊 What Gets Saved

Each check-in creates a new row in your Notion database:

| Date | Mood | Objectives | Summary |
|------|------|------------|---------|
| 2025-11-24 | Feeling energized and optimistic | Complete project, Take a walk, Meditate | User is in good spirits and ready to tackle the day |

---

## 🎨 Customization Ideas

### Add More Properties
You can add additional columns to track:
- **Energy Level** (Select: Low, Medium, High)
- **Stress Level** (Number: 1-10)
- **Sleep Quality** (Select: Poor, Fair, Good, Excellent)
- **Tags** (Multi-select: Work, Personal, Health, etc.)

### Create Views
- **Calendar View**: See check-ins by date
- **Gallery View**: Visual cards for each entry
- **Timeline View**: Track your wellness journey over time

### Add Filters
- Show only entries from this week
- Filter by mood keywords
- Group by energy level

---

## 🔒 Privacy & Security

- **Your data stays in your Notion workspace**
- **Integration token is private** - never share it
- **Local backup** - Data is also saved to `wellness_log.json`
- **You control access** - Revoke integration anytime in Notion settings

---

## 🐛 Troubleshooting

### "Failed to save to Notion"
- Check that your `NOTION_API_TOKEN` is correct
- Verify the `NOTION_DATABASE_ID` is correct
- Make sure you shared the database with your integration

### "Notion API error: 401"
- Your integration token is invalid or expired
- Create a new integration and update the token

### "Notion API error: 404"
- Database ID is incorrect
- Database was deleted or moved
- Integration doesn't have access to the database

### Check Logs
Look at the backend terminal for detailed error messages:
```
ERROR agent Error saving to Notion: ...
```

---

## 📱 Access Your Wellness Journal

### On Desktop
- Open Notion app or web
- Navigate to your "Daily Wellness Journal"

### On Mobile
- Open Notion mobile app
- Find your wellness database
- View and edit entries on the go

### Share with Others
- Share the database with your therapist, coach, or accountability partner
- Set appropriate permissions (view-only or edit)

---

## 🎯 Benefits

### Track Patterns
- See mood trends over time
- Identify what affects your energy
- Notice recurring themes in objectives

### Accountability
- Visual record of your goals
- Easy to review what you accomplished
- Celebrate your progress

### Insights
- Export data for analysis
- Create charts and graphs
- Share insights with healthcare providers

---

## 🚀 Advanced: Using Notion MCP Server (Optional)

If you want even more Notion integration (like querying past entries during conversations), you can set up the Notion MCP server.

### MCP Config
Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/mcp-server-notion"],
      "env": {
        "NOTION_API_KEY": "your_integration_token_here"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

This allows the agent to:
- Query past check-ins
- Search for specific entries
- Update existing entries
- Create more complex database structures

---

**Result**: A beautiful, searchable wellness journal in Notion that grows with each check-in! 🌿✨
