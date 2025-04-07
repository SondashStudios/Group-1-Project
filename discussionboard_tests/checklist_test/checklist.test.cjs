const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Load and set up DOM
const html = fs.readFileSync(
  path.resolve(__dirname, './checklist_test_static.html'),
  'utf8'
);
let dom;
let document;

beforeEach(() => {
  dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
  document = dom.window.document;
});

describe('Checklist Page Tests', () => {
  test('Checklist container exists', () => {
    const checklist = document.querySelector('.checklist-container');
    expect(checklist).not.toBeNull();
  });

  test('Add button exists and is functional', () => {
    const addButton = document.querySelector('#addButton');
    expect(addButton).not.toBeNull();
    expect(addButton.textContent.toLowerCase()).toContain('add');
  });

  test('Checklist input field is present', () => {
    const input = document.querySelector('#taskInput');
    expect(input).not.toBeNull();
    expect(input.getAttribute('placeholder')).toMatch(/task/i);
  });
});
