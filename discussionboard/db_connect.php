<?php
$servername = "localhost";
$username = "root"; // Change if needed
$password = "Pr1t1kaBugga123$"; // Change if needed
$dbname = "discussion_board";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
