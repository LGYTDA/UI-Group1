import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

MY_NAME = "Abraham Alemu"

BASE_DIR = os.path.dirname(__file__)

LESSONS = {
    1:{"title" : "..."},
    2:{"title" : "...."},
    3:{"title" : "....."}
}

with open(os.path.join(BASE_DIR, "data", "quiz.json"), "r") as f:
    QUIZ = json.load(f)


answers = []

INTERACTIVE = {
    "1": ["highlights", "brilliance", "saturation"],
    "2": ["exposure", "contrast", "warmth"],
    "3": ["shadows", "definition", "vignette"]
}


@app.route("/")
def home_page():
    answers.clear()
    return render_template("home.html", user=MY_NAME)


@app.route("/quiz/<int:q_num>", methods=["GET", "POST"])
def quiz_page(q_num):
    total = len(QUIZ)
    if q_num > total:
        return redirect(url_for("quiz_result"))

    question = QUIZ.get(str(q_num))
    if not question:
        return redirect(url_for("quiz_result"))

    if request.method == "POST":
        selected = request.form.get("choice")
        answers.append({"q": q_num, "choice": selected})
        return redirect(url_for("quiz_page", q_num=q_num + 1))

    return render_template(
        "quiz.html",
        question_num=q_num,
        total=total,
        question=question
    )


@app.route("/quiz_interactive/<int:q_num>")
def quiz_interactive(q_num):
    """
    Renders the fully interactive quiz page for image #q_num.
    The template will use JS to let users click icons, show checks/Xs,
    and apply CSS filters based on the INTERACTIVE mapping below.
    """
    raw_filename = f"raw{q_num}.jpg"
    edited_filename = raw_filename  # start same; JS will toggle filter classes
    correct_tools = INTERACTIVE.get(str(q_num), [])
    return render_template(
        "quiz_interactive.html",
        q_num=q_num,
        raw_img=raw_filename,
        edited_img=edited_filename,
        correct_tools=correct_tools
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


@app.route("/lesson/<int:page_num>")
def lesson_page(page_num):
    total_pages = len(LESSONS)

    if page_num not in LESSONS:
        return redirect(url_for("lesson_page.html", page_num=1))

    lesson = LESSONS[page_num]
    return render_template(
        "lesson_page.html",
        page_num=page_num,
        total_pages=total_pages,
        lesson=lesson
    )
if __name__ == "__main__":
    app.run(debug=True, port=5001)
