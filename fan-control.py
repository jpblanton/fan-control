import argparse
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# what to put in main() and what to spread out
# wrapper for changing fan settings?
# also, HIGH is off and LOW and is on
def main(pins, topic, host):
    GPIO.setmode(GPIO.BCM)
    for n in pins:
        GPIO.setup(n, GPIO.OUT)

def on_message(client, userdata, message):
    #tentX/fanY/status
    # look into how to subscribe since we'll need a few

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpio', type=int, nargs='+', required=True, help='List of integers representing GPIO pins')
    parser.add_argument('--topic', type=str, required=True, help='Topic for the script to publish to')
    parser.add_argument('--host', type=str, required=True, help='Hostname or IP of the MQTT broker')
    args = parser.parse_args()

    n_fans = len(args.gpio)
    
    client = mqtt.Client()
    client.connect(args.host, 1883)
    client.subscribe(args.topic)
    client.loop_start()