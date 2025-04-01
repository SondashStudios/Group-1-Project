const { postQuestion, loadQuestions } = require("../discussionboard/main");

global.fetch = jest.fn(() =>
  Promise.resolve({
    text: () => Promise.resolve("success"),
    json: () => Promise.resolve([{ id: 1, title: "Test Question" }]),
  })
);

describe("postQuestion", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="questionTitle" value="New Question" />
      <div id="questionsContainer"></div>
    `;
    delete window.location;
    window.location = { search: "?user=Bugga" };
  });

  it("submits a question with a username from URL", async () => {
    await postQuestion();
    expect(fetch).toHaveBeenCalledWith(
      "post_question.php",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ title: "New Question", username: "Bugga" }),
      })
    );
  });
});
