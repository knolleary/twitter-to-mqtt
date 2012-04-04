Twitter to MQTT Publisher
=========================

A python daemon that uses the Twitter Streaming API to access tweets and republishes them to an MQTT topic.

Prerequisites
-------------

The daemon uses the Mosquitto Python client - http://mosquitto.org/

Configuration
-------------

Update settings.py with:
1. Your twitter username/password
2. The twitter streaming API url to use (see https://dev.twitter.com/docs/streaming-api)
3. The MQTT broker details and topic to publish to

Running
-------
To start the daemon, run:
    $ python twitter-to-mqtt.py

It can be stopped with Ctrl^C, but thanks to the way pycurl works, it will not exit until the next tweet is received. Alternatively, kill the process.


