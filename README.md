# 🌟 AI Wellness Voice Companion

> A voice-powered wellness companion that conducts daily check-ins, tracks your mood and goals, and manages your tasks through natural conversation—all integrated with Notion for seamless journaling and productivity.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-15-black.svg)

## ✨ Features

### 🎤 Voice-First Interaction
- Natural voice conversations powered by Google Gemini 2.5 Flash
- Real-time speech-to-text with Deepgram Nova-3
- Human-like voice responses using Murf TTS
- LiveKit-powered low-latency audio streaming

### 💚 Wellness Check-ins
- Daily mood and energy level tracking
- Stress and emotion assessment
- Goal setting (1-3 daily objectives)
- Personalized, grounded wellness advice
- Context-aware conversations using check-in history

### 📝 Smart Todo List Management
Complete CRUD operations through voice commands:
- **Create**: "Add 'finish report' to my todo list"
- **Read**: "What tasks do I have?"
- **Update**: "Change 'call mom' to 'call parents'"
- **Complete**: "I finished the report"
- **Delete**: "Remove the groceries task"

### 🔗 Notion Integration
- Dual database setup (Wellness Journal + Todo List)
- Automatic sync of check-ins and tasks
- Real-time updates to your Notion workspace
- Local JSON backup for offline access

### 🎨 Beautiful UI/UX
- Minimalistic glassmorphism design
- Animated breathing orb with pulsing effects
- Floating animations and smooth transitions
- Gradient backgrounds with blur effects
- Fully responsive layout

## 🛠️ Tech Stack

**Backend:**
- Python 3.13
- LiveKit Agents SDK
- Google Gemini 2.5 Flash (LLM)
- Murf TTS (Text-to-Speech)
- Deepgram STT (Speech-to-Text)
- Notion API
- aiohttp for async requests

**Frontend:**
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- LiveKit Client SDK
- Custom CSS animations

**Infrastructure:**
- LiveKit Server (local/cloud)
- Notion databases (cloud)
- JSON file storage (local backup)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- pnpm
- Notion account with API access

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/wellness-voice-companion.git
cd wellness-voice-companion
```

2. **Set up Backend**
```bash
cd backend
# Install UV package manager
pip install uv
# Install dependencies
uv sync
# Configure environment variables
cp .env.example .env
# Add your API keys to .env
```

3. **Set up Frontend**
```bash
cd frontend
pnpm install
# Configure environment variables
cp .env.example .env.local
```

4. **Configure Notion**
- Create two Notion databases (Wellness Journal + Todo List)
- Get your Notion API token from https://www.notion.so/my-integrations
- Add database IDs to `backend/.env`

See [NOTION_SETUP_GUIDE.md](NOTION_SETUP_GUIDE.md) for detailed instructions.

5. **Start Services**
```bash
# Terminal 1: Start LiveKit Server
cd livekit-server
./livekit-server --dev --config ../livekit.yaml

# Terminal 2: Start Backend Agent
cd backend
uv run python src/agent.py dev

# Terminal 3: Start Frontend
cd frontend
pnpm dev
```

6. **Open the App**
Navigate to `http://localhost:3000` and click "Connect"

## 📖 Usage Examples

### Daily Wellness Check-in
```
You: "Hi, I want to do my check-in"
Agent: "How are you feeling today?"
You: "I'm feeling good, a bit stressed about work"
Agent: "What would you like to accomplish today?"
You: "Finish my report, exercise, and call my mom"
Agent: [Provides supportive advice and saves to Notion]
```

### Managing Tasks
```
You: "What tasks do I have?"
Agent: "Here are your tasks: Finish report (In progress), Buy groceries (Not started)..."

You: "I finished the report"
Agent: "Great! I've marked 'Finish report' as complete."

You: "Add 'prepare presentation' to my list"
Agent: "Created 1 task in your Notion todo list: prepare presentation"
```

## 🔐 Environment Variables

**Backend (.env):**
```env
GOOGLE_API_KEY=your_gemini_api_key
MURF_API_KEY=your_murf_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
NOTION_API_TOKEN=your_notion_token
NOTION_WELLNESS_DB_ID=your_wellness_db_id
NOTION_TODO_DB_ID=your_todo_db_id
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

## 📁 Project Structure

```
wellness-voice-companion/
├── backend/
│   ├── src/
│   │   └── agent.py          # Main agent logic with all functions
│   ├── .env                   # Backend configuration
│   └── wellness_log.json      # Local check-in storage
├── frontend/
│   ├── components/
│   │   └── app/
│   │       ├── session-view.tsx    # Main UI
│   │       ├── breathing-orb.tsx   # Animated orb
│   │       └── welcome-view.tsx    # Landing page
│   ├── styles/
│   │   └── globals.css        # Custom animations
│   └── .env.local             # Frontend configuration
├── livekit-server/            # LiveKit server files
└── docs/                      # Documentation
```

## 🎯 Key Functions

The agent includes 6 main function tools:

- `save_checkin()` - Save wellness data to JSON + Notion
- `create_todo_tasks()` - Create new tasks
- `get_todo_tasks()` - Fetch pending tasks
- `complete_todo_task()` - Mark tasks as done
- `update_todo_task()` - Modify task details
- `delete_todo_task()` - Remove tasks

## 📚 Documentation

- [Setup Requirements](SETUP_REQUIREMENTS.md) - Detailed setup instructions
- [Notion Setup Guide](NOTION_SETUP_GUIDE.md) - Configure Notion integration
- [Todo List Usage](HOW_TO_USE_TODO.md) - How to use todo list features
- [Testing Guide](TESTING_GUIDE.md) - Test all features

## 🧪 Testing

Run the test suite to verify everything is working:

```bash
# Test backend
cd backend
uv run python -m pytest

# Test frontend
cd frontend
pnpm test
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LiveKit](https://livekit.io/) for real-time communication infrastructure
- [Google Gemini](https://deepmind.google/technologies/gemini/) for LLM capabilities
- [Murf AI](https://murf.ai/) for natural voice synthesis
- [Deepgram](https://deepgram.com/) for speech recognition
- [Notion](https://www.notion.so/) for database and journaling

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure all API keys are set in `.env`
- Check Python version is 3.13+
- Run `uv sync` to install dependencies

**Frontend connection issues:**
- Verify LiveKit server is running
- Check `NEXT_PUBLIC_LIVEKIT_URL` in `.env.local`
- Ensure backend agent is running

**Notion integration not working:**
- Verify Notion API token is valid
- Check database IDs are correct
- Ensure Notion integration has access to databases

## 📧 Support

For questions or issues, please:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

**Built with ❤️ for mental wellness and productivity**
