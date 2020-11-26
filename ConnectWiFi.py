def WiFiConnect(ssid, password):
  wlan = WLAN(STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...', ssid)
      wlan.connect(ssid, password)
      wating_time = 0
      while not wlan.isconnected():
        print(".", end="")
        time.sleep_ms(1000)
        wating_time += 1
        if(wating_time == 20):
          print(" Bad WiFi credentials for", ssid)
          return
  print()
  print('network config:', wlan.ifconfig()[0])

