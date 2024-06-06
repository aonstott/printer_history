function navigateToSelectedURL() {
    // Get the selected option from the dropdown
    var selectedOption = document.getElementById("timeframe").value;
    
    // Define the base URL
    var baseURL = "http://localhost:5000/"; // Replace with your base URL
    
    // Define the URLs for each option
    var urlMapping = {
        "last_day": "pages-day",
        "last_week": "pages-week",
        "last_month": "pages-month",
        "last_year": "pages-year"
        // Add more URL mappings as needed
    };
    
    // Navigate to the corresponding URL
    var selectedURL = baseURL + urlMapping[selectedOption];
    window.location.href = selectedURL;
}

function navigateToSelectedJamURL() {
    // Get the selected option from the dropdown
    var selectedOption = document.getElementById("timeframe").value;
    
    // Define the base URL
    var baseURL = "http://localhost:5000/"; // Replace with your base URL
    
    // Define the URLs for each option
    var urlMapping = {
        "all_time": "jams",
        "last_day": "jams-day",
        "last_week": "jams-week",
        "last_month": "jams-month",
        "last_year": "jams-year"
        // Add more URL mappings as needed
    };
    
    // Navigate to the corresponding URL
    var selectedURL = baseURL + urlMapping[selectedOption];
    window.location.href = selectedURL;
}

function runAway() {
    var button = document.getElementById('runaway-button');
    var maxX = window.innerWidth - button.offsetWidth;
    var maxY = window.innerHeight - button.offsetHeight;

    // Generate random position
    var newX = Math.floor(Math.random() * maxX);
    var newY = Math.floor(Math.random() * maxY);

    // Set new position
    button.style.left = newX + 'px';
    button.style.top = newY + 'px';
}