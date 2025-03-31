/**
 * @jest-environment jsdom (npx jest)
 */
const { postReply, loadReplies } = require('../discussionboard/discussion.js');


function flushPromises() {
  return new Promise(resolve => setTimeout(resolve, 0));
}

beforeEach(() => {
  document.body.innerHTML = `
    <textarea id="replyText"></textarea>
    <div id="repliesContainer"></div>
  `;
  global.fetch = jest.fn();
});

test("should not post an empty reply", async () => {
  document.getElementById("replyText").value = "";

  const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {});
  await postReply("Definitely LeetCode and HackerRank");

  expect(alertMock).toHaveBeenCalledWith("Reply cannot be empty!");
  alertMock.mockRestore();
});

test("should post valid reply and reload replies", async () => {
  document.getElementById("replyText").value = "This is a test reply";

  // 1st: post the reply
  fetch.mockResolvedValueOnce({
    json: () => Promise.resolve({ success: true })
  });

  // 2nd: get replies after posting
  fetch.mockResolvedValueOnce({
    json: () => Promise.resolve([])
  });

  await postReply("123");
  await flushPromises();

  expect(fetch).toHaveBeenCalledWith("/post_reply.php", expect.any(Object));
  expect(document.getElementById("replyText").value).toBe("");
});
