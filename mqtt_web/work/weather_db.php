<?php
// weather_db.php

// Connect to the SQLite database
$db = new SQLite3('weather.db');

// Create table if it doesn't exist
$db->exec('
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
');
?>
