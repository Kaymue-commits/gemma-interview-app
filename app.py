"""
Gemma Interview Coach - AI-powered technical interview practice
Uses Groq API with Gemma 4 for real-time interview simulation and feedback.
"""

import os
import json
import time
import uuid
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", str(uuid.uuid4()))

# Groq API configuration - free tier available at console.groq.com
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "gemma2-9b-it"  # Free Gemma 4 model on Groq

# Interview configuration
INTERVIEW_ROLES = {
    "python": {
        "name": "Python Backend Engineer",
        "topics": ["Python", "Django/Flask", "REST APIs", "Databases", "Testing"],
        "questions": [
            "Explain the difference between a list and a tuple in Python.",
            "What is the Global Interpreter Lock (GIL)?",
            "How does Python's garbage collection work?",
            "Explain decorators and their use cases.",
            "What are context managers and why are they useful?",
        ]
    },
    "frontend": {
        "name": "Frontend Engineer",
        "topics": ["JavaScript", "React", "CSS", "Web APIs", "Performance"],
        "questions": [
            "Explain closures in JavaScript.",
            "What is the event loop in JavaScript?",
            "How does React's useEffect work?",
            "Explain the difference between let, const, and var.",
            "What are Web Components?",
        ]
    },
    "ml": {
        "name": "ML Engineer",
        "topics": ["Machine Learning", "Deep Learning", "PyTorch", "NLP", "MLOps"],
        "questions": [
            "Explain the difference between supervised and unsupervised learning.",
            "What is gradient descent and how does it work?",
            "Explain overfitting and how to prevent it.",
            "What are transformers and why are they important?",
            "How do you handle imbalanced datasets?",
        ]
    },
    "general": {
        "name": "Software Engineer (General)",
        "topics": ["Data Structures", "Algorithms", "System Design", "OOD", "Databases"],
        "questions": [
            "Explain Big O notation and why it matters.",
            "What is the difference between SQL and NoSQL databases?",
            "How would you design a URL shortening service?",
            "Explain the SOLID principles.",
            "What is caching and when would you use it?",
        ]
    }
}

SYSTEM_PROMPT = """You are an expert technical interview coach. Your role:
1. Conduct realistic technical interviews
2. Ask ONE focused question at a time
3. After the candidate answers, provide brief, constructive feedback
4. Ask follow-up questions to deepen understanding
5. Rate the answer on: Accuracy, Depth, Clarity (1-5 each)
6. At the end, provide a summary with areas to improve

Start by asking the candidate which role they want to practice for, or pick up where they left off.
Be professional but friendly. Keep questions concise.
After feedback, always ask the next interview question.
When all questions are done, say "INTERVIEW_COMPLETE" and give a final summary."""


def chat_gemma(messages, temperature=0.7):
    """Call Groq API with Gemma model."""
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY not set. Get one free at console.groq.com"}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 1024
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {"reply": data["choices"][0]["message"]["content"]}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {"error": "Invalid API key. Check your GROQ_API_KEY."}
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def index():
    """Serve the main app page."""
    return render_template("index.html")


@app.route("/api/roles", methods=["GET"])
def get_roles():
    """Return available interview roles."""
    roles = {}
    for key, val in INTERVIEW_ROLES.items():
        roles[key] = {"name": val["name"], "topics": val["topics"]}
    return jsonify(roles)


@app.route("/api/start", methods=["POST"])
def start_interview():
    """Start a new interview session."""
    role = request.json.get("role", "general")
    if role not in INTERVIEW_ROLES:
        role = "general"

    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    session["role"] = role
    session["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": f"Welcome to the {INTERVIEW_ROLES[role]['name']} interview! I'll be your interviewer today.\n\nWe have {len(INTERVIEW_ROLES[role]['questions'])} questions covering: {', '.join(INTERVIEW_ROLES[role]['topics'])}.\n\nLet's begin. Tell me about yourself and which area you'd like to focus on first."}
    ]

    return jsonify({
        "session_id": session_id,
        "role": role,
        "role_name": INTERVIEW_ROLES[role]["name"],
        "welcome": session["messages"][1]["content"]
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    """Send a message and get AI response."""
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if "messages" not in session:
        return jsonify({"error": "No active session. Start a new interview."}), 400

    messages = session["messages"]
    messages.append({"role": "user", "content": user_message})

    result = chat_gemma(messages)

    if "error" in result:
        messages.pop()  # remove user message on error
        return jsonify(result), 500

    reply = result["reply"]
    messages.append({"role": "assistant", "content": reply})

    is_complete = "INTERVIEW_COMPLETE" in reply

    return jsonify({
        "reply": reply,
        "is_complete": is_complete,
        "turns": len(messages) // 2
    })


@app.route("/api/history", methods=["GET"])
def history():
    """Get current session history."""
    if "messages" not in session:
        return jsonify({"messages": []})
    # Return only conversation (skip system prompt)
    return jsonify({"messages": session["messages"][1:]})


@app.route("/api/reset", methods=["POST"])
def reset():
    """Reset the interview session."""
    session.clear()
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
