// (Optional) You can add logging or analytics here.
// Example: record the timestamp whenever the user loads a quiz question.
$(document).ready(function () {
    console.log("Loaded quiz question at", new Date().toISOString());
});

$(document).ready(function () {
    console.log("Loaded interactive lesson page at", new Date().toISOString());

    if (typeof interactiveControls !== 'undefined' && interactiveControls.length) {
        interactiveControls.forEach(function(control) {
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


//loads interactive image setting changes
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
            let blurAmount = (100 - parsedValue) / 10;
            image.css("filter", "blur(" + blurAmount + "px)");
            break;
        case "definition":
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
