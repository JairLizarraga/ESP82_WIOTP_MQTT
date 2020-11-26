from machine import Pin
from network import WLAN, STA_IF
from time import sleep_ms
from umqtt.robust import MQTTClient
import ujson

ledTopic = "iot-2/cmd/led/fmt/json"
publishTopic = "iot-2/evt/status/fmt/json"
responseTopic = "iotdm-1/response"
manageTopic = "iotdevice-1/mgmt/manage"
updateTopic = "iotdm-1/device/update"
rebootTopic = "iotdm-1/mgmt/initiate/device/reboot"

#led = Pin(16, Pin.OUT)
led =Pin(2,Pin.OUT) 
button = Pin(5, Pin.IN, Pin.PULL_UP)

def connectWiFi(ssid, password, timeout = 20):
  wlan = WLAN(STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...', ssid)
      wlan.connect(ssid, password)
      wating_time = 0
      while not wlan.isconnected():
        print(".", end="")
        sleep_ms(1000)
        wating_time += 1
        if(wating_time == timeout):
          print(" Bad WiFi credentials for", ssid)
          return
  print()
  print('network config:', wlan.ifconfig()[0])
    
def Conexion_MQTT_WIOTP(ORG, DEVICE_TYPE, DEVICE_ID, TOKEN):
    port_mqtt = 1883
    server = ORG + ".messaging.internetofthings.ibmcloud.com"
    client_id = "d:" + ORG + ":" + DEVICE_TYPE + ":" + DEVICE_ID
    token = TOKEN
    username = "use-token-auth"
    client = MQTTClient(client_id, server,port_mqtt,username,token) 
    client.set_callback(callback)
    client.connect()
    return client
    
    
def callback(topic, msg):
  if(topic.decode("utf-8") == ledTopic):
    msg = msg.decode("utf-8")
    response = {}
    if(msg == "0"):
      print("off")
      response["led_status"] = "off"
      led.value(1)
    elif(msg == "1"):
      print("on")
      response["led_status"] = "on"
      led.value(0)
    else:
      print("nope")
    mqttClient.publish(publishTopic, ujson.dumps(response))
  



connectWiFi("MiKodaPlay", "Qu3nTocaP3ta")
mqttClient = Conexion_MQTT_WIOTP("31pdmc", "ESP8266", "ESP1", "password")
mqttClient.subscribe(ledTopic)

count = 0
msg = ujson.dumps({"hey": "hola"})
while True:
  mqttClient.check_msg()
  sleep_ms(100)
  
mqttClient.disconnect()







