<?php
/*
CREATE DATABASE `inn_ul` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `actual_inn_ul` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `inn` varchar(255) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `inn` (`inn`)
)  ENGINE=MyISAM;
*/

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "actual_inn_ul";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
$inn = $_REQUEST['inn'];
$sql = "REPLACE INTO actual_inn_ul (`inn`) VALUES ('$inn')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
