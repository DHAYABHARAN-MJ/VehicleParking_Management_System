<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "vehicle_parking";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get filters from the frontend
$from_date = isset($_GET['from_date']) ? $_GET['from_date'] : '';
$to_date = isset($_GET['to_date']) ? $_GET['to_date'] : '';
$currently_parked = isset($_GET['currently_parked']) ? $_GET['currently_parked'] : 0;

// Build the base SQL query
$sql = "SELECT id, car_number, in_time, out_time, date, 
        TIMESTAMPDIFF(MINUTE, in_time, IFNULL(out_time, NOW())) AS total_time, 
        (TIMESTAMPDIFF(MINUTE, in_time, IFNULL(out_time, NOW())) * 5) AS cost 
        FROM parking_records WHERE 1=1";

// Apply date range filter if provided
if (!empty($from_date)) {
    $sql .= " AND date >= '$from_date'";
}
if (!empty($to_date)) {
    $sql .= " AND date <= '$to_date'";
}

// Apply currently parked filter if checked (out_time is NULL)
if ($currently_parked == 1) {
    $sql .= " AND out_time IS NULL";
}

// Execute the query
$result = $conn->query($sql);

$data = [];
if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

// Return the results as JSON
echo json_encode($data);

$conn->close();
?>
