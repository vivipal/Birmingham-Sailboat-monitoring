<?php

$username="";
$password="";
$database="";
$hostname="localhost";


$conn = mysqli_connect($hostname, $username, $password, $database);

// Check connection

if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}



?>
