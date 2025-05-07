import os
import json
from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 


MY_NAME = "Team 1"
BASE_DIR = os.path.dirname(__file__)

# Load your quiz questions
with open(os.path.join(BASE_DIR, "data", "quiz.json"), "r") as f:
    QUIZ = json.load(f)

# Track non‑interactive answers
answers = []

QUIZ = [
    {"raw_img": "raw1.jpg", "correct": ["brilliance", "exposure", "black_point"]},
    {"raw_img": "raw2.jpg", "correct": ["highlights", "saturation", "brilliance"]},
    {"raw_img": "raw3.jpg", "correct": ["brightness", "black_point", "highlights"]},
]

CORRECT_TOOLS = {
    1: ["black_point","brilliance","exposure"],
    2: ["brilliance","highlights","saturation"],
    3: ["brightness","highlights","black_point"]
}

# Lesson content
LESSONS = {
    1: {
        "title": "Smart Exposure",
        "left_label": "Exposure",
        "left_explanation": Markup("<strong>Raises</strong> or <strong>lowers</strong> overall <strong>light levels</strong> across the whole photo; first stop when everything looks too dark or blown‑out."),
        "left_video": "exposure.gif",
        "right_label": "Brilliance",
        "right_explanation": Markup("Smartly <strong>lifts shadow detail</strong> and <strong>tones down highlights</strong> simultaneously, adding subtle \"HDR\" pop without flattening contrast. "
                                    "Adjusts a photo to make it look <strong>richer</strong> and more <strong>vibrant</strong>, brightening dark areas, pulling in highlights, and <strong>adding contrast</strong> to reveal hidden detail."),
        "right_video": "brilliance.gif"
    },
    2: {
        "title": "Dynamic Range Rescue",
        "left_label": "Highlights",
        "left_explanation": Markup("<strong>Recovers detail in bright areas</strong> (e.g., blown‑out skies) without touching mid‑tones; unique for salvaging over‑bright whites. <strong>Increasing</strong> highlights makes <strong>brighter areas brighter</strong>. <strong>Decreasing</strong> highlights makes <strong>brighter areas darker</strong>."),
        "left_video": "highlights.gif",
        "right_label": "Shadows",
        "right_explanation": Markup("<strong>Brightens the darkest regions</strong> while <strong>preserving bright parts</strong>; great for back‑lit subjects hidden in shade. <strong>Increasing</strong> shadows makes <strong>darker areas brighter</strong>. <strong>Decreasing</strong> shadows makes <strong>darker areas darker</strong>."),
        "right_video": "shawdows.gif"
    },
    3: {
        "title": "Mid‑Tone Control",
        "left_label": "Brightness",
        "left_explanation": Markup("<strong>Adjusts mid‑tones</strong> only, letting you lighten an image without clipping highlights."),
        "left_video": "brightness.gif",
        "right_label": "Contrast",
        "right_explanation": Markup("<strong>Widens</strong> or <strong>narrows</strong> the <strong>gap between lights</strong> and <strong>darks</strong> for extra punch or a flatter look."),
        "right_video": "contrast.gif"
    },
    4: {
        "title": "Deep‑Tone Finish",
        "left_label": "Black Point",
        "left_explanation": Markup("<strong>Deepens true blacks</strong> to add <strong>richness</strong> and <strong>depth</strong>, great for hazy shots."),
        "left_video": "black-point.gif",
        "right_label": "Vignette",
        "right_explanation": Markup("<strong>Darkens</strong> (or <strong>lightens</strong>) <strong>edges</strong> to draw attention toward the center of the frame."),
        "right_video": "vignette.gif"
    },
    5: {
        "title": "White‑Balance Fix",
        "left_label": "Warmth",
        "left_explanation": Markup("<strong>Shifts</strong> the whole <strong>image toward blue or orange</strong> to correct lighting color casts. Warmth <strong>adjusts</strong> the <strong>color tone</strong> of your photo by adding or removing orange and blue tints. <strong>Increasing warmth</strong> adds <strong>more orange</strong>, making the photo look sunnier and cozier. <strong>Decreasing</strong> it adds <strong>more blue</strong>, giving the photo a cooler, more muted look."),
        "left_video": "warmth.gif",
        "right_label": "Tint",
        "right_explanation": Markup("<strong>Fine‑tunes green ↔ magenta balance</strong>, perfect for fluorescent‑light fixes."),
        "right_video": "tint.gif"
    },
    6: {
        "title": "Color Enhancement",
        "left_label": "Saturation",
        "left_explanation": Markup("Saturation <strong>controls</strong> how <strong>intense</strong> or <strong>rich the colors</strong> in your photo <strong>appear</strong>. <strong>Increasing</strong> saturation makes the <strong>colors look brighter</strong>, bolder, and more vibrant. "
                            "<strong>Decreasing</strong> it makes the <strong>colors look faded, softer, or more neutral</strong>. Turning it all the way down can even make the photo look black and white."),
        "left_video": "saturation.gif",
        "right_label": "Vibrance",
        "right_explanation": Markup("Similar to saturation but more subtle with <strong>skin tones</strong>, <strong>enhancing less saturated colors</strong> while preserving already vibrant ones."),
        "right_video": "vibrance.gif"
    },
    7: {
        "title": "Texture Tweaks",
        "left_label": "Sharpness",
        "left_explanation": Markup("<strong>Accentuates edges</strong> for crisper <strong>detail</strong>; best checked at 100% to avoid halos."),
        "left_video": "sharpness.gif",
        "right_label": "Definition",
        "right_explanation": Markup("Mid‑frequency <strong>clarity</strong> that <strong>adds texture</strong> and <strong>micro‑contrast</strong> (similar to \"Clarity\" in Lightroom)."),
        "right_video": "definition.gif"
    },
    # Practice content
    8: {
        "title": "Practice Material - Play with Exposure & Brilliance",
        "left_label": "Exposure",
        "left_explanation": "Play around with the overall exposure of your image to see how light and dark adjustments affect the mood.",
        "right_label": "Brilliance",
        "right_explanation": "Experiment with brilliance to balance shadows and highlights in real-time, exploring the HDR-like effect.",
        "is_practice": True
    },
    9: {
        "title": "Practice Material - Explore Shadows & Highlights",
        "left_label": "Shadows",
        "left_explanation": "Adjust shadows to brighten dark areas and reveal hidden details without affecting highlights.",
        "right_label": "Highlights",
        "right_explanation": "Refine highlights to recover details in over-exposed parts of your photo and restore balance.",
        "is_practice": True
    },
    10: {
        "title": "Practice Material - Play with Saturation & Vibrance",
        "left_label": "Saturation",
        "left_explanation": "Experiment with saturation to control how vibrant or muted the colors in your image appear.",
        "right_label": "Vibrance",
        "right_explanation": "Adjust vibrance to subtly enhance colors without over-saturating skin tones or highly saturated regions.",
        "is_practice": True
    },
    11: {
        "title": "Practice Material - Texture Control",
        "left_label": "Sharpness",
        "left_explanation": "Tweak sharpness to adjust the clarity of fine details and edges, adding definition to your photo.",
        "right_label": "Definition",
        "right_explanation": "Use definition to adjust the mid-frequency clarity and bring out the textures in your image.",
        "is_practice": True
    },
    12: {
        "title": "Practice Material - Explore Vignette & Contrast",
        "left_label": "Vignette",
        "left_explanation": "Play around with vignette settings to create a focus effect, darkening or lightening the edges of your photo.",
        "right_label": "Contrast",
        "right_explanation": "Adjust contrast to create a stronger distinction between light and dark areas, increasing or reducing intensity.",
        "is_practice": True
    },
    13: {
        "title": "Practice Material - Fine-Tune with Warmth & Tint",
        "left_label": "Warmth",
        "left_explanation": "Experiment with warmth to shift the color tone of your photo, making it appear cooler or warmer.",
        "right_label": "Tint",
        "right_explanation": "Adjust tint for fine-tuning the green-magenta balance in your image, perfect for removing color casts.",
        "is_practice": True
    }
}

