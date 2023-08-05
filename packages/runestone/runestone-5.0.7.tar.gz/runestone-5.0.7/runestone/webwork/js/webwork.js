import RunestoneBase from "../../common/js/runestonebase";

let rb = new RunestoneBase();

function logWebWork(e, data) {
    var correct = false;
    let correctCount = 0;
    let qCount = 0;
    let actString = "check:";
    for (let k of Object.keys(data.answers)) {
        qCount += 1;
        if (data.answers[k].score == 1) {
            correctCount += 1;
        }
        actString += `actual:${data.answers[k].student_ans}:expected:${data.answers[k].correct_value}:`;
    }
    let pct = correctCount / qCount;
    actString += `correct:${correctCount}:count:${qCount}:pct:${pct}`;
    if (pct == 1.0) {
        correct = true;
    }
    rb.logBookEvent({
        event: "webwork",
        div_id: data.ww_id,
        act: actString,
        correct: correct,
    });
}

function logShowCorrect(e, data) {
    rb.logBookEvent({
        event: "webwork",
        div_id: data.ww_id,
        act: "show",
    });
}

$(document).ready(function () {
    $("body").on("runestone_ww_check", logWebWork);
    $("body").on("runestone_show_correct", logShowCorrect);
});
