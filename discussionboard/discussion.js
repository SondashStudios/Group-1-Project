document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get("id");

    if (!questionId) {
        document.getElementById("questionTitle").innerText = "Invalid Question ID";
        return;
    }

    fetch(`get_question.php?id=${questionId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("questionTitle").innerText = data.error ? "Invalid Question ID" : data.title;
        })
        .catch(error => console.error("Error fetching question:", error));

    loadReplies();

    document.getElementById("replyForm").addEventListener("submit", function (e) {
        e.preventDefault();
        postReply(questionId);
    });
});

function getLoggedInUserFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("user") || "Anonymous";
}

function loadReplies() {
    const questionId = new URLSearchParams(window.location.search).get("id");

    fetch(`get_replies.php?id=${questionId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("repliesContainer");
            container.innerHTML = data.length === 0
                ? "<p>No replies yet. Be the first to respond!</p>"
                : "";
            data.forEach(reply => {
                container.appendChild(createReplyElement(reply));
            });
        })
        .catch(error => console.error("Error loading replies:", error));
}

function createReplyElement(reply, level = 0) {
    const replyDiv = document.createElement("div");
    replyDiv.classList.add("reply");
    replyDiv.style.marginLeft = `${level * 20}px`;

    replyDiv.innerHTML = `
        <div class="reply-header">
            <span class="reply-username">${reply.username}</span>
            <small class="reply-time">(${reply.created_at})</small>
        </div>
        <p class="reply-content">${reply.reply}</p>
    `;

    const replyButton = document.createElement("button");
    replyButton.textContent = "Reply";
    replyButton.classList.add("reply-btn");

    replyButton.addEventListener("click", () => {
        replyButton.disabled = true;

        const form = document.createElement("form");
        form.innerHTML = `
            <textarea required placeholder="Write a reply..."></textarea>
            <button type="submit">Post</button>
            <button type="button" class="cancel-btn">Cancel</button>
        `;

        form.querySelector(".cancel-btn").addEventListener("click", () => {
            form.remove();
            replyButton.disabled = false;
        });

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const replyText = form.querySelector("textarea").value.trim();
            if (!replyText) {
                alert("Reply cannot be empty!");
                return;
            }
            const questionId = new URLSearchParams(window.location.search).get("id");
            postReply(questionId, reply.id, replyText);
        });

        replyDiv.appendChild(form);
    });

    replyDiv.appendChild(replyButton);

    if (reply.children && reply.children.length > 0) {
        reply.children.forEach(child => {
            replyDiv.appendChild(createReplyElement(child, level + 1));
        });
    }

    return replyDiv;
}

function postReply(questionId, parentId = null, replyOverride = null) {
    const replyInput = replyOverride ? { value: replyOverride } : document.getElementById("replyText");
    const replyText = replyInput.value.trim();
    if (!replyText) return alert("Reply cannot be empty!");

    const formData = new URLSearchParams();
    formData.append("question_id", questionId);
    formData.append("reply", replyText);
    formData.append("username", getLoggedInUserFromURL());
    if (parentId) formData.append("parent_id", parentId);

    fetch("post_reply.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString()
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (!replyOverride) replyInput.value = "";
                loadReplies();
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
}

if (typeof module !== "undefined") {
    module.exports = { postReply, loadReplies };
}