@app.route("/intro")
def intro_page():
    return render_template("intro_page.html")

@app.route("/pre_practice")
def pre_practice_page():
    return render_template("pre_practice.html")

@app.route("/")
def home_page():
    answers.clear()
    return render_template("home.html", user=MY_NAME)

@app.route("/quiz")
@app.route("/quiz/<int:q_num>")
def quiz_page(q_num=1):
    # reset total on quiz start
    session["total_correct_tools"] = 0
    return render_template("quiz.html", q_num=q_num)


@app.route('/quiz_interactive/<int:q_num>')
def quiz_interactive(q_num):
    raw_img = f"raw{q_num}.jpg"
    correct_tools = CORRECT_TOOLS[q_num]
    return render_template('quiz_interactive.html',
                           q_num=q_num,
                           raw_img=raw_img,
                           correct_tools=correct_tools)

@app.route('/submit_interactive', methods=['POST'])
def submit_interactive():
    data = request.get_json()
    q_num = data.get('q_num')
    selected = data.get('selected', [])

    # compute how many of the selected are correct
    correct_list = CORRECT_TOOLS.get(q_num, [])
    correct_count = sum(1 for t in selected if t in correct_list)

    # initialize per‐question scoring dict if needed
    if 'per_question_scores' not in session:
        session['per_question_scores'] = {}

    # keep the *highest* score seen so far for this question
    prev_best = session['per_question_scores'].get(str(q_num), 0)
    session['per_question_scores'][str(q_num)] = max(prev_best, correct_count)

    # recompute the total across all questions
    session['total_correct_tools'] = sum(session['per_question_scores'].values())

    return jsonify({
        'this_round': correct_count,
        'total_correct': session['total_correct_tools']
    })

@app.route('/quiz_result')
def quiz_result():
    score = session.get('total_correct_tools', 0)
    # reset for next time if you like:
    # session.pop('per_question_scores', None)
    # session.pop('total_correct_tools', None)
    return render_template('quiz_result.html', score=score)


