# Pour atelier capteur CO2 Yoctopuce - Saint Pée sur Nivelle 2024
import os
import sys
import json
import time
import paho.mqtt.client as mqtt
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_carbondioxide import YCarbonDioxide
from yoctopuce.yocto_humidity import YHumidity
from yoctopuce.yocto_pressure import YPressure

# Initialize Yoctopuce API
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
  sys.exit(f"Initialization error: {errmsg.value}")

# Retrieve sensor objects
carbondioxide = YCarbonDioxide.FindCarbonDioxide("YCO2MK02-11E865.carbonDioxide")
humidity = YHumidity.FindSensor("YCO2MK02-11E865.humidity")
pressure = YPressure.FindSensor("YCO2MK02-11E865.pressure")

# Check if the module is online
if not carbondioxide.isOnline():
  sys.exit("Module not connected")

# MQTT configuration
broker_address = "127.0.0.1"
broker_port = 1883
mqtt_topic = "sensors/co2"
broker_name = "mosquitto"


client = mqtt.Client()
client.connect(broker_address, broker_port, 60)

try:
  while True:
    co2 = carbondioxide.get_currentValue()
    hum = humidity.get_currentValue()
    press = pressure.get_currentValue()

    payload = {
      "co2": co2,
      "humidity": hum,
      "pressure": press,
      "unit": "ppm"
    }

    client.publish(mqtt_topic, json.dumps(payload))
    print(f"Published {payload} to topic {mqtt_topic}")

    time.sleep(10)
except KeyboardInterrupt:
  client.disconnect()
  print("Bot stopped.")