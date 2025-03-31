<?php
include 'db_connect.php';

$question_id = isset($_GET['id']) ? intval($_GET['id']) : null;

if (!$question_id) {
    echo json_encode(["error" => "No question ID provided"]);
    exit;
}

$stmt = $conn->prepare("SELECT title FROM questions WHERE id = ?");
$stmt->bind_param("i", $question_id);
$stmt->execute();
$result = $stmt->get_result();

if ($row = $result->fetch_assoc()) {
    echo json_encode($row);
} else {
    echo json_encode(["error" => "Question not found"]);
}

$stmt->close();
$conn->close();
?>
