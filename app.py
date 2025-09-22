from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret"
app.permanent_session_lifetime = timedelta(days=7)

# --------------------------- Quiz Questions -----------------------------
QUESTIONS = {
    "Easy": [
        {"question": "What is the output of print(2 + 3)?", "options": ["23", "5", "2+3", "None"], "answer": "5"},
        {"question": "What symbol is used to comment a line in Python?", "options": ["#", "//", "--", "/*"], "answer": "#"},
        {"question": "Which function is used to get input from the user?", "options": ["get()", "input()", "read()", "scan()"], "answer": "input()"},
        {"question": "Which data type is used for True or False?", "options": ["int", "str", "bool", "float"], "answer": "bool"},
        {"question": "What is the correct file extension for Python files?", "options": [".pyth", ".pt", ".py", ".p"], "answer": ".py"},
    ],
    "Medium": [
        {"question": "What does len('Python') return?", "options": ["5", "6", "7", "Error"], "answer": "6"},
        {"question": "What is a correct way to define a function?", "options": ["def myFunc():", "function myFunc()", "func myFunc()", "define myFunc()"], "answer": "def myFunc():"},
        {"question": "Which of these is a tuple?", "options": ["[1,2,3]", "{1,2,3}", "(1,2,3)", "<1,2,3>"], "answer": "(1,2,3)"},
        {"question": "What is the output of 3 * 'Hi '?", "options": ["Hi Hi Hi ", "HiHiHi", "Error", "3Hi"], "answer": "Hi Hi Hi "},
        {"question": "Which keyword is used for loops in Python?", "options": ["loop", "iterate", "for", "repeat"], "answer": "for"},
    ],
    "Hard": [
        {"question": "What does the 'map' function do?", "options": ["Maps values to keys", "Transforms items in an iterable", "Creates a graph", "None"], "answer": "Transforms items in an iterable"},
        {"question": "Which module is used for regular expressions?", "options": ["re", "regex", "expression", "match"], "answer": "re"},
        {"question": "What is a lambda function?", "options": ["Anonymous function", "Loop function", "Named function", "Error"], "answer": "Anonymous function"},
        {"question": "How do you handle exceptions in Python?", "options": ["try/except", "catch/throw", "handle/catch", "error/try"], "answer": "try/except"},
        {"question": "What is the result of bool([])?", "options": ["True", "False", "None", "Error"], "answer": "False"},
    ]
}

# Simple in-memory leaderboard (persists only while server runs)
leaderboard = []

# --------------------------- Routes ------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('login.html', error='Please enter a username')
        session.permanent = True
        session['username'] = username
        return redirect(url_for('level'))
    return render_template('login.html')

@app.route('/level')
def level():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('level.html', username=session['username'])

@app.route('/start/<level>')
def start(level):
    level = level.capitalize()
    if level not in QUESTIONS:
        return redirect(url_for('level'))

    # Prepare quiz state
    qlist = QUESTIONS[level].copy()
    random.shuffle(qlist)
    session['questions'] = qlist
    session['q_index'] = 0
    session['score'] = 0
    session['selected'] = []
    session['level'] = level
    return redirect(url_for('question'))

@app.route('/question', methods=['GET'])
def question():
    if 'questions' not in session:
        return redirect(url_for('login'))
    q_index = session.get('q_index', 0)
    questions = session['questions']
    if q_index >= len(questions):
        return redirect(url_for('result'))
    q = questions[q_index]
    # send remaining time default 20 seconds (handled client-side)
    return render_template('question.html', q=q, qnum=q_index+1, total=len(questions))

@app.route('/answer', methods=['POST'])
def answer():
    if 'questions' not in session:
        return redirect(url_for('login'))
    
    q_index = session.get('q_index', 0)
    questions = session['questions']

    # if somehow index is already out of range → go to results
    if q_index >= len(questions):
        return redirect(url_for('result'))

    selected = request.form.get('option', 'Not Answered')

    # store selected
    session['selected'].append(selected)

    # check correctness
    correct = questions[q_index]['answer']
    if selected == correct:
        session['score'] = session.get('score', 0) + 1

    # increment
    session['q_index'] = q_index + 1

    # finished all questions → show result
    if session['q_index'] >= len(questions):
        return redirect(url_for('result'))
    
    return redirect(url_for('question'))


@app.route('/result')
def result():
    if 'questions' not in session:
        return redirect(url_for('login'))
    username = session.get('username', 'Anonymous')
    score = session.get('score', 0)
    questions = session['questions']
    selected = session.get('selected', [])

    # update leaderboard
    leaderboard.append((username, score))
    # keep top 50
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    if len(leaderboard) > 50:
        leaderboard[:] = leaderboard[:50]

    return render_template('result.html', score=score, total=len(questions), questions=questions, selected=selected)

@app.route('/leaderboard')
def show_leaderboard():
    return render_template('leaderboard.html', leaderboard=leaderboard[:10])

@app.route('/restart')
def restart():
    session.pop('questions', None)
    session.pop('q_index', None)
    session.pop('score', None)
    session.pop('selected', None)
    session.pop('level', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)