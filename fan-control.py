import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

def main():
    GPIO.setup()
    client = mqtt.Client()
    client.connect()
    client.subscribe()
    client.loop_start()

def on_receive():
    #filter by message type

