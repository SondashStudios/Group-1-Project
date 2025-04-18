<?php
include 'db_connect.php';

$question_id = $_POST['question_id'];
$reply = $_POST['reply'];
$parent_id = $_POST['parent_id'] ?? null;
$username = $_POST['username'] ?? 'Anonymous';

$sql = "INSERT INTO replies (question_id, reply, parent_id, username) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("isis", $question_id, $reply, $parent_id, $username);
$success = $stmt->execute();

echo json_encode(['success' => $success]);
?>
