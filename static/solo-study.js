document.addEventListener("DOMContentLoaded", function () {
    // Focus Mode Toggle
    const focusToggle = document.getElementById("focusToggle");
    const body = document.body;

    focusToggle.addEventListener("change", function () {
        if (this.checked) {
            body.classList.add("focus-mode-active");
        } else {
            body.classList.remove("focus-mode-active");
        }
    });

    // Pomodoro Timer
    let timer;
    let isRunning = false;
    let timeLeft = 25 * 60; // 25 minutes

    const timerDisplay = document.querySelector(".timer-display"); // Fixed selector
    const startButton = document.getElementById("start-timer");
    const pauseButton = document.getElementById("pause-timer");
    const resetButton = document.getElementById("reset-timer");

    function updateDisplay() {
        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }

    startButton.addEventListener("click", function () {
        if (!isRunning) {
            isRunning = true;
            timer = setInterval(() => {
                if (timeLeft > 0) {
                    timeLeft--;
                    updateDisplay();
                } else {
                    clearInterval(timer);
                    isRunning = false;
                    alert("Time's up!");
                }
            }, 1000);
        }
    });

    pauseButton.addEventListener("click", function () {
        clearInterval(timer);
        isRunning = false;
    });

    resetButton.addEventListener("click", function () {
        clearInterval(timer);
        isRunning = false;
        timeLeft = 25 * 60;
        updateDisplay();
    });

    updateDisplay(); // Initial display update

    // Study Music Player
    const musicSelect = document.getElementById("music-select");
    const playMusicButton = document.getElementById("play-music");
    let currentAudio = null;

    playMusicButton.addEventListener("click", function () {
        if (currentAudio) {
            currentAudio.pause();
            currentAudio = null;
            playMusicButton.textContent = "Play";
            return;
        }

        const selectedMusic = musicSelect.value;
        const musicFiles = {
            "lofi": "static/audios/lofi.mp3",
            "nature": "static/nature.mp3",
            "classical": "static/classical.mp3"
        };

        currentAudio = new Audio(musicFiles[selectedMusic]);
        currentAudio.loop = true;
        currentAudio.play();
        playMusicButton.textContent = "Pause";
    });

    // To-Do List Functionality
    const todoInput = document.getElementById("todo-input");
    const addTaskButton = document.getElementById("add-task");
    const todoList = document.getElementById("todo-items");

    addTaskButton.addEventListener("click", function () {
        const taskText = todoInput.value.trim();
        if (taskText === "") return;

        const listItem = document.createElement("li");
        listItem.innerHTML = `${taskText} <button class="delete-task">X</button>`;
        todoList.appendChild(listItem);

        listItem.querySelector(".delete-task").addEventListener("click", function () {
            listItem.remove();
        });

        todoInput.value = "";
    });

    // Notepad Save Functionality
    const noteArea = document.getElementById("note-area");
    const saveNoteButton = document.getElementById("save-note");

    saveNoteButton.addEventListener("click", function () {
        localStorage.setItem("savedNote", noteArea.value);
    });

    // Load Saved Note on Page Load
    if (localStorage.getItem("savedNote")) {
        noteArea.value = localStorage.getItem("savedNote");
    }
});
