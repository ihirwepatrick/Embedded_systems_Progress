<?php
// mqtt_listener.php

// Path to your mosquitto_sub binary (adjust as needed)
$broker = "157.173.101.159"; // MQTT Broker IP
$port = 1883; // MQTT Port (use 1883 for normal, or 9001 for WebSockets)
$topic_temperature = "/work_group_01/room_temp/temperature";
$topic_humidity = "/work_group_01/room_temp/humidity";

// Command to subscribe to the MQTT topics
$command = "mosquitto_sub -h $broker -p $port -t '$topic_temperature' -t '$topic_humidity'";

// Run the command and capture the output
exec($command, $output);

$db = new SQLite3('weather.db');

// Process the incoming messages
foreach ($output as $message) {
    // Check which topic the message is from
    if (strpos($message, 'temperature') !== false) {
        $temp = floatval(substr($message, strpos($message, ":") + 1));
        $db->exec("INSERT INTO weather_data (temperature, humidity) VALUES ($temp, 0)");
    } elseif (strpos($message, 'humidity') !== false) {
        $humidity = floatval(substr($message, strpos($message, ":") + 1));
        $db->exec("INSERT INTO weather_data (temperature, humidity) VALUES (0, $humidity)");
    }
}

echo "Data received and stored in database.";
?>
