function submitAnswers() {
    const submitButton = document.querySelector('button[type="button"]');
    submitButton.disabled = true; 

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
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = `
                <p> You got ${data.correct.length} out of 3 questions correct.</p>
                <p> Correct: ${data.correct.join(', ')}</p>
            `;

            const correctAnswersDiv = document.createElement('div');
            correctAnswersDiv.innerHTML = `
                <h3>Correct Answers:${data.answers.q1}, ${data.answers.q2}, ${data.answers.q3}</h3>
            `;
            resultDiv.appendChild(correctAnswersDiv);

            // form.reset(); 
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while submitting the answers.');
        })
        .finally(() => {
            submitButton.disabled = false;
        });
}
