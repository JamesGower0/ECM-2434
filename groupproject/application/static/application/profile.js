// Author: Maryia Fralova
// Displays either inventory or metrics in profile.html


// Displaying inventory or metrics
document.addEventListener("DOMContentLoaded", function() {
    // Button to toggle inventory visibility
    var invButton = document.getElementById("inv-btn");
    // Button to toggle metrics visibility
    var metButton = document.getElementById("met-btn");

    // Div containing inventory items
    var inventoryDiv = document.getElementById("inventory");
    // Div containing metrics
    var metricsDiv = document.getElementById("metrics");

    // Add event listener for inventory button
    invButton.addEventListener("click", function() {
        // Show inventory and hide metrics
        inventoryDiv.style.display = "grid";
        metricsDiv.style.display = "none";
    });

    // Add event listener for metrics button
    metButton.addEventListener("click", function() {
        // Show metrics and hide inventory
        metricsDiv.style.display = "grid";
        inventoryDiv.style.display = "none";
    });
});


// Putting an accessory on


// Changing the bird

