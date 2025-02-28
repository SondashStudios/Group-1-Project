<?php
include 'db_connect.php';

$question_id = $_GET['id'] ?? 0;

$stmt = $conn->prepare("SELECT * FROM questions WHERE id = ?");
$stmt->bind_param("i", $question_id);
$stmt->execute();
$result = $stmt->get_result();
$question = $result->fetch_assoc();

if (!$question) {
    echo json_encode(["error" => "Question not found"]);
} else {
    echo json_encode($question);
}
$conn->close();
?>
