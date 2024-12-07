document.getElementById("submit").addEventListener("click", async () => {
    const answers = document.getElementById("answers").value.split(",");
    const topN = document.getElementById("top-n").value;

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ answers, top_n: topN })
    });

    const predictions = await response.json();
    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "<h3>Predicted Answers:</h3>";
    Object.entries(predictions).forEach(([key, value]) => {
        resultsDiv.innerHTML += `<p>${key}: ${value}</p>`;
    });
});
