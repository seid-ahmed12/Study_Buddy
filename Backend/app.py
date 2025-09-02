from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from config import DB_CONFIG
import spacy
import random

app = Flask(__name__)
CORS(app)

# DB connection
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor(dictionary=True)

# Load small English model
nlp = spacy.load("en_core_web_sm")

# Home route
@app.route('/')
def home():
    return "Flask is working!"

# /generate route: creates interactive multiple-choice flashcards
@app.route("/generate", methods=["POST"])
def generate_flashcards():
    data = request.json
    notes = data.get("notes")

    if not notes:
        return jsonify({"error": "No notes provided"}), 400

    doc = nlp(notes)
    sentences = list(doc.sents)
    flashcards = []

    dummy_choices = ["Python", "Flask", "AI", "JSON", "MySQL", "Database", "Programming", "Framework"]

    for sentence in sentences[:10]:  # take up to 10 sentences
        keywords = [token.text for token in sentence if token.pos_ in ["NOUN", "PROPN", "VERB"]]
        if not keywords:
            continue

        key_term = random.choice(keywords)
        question = f"What is the meaning or role of '{key_term}' in this context?"

        # Generate multiple-choice options
        choices = random.sample(dummy_choices, 3)
        if key_term not in choices:
            choices[random.randint(0, 2)] = key_term
        random.shuffle(choices)

        flashcards.append({
            "question": question,
            "answer": key_term,
            "options": choices
        })

        # Save to DB
        cursor.execute(
            "INSERT INTO flashcards (question, answer) VALUES (%s, %s)",
            (question, key_term)
        )
        db.commit()

    return jsonify(flashcards)

# /flashcards route: fetch all saved flashcards
@app.route("/flashcards", methods=["GET"])
def get_flashcards():
    cursor.execute("SELECT * FROM flashcards ORDER BY created_at DESC")
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
