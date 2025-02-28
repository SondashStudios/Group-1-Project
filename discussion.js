document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get("id");

    if (!questionId) {
        document.getElementById("questionTitle").innerText = "Invalid Question ID";
        return;
    }

    fetch(`/get_question.php?id=${questionId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("questionTitle").innerText = data.title;
        });

    loadReplies();

    document.getElementById("postReplyBtn").addEventListener("click", function () {
        postReply(questionId);
    });
});

// Function to load replies
function loadReplies() {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get("id");

    fetch(`/get_replies.php?id=${questionId}`)
        .then(response => response.json())
        .then(replies => {
            const repliesContainer = document.getElementById("repliesContainer");
            repliesContainer.innerHTML = "";
            replies.forEach(reply => {
                const replyElement = createReplyElement(reply);
                repliesContainer.appendChild(replyElement);
            });
        });
}

// Function to create a reply element with indentation
function createReplyElement(reply, depth = 0) {
    const replyDiv = document.createElement("div");
    replyDiv.classList.add("reply");
    replyDiv.style.marginLeft = `${depth * 30}px`; // Indent replies
    replyDiv.innerHTML = `
        <div class="reply-header">
            <span class="reply-username">User</span> 
            <small class="reply-time">(${reply.created_at})</small>
        </div>
        <p class="reply-content">${reply.reply}</p>
        <button class="reply-btn" data-id="${reply.id}">Reply</button>
        <div id="reply-box-${reply.id}" class="nested-reply-box"></div>
        <div class="nested-replies"></div>
    `;

    // Handle nested replies
    if (reply.children && reply.children.length > 0) {
        const nestedContainer = replyDiv.querySelector(".nested-replies");
        reply.children.forEach(childReply => {
            nestedContainer.appendChild(createReplyElement(childReply, depth + 1));
        });
    }

    // Attach event listener for reply button
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

// Function to post a reply (Handles both main & nested replies)
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
    if (parentId) {
        formData.append("parent_id", parentId);
    }

    fetch("/post_reply.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            replyInput.value = ""; 
            if (parentId) {
                document.getElementById(`reply-box-${parentId}`).innerHTML = "";
            }
            loadReplies(); // Refresh replies dynamically
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Function to close the reply box on cancel
function cancelReply(parentId) {
    const replyBox = document.getElementById(`reply-box-${parentId}`);
    if (replyBox) replyBox.innerHTML = "";
}
