/*
    TODO:
        - Fix bug where pressing the 'get next question' button then buzzing with spacebar skips the question
        - Fix visual bug where the button to change correctness loses its CSS when it reads 'I was correct' 
*/
function Timer(callback, delay) {
    var args = arguments,
        self = this,
        timer, start;

    this.clear = function () {
        clearTimeout(timer);
    };

    this.pause = function () {
        this.clear();
        delay -= new Date() - start;
    };

    this.resume = function () {
        start = new Date();
        timer = setTimeout(function () {
            callback.apply(self, Array.prototype.slice.call(args, 2, args.length));
        }, delay);
    };

    this.resume();
}

function toggleVisibility(id) {
    const element = document.getElementById(id);
    const buttonElement = document.getElementById(id+"Button");

    // I (sophia) put an extra check for '' (it's still hidden at '')
    if (element.style.display === "none" || element.style.display === '') {
        element.style.display = "block";
        buttonElement.style.borderRadius = '15px 15px 0px 0px';
    } else {
        element.style.display = "none";
        buttonElement.style.borderRadius = '15px';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('audio');
    const audioSource = document.getElementById('audioSource');
    const buzzer = document.getElementById('buzzer');
    const nextButton = document.getElementById('nextQuestion');
    const textDiv = document.getElementById('question');
    const textInput = document.getElementById('answer');
    const answerBox = document.getElementById('answerLine');
    const answerDisplay = document.getElementById('actualAnswer');
    const displayedScore = document.getElementById('score');
    const answerRight = document.getElementById('answerRight');
    const readingSpeed = document.getElementById('readingSpeed');

    let score = 0;
    let textCues = [];
    let answer = '';
    let lastDisplayedText = '';
    let onWord = 0;
    let intervalId = null;
    let reading_speed = 0;

    let buzzedIn = false;
    let questionEnded = false;
    let questionDone = false;
    let inPower = false;
    let interrupt = false;
    let questionLoaded = true;
    let parametersChanged = false;

    let timer = null;
    let timerPaused = false;

    let previousSubjects = [];
    let previousDifficulties = [];

    const audioUrl = "{{ url_for('audio', filename='audio.mp3') }}";
    console.log(audioUrl);

    function get_params() {
        const subjects = Array.from(document.querySelectorAll('#categories input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
        const question_numbers = Array.from(document.querySelectorAll('#difficulties input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
        reading_speed = readingSpeed.value / 100;
        
        parametersChanged = JSON.stringify(subjects) !== JSON.stringify(previousSubjects) || 
                            JSON.stringify(question_numbers) !== JSON.stringify(previousDifficulties);
        
        previousSubjects = subjects;
        previousDifficulties = question_numbers;
    }

    function get_next_question() {
        const params = new URLSearchParams({
            subjects: JSON.stringify(previousSubjects),
            question_numbers: JSON.stringify(previousDifficulties),
            readingSpeed: JSON.stringify(reading_speed)
        });

        return fetch('/api/get_next_question?' + params.toString());
    }

    const fetchTextCues = () => fetch('/api/get_text')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            textCues = data; 
        })
        .catch(error => console.error('Error fetching text cues:', error));

    const fetchAnswer = () => fetch('/api/get_answer')
        .then(response => response.text()) // Corrected typo here
        .then(text => {
        answer = text;
        console.log("Answewwerr: ", answer);
        })
        .catch(error => console.error('Error fetching text cues:', error));

    const updateText = () => {
        const currentTime = audio.currentTime;
    
        // Loop through all text cues that should have been displayed by now
        while (onWord < textCues.length && currentTime >= textCues[onWord][0]) {
            const latestText = textCues[onWord][1];
            onWord++;
            if (latestText !== lastDisplayedText) {
                textDiv.textContent += " " + latestText;
                lastDisplayedText = latestText;
            }
        }
    };

    const checkAnswer = userAnswer => answer.toLocaleLowerCase().indexOf(userAnswer.toLocaleLowerCase());

    const calculateScore = correct => {
        if (correct != -1) {
            if (textDiv.textContent.indexOf('(*)') < 0) {
                inPower = true;
            }
            if (inPower) {
                score += 5;
            }
            score += 10;
        }
        else {
            if (!questionEnded)
                score -= 5;
        }
        console.log("Score: ", score);
        displayedScore.textContent = "Score: " + score;
    };            

    nextButton.addEventListener('click', async () => {
        const resetAndFetch = async () => {
            answerBox.style.display = 'none';
            textInput.style.display = 'none';
            audio.pause();
            audio.currentTime = 0;
            lastDisplayedText = '';
            textDiv.textContent = '';
            textInput.value = "";
            textCues = [];
            onWord = 0;
            const audioSource = document.getElementById('audioSource');
            const audioUrl = audioSource.getAttribute('src');
            audioSource.src = `${audioUrl}?t=${new Date().getTime()}`;
            audio.load();
            await fetchTextCues();
            fetchAnswer();
            audio.play();
            questionEnded = false;
            questionDone = false;
            buzzedIn = false;
            interrupt = false;
            inPower = 0;
            intervalId = setInterval(updateText, 100);
        };

        try {
            questionLoaded = false;

            clearInterval(intervalId);
            audio.pause();
            console.log("Question paused");
            await get_params();

            if (parametersChanged) {
                await get_next_question();
                resetAndFetch();
                get_next_question().then(
                resetAndFetch().then(
                        console.log("Finished fetching text")
                    )
                );
            }
            else {
                await get_next_question().then(
                resetAndFetch().then(
                    console.log("Finished fetching text")
                )
            );
            }

            questionLoaded = true;
        } catch (error) {
            console.error('Error fetching next question and answer:', error);
        }
    });

    buzzer.addEventListener('click', () => {
        buzzedIn = !buzzedIn;
        console.log("buzzedIn? ", buzzedIn);
        if (buzzedIn) {
        textInput.style.display = 'block';
        audio.pause();
        if (questionDone) {
            timer.pause();
            timerPaused = true;
        } else {
            interrupt = true;
        }
        } else {
            textInput.style.display = 'none';
            audio.play();
            setInterval(updateText, 100);
        }
    });

    document.addEventListener('keydown', event => {
        if (!buzzedIn && (event.key === 'n' || event.key === 'N')) {
            if (questionLoaded) nextButton.click();
            else alert("You cannot skip the question yet.");
        } else if (!questionEnded && !buzzedIn && event.key === ' ') {
            buzzer.click();
        } else if (buzzedIn && event.key === 'Enter') {
            console.log("test");
            const inputValue = textInput.value;
            const correct = checkAnswer(inputValue);
            calculateScore(correct);
            if (timerPaused) timer.resume();
            if (correct !== -1) {
                questionEnded = true;
                textDiv.textContent = textCues.map(row => row[1]).join(' ');
                audio.pause();
                answerDisplay.textContent = "Answer: " + answer;
                if (timer) timer.clear();
                answerRight.textContent = "I was incorrect";
                answerRight.classList.add('btn-outline-danger');
                audio.dispatchEvent(new Event('ended'));
            } else {
                textInput.style.display = 'none';
                audio.play();
                setInterval(updateText, 100);
                textInput.value = "";
                // answerRight.textContent = "I was correct";
                // answerRight.classList.add('btn-outline-success');
            }
        }
    });

    audio.addEventListener('ended', () => {
        questionDone = true;
        answerDisplay.textContent = "Answer: " + answer;
        clearInterval(updateText);
        // answerRight.textContent = "I was correct";
        // answerRight.classList.add('btn-outline-success');
        if (!questionEnded) {
            timer = new Timer(() => {
                answerBox.style.display = 'block';
                questionEnded = true;
            }, 5000);
        } else {
            answerBox.style.display = 'block';
        }
    });

    answerRight.addEventListener('click', () => {
        const wasCorrect = answerRight.textContent === "I was incorrect";
        score += wasCorrect ? (inPower ? -15 : -10) : (inPower ? 15 : 10);
        if (interrupt) score += wasCorrect ? -5 : 5;
        displayedScore.textContent = "Score: " + score;
        answerRight.textContent = wasCorrect ? "I was correct" : "I was incorrect";
        if (wasCorrect) {
            answerRight.classList.remove('btn-outline-success');
            answerRight.classList.add('btn-outline-danger');
        }
        else {
            answerRight.classList.remove('btn-outline-danger');
            answerRight.classList.add('btn-outline-success');
        }
    });
});