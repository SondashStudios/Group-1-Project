<?php
include 'db_connect.php';

$question_id = $_GET['id'];
$replies = [];

function fetchReplies($conn, $question_id, $parent_id = null) {
    $stmt = $conn->prepare("SELECT id, reply, parent_id, created_at, username FROM replies WHERE question_id = ? AND parent_id " . (is_null($parent_id) ? "IS NULL" : "= ?") . " ORDER BY created_at");
    if (is_null($parent_id)) {
        $stmt->bind_param("i", $question_id);
    } else {
        $stmt->bind_param("ii", $question_id, $parent_id);
    }
    $stmt->execute();
    $result = $stmt->get_result();
    $tree = [];

    while ($row = $result->fetch_assoc()) {
        $children = fetchReplies($conn, $question_id, $row['id']);
        $row['children'] = $children;
        $tree[] = $row;
    }

    return $tree;
}

$replies = fetchReplies($conn, $question_id);
echo json_encode($replies);
?>
