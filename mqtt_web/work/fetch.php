<?php
// fetch_data.php

// Connect to SQLite database
$db = new SQLite3('weather.db');

// Fetch the latest data from the database (last 20 entries)
$result = $db->query('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 20');

// Store the data in an array
$data = [];
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $data[] = $row;
}

// Return the data as JSON
echo json_encode($data);
?>
