// Author: Theo Smith
// The webpage after the user has finished the minigame in gameover.html

// Retrieve the scores from localStorage
document.getElementById('current-score').textContent = localStorage.getItem('currentScore');

let bestScore = localStorage.getItem('bestScore');
bestScore === null  ? 0 : document.getElementById('best-score').textContent = localStorage.getItem('bestScore');

const restartGame = () => {
    // Clear stored scores and redirect back to the main game page
    localStorage.removeItem('currentScore');
    window.location.href = backtohomepage;
};

