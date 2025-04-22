import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

MY_NAME = "Team 1"

BASE_DIR = os.path.dirname(__file__)

# (Your existing quiz data)
with open(os.path.join(BASE_DIR, "data", "quiz.json"), "r") as f:
    QUIZ = json.load(f)

answers = []

INTERACTIVE = {
    "1": ["exposure", "brilliance", "black point"],
    "2": ["exposure", "contrast", "warmth"],
    "3": ["shadows", "definition", "vignette"]
}
# (Optional) if you still have LESSONS and lesson_page)
LESSONS = {
    1: {
        "title": "Smart Exposure",
        "left_label": "Exposure",
        "left_explanation": "Raises or lowers overall light levels across the whole photo; first stop when everything looks too dark or blown‑out.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Brilliance",
        "right_explanation": "Smartly lifts shadow detail and tones down highlights simultaneously, adding subtle \"HDR\" pop without flattening contrast. Adjusts a photo to make it look richer and more vibrant, brightening dark areas, pulling in highlights, and adding contrast to reveal hidden detail.",
        "right_video": "Tabeer_rec.mov"
    },
    2: {
        "title": "Dynamic Range Rescue",
        "left_label": "Highlights",
        "left_explanation": "Recovers detail in bright areas (e.g., blown‑out skies) without touching mid‑tones; unique for salvaging over‑bright whites. Increasing highlights makes brighter areas brighter. Decreasing highlights makes brighter areas darker.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Shadows",
        "right_explanation": "Brightens the darkest regions while preserving bright parts; great for back‑lit subjects hidden in shade. Increasing shadows makes darker areas brighter. Decreasing shadows makes darker areas darker.",
        "right_video": "Tabeer_rec.mov"
    },
    3: {
        "title": "Mid‑Tone Control",
        "left_label": "Brightness",
        "left_explanation": "Adjusts mid‑tones only, letting you lighten an image without clipping highlights.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Contrast",
        "right_explanation": "Widens or narrows the gap between lights and darks for extra punch or a flatter look.",
        "right_video": "Tabeer_rec.mov"
    },
    4: {
        "title": "Deep‑Tone Finish",
        "left_label": "Black Point",
        "left_explanation": "Deepens true blacks to add richness and depth, great for hazy shots.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Vignette",
        "right_explanation": "Darkens (or lightens) edges to draw attention toward the center of the frame.",
        "right_video": "Tabeer_rec.mov"
    },
    5: {
        "title": "White‑Balance Fix",
        "left_label": "Warmth",
        "left_explanation": "Shifts the whole image toward blue or orange to correct lighting color casts. Warmth adjusts the color tone of your photo by adding or removing orange and blue tints. Increasing warmth adds more orange, making the photo look sunnier and cozier. Decreasing it adds more blue, giving the photo a cooler, more muted look.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Tint",
        "right_explanation": "Fine‑tunes green ↔ magenta balance, perfect for fluorescent‑light fixes.",
        "right_video": "Tabeer_rec.mov"
    },
    6: {
        "title": "Color Enhancement",
        "left_label": "Saturation",
        "left_explanation": "Saturation controls how intense or rich the colors in your photo appear. Increasing saturation makes the colors look brighter, bolder, and more vibrant. Decreasing it makes the colors look faded, softer, or more neutral. Turning it all the way down can even make the photo look black and white.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Vibrance",
        "right_explanation": "Similar to saturation but more subtle with skin tones, enhancing less saturated colors while preserving already vibrant ones.",
        "right_video": "Tabeer_rec.mov"
    },
    7: {
        "title": "Texture Tweaks",
        "left_label": "Sharpness",
        "left_explanation": "Accentuates edges for crisper detail; best checked at 100% to avoid halos.",
        "left_video": "Tabeer_rec.mov",
        "right_label": "Definition",
        "right_explanation": "Mid‑frequency clarity that adds texture and micro‑contrast (similar to \"Clarity\" in Lightroom).",
        "right_video": "Tabeer_rec.mov"
    }
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
    # Hard‑coded for Image 1
    raw_img       = f"raw{q_num}.jpg"
    correct_tools = ["black_point", "brilliance", "exposure"]
    return render_template(
        "quiz_interactive.html",
        q_num=q_num,
        raw_img=raw_img,
        correct_tools=correct_tools
    )

@app.route("/quiz_result")
def quiz_result():
    correct = sum(
        1 for entry in answers
        if entry["choice"] == QUIZ[str(entry["q"])]["correct"]
    )
    score = f"{correct}/{len(QUIZ)}"
    return render_template("result.html", score=score)

@app.route("/lesson/<int:page_num>")
def lesson_page(page_num):
    total_pages = len(LESSONS)
    if page_num not in LESSONS:
        return redirect(url_for("lesson_page", page_num=1))
    lesson = LESSONS[page_num]
    return render_template(
        "lesson_page.html",
        page_num=page_num,
        total_pages=total_pages,
        lesson=lesson
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
