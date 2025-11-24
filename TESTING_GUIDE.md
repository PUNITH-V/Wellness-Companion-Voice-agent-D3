# Testing Guide - Wellness Voice Companion

## Prerequisites
✅ All services running:
- LiveKit Server (port 7880)
- Backend Agent (Python)
- Frontend (port 3000)

✅ Configuration complete:
- Notion API token set
- Wellness database ID configured
- Todo database ID configured

## Test Scenarios

### 1. Wellness Check-in Test

**Steps:**
1. Open `http://localhost:3000`
2. Click "Connect" to start voice session
3. Say: "Hi, I want to do my daily check-in"
4. Agent will ask about your mood
5. Respond: "I'm feeling good, energetic"
6. Agent will ask about stress/feelings
7. Respond: "A bit stressed about work deadlines"
8. Agent will ask about goals
9. Respond: "I want to finish my report, exercise, and call my mom"
10. Agent provides advice and saves check-in

**Expected Results:**
- ✅ Data saved to `backend/wellness_log.json`
- ✅ New entry created in Notion Wellness Database
- ✅ Agent confirms save with mood and objectives

---

### 2. Create Todo Tasks Test

**Steps:**
1. In active session, say: "Add these to my todo list: finish report, buy groceries, exercise"
2. Wait for agent response

**Expected Results:**
- ✅ 3 tasks created in Notion Todo Database
- ✅ Agent confirms: "Created 3 task(s) in your Notion todo list: finish report, buy groceries, exercise"
- ✅ Tasks visible in Notion with "Not started" status

---

### 3. View Todo Tasks Test

**Steps:**
1. Say: "What tasks do I have?"
2. Wait for agent response

**Expected Results:**
- ✅ Agent lists all pending tasks
- ✅ Shows task names and status
- ✅ Maximum 10 tasks displayed

---

### 4. Complete Task Test

**Steps:**
1. Say: "I finished the report"
2. Wait for agent response

**Expected Results:**
- ✅ Task status changed to "Done" in Notion
- ✅ Agent confirms: "Great! I've marked 'finish report' as complete."
- ✅ Task no longer appears in pending tasks list

---

### 5. Update Task Test

**Steps:**
1. Say: "Change 'buy groceries' to 'buy groceries and cook dinner'"
2. Wait for agent response

**Expected Results:**
- ✅ Task name updated in Notion
- ✅ Agent confirms the update
- ✅ New name visible in Notion

**Alternative Test:**
1. Say: "Update the exercise task to 'In progress'"
2. Expected: Status changed to "In progress"

---

### 6. Delete Task Test

**Steps:**
1. Say: "Delete the groceries task"
2. Wait for agent response

**Expected Results:**
- ✅ Task archived in Notion
- ✅ Agent confirms: "I've deleted the task 'buy groceries and cook dinner' from your todo list."
- ✅ Task no longer visible in database

---

## Verification Checklist

### Backend Verification:
- [ ] Check `backend/wellness_log.json` for new entries
- [ ] Check backend logs for function calls
- [ ] Verify no errors in console

### Notion Verification:
- [ ] Open Notion Wellness Database
- [ ] Verify new check-in entry with Date, Mood, Objectives, Summary
- [ ] Open Notion Todo Database
- [ ] Verify tasks created, updated, completed, deleted

### Frontend Verification:
- [ ] Chat transcript shows conversation
- [ ] Agent responses are clear and natural
- [ ] No UI errors or glitches
- [ ] Breathing orb animates smoothly

---

## Troubleshooting

### Issue: "Todo list is not configured"
**Solution**: Check `.env` file has:
```
NOTION_API_TOKEN=your_token
NOTION_TODO_DB_ID=your_db_id
```

### Issue: "I couldn't find a task matching..."
**Solution**: 
- Task name might not match exactly
- Try using more specific keywords
- Check Notion database for exact task name

### Issue: Agent doesn't call functions
**Solution**:
- Restart backend agent
- Check backend logs for errors
- Verify LLM prompt includes todo list instructions

### Issue: Notion API errors
**Solution**:
- Verify Notion integration has access to databases
- Check database properties match expected schema
- Verify API token is valid

---

## Advanced Testing

### Stress Test:
1. Create 20 tasks at once
2. Complete multiple tasks in one sentence
3. Update and delete tasks rapidly

### Edge Cases:
1. Try to complete non-existent task
2. Try to delete already deleted task
3. Create task with special characters
4. Update task with empty name

### Integration Test:
1. Do full wellness check-in
2. Create tasks from objectives
3. View tasks
4. Complete some tasks
5. Update remaining tasks
6. Delete unnecessary tasks
7. Do another check-in next day

---

## Success Criteria

✅ All 6 function tools work correctly
✅ Data persists in both JSON and Notion
✅ Agent responds naturally to voice commands
✅ UI is responsive and visually appealing
✅ No errors in console or logs
✅ Notion databases update in real-time

---

## Status: Ready for Testing

All features implemented and backend restarted with latest code.
Frontend and LiveKit server already running.
Ready to test all functionality!
