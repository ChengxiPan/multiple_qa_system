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
    user_answers = request.json.get('answers')  # 用户提交的答案
    # 从 DataFrame 中提取正确答案 (假设 df 中有 'prompt' 和 'answer' 两列)
    correct_answers = {f"q{index + 1}": q['answer'] for index, q in df.iterrows()}  # 构造 q1, q2 格式的键
    
    result = {
        'correct': [],
        'wrong': [],
        'answers': correct_answers  
    }
    
    for question, answer in user_answers.items():
        if answer == correct_answers.get(question):
            result['correct'].append(question)  # 答对的题目
        else:
            result['wrong'].append(question)  # 答错的题目
    
    return jsonify(result)  # 返回包含正确答案的 JSON

@app.route('/submitQA', methods=['POST'])
def submit_customized_qa():
    try:
        # 从POST请求中获取JSON数据
        data = request.json

        # 验证数据是否完整
        question = data.get('question')
        answerA = data.get('answerA')
        answerB = data.get('answerB')
        answerC = data.get('answerC')
        answerD = data.get('answerD')

        if not question or not all([answerA, answerB, answerC, answerD]):
            return jsonify({'error': 'Invalid input: Question and all answers are required.'}), 400

        # 调用预测函数
        example = {
            'prompt': question,
            'A': answerA,
            'B': answerB,
            'C': answerC,
            'D': answerD
        }

        ranked_answers = get_predictions(example)

        # 返回结果
        return jsonify({'ranked_answers': ranked_answers})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
