// Get the current date in the format "yyyy-mm-dd"
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
var yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;

// Set the min attribute of the input field to today
document.getElementById("check_out").min = today;