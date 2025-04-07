<?php
include 'db_connect.php';

// Get raw JSON input
$data = json_decode(file_get_contents("php://input"), true);

// Validate input
if (!isset($data['title']) || empty($data['title'])) {
    echo json_encode(["status" => "error", "message" => "Question title is required."]);
    exit;
}

$title = $data['title'];

$stmt = $conn->prepare("INSERT INTO questions (title) VALUES (?)");
$stmt->bind_param("s", $title);

if ($stmt->execute()) {
    echo json_encode(["status" => "success", "message" => "Question added."]);
} else {
    echo json_encode(["status" => "error", "message" => "Database error."]);
}

$stmt->close();
$conn->close();
?>