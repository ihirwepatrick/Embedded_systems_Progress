import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully!")
        client.subscribe("/i-gabriel/light_control")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    if command == "ON":
        print("Light is turned ON")
    elif command == "OFF":
        print("Light is turned OFF")
    else:
        print(f"Unknown command: {command}")

# Specify transport as "websockets"
client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect using only the host and port
    client.connect("157.173.101.159", 9001, 60)
    client.loop_forever()
except Exception as e:
    print(f"Failed to connect or error occurred: {e}")
except KeyboardInterrupt:
    print("Simulation stopped.")
