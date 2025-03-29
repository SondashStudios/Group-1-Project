import { jest } from '@jest/globals';
import { postQuestion, loadQuestions } from '../discussionboard/main.js';

function flushPromises() {
  return new Promise(resolve => setTimeout(resolve, 0));
}

beforeEach(() => {
  document.body.innerHTML = `
    <input type="text" id="questionTitle" />
    <div id="questionsContainer"></div>
  `;
  global.fetch = jest.fn();
});

test("posts a question with valid input", async () => {
  document.getElementById("questionTitle").value = "What sites can be used to practice for technical interviews?";

  // Mock both the POST request and the follow-up question reload
  fetch.mockResolvedValueOnce({ text: () => Promise.resolve("OK") });
  fetch.mockResolvedValueOnce({ json: () => Promise.resolve([]) });

  await postQuestion();
  await flushPromises();

  expect(fetch).toHaveBeenCalledWith("post_question.php", expect.objectContaining({
    method: "POST",
  }));
});

test("shows message when no questions exist", async () => {
  fetch.mockResolvedValueOnce({ json: () => Promise.resolve([]) });

  await loadQuestions();
  await flushPromises();

  expect(document.getElementById("questionsContainer").innerHTML)
    .toContain("No questions yet");
});
