function generateResponse() {
    var prompt = document.getElementById('prompt').value;
    var form = new FormData();
    form.append('prompt', prompt);

    fetch('/generate', {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.choices[0].text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}