@app.route("/lesson/<int:page_num>")
def lesson_page(page_num):
    # Redirect to intro page if coming from home
    if page_num == 1 and request.referrer and 'home' in request.referrer:
        return redirect(url_for("intro_page"))

    # Redirect to pre-practice page when moving from lesson 7 to practice lesson 8
    if page_num == 8 and request.referrer and 'lesson/7' in request.referrer:
        return redirect(url_for("pre_practice_page"))
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
        "title": "Warmup Quiz Question # 1: Select the Correct Option",
        "question": "Which slider would you adjust to increase the brightness in this photo?",
        "option_1": "A) Brilliance",
        "option_2": "B) Exposure",
        "option_3": "C) Warmth",
        "correct": "option_2",
        "right_label": "Correct!",
        "right_explanation": "Increasing Exposure lightens the overall image. This should be your first step when a photo is too dark, because it corrects the global brightness before fine-tuning other settings like Contrast or Brilliance.",
        "wrong_label": "Incorrect!",
        "wrong_explanation":"Not quite. Adjusting Contrast or Brilliance alone won’t fix an underexposed image. Try increasing the Exposure slider first!Contrast affects the difference between light and dark areas, while Brilliance can tweak shadows and highlights. But if the entire photo is too dark, you need to boost its overall brightness using Exposure.",
        "photo": "Warmup-pic-1.png"
    },
    2: {
        "title": "Warmup Quiz Question # 2: Select the Correct Option",
       "question": "Your photo looks too orange. Which tool helps you fix this?",
        "option_1": "A) Exposure",
        "option_2": "B) Saturation",
        "option_3": "C) Warmth(Temperature)",
        "correct": "option_3",
        "right_label": "Correct!",
        "right_explanation": "Yes! Adjusting the Warmth slider helps fix an orange or blue tint. Great job!Increasing or decreasing Warmth (or ‘Temperature’) balances the color to make it look more natural. Saturation can make colors more vibrant, but won’t correct an orange or blue tint.",
        "wrong_label": "Incorrect!",
        "wrong_explanation":"Not quite. Exposure brightens or darkens the whole image, and Saturation affects color intensity. Warmth specifically adjusts the color cast, so it’s the best tool here.",
        "photo": "Warmup-pic-2.png"
    },
    3: {
        "title": "Warmup Quiz Question # 3: Fill in the Blanks",
        "question": "Increasing shadows makes ____ areas ______",
        "option_1": "A) Brighter, Darker",
        "option_2": "B) Darker, Brighter",
        "option_3": "C) Darker, Darker",
        "correct": "option_2",
        "right_label": "Correct!",
        "right_explanation": "Yes! Increasing shadows brightens the darker areas of an image. This adjustment lifts the shadow tones, making details in those areas more visible without changing the brightness of the lighter parts.",
        "wrong_label": "Incorrect!",
        "wrong_explanation":"Not quite. The correct answer is Increasing shadows makes darker areas brighter A) Brighter, Darker – Incorrect: This is incorrect because increasing shadows does not make bright areas darker. It specifically affects the dark areas, making them brighter, not the other way around. C) Darker, Darker – Incorrect: This is incorrect because increasing shadows doesn’t make anything darker. It actually makes the dark areas brighter, helping to reveal more detail in those parts of the image.",
        "photo": "Taabeer_rec.mov"
    },
    4: {
        "title": "Warmup Quiz Question # 4: Fill in the Blanks",
       "question": "Increasing higlights makes ____ areas ______",
        "option_1": "A) Darker, Darker",
        "option_2": "B) Brighter, Darker",
        "option_3": "C) Brighter, Brighter",
        "correct": "option_3",
        "right_label": "Correct!",
        "right_explanation": "Yes! Increasing highlights makes the already bright areas even brighter. This adjustment affects the lighter parts of an image, enhancing their brightness without changing the darker areas.",
        "wrong_label": "Incorrect!",
        "wrong_explanation":"Not quite. Increasing highlights makes brighter areas brighter Incorrect Answer: A) Darker, Darker Explanation: This is incorrect because increasing highlights doesn't make anything darker. It specifically affects the bright parts of an image by making them brighter, not darker. Incorrect Answer: B) Brighter, Darker Explanation: This answer is wrong because increasing highlights does not make any area darker. It only affects the brighter areas, and it makes them even brighter, not darker.",
        "photo": "Taabeer_rec.mov"
    },
}
@app.route('/submit_warmup', methods=['POST'])
def submit_warmup():
    data = request.get_json()
    page_num = data['page_num']
    selected = data['selected']
    question = WARMUP[page_num]
    
    is_correct = (selected == question['correct'])
    
    return jsonify({
        'is_correct': is_correct,
        'right_label': question['right_label'],
        'right_explanation': question['right_explanation'],
        'wrong_label': question['wrong_label'],
        'wrong_explanation': question['wrong_explanation']
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
