import os,sys
from yoctopuce.yocto_api import *
from yoctopuce.yocto_carbondioxide import *
from time import sleep


# Initialize influxdb client
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = os.getenv("INFLUX_TOKEN")
org = "rechercher_peyote_0h@icloud.com"
bucket = "CO2bucket"



# On active la détection des modules sur USB
errmsg=YRefParam()
YAPI.RegisterHub("usb",errmsg)

for time in range(0,1000):
  print(time)
  # On récupère l'objet permettant d'intéragir avec le module
  carbondioxide = YCarbonDioxide.FindCarbonDioxide("YCO2MK02-11E865.carbonDioxide")
  humidity = YSensor.FindSensor("YCO2MK02-11E865.humidity")
  pressure = YSensor.FindSensor("YCO2MK02-11E865.pressure")

    # Pour gérer le hot-plug, on vérifie que le module est là
  if carbondioxide.isOnline():
  # use carbondioxide.get_currentValue() [...]
    co2 = carbondioxide.get_currentValue()
    hum = humidity.get_currentValue()
    press = pressure.get_currentValue()

  # write to influx DB
  with InfluxDBClient(url="https://europe-west1-1.gcp.cloud2.influxdata.com", token=token,
                      org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("Yoctopuce") \
      .tag("Yocto", "Yocto1") \
      .field("co2", co2) \
      .field("humidity", hum) \
      .field("pressure", press) \
      .time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(bucket, org, point)

  sleep(10)

client.close()
