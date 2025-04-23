
// Wait until DOM + jQuery are ready
$(function () {
    // --- Optional logging ---
    console.log("Loaded quiz question at", new Date().toISOString());

    // --- Pull in globals set by your template ---
    const correctTools = window.correctTools || [];
    const comboBase = window.comboBase || "/static/img/combos/";

    // Map to your combo‑file codes
    const codeMap = {
        black_point: "blk",
        brilliance: "bri",
        exposure: "exp"
    };

    // State of our selections
    let selected = [];

    // 1) Icon click → select up to correctTools.length
    $(".icon-wrapper").on("click", function () {
        const $this = $(this);
        const tool = $this.data("tool");

        // already chosen or maxed out?
        if ($this.hasClass("selected") || selected.length >= correctTools.length) {
            return;
        }

        // mark it
        $this.addClass("selected");
        selected.push(tool);

        // enable “Check Response” only when user has picked exactly that many
        $("#check-btn").prop("disabled", selected.length !== correctTools.length);
    });

    // 2) Check button → show feedback and score
    $("#check-btn").on("click", function () {
        const total = correctTools.length;
        let score = 0;

        // Loop through picks in order
        selected.forEach((tool, i) => {
            const $wrapper = $(`.icon-wrapper[data-tool="${tool}"]`);
            const $fb = $wrapper.find(".feedback-icon");

            // correct?
            if (correctTools.includes(tool)) {
                score++;
                $fb.addClass("check").text("✓");
                // update edited-photo preview
                const picks = selected
                    .slice(0, i + 1)
                    .map(t => codeMap[t] || t)
                    .join("-");
                $("#edited-img").attr("src", comboBase + "q1-" + picks + ".jpg");
            } else {
                $fb.addClass("wrong").text("✕");
            }
        });

        // lock everything down
        $(".icon-wrapper").off("click");
        $(this).prop("disabled", true);
        $("#next-btn").fadeIn();
    });
});

$(document).ready(function () {
    console.log("Loaded interactive lesson page at", new Date().toISOString());

    if (typeof interactiveControls !== 'undefined' && interactiveControls.length) {
        interactiveControls.forEach(function(control) {
            // Assumes that the HTML element IDs match the control strings exactly.
            let slider = $("#" + control + "Range");
            let valueDisplay = $("#" + control + "-value");

            slider.on('input', function() {
                let value = $(this).val();
                console.log("Slider value for " + control + ": " + value);
                valueDisplay.text(value);
                applyImageEffect(control, value);
            });
        });
    }
});

function applyImageEffect(control, value) {
    let image = $("#editCanvas");
    let ctl = control.toLowerCase();
    let parsedValue = parseInt(value);
    switch (ctl) {
        case "exposure":
            image.css("filter", "brightness(" + (100 + parsedValue) + "%)");
            break;
        case "brilliance":
            image.css("filter", "contrast(" + (100 + parsedValue) + "%)");
            break;
        case "black point":
            image.css("filter", "brightness(" + (100 - parsedValue) + "%)");
            break;
        case "contrast":
            image.css("filter", "contrast(" + (100 + parsedValue) + "%)");
            break;
        case "warmth":
            image.css("filter", "sepia(" + (parsedValue / 100) + ")");
            break;
        case "shadows":
            image.css("filter", "brightness(" + (100 - parsedValue) + "%)");
            break;
        case "highlights":
            image.css("filter", "brightness(" + (100 + parsedValue) + "%)");
            break;
        case "saturation":
            image.css("filter", "saturate(" + (100 + parsedValue) + "%)");
            break;
        case "vibrance":
            image.css("filter", "contrast(" + (100 + parsedValue) + "%)");
            break;
        case "sharpness":
            // Invert the slider: higher value means less blur (i.e., sharper image)
            let blurAmount = (100 - parsedValue) / 10;
            image.css("filter", "blur(" + blurAmount + "px)");
            break;
        case "definition":
            // Enhance clarity by boosting contrast and a tad of saturation
            image.css("filter", "contrast(" + (100 + parsedValue) + "%) saturate(" + (100 + parsedValue/2) + "%)");
            break;
        case "vignette":
            image.css("filter", "brightness(" + (100 - parsedValue) + "%)");
            break;
        case "tint":
            image.css("filter", "grayscale(" + (100 - parsedValue) + "%)");
            break;
        default:
            console.log("Unknown control: " + control);
            break;
    }
}
