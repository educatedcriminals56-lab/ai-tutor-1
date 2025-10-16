from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

sessions = {}

DEFAULT_PROMPT = "Welcome to our dialogue on justice. To begin, could you share your initial thoughts on what justice means to you?"

TOPIC_RESPONSES = {
    "justice": [
        "That's an interesting perspective. Can you explain why you believe justice should be defined that way?",
        "I see. But consider this: if justice is about giving people what they deserve, how do we determine what someone deserves?",
        "That definition seems to rely on certain assumptions about fairness. What if those assumptions were challenged?",
        "You've mentioned fairness. But is fairness always just? Consider situations where treating everyone equally leads to unjust outcomes.",
        "Interesting. Now, let me ask: if justice is about following rules, what makes a rule just in the first place?",
        "You seem to be equating justice with legality. But can laws themselves be unjust? Think about historical examples."
    ]
}

FALLACIES = [
    "Unstated assumption: Equating justice with legality",
    "Potential circular reasoning: Using justice to define fairness and fairness to define justice",
    "Overgeneralization: Applying a specific case to all situations",
    "False dichotomy: Presenting only two options when more exist",
    "Appeal to emotion: Relying on emotional response rather than logical reasoning"
]

def create_session(sess_id):
    sessions[sess_id] = {
        "topic": "justice",
        "history": [{"sender": "ai", "content": DEFAULT_PROMPT, "ts": datetime.utcnow().isoformat()}],
        "progress": {"identifying_assumptions": 30, "recognizing_fallacies": 20, "constructing_arguments": 40},
        "fallacies": []
    }
    return sessions[sess_id]

def get_session(sess_id):
    if sess_id not in sessions:
        return create_session(sess_id)
    return sessions[sess_id]

def synthesize_ai_response(topic, user_message):
    return random.choice(TOPIC_RESPONSES.get(topic, TOPIC_RESPONSES["justice"]))

def analyze_reasoning(user_message):
    identified = random.choice(FALLACIES)
    return {
        "user_statement": user_message,
        "identified_pattern": identified,
        "socratic_strategy": "Challenging underlying assumptions to expose contradictions in reasoning."
    }

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.json or {}
    sess_id = data.get('session_id', 'default')
    user_message = data.get('message', '').strip()
    topic = data.get('topic', 'justice')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    session = get_session(sess_id)
    session['topic'] = topic

    session['history'].append({"sender": "user", "content": user_message, "ts": datetime.utcnow().isoformat()})
    ai_response = synthesize_ai_response(topic, user_message)
    session['history'].append({"sender": "ai", "content": ai_response, "ts": datetime.utcnow().isoformat()})

    reasoning = analyze_reasoning(user_message)

    for k in session['progress']:
        session['progress'][k] = min(session['progress'][k] + random.randint(3, 6), 100)

    new_fallacy = reasoning['identified_pattern']
    if new_fallacy not in session['fallacies']:
        session['fallacies'].insert(0, new_fallacy)
    session['fallacies'] = session['fallacies'][:4]

    return jsonify({
        "ai_response": ai_response,
        "reasoning_trace": reasoning,
        "progress": session['progress'],
        "fallacies": session['fallacies'],
        "history": session['history'][-20:]
    })

@app.route('/api/restart', methods=['POST'])
def restart():
    data = request.json or {}
    sess_id = data.get('session_id', 'default')
    topic = data.get('topic', 'justice')
    sessions[sess_id] = create_session(sess_id)
    return jsonify({"status": "ok", "session": sessions[sess_id]})

@app.route('/api/summary', methods=['POST'])
def summary():
    sess_id = (request.json or {}).get('session_id', 'default')
    session = get_session(sess_id)
    return jsonify({
        "summary_text": "Learning summary generated.",
        "last_messages": session['history'][-10:],
        "progress": session['progress'],
        "identified_fallacies": session['fallacies']
    })

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
