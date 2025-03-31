document.addEventListener("DOMContentLoaded", () => {
    loadQuestions();

    document.getElementById("questionForm").addEventListener("submit", function (e) {
        e.preventDefault();
        postQuestion();
    });
});

function getLoggedInUserFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("user") || "Anonymous";
}

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
                    div.innerHTML = `<p><a href="discussion.html?id=${q.id}&user=${getLoggedInUserFromURL()}">${q.title}</a></p>`;
                    container.appendChild(div);
                });
            }
        })
        .catch(error => console.error("Error loading questions:", error));
}

function postQuestion() {
    const title = document.getElementById("questionTitle").value;

    fetch("post_question.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title, username: getLoggedInUserFromURL() })
    })
    .then(response => response.text())
    .then(() => {
        document.getElementById("questionTitle").value = "";
        loadQuestions();
    });
}

if (typeof module !== "undefined") {
    module.exports = { postQuestion, loadQuestions };
}
