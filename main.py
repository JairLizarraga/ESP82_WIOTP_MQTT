from machine import unique_id,Pin
import network
import time
import ujson
from umqtt.robust import MQTTClient

#Entradas y salidas
led = Pin(16, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)

def WiFiConnect(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...', ssid)
      wlan.connect(ssid, password)
      wating_time = 0.0
      while not wlan.isconnected():
        wating_time += 0.5
        if(wating_time == 10.0):
          print(" Bad WiFi credentials for", ssid)
          return
        time.sleep_ms(500)
        print(".", end="")

  print()
  print('network config:', wlan.ifconfig())

def Conexion_MQTT_WIOTP(ORG, DEVICE_TYPE, DEVICE_ID, TOKEN):
    port_mqtt = 1883
    server = ORG + ".messaging.internetofthings.ibmcloud.com"
    
    #client_id = "a:31pdmc:app2"
    #username = "a-31pdmc-mo0bftwcxl"
    #token = "@r-vLX1x-i2UWNpfna"
    
    client_id = "d:" + ORG + ":" + DEVICE_TYPE + ":" + DEVICE_ID
    token = TOKEN
    username = "use-token-auth"
    
    client = MQTTClient(client_id, server,port_mqtt,username,token) 
    client.set_callback(callback)
    client.connect()
    return client
    
    
def callback(topic, msg):
  print(topic, msg)
  

publishTopic = "iot-2/evt/status/fmt/json"
responseTopic = "iotdm-1/response"
manageTopic = "iotdevice-1/mgmt/manage"
updateTopic = "iotdm-1/device/update"
rebootTopic = "iotdm-1/mgmt/initiate/device/reboot"

myTopic = "iot-2/cmd/interval/fmt/json"

WiFiConnect("MiKodaPlay", "Qu3nTocaP3ta")
mqttClient = Conexion_MQTT_WIOTP("31pdmc", "ESP8266", "ESP1", "password")

print("Suscribiendo...")
mqttClient.subscribe(myTopic)
print("Suscrito...")

count = 0
msg = ujson.dumps({"hey": "hola"})
while True:
  mqttClient.check_msg()
  time.sleep_ms(1000)
  
  
  print("Publishing: ", msg)
  mqttClient.publish(publishTopic, msg)
  print(".", end="")
  count += 1
  if(count >= 30):
    break
  
mqttClient.disconnect()