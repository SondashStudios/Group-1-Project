/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

// Load the HTML structure with a repliesContainer div
beforeEach(() => {
  document.body.innerHTML = `
    <div id="repliesContainer"></div>
  `;
});

// Load the JS file you're testing
const script = fs.readFileSync(path.resolve(__dirname, "../discussionboard/discussion.js"), "utf8");
eval(script); // Load your actual loadReplies() function into the test environment

// Mock fetch with nested replies
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
              children: []
            }
          ]
        }
      ])
  })
);

describe("loadReplies", () => {
  test("renders parent and nested replies correctly", async () => {
    await loadReplies();

    // Wait for DOM to update
    await new Promise((r) => setTimeout(r, 100));

    const replies = document.querySelectorAll(".reply");

    expect(replies.length).toBeGreaterThanOrEqual(2);
    expect(replies[0].textContent).toMatch(/Pritika|Parent Reply/);
    expect(replies[1].textContent).toMatch(/Noor|Nested Reply/);
  });
});
