#!/usr/bin/env python
import os, pycurl, json, StringIO, threading

import mosquitto
import settings

class TwitterStreamClient:
  def __init__(self):
    self.buffer = ""
    self.shutdown = False
    self.client = mosquitto.Mosquitto("TwitterFeed_%s"%(os.urandom(4).encode("hex"),))
    self.client.on_connect = self.onmqttconnect
    self.client.connect(settings.MQTT_HOST,settings.MQTT_PORT,keepalive=60)
    try:
      while True:
        self.client.loop(1000)
    except:
      self.client.disconnect()
      self.shutdown = True;
    
  def onmqttconnect(self,client,obj,rc):
    if rc == 0:
      self.streamthread = threading.Thread(target=self.startstream)
      self.streamthread.start()

  def startstream(self):
    self.conn = pycurl.Curl()
    self.conn.setopt(pycurl.USERPWD, "%s:%s" % (settings.TWITTER_USER, settings.TWITTER_PASS))
    self.conn.setopt(pycurl.URL, settings.TWITTER_STREAM_URL)
    self.conn.setopt(pycurl.WRITEFUNCTION, self.onstreamreceive)
    self.conn.perform()
    
  
  def onstreamreceive(self, data):
    self.buffer += data
    if data.endswith("\r\n") and self.buffer.strip():
      self.client.publish(settings.MQTT_TOPIC,self.buffer)
      self.buffer = ""
    if self.shutdown:
      return 0
      
client = TwitterStreamClient()

