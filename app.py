import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

MY_NAME = "Team 1"
BASE_DIR = os.path.dirname(__file__)

# Load your quiz questions
with open(os.path.join(BASE_DIR, "data", "quiz.json"), "r") as f:
    QUIZ = json.load(f)

# Track non‑interactive answers
answers = []

# Map q_num → the three correct tool‐IDs
INTERACTIVE_CORRECT = {
    1: ["exposure",  "brilliance",   "black_point"],
    2: ["highlights","brilliance",   "saturation"],
    3: ["highlights","black_point",  "brightness"]
}

# Lesson content
LESSONS = {
    1: {
        "title": "Smart Exposure",
        "left_label": "Exposure",
        "left_explanation": "Raises or lowers overall light levels across the whole photo; first stop when everything looks too dark or blown‑out.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Brilliance",
        "right_explanation": "Smartly lifts shadow detail and tones down highlights simultaneously, adding subtle \"HDR\" pop without flattening contrast. Adjusts a photo to make it look richer and more vibrant, brightening dark areas, pulling in highlights, and adding contrast to reveal hidden detail.",
        "right_video": "Taabeer_rec.mov"
    },
    2: {
        "title": "Dynamic Range Rescue",
        "left_label": "Highlights",
        "left_explanation": "Recovers detail in bright areas (e.g., blown‑out skies) without touching mid‑tones; unique for salvaging over‑bright whites. Increasing highlights makes brighter areas brighter. Decreasing highlights makes brighter areas darker.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Shadows",
        "right_explanation": "Brightens the darkest regions while preserving bright parts; great for back‑lit subjects hidden in shade. Increasing shadows makes darker areas brighter. Decreasing shadows makes darker areas darker.",
        "right_video": "Taabeer_rec.mov"
    },
    3: {
        "title": "Mid‑Tone Control",
        "left_label": "Brightness",
        "left_explanation": "Adjusts mid‑tones only, letting you lighten an image without clipping highlights.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Contrast",
        "right_explanation": "Widens or narrows the gap between lights and darks for extra punch or a flatter look.",
        "right_video": "Taabeer_rec.mov"
    },
    4: {
        "title": "Deep‑Tone Finish",
        "left_label": "Black Point",
        "left_explanation": "Deepens true blacks to add richness and depth, great for hazy shots.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Vignette",
        "right_explanation": "Darkens (or lightens) edges to draw attention toward the center of the frame.",
        "right_video": "Taabeer_rec.mov"
    },
    5: {
        "title": "White‑Balance Fix",
        "left_label": "Warmth",
        "left_explanation": "Shifts the whole image toward blue or orange to correct lighting color casts. Warmth adjusts the color tone of your photo by adding or removing orange and blue tints. Increasing warmth adds more orange, making the photo look sunnier and cozier. Decreasing it adds more blue, giving the photo a cooler, more muted look.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Tint",
        "right_explanation": "Fine‑tunes green ↔ magenta balance, perfect for fluorescent‑light fixes.",
        "right_video": "Taabeer_rec.mov"
    },
    6: {
        "title": "Color Enhancement",
        "left_label": "Saturation",
        "left_explanation": "Saturation controls how intense or rich the colors in your photo appear. Increasing saturation makes the colors look brighter, bolder, and more vibrant. Decreasing it makes the colors look faded, softer, or more neutral. Turning it all the way down can even make the photo look black and white.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Vibrance",
        "right_explanation": "Similar to saturation but more subtle with skin tones, enhancing less saturated colors while preserving already vibrant ones.",
        "right_video": "Taabeer_rec.mov"
    },
    7: {
        "title": "Texture Tweaks",
        "left_label": "Sharpness",
        "left_explanation": "Accentuates edges for crisper detail; best checked at 100% to avoid halos.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Definition",
        "right_explanation": "Mid‑frequency clarity that adds texture and micro‑contrast (similar to \"Clarity\" in Lightroom).",
        "right_video": "Taabeer_rec.mov"
    },
    # Practice content
    8: {
        "title": "Practice Material - Play with Exposure & Brilliance",
        "left_label": "Exposure",
        "left_explanation": "Play around with the overall exposure of your image to see how light and dark adjustments affect the mood.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Brilliance",
        "right_explanation": "Experiment with brilliance to balance shadows and highlights in real-time, exploring the HDR-like effect.",
        "right_video": "Taabeer_rec.mov"
    },
    9: {
        "title": "Practice Material - Explore Shadows & Highlights",
        "left_label": "Shadows",
        "left_explanation": "Adjust shadows to brighten dark areas and reveal hidden details without affecting highlights.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Highlights",
        "right_explanation": "Refine highlights to recover details in over-exposed parts of your photo and restore balance.",
        "right_video": "Taabeer_rec.mov"
    },
    10: {
        "title": "Practice Material - Play with Saturation & Vibrance",
        "left_label": "Saturation",
        "left_explanation": "Experiment with saturation to control how vibrant or muted the colors in your image appear.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Vibrance",
        "right_explanation": "Adjust vibrance to subtly enhance colors without over-saturating skin tones or highly saturated regions.",
        "right_video": "Taabeer_rec.mov"
    },
    11: {
        "title": "Practice Material - Texture Control",
        "left_label": "Sharpness",
        "left_explanation": "Tweak sharpness to adjust the clarity of fine details and edges, adding definition to your photo.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Definition",
        "right_explanation": "Use definition to adjust the mid-frequency clarity and bring out the textures in your image.",
        "right_video": "Taabeer_rec.mov"
    },
    12: {
        "title": "Practice Material - Explore Vignette & Contrast",
        "left_label": "Vignette",
        "left_explanation": "Play around with vignette settings to create a focus effect, darkening or lightening the edges of your photo.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Contrast",
        "right_explanation": "Adjust contrast to create a stronger distinction between light and dark areas, increasing or reducing intensity.",
        "right_video": "Taabeer_rec.mov"
    },
    13: {
        "title": "Practice Material - Fine-Tune with Warmth & Tint",
        "left_label": "Warmth",
        "left_explanation": "Experiment with warmth to shift the color tone of your photo, making it appear cooler or warmer.",
        "left_video": "Taabeer_rec.mov",
        "right_label": "Tint",
        "right_explanation": "Adjust tint for fine-tuning the green-magenta balance in your image, perfect for removing color casts.",
        "right_video": "Taabeer_rec.mov"
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
    # make sure it’s a valid question
    if q_num not in INTERACTIVE_CORRECT:
        return redirect(url_for("quiz_result"))

    raw_img      = f"raw{q_num}.jpg"
    correct_tools = INTERACTIVE_CORRECT[q_num]

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

    interactive_controls = []

    INTERACTIVE_LESSONS = {
        8: ["Exposure", "Brilliance"],
        9: ["Shadows", "Highlights"],
        10: ["Saturation", "Vibrance"],
        11: ["Sharpness", "Definition"],
        12: ["Vignette", "Contrast"],
        13: ["Warmth", "Tint"]
    }

    if page_num in INTERACTIVE_LESSONS:
        interactive_controls = INTERACTIVE_LESSONS[page_num]

    return render_template(
        "lesson_page.html",
        page_num=page_num,
        total_pages=total_pages,
        lesson=lesson,
        interactive_controls=interactive_controls,
        lessons=LESSONS
    )



@app.route("/warmup/<int:page_num>")
def warmup_page(page_num):
    total_pages = len(WARMUP)
    if page_num not in WARMUP:
        return redirect(url_for("warmup_page", page_num=1))
    question = WARMUP[page_num]

    return render_template(
        "warmup_quiz.html",
        page_num=page_num,
        total_pages=total_pages,
        question=question,
        questions=WARMUP
    )
WARMUP = {
    1: {
        "title": "Quiz Question # 1: Select the Correct Option",
        "question": "Which slider would you adjust to increase the brightness in this photo?",
        "option_1": "A) Brilliance",
        "option_2": "B) Exposure",
        "option_3": "C) Warmth",
        "photo": "Warmup-pic-1.mov"
    },
    2: {
        "title": "Quiz Question # 2: Select the Correct Option",
       "question": "Your photo looks too orange. Which tool helps you fix this?",
        "option_1": "A) Exposure",
        "option_2": "B) Saturation",
        "option_3": "C) Warmth(Temperature)",
        "photo": "Warmup-pic-2.mov"
    },
    3: {
        "title": "Quiz Question # 3: Fill in the Blanks",
        "question": "Increasing shadows makes ____ areas ______",
        "option_1": "A) Brighter, Darker",
        "option_2": "B) Darker, Brighter",
        "option_3": "C) Darker, Darker",
        "photo": "Taabeer_rec.mov"
    },
    4: {
        "title": "Quiz Question # 4: Fill in the Blanks",
       "question": "Increasing higlights makes ____ areas ______",
        "option_1": "A) Darker, Darker",
        "option_2": "B) Brighter, Darker",
        "option_3": "C) Brighter, Brighter",
        "photo": "Taabeer_rec.mov"
    },
}



if __name__ == "__main__":
    app.run(debug=True, port=5001)
