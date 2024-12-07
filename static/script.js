function submitAnswers() {
    const form = document.getElementById('qa-form');
    const formData = new FormData(form);

    const answers = {};
    for (let [key, value] of formData.entries()) {
        answers[key] = value;
    }

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers }),
    })
        .then((response) => response.json())
        .then((data) => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<p>Correct: ${data.correct.join(', ')}</p>
                                   <p>Wrong: ${data.wrong.join(', ')}</p>`;
        })
        .catch((error) => console.error('Error:', error));
}
