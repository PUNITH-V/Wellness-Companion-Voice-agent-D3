# 📝 How to Use the Todo List Feature

## ✅ Backend is Now Restarted with Notion Integration!

Your wellness companion can now interact with your Notion todo list.

---

## 🎯 How to Create Tasks

During your wellness check-in, when the agent asks about your goals, you can say:

### Option 1: Explicit Request
After mentioning your goals, say:
- **"Add these to my todo list"**
- **"Create tasks for these goals"**
- **"Turn these into tasks"**
- **"Save these as tasks in Notion"**

### Option 2: During Conversation
When the agent asks "What would you like to accomplish today?", respond with:
- "I want to finish the project report, go for a walk, and call my mom. Please add these to my todo list."

---

## 📋 How to View Tasks

At any time during the conversation, you can say:
- **"Show me my tasks"**
- **"What's on my todo list?"**
- **"What do I need to do today?"**

The agent will read out your pending tasks from Notion.

---

## ✅ How to Complete Tasks

When you've finished a task, say:
- **"Mark [task name] as done"**
- **"I completed [task name]"**
- **"Check off [task name]"**

Example:
- "Mark finish project report as done"
- "I completed the walk"

---

## 🧪 Test It Now!

1. **Refresh your browser** at http://localhost:3000
2. **Start a new check-in**
3. **When asked about goals**, say something like:
   ```
   "I want to complete my project documentation, 
   take a 30-minute walk, and practice meditation. 
   Please add these to my todo list."
   ```
4. **The agent should respond**: "Created 3 tasks in your Notion todo list..."
5. **Check your Notion** - You should see 3 new tasks!

---

## 🔍 Troubleshooting

### Tasks Not Being Created?

**Check 1: Did you explicitly ask?**
- The agent won't automatically create tasks
- You must say "add to todo list" or similar

**Check 2: Is Notion configured?**
- Check `backend/.env` has both database IDs
- Verify your integration token is correct

**Check 3: Database shared?**
- Make sure you shared the todo database with your integration
- Go to Notion → Click "..." → Add connections

**Check 4: Column names correct?**
Your todo database must have:
- **Task** (Title/Name column)
- **Status** (Status type with options: "Not started", "In progress", "Done")
- **Created** (Date type)

### Check Backend Logs
Look at the backend terminal for errors:
```bash
ERROR agent Error creating task: ...
```

---

## 📊 What Gets Saved

### Wellness Database
Every check-in automatically saves:
- Date & time
- Mood
- Objectives
- Summary

### Todo Database
Only when you explicitly ask:
- Task name
- Status: "Not started"
- Created date

---

## 💡 Pro Tips

### Combine Features
1. Have your wellness check-in
2. Mention your goals
3. Ask to add them to todo list
4. Later, ask "show me my tasks"
5. As you complete them, mark them done

### Natural Language
The agent understands natural requests:
- "Put these on my list"
- "I need to remember to do these"
- "Make tasks for my goals"

### Task Management
- View tasks anytime: "What's on my list?"
- Complete tasks: "I finished [task]"
- The agent will confirm each action

---

**Ready to try?** Start a new conversation and explicitly ask the agent to add your goals to the todo list! 🎯✨
