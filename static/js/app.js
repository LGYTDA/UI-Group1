
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

        // show result
        alert(`You got ${score} out of ${total} correct!`);

        // lock everything down
        $(".icon-wrapper").off("click");
        $(this).prop("disabled", true);
        $("#next-btn").fadeIn();
    });
});