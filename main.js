document.addEventListener("DOMContentLoaded", () => {
    loadQuestions();

    document.getElementById("questionForm").addEventListener("submit", function(e) {
        e.preventDefault();
        postQuestion();
    });
});

// Fetch questions from database
function loadQuestions() {
    fetch("get_questions.php")
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById("questionsContainer");
        container.innerHTML = "";
        if (data.length === 0) {
            container.innerHTML = "<p>No questions yet. Be the first to ask!</p>";
        } else {
            data.forEach(q => {
                const div = document.createElement("div");
                div.innerHTML = `<p><a href="discussion.html?id=${q.id}">${q.title}</a></p>`;
                container.appendChild(div);
            });
        }
    });
}

// Post a new question
function postQuestion() {
    const title = document.getElementById("questionTitle").value;

    fetch("post_question.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title })
    })
    .then(response => response.text())
    .then(() => {
        document.getElementById("questionTitle").value = "";
        loadQuestions(); // Refresh list
    });
}
