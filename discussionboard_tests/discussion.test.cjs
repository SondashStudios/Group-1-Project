/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

// Set up a clean DOM before each test
beforeEach(() => {
  document.body.innerHTML = `<div id="repliesContainer"></div>`;
  localStorage.clear(); // Clear vote history before each test
});

// Load the JS file you're testing
const script = fs.readFileSync(
  path.resolve(__dirname, "../discussionboard/discussion.js"),
  "utf8"
);
eval(script); // Injects all functions like loadReplies()

// Mock fetch to return nested replies
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve([
        {
          id: 1,
          username: "Pritika",
          reply: "Parent Reply",
          created_at: "2025-03-31",
          children: [
            {
              id: 2,
              username: "Noor",
              reply: "Nested Reply",
              created_at: "2025-03-31",
              children: [],
            },
          ],
        },
      ]),
  })
);

describe("loadReplies", () => {
  test("renders parent and nested replies correctly", async () => {
    await loadReplies();
    await new Promise((r) => setTimeout(r, 50));

    const replies = document.querySelectorAll(".reply");

    expect(replies.length).toBeGreaterThanOrEqual(2);
    expect(replies[0].textContent).toMatch(/Pritika|Parent Reply/);
    expect(replies[1].textContent).toMatch(/Noor|Nested Reply/);
  });

  test("upvoting increases vote count and disables buttons", async () => {
    await loadReplies();
    await new Promise((r) => setTimeout(r, 50));

    const upvoteBtn = document.querySelector(".upvote-btn");
    const downvoteBtn = document.querySelector(".downvote-btn");
    const voteCount = document.querySelector(".vote-count");

    expect(voteCount.textContent).toBe("0");

    upvoteBtn.click(); // Simulate vote

    expect(voteCount.textContent).toBe("1");
    expect(upvoteBtn.disabled).toBe(true);
    expect(downvoteBtn.disabled).toBe(true);
  });

  test("duplicate voting is blocked", async () => {
    // Pre-set vote in localStorage
    localStorage.setItem("voted-1", "up");
    localStorage.setItem("vote-count-1", "3");

    await loadReplies();
    await new Promise((r) => setTimeout(r, 50));

    const voteCount = document.querySelector(".vote-count");
    const upvoteBtn = document.querySelector(".upvote-btn");

    expect(voteCount.textContent).toBe("3");
    expect(upvoteBtn.disabled).toBe(true);
  });
});
