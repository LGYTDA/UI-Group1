# iEdit

iPhone Photo Editing 101 — an interactive web app to teach Users to edit photos on their IPhones!

## Features

* **Lessons**: Step‑by‑step demos for each iPhone editing tool.
* **Practice**: Adjustable sliders to experiment with tools live.
* **Warmup Quiz**: A mini practice quiz to provide User feedback a simply practice before the main quiz.
* **Quiz**: Three challenges; identify the 3 tools used per image, scored out of 9.

## Running the App

```
python app.py
```

Open your browser at `http://localhost:5001`.

## Project Structure

```
.
├── app.py                    # Flask routes & application logic
├── requirements.txt          # Python dependencies
├── static/
│   ├── css/style.css         # Custom styles
│   ├── js/app.js             # Shared JavaScript helpers
│   └── img/
│       ├── canvas.png        # Lesson canvas base image
│       ├── icons/            # Tool icons & combo images
│       └── Lesson‑Videos/    # GIF demos for lessons
├── templates/
│   ├── index.html            # Base layout template
│   ├── home.html             # Home screen
│   ├── intro_page.html       # Lessons intro
│   ├── lesson_page.html      # Lesson content pages
│   ├── pre_practice.html     # Practice intro
│   ├── quiz.html             # Quiz intro
│   ├── quiz_interactive.html # Interactive quiz pages
│   ├── quiz_result.html      # Quiz results display
│   ├── warmup_quiz.html      # Warm‑up quiz pages
│   └── ...
└── README.md                 # This documentation file
```

## 🔗 Application Routes

| **Path**                 | **Method** | **Description**                     |
| ------------------------ | ---------- | ----------------------------------- |
| `/`                      | GET        | Home page                           |
| `/intro`                 | GET        | Intro to lessons                    |
| `/lesson/<int:page_num>` | GET        | Lesson page `page_num`              |
| `/pre_practice`          | GET        | Practice introduction               |
| `/quiz`                  | GET        | Quiz introduction                   |
| `/quiz/<int:q_num>`      | GET        | Quiz challenge `q_num`              |
| `/submit_interactive`    | POST       | AJAX: record interactive quiz state |
| `/quiz_result`           | GET        | Final quiz results (score out of 9) |
| `/warmup/<int:page_num>` | GET/POST   | Warm‑up quiz pages                  |
| `/submit_warmup`         | POST       | AJAX: submit warm‑up answer         |
