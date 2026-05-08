from flask import Flask, render_template_string
import random
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fun Facts Galaxy</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            color: white;
        }

        .container {
            width: 100%;
            max-width: 900px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 35px;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }

        h1 {
            text-align: center;
            margin-bottom: 25px;
            font-size: 3rem;
            color: #00ffd5;
        }

        .fact-box {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 35px;
            text-align: center;
            margin-bottom: 25px;
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: 0.3s;
        }

        .fact-box:hover {
            transform: scale(1.02);
        }

        .emoji {
            font-size: 70px;
            margin-bottom: 15px;
        }

        .fact-text {
            font-size: 1.4rem;
            line-height: 1.8;
            margin-bottom: 15px;
        }

        .category {
            display: inline-block;
            background: #00ffd5;
            color: black;
            padding: 10px 25px;
            border-radius: 50px;
            font-weight: bold;
        }

        .buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        button {
            padding: 16px;
            border: none;
            border-radius: 15px;
            font-size: 1rem;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
            background: #00ffd5;
            color: black;
        }

        button:hover {
            transform: translateY(-5px);
            background: white;
        }

        .counter {
            margin-top: 25px;
            text-align: center;
            font-size: 1.1rem;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #ccc;
            font-size: 0.9rem;
        }

        .time {
            margin-top: 10px;
            color: #00ffd5;
        }
    </style>
</head>
<body>

<div class="container">

    <h1>🌌 Fun Facts Galaxy</h1>

    <div class="fact-box" id="factBox">
        <div class="emoji" id="emoji">🤖</div>
        <div class="fact-text" id="factText">
            Click any category button to discover an amazing fact.
        </div>
        <div class="category" id="category">Random Fact</div>
    </div>

    <div class="buttons">
        <button onclick="showFact('technology')">💻 Technology</button>
        <button onclick="showFact('animals')">🐼 Animals</button>
        <button onclick="showFact('space')">🚀 Space</button>
        <button onclick="showFact('science')">🧪 Science</button>
        <button onclick="showFact('history')">📜 History</button>
        <button onclick="showFact('food')">🍔 Food</button>
        <button onclick="showFact('random')">🎲 Random</button>
    </div>

    <div class="counter">
        Facts Viewed: <span id="count">0</span>
        <div class="time" id="time"></div>
    </div>

    <div class="footer">
        Made with Flask + JavaScript 🚀
    </div>

</div>

<script>

    let count = 0;

    const facts = {
        technology: [
            "The first computer mouse was made of wood.",
            "More than 90% of the world's currency exists only digitally.",
            "The first website is still online today.",
            "Over 5 billion people use the internet."
        ],

        animals: [
            "Dolphins can recognize themselves in mirrors.",
            "Koalas sleep up to 22 hours a day.",
            "Octopuses have three hearts.",
            "A group of pandas is called an embarrassment."
        ],

        space: [
            "One million Earths can fit inside the Sun.",
            "Neutron stars are incredibly dense.",
            "Space has no sound because there is no air.",
            "Mars sunsets appear blue."
        ],

        science: [
            "Water can boil and freeze at the same time.",
            "Lightning is hotter than the Sun’s surface.",
            "Your body contains around 37 trillion cells.",
            "Bananas are naturally radioactive."
        ],

        history: [
            "The shortest war lasted only 38 minutes.",
            "Ancient Romans used urine as mouthwash.",
            "The pyramids were once covered in shiny limestone.",
            "Napoleon was once attacked by rabbits."
        ],

        food: [
            "Honey never spoils.",
            "Potatoes were the first vegetable grown in space.",
            "Dark chocolate contains antioxidants.",
            "Apples float because they are 25% air."
        ],

        random: [
            "Sharks existed before trees.",
            "Wombat poop is cube-shaped.",
            "A day on Venus is longer than its year.",
            "Some turtles can breathe through their butts."
        ]
    };

    const emojis = {
        technology: '💻',
        animals: '🐼',
        space: '🚀',
        science: '🧪',
        history: '📜',
        food: '🍔',
        random: '🎲'
    };

    function showFact(category) {

        const categoryFacts = facts[category];

        const randomFact = categoryFacts[Math.floor(Math.random() * categoryFacts.length)];

        document.getElementById('factText').innerText = randomFact;

        document.getElementById('emoji').innerText = emojis[category];

        document.getElementById('category').innerText = category.toUpperCase() + ' FACT';

        count++;

        document.getElementById('count').innerText = count;

        const now = new Date();

        document.getElementById('time').innerText =
            'Last Updated: ' + now.toLocaleTimeString();
    }

    window.onload = function() {
        showFact('random');
    }

</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    print('=' * 50)
    print('🌌 FUN FACTS GALAXY STARTED')
    print('=' * 50)
    print('Open Browser: http://127.0.0.1:5000')
    print('=' * 50)

    app.run(debug=True)
