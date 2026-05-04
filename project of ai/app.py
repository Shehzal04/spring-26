from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    user_input = request.json.get('message', '').strip()

    if not user_input:
        return jsonify({'response': 'Please type something!'})

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SmartBot, an intelligent and friendly AI assistant. "
                        "You are helpful, concise, and conversational. "
                        "You were created as a 4th semester AI project using Flask and Groq API. "
                        "If asked your name, say SmartBot. "
                        "Keep responses clear and to the point."
                    )
                }
            ] + conversation_history,
            max_tokens=1024,
            temperature=0.7,
        )

        response = completion.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": response
        })

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        return jsonify({'response': response, 'status': 'success'})

    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}', 'status': 'error'})


@app.route('/clear', methods=['POST'])
def clear():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    app.run(debug=True)