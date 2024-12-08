from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

df = pd.read_csv('./test.csv')

def get_random_questions(n=3):
    questions = df.sample(n=n).to_dict(orient='records')
    return questions

@app.route('/')
def index():
    questions = get_random_questions()
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.json.get('answers') 
    correct_answers = {q['prompt']: q['answer'] for _, q in df.iterrows()}
    result = {
        'correct': [],
        'wrong': []
    }
    
    for question, answer in user_answers.items():
        if answer == correct_answers.get(question):
            result['correct'].append(question)
        else:
            result['wrong'].append(question)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
