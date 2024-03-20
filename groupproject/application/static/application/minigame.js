
// Selecting html elements and assign them variables
// Const keyword for wordText variable so value cannot be reassigned
const wordText = document.querySelector(".word"),
    hintText = document.querySelector(".hint span"),
    timeText = document.querySelector(".time b"),
    inputField = document.querySelector("input"),
    refreshBtn = document.querySelector(".refresh-word"),
    checkBtn = document.querySelector(".check-word");

// Variable to store best score
var bestScore;
// Check if bestscore is present in localstorage if not then set it to 0.
localStorage.getItem('bestScore') === null  ? bestScore = 0 : bestScore = localStorage.getItem('bestScore');
// declaring 3 variables, values assigned during game initilization
let correctWord, timer, currentScore = 0;

// Init time function takes a single parameter maxTime
const initTimer = maxTime => {
    clearInterval(timer);
    timer = setInterval(() => {
        if (maxTime > 0) {
            maxTime--;
            return timeText.innerText = maxTime;
        }
        displayGameOver();
    }, 1000);
}

const initGame = () => {
    console.log("Starting new round!");
    // Change visibility of elements on screen, once start-game button is pressed it then becomes invisisble
    // These variables are then shown
    document.getElementById('start-game').classList.add('invisible');
    document.getElementById('check-word').classList.remove('invisible');
    document.getElementById('details').classList.remove('invisible');
    document.getElementById('input-word').classList.remove('invisible');
    // 30 seconds passed as parameter to the initTimer function
    initTimer(30);
    // Generates a random index within range of valid indices for 'words array', array is declared in a seperate JS file
    let randomObj = words[Math.floor(Math.random() * words.length)];
    let wordArray = randomObj.word.split("");
    // Shuffling the letters of a randomly selected word
    for (let i = wordArray.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [wordArray[i], wordArray[j]] = [wordArray[j], wordArray[i]];
    }
    wordText.innerText = wordArray.join("");
    hintText.innerText = randomObj.hint;
    correctWord = randomObj.word.toLowerCase();
    inputField.value = "";
    inputField.setAttribute("maxlength", correctWord.length);
}

const checkWord = () => {
    let userWord = inputField.value.toLowerCase().trim();
    if (!userWord) return displayPopup("Please enter the word to check!");

    if (userWord !== correctWord) {
      displayPopup(`Oops! ${userWord} is not the correct word`);
      setTimeout(() => {
        displayGameOver();
      }, 1000); // Delay to show the "Oops" message
    } if(userWord == correctWord) {
      displayPopup(`Congrats! ${correctWord.toUpperCase()} is the correct word`);
      // Increment current score by 1
      currentScore ++;
      // Call updateScore method, responsible for setting current to best score if current> best
      updateScore();
      // After call initgame function to generate a new word
      initGame();
    }
  }

// Function to change the bestscore, if the currentscore exceeds bestscore
const displayGameOver = () => {
    if (currentScore > bestScore) {
        bestScore = currentScore;
        localStorage.setItem('bestScore', bestScore);
    }
    // Save the current score to local storage for the game-over page
    localStorage.setItem('currentScore', currentScore);
    // Redirect to the game-over page
    window.location.href = gameoverURL;
}

const updateScore = () => {
    localStorage.setItem('currentScore', currentScore);
    localStorage.setItem('bestScore', bestScore);
}

const displayPopup = message => {
    const popup = document.createElement("div");
    popup.className = "popup";
    popup.innerHTML = `<p>${message}</p>`;
    document.body.appendChild(popup);

    setTimeout(() => {
        popup.remove();
    }, 2000);
}


// Event listeners for checking words and starting the game
refreshBtn.addEventListener("click", initGame);
checkBtn.addEventListener("click", checkWord);
