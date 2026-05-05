from flask import Flask, render_template, request, jsonify
import re
import random

app = Flask(__name__)

# ── Sentiment Analysis (VADER-style simple implementation) ──────────────────
POSITIVE_WORDS = {
    "good", "great", "happy", "joy", "love", "wonderful", "excellent",
    "fantastic", "amazing", "glad", "thankful", "grateful", "hopeful",
    "better", "positive", "calm", "peaceful", "excited", "blessed", "awesome"
}
NEGATIVE_WORDS = {
    "sad", "bad", "terrible", "awful", "depressed", "anxious", "stress",
    "angry", "hate", "hopeless", "worthless", "lonely", "scared", "hurt",
    "pain", "cry", "useless", "failure", "disaster", "horrible", "miserable"
}

def analyze_sentiment(text):
    words = re.findall(r'\b\w+\b', text.lower())
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    if pos > neg:
        return {"label": "Positive", "icon": "😊", "color": "#4ade80"}
    elif neg > pos:
        return {"label": "Negative", "icon": "😔", "color": "#f87171"}
    else:
        return {"label": "Neutral",  "icon": "😐", "color": "#94a3b8"}

# ── Chatbot Pairs ───────────────────────────────────────────────────────────
pairs = [
    (r"(?i)hello|hi|hey", [
        "Hello! I'm here to listen and support you. How are you feeling today?",
        "Hi there. This is a safe space. What's on your mind?",
        "Hey! I'm glad you reached out. How can I support you today?"
    ]),
    (r"(?i).*(how are you|how do you feel).*", [
        "I'm here and ready to listen. More importantly, how are YOU feeling?",
        "I'm doing well, thank you! But let's focus on you — how are you doing?"
    ]),
    (r"(?i).*(sad|depressed|depression|unhappy|down|hopeless).*", [
        "I'm really sorry you're feeling this way. You're not alone, and your feelings are completely valid.",
        "It's okay to feel sad sometimes. Would you like to talk about what's been making you feel this way?",
        "Depression can feel overwhelming. Please remember that help is available, and you deserve support."
    ]),
    (r"(?i).*(anxious|anxiety|stressed|stress|nervous|worried|overwhelmed).*", [
        "Anxiety and stress can be really tough. Try taking slow, deep breaths — inhale for 4 counts, hold for 4, exhale for 4.",
        "It sounds like you're carrying a lot right now. What's been causing you the most stress lately?",
        "You're not alone in feeling overwhelmed. Breaking things into small steps can sometimes help. Would you like to talk through it?"
    ]),
    (r"(?i).*(lonely|alone|isolated|no one cares|no friends).*", [
        "Feeling lonely is painful. I want you to know that I'm here with you right now.",
        "You matter more than you know. Would you like to talk about what's been making you feel alone?",
        "Isolation can be really hard. Have you been able to connect with anyone lately, even briefly?"
    ]),
    (r"(?i).*(panic attack|panic|can't breathe|heart racing).*", [
        "If you're having a panic attack, try grounding yourself: name 5 things you can see, 4 you can touch, 3 you can hear.",
        "Panic attacks are frightening but they do pass. Focus on slow, controlled breathing — you are safe.",
        "Try to place your feet flat on the floor and take slow deep breaths. You're going to be okay."
    ]),
    (r"(?i).*(can't sleep|insomnia|sleep problem|not sleeping|sleepless).*", [
        "Sleep struggles can really affect your mood and energy. Are you finding it hard to fall asleep or stay asleep?",
        "Poor sleep and mental health are closely linked. Try a calming bedtime routine — no screens, soft lighting, and deep breathing.",
        "How long have you been having trouble sleeping? It might help to talk to a doctor if it's been a while."
    ]),
    (r"(?i).*(hate myself|worthless|useless|not good enough|failure|loser).*", [
        "I'm sorry you're speaking so harshly about yourself. You are not defined by your worst moments.",
        "Those thoughts are not the truth about you. Everyone struggles, and you deserve kindness — especially from yourself.",
        "You matter. Your feelings are valid, but please don't believe every negative thought you have about yourself."
    ]),
    (r"(?i).*(angry|anger|furious|frustrated|rage|mad).*", [
        "It sounds like you're really frustrated right now. That's completely valid. What's going on?",
        "Anger can be a signal that something important to you has been hurt or ignored. What triggered these feelings?",
        "When anger feels overwhelming, try stepping away briefly and taking a few deep breaths before reacting."
    ]),
    (r"(?i).*(grief|lost someone|death|died|mourning|miss them|bereavement).*", [
        "I'm so sorry for your loss. Grief is one of the hardest human experiences, and there's no right way to go through it.",
        "Losing someone you love is incredibly painful. Please be gentle with yourself during this time.",
        "It's okay to cry, to feel numb, or to feel anger — grief looks different for everyone. I'm here to listen."
    ]),
    (r"(?i).*(therapist|therapy|counselor|psychologist|psychiatrist|professional help).*", [
        "Seeking professional help is one of the bravest and most powerful things you can do for yourself.",
        "A therapist or counselor can provide personalized support. Would you like tips on how to find one?",
        "There's no shame in seeing a mental health professional. They are trained to help exactly with what you're going through."
    ]),
    (r"(?i).*(cope|coping|manage|feel better|tips|help me).*", [
        "Some helpful coping strategies include journaling, exercise, talking to someone you trust, and mindfulness.",
        "Deep breathing, grounding exercises, and regular self-care can make a big difference over time.",
        "Would you like to try a simple breathing exercise together? It can help calm your mind quickly."
    ]),
    (r"(?i).*(suicidal|suicide|kill myself|end my life|don't want to live|want to die).*", [
        "I hear you, and I'm very concerned about your safety. Please reach out to a crisis helpline immediately — you don't have to face this alone. Pakistan: 0311-7786264 | International: befrienders.org",
        "Your life has value. Please contact a crisis line right away. You deserve support and care.",
        "I'm so glad you're talking about this. Please tell someone you trust or call a helpline right now."
    ]),
    (r"(?i).*(breathing exercise|breath|breathe|calm down|relax).*", [
        "Let's try box breathing: Inhale for 4 counts... Hold for 4... Exhale for 4... Hold for 4. Repeat 3 times.",
        "Close your eyes if you can. Breathe in deeply through your nose, hold, and slowly exhale through your mouth.",
        "Focus only on your breath. In through the nose... out through the mouth. You're doing great."
    ]),
    (r"(?i).*(motivation|motivated|give up|can't do this|too hard|no point).*", [
        "Even on the hardest days, taking one small step forward counts. You don't have to do everything at once.",
        "It's okay to feel like giving up sometimes — but please don't. You've gotten through hard days before.",
        "Progress isn't always visible. Rest if you need to, but don't quit. You're stronger than you think."
    ]),
    (r"(?i).*(happy|grateful|better|good|great|thankful|hopeful).*", [
        "That's wonderful to hear! Hold onto that feeling. What's been making you feel this way?",
        "It's great that you're feeling positive! Nurturing gratitude daily can really support mental wellbeing.",
        "I'm so glad to hear that! Keep doing whatever is helping you feel this way."
    ]),
    (r"(?i)bye|goodbye|take care|see you", [
        "Take care of yourself. Remember, it's okay to ask for help anytime.",
        "Goodbye! I'm always here if you need to talk. Be kind to yourself.",
        "See you! Remember — small steps, self-compassion, and reaching out all make a difference."
    ]),
]

def get_response(user_input):
    for pattern, responses in pairs:
        if re.search(pattern, user_input):
            return random.choice(responses)
    return "I'm here to listen. Could you tell me more about how you're feeling?"

# ── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"response": "Please type something."})
    response = get_response(user_msg)
    return jsonify({"response": response})

@app.route("/sentiment", methods=["POST"])
def sentiment():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided."})
    result = analyze_sentiment(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
