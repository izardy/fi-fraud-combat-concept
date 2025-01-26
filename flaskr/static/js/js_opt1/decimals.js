// Select all elements with the class 'decimal-cell' and round the content to 2 decimal places
document.querySelectorAll('.decimal-cell').forEach(function(cell) {
    var originalContent = cell.textContent;
    var roundedContent = parseFloat(originalContent).toFixed(2); // Round to 2 decimal places
    cell.textContent = roundedContent;
});
