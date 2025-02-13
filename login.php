<?php
// Database configuration
$servername = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "vehicle_parking";

// Establish a connection to the database
$conn = new mysqli($servername, $dbusername, $dbpassword, $dbname);

// Check if the connection was successful
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form is submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get the username and password from the form
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Prepare the SQL statement to prevent SQL injection
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();

    // Check if the credentials are correct
    if ($result->num_rows > 0) {
        // Redirect to main.html if login is successful
        header("Location: main.html");
        exit();
    } else {
        // Display an error message if login fails
        echo "<div class='error'>Invalid Credentials</div>";
    }

    // Close the statement and the connection
    $stmt->close();
    $conn->close();
}
?>
