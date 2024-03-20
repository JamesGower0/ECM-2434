// Author: James Gower
// Navigation bar for every page

function includeNavBar(navBarUrl) {
    // Get screen width using JavaScript
    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    // Check screen width and include nav bar accordingly
    if (screenWidth >= 1300) {
        // Include nav bar at the beginning of the body
        $.get(navBarUrl, function(data) {
            $('body').prepend(data);
        });
    } else {
        // Include nav bar at the end of the body
        $.get(navBarUrl, function(data) {
            $('body').append(data);
        });
    }
}

// Call the function when the DOM is ready
$(document).ready(function() {
    var navBarUrl = $('body').data('nav-url');
    includeNavBar(navBarUrl);
});