from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
from model import get_predictions


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
    user_answers = request.json.get('answers')  # The answer submitted by the user
    # from DataFrame The correct answer to extract (Hypothesis df In the middle 'prompt' and 'answer' Two columns)
    correct_answers = {f"q{index + 1}": q['answer'] for index, q in df.iterrows()}  # structure q1, q2 Format key
    
    result = {
        'correct': [],
        'wrong': [],
        'answers': correct_answers  
    }
    
    for question, answer in user_answers.items():
        if answer == correct_answers.get(question):
            result['correct'].append(question)  # Answer questions
        else:
            result['wrong'].append(question)  # The question that is wrong
    
    return jsonify(result)  # Return to the correct answer JSON

@app.route('/submitQA', methods=['POST'])
def submit_customized_qa():
    try:
        # fromPOSTGet in requestJSONdata
        data = request.json

        # data
        question = data.get('question')
        answerA = data.get('answerA')
        answerB = data.get('answerB')
        answerC = data.get('answerC')
        answerD = data.get('answerD')

        if not question or not all([answerA, answerB, answerC, answerD]):
            return jsonify({'error': 'Invalid input: Question and all answers are required.'}), 400

        # Call prediction function
        example = {
            'prompt': question,
            'A': answerA,
            'B': answerB,
            'C': answerC,
            'D': answerD
        }

        ranked_answers = get_predictions(example)

        # Return result
        return jsonify({'ranked_answers': ranked_answers})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
