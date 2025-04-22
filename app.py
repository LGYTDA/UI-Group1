import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

MY_NAME = "Abraham Alemu"

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "data", "quiz.json"), "r") as f:
    QUIZ = json.load(f)

answers = []

@app.route("/")
def home_page():
    answers.clear()
    return render_template("home.html", user=MY_NAME)

@app.route("/quiz/<int:q_num>", methods=["GET", "POST"])
def quiz_page(q_num):
    total = len(QUIZ)
    # If past the last question, show results
    if q_num > total:
        return redirect(url_for("quiz_result"))

    question = QUIZ.get(str(q_num))
    if not question:
        return redirect(url_for("quiz_result"))

    if request.method == "POST":
        # record answer and move on
        selected = request.form.get("choice")
        answers.append({"q": q_num, "choice": selected})
        return redirect(url_for("quiz_page", q_num=q_num + 1))

    return render_template(
        "quiz.html",
        question_num=q_num,
        total=total,
        question=question
    )

@app.route("/quiz_result")
def quiz_result():
    correct = 0
    for entry in answers:
        qid = str(entry["q"])
        if entry["choice"] == QUIZ[qid]["correct"]:
            correct += 1
    score = f"{correct}/{len(QUIZ)}"
    return render_template("result.html", score=score)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
