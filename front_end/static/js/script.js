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