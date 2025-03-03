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

// Function to create a reply element (No nesting)
function createReplyElement(reply) {
    const replyDiv = document.createElement("div");
    replyDiv.classList.add("reply");

    replyDiv.innerHTML = `
        <div class="reply-header">
            <span class="reply-username">User</span> 
            <small class="reply-time">(${reply.created_at})</small>
        </div>
        <p class="reply-content">${reply.reply}</p>
        <button class="reply-btn" data-id="${reply.id}">Reply</button>
        <div id="reply-box-${reply.id}" class="nested-reply-box"></div>
    `;

    // Attach event listener to the reply button
    replyDiv.querySelector(".reply-btn").addEventListener("click", function () {
        showReplyBox(reply.id);
    });

    return replyDiv;
}

// Function to show the reply input box
function showReplyBox(parentId) {
    const replyBox = document.getElementById(`reply-box-${parentId}`);
    if (replyBox.innerHTML.trim() !== "") return;

    replyBox.innerHTML = `
        <textarea id="reply-input-${parentId}" class="nested-reply-text" placeholder="Write a reply..."></textarea>
        <button class="submit-nested-reply" onclick="postReply(null, ${parentId})">Post Reply</button>
        <button class="cancel-nested-reply" onclick="cancelReply(${parentId})">Cancel</button>
    `;
}

// Function to post a reply (No nesting)
function postReply(questionId = null, parentId = null) {
    const replyInput = parentId
        ? document.getElementById(`reply-input-${parentId}`)
        : document.getElementById("replyText");

    const replyText = replyInput.value.trim();
    if (!replyText) {
        alert("Reply cannot be empty!");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("question_id", questionId || new URLSearchParams(window.location.search).get("id"));
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

// Function to cancel a reply
function cancelReply(parentId) {
    const replyBox = document.getElementById(`reply-box-${parentId}`);
    if (replyBox) replyBox.innerHTML = "";
}
