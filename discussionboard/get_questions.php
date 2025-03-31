<?php
include 'db_connect.php';

$result = $conn->query("SELECT id, title FROM questions ORDER BY created_at DESC");

$questions = [];
while ($row = $result->fetch_assoc()) {
    $questions[] = $row;
}

echo json_encode($questions);
$conn->close();
?>