/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

// Setup before each test
beforeEach(() => {
  document.body.innerHTML = `<div id="repliesContainer"></div>`;
  localStorage.clear();

  global.window = Object.create(window);
  window.location = {
    search: "?user=testuser"
  };
});

// Load and evaluate discussion.js
const script = fs.readFileSync(
  path.resolve(__dirname, "../discussionboard/discussion.js"),
  "utf8"
);
eval(script);

describe("loadReplies", () => {
  test("renders replies correctly", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve([
            {
              id: 1,
              username: "Pritika",
              reply: "Test Reply",
              created_at: "2025-03-31",
              votes: 0,
              children: [],
            },
          ]),
      })
    );

    await loadReplies();
    await new Promise((r) => setTimeout(r, 50));

    const reply = document.querySelector(".reply");
    expect(reply).not.toBeNull();
    expect(reply.textContent).toMatch(/Pritika|Test Reply/);
  });

  test("clicking upvote increases vote count", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve([
            {
              id: 1,
              username: "TestUser",
              reply: "Vote Test",
              created_at: "2025-03-31",
              votes: 0,
              children: [],
            },
          ]),
      })
    );

    await loadReplies();
    await new Promise((r) => setTimeout(r, 50));

    const voteCount = document.querySelector(".vote-count");
    const upvoteBtn = document.querySelector(".upvote-btn");

    expect(voteCount.textContent).toBe("0");
    upvoteBtn.click();
    await new Promise((r) => setTimeout(r, 50));
    expect(parseInt(voteCount.textContent)).toBeGreaterThanOrEqual(1);
  });

  test("shows 3 votes if already voted", async () => {
    localStorage.setItem("voted-testuser-1", "up");
    localStorage.setItem("vote-count-1", "3");

    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve([
            {
              id: 1,
              username: "AlreadyVoted",
              reply: "Locked Vote",
              created_at: "2025-03-31",
              votes: 3,
              children: [],
            },
          ]),
      })
    );

    await loadReplies();
    await new Promise((r) => setTimeout(r, 100));

    const voteCount = document.querySelector(".vote-count");
    expect(voteCount.textContent).toBe("3");
  });
});
