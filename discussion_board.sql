CREATE DATABASE discussion_board;
USE discussion_board;

-- Questions table 
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Replies table 
CREATE TABLE replies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    reply TEXT NOT NULL,
    parent_id INT DEFAULT NULL,
    username VARCHAR(255) NOT NULL DEFAULT 'Anonymous',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES replies(id) ON DELETE CASCADE
);
