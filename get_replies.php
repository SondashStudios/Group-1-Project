<?php
include 'db_connect.php';

$question_id = isset($_GET['id']) ? intval($_GET['id']) : 0;

// Fetch all replies for the given question
$stmt = $conn->prepare("SELECT id, reply, created_at, parent_id FROM replies WHERE question_id = ? ORDER BY created_at ASC");
$stmt->bind_param("i", $question_id);
$stmt->execute();
$result = $stmt->get_result();

// Organize replies into a tree structure
$replies = [];
$replyMap = [];

while ($row = $result->fetch_assoc()) {
    $row["created_at"] = date("h:i A - M d, Y", strtotime($row["created_at"])); // Format time
    $row["children"] = []; // Initialize children array
    $replyMap[$row["id"]] = $row; // Store reference to each reply
}

// Nest replies under their respective parent_id
foreach ($replyMap as $id => &$reply) {
    if ($reply["parent_id"] !== null && isset($replyMap[$reply["parent_id"]])) {
        $replyMap[$reply["parent_id"]]["children"][] = &$reply;
    } else {
        $replies[] = &$reply; // Top-level replies
    }
}

// Send JSON response
echo json_encode(array_values($replies));

$stmt->close();
$conn->close();
?>
