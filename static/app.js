$game = $("#game")
$gameInfo = $("#game-info")
$end = $("#end")

$startBtn = $("#start-btn")
$restartBtn = $("#restart-btn")

$guess = $("#guess")
$guessForm = $("#guess-form")
$message = $("#message")
$score = $("#score")
$timer = $("#timer")
$userInfo = $("#user-info")

let score = 0;
const words = []

$game.show()

$gameInfo.hide()
$end.hide()

function startTimer(limit) {
    let time = limit;
    let interval = setInterval(async() => {
        $timer.text(`${time} seconds`)
        if (time == 0) {
            clearInterval(interval);
            await gameOver();
        } else {
            time --;
        }
    }, 1000);
}

async function gameOver() {
    $gameInfo.hide();
    $end.show();

    results = await axios.post("/end", {"score": score});
    $userInfo.show();
    $userInfo.append(`<h2 class="info">Games played: ${results.data.games_played}</h2>`);
    $userInfo.append(`<h2 class="info">High score: ${results.data.high_score}</h2>`);
}

$startBtn.on("click", (evt) => {
    $startBtn.hide();
    $gameInfo.show();
    $guess.focus();
    
    startTimer(60);
}
)

$guessForm.on("submit", async (evt) => {
    evt.preventDefault();

    guess = $guess.val();
    let message = "";

    if (!words.includes(guess)) {
        const results = await axios.get("/guess", {params: {"guess": guess}});
        
        if (results.data.result == "ok") {
            message = "You have selected a valid word";
            score += guess.length
            $score.text(`Score: ${score}`);
            words.push(guess)
        } else if (results.data.result == "not-on-board") {
            message = "That word is not on the board";
        } else if (results.data.result == "not-word") {
            message = "That is not a valid word";
        } 
    } else {
        message = "You have already selected that word";
    }
    $message.text(message);
    $guess.val("");
})

$restartBtn.on("click", () => {
    window.location.href = "/"
}
)


