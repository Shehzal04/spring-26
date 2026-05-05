# MindEase – Mental Health Support Chatbot (Flask)

## Project Structure
```
mental_health_bot/
├── app.py               # Flask backend with chatbot + sentiment logic
├── requirements.txt
└── templates/
    └── index.html       # Full frontend UI
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
http://127.0.0.1:5000
```

## Features
- 💬 Rule-based Mental Health Chatbot (17 topic pairs)
- 😊 Sentiment Analysis (Positive / Negative / Neutral)
- 🌿 Quick Topic buttons (Anxiety, Depression, Loneliness, etc.)
- 🆘 Crisis helpline info always visible
- ⌨️  Typing indicator with realistic delay
- 🎨 Dark, calming UI with smooth animations
