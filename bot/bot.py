import paho.mqtt.client as mqtt
import json
import time
import os
import random

mqtt_broker = os.getenv('MQTT_BROKER', 'mosquitto')
mqtt_port = int(os.getenv('MQTT_PORT', 1883))
mqtt_topic = os.getenv('MQTT_TOPIC', 'sensors/temperature')

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)

try:
    while True:
        base_value = 20
        variation = random.uniform(-1, 1)
        payload = {
            "value": base_value + variation,
            "unit": "C"
        }
        client.publish(mqtt_topic, json.dumps(payload))
        print(f"Published {payload} to topic {mqtt_topic}")
        time.sleep(10)
except KeyboardInterrupt:
    client.disconnect()
    print("Bot stopped.")

