from flask import Flask, render_template, request, jsonify
from model import get_predictions

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    answers = data.get("answers", [])
    top_n = int(data.get("top_n", 1))
    
    predictions = get_predictions(answers, top_n)
    
    return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True)
