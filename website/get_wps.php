<?php

	header('Content-Type: application/json');
	header("Access-Control-Allow-Origin: *");

	// Connect to the database
	include("connect.php");

	// Read the record
	$sql = mysqli_query($conn,"SELECT lat,lon FROM waypoints ORDER BY id ASC;");
	$data = mysqli_fetch_all($sql, MYSQLI_NUM);

	$posArray = array();

	foreach($data as $row){
        	array_push($posArray, array('lat' => $row["0"],'lon' => $row["1"]));
	}

	mysqli_close($conn);

	print json_encode($posArray);
?>
