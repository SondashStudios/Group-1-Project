<?php
include 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $question_id = $_POST['question_id'];
    $reply_text = $_POST['reply'];
    $parent_id = isset($_POST['parent_id']) ? $_POST['parent_id'] : NULL;

    if (empty($reply_text)) {
        echo json_encode(["error" => "Reply cannot be empty."]);
        exit;
    }

    $stmt = $conn->prepare("INSERT INTO replies (question_id, reply, parent_id) VALUES (?, ?, ?)");
    $stmt->bind_param("isi", $question_id, $reply_text, $parent_id);

    if ($stmt->execute()) {
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["error" => $stmt->error]);
    }

    $stmt->close();
    $conn->close();
}
?>
