document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get("id");

    if (!questionId) {
        document.getElementById("questionTitle").innerText = "Invalid Question ID";
        return;
    }

    // Fetch question title
    fetch(`/get_question.php?id=${questionId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("questionTitle").innerText = "Invalid Question ID";
            } else {
                document.getElementById("questionTitle").innerText = data.title;
            }
        })
        .catch(error => console.error("Error fetching question:", error));

    // Load replies
    loadReplies();

    document.getElementById("replyForm").addEventListener("submit", function (e) {
        e.preventDefault();
        postReply(questionId);
    });
});

// Function to load replies (Flat structure, No nesting)
function loadReplies() {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get("id");

    fetch(`/get_replies.php?id=${questionId}`)
        .then(response => response.json())
        .then(data => {
            const repliesContainer = document.getElementById("repliesContainer");
            repliesContainer.innerHTML = "";

            if (data.error) {
                repliesContainer.innerHTML = `<p>No replies yet. Be the first to respond!</p>`;
                return;
            }

            // Display all replies at the same level (no nesting)
            data.forEach(reply => {
                repliesContainer.appendChild(createReplyElement(reply));
            });
        })
        .catch(error => console.error("Error fetching replies:", error));
}

// Function to create a reply element (Reply button is visible but does nothing for now)
function createReplyElement(reply) {
    const replyDiv = document.createElement("div");
    replyDiv.classList.add("reply");

    replyDiv.innerHTML = `
        <div class="reply-header">
            <span class="reply-username">User</span> 
            <small class="reply-time">(${reply.created_at})</small>
        </div>
        <p class="reply-content">${reply.reply}</p>
    `;

    // Create and append the reply button (Does nothing for now)
    const replyButton = document.createElement("button");
    replyButton.classList.add("reply-btn");
    replyButton.setAttribute("data-id", reply.id);
    replyButton.textContent = "Reply";
    
    // Placeholder for future functionality
    replyButton.addEventListener("click", function () {
        console.log("Reply button clicked for reply ID:", reply.id);
    });

    replyDiv.appendChild(replyButton);
    
    return replyDiv;
}

// Function to post a reply (Only allows replies to the main question)
function postReply(questionId) {
    const replyInput = document.getElementById("replyText");
    const replyText = replyInput.value.trim();

    if (!replyText) {
        alert("Reply cannot be empty!");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("question_id", questionId);
    formData.append("reply", replyText);

    fetch("/post_reply.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            replyInput.value = ""; 
            loadReplies(); // Refresh replies dynamically
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}
