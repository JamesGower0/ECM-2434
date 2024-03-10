// Author: James Gower

// Checks the users location then checks if they're close to a quiz
function checkLocation(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
        (position) => {
            const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            };

            let quizLocaitons = [
                [50.73781086413985, -3.5369991064472885], //Sports Park
                [50.7375072917037, -3.5334938730196983], //Laver Building
                [50.7352855459596, -3.5333676503524343], //Forum Library
                [50.734399309503075, -3.5375457289062844], //Reed Pond
                [50.73764355152051, -3.527791142400209] //East Park
            ]

            for (let i = 0; i < quizLocaitons.length; i++){
                if (isInRadius(pos, quizLocaitons[i])){
                    let questionURL = "../qr/questions" + (i + 1);
                    window.open(questionURL);
                }
            }

        },

        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation.",
    );
    infoWindow.open(map);
}

// adjustable to set radius (in km)
// currently 100m
const radius = 0.1;

function degreesToRadians(degrees) {
    return degrees * Math.PI / 180;
}

function distanceInKmBetweenEarthCoordinates(lat1, lon1, lat2, lon2) {
    var earthRadiusKm = 6371;

    var dLat = degreesToRadians(lat2-lat1);
    var dLon = degreesToRadians(lon2-lon1);

    lat1 = degreesToRadians(lat1);
    lat2 = degreesToRadians(lat2);

    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    return earthRadiusKm * c;
}

// checks if the player is close to one of the quizes
function isInRadius(currentLocation, quizLocation) {
    const distance = distanceInKmBetweenEarthCoordinates(currentLocation.lat, currentLocation.lng, quizLocation[0], quizLocation[1]);
    const calculationResult = distance <= radius;
    return calculationResult;
}

checkLocation();