import argparse
import atexit

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


def cleanup(client):
    GPIO.cleanup()
    print("Cleaning up")
    client.loop_stop()


# consider a topic that would affect all fans at once
# or eg tent1/fans/all tent1/fans/1 tent1/fans/2 etc
# tent1/allfans/status
def on_message(client, userdata, message):
    # tentX/fanY/status
    # look into how to subscribe since we'll need a few
    payload = message.payload
    place, device, metric = message.topic.split("/")
    pin = userdata[device]
    if payload == b"True":
        GPIO.output(pin, GPIO.LOW)
    elif payload == b"False":
        GPIO.output(pin, GPIO.HIGH)


def mqtt_connect(host, topics, userdata):
    client = mqtt.Client(userdata=userdata)
    client.connect(host, 1883)
    for topic in topics:
        client.subscribe(topic)
    return client


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, required=True, help="Hostname or IP of the MQTT broker"
    )
    parser.add_argument(
        "--gpio",
        type=int,
        nargs="+",
        required=True,
        help="List of integers representing GPIO pins",
    )
    parser.add_argument(
        "--topics",
        type=str,
        nargs="+",
        required=True,
        help="Topics for the script to publish to",
    )
    args = parser.parse_args()
    GPIO.setmode(GPIO.BCM)
    for pin in args.gpio:
        GPIO.setup(pin, GPIO.OUT)
    n_fans = len(args.gpio)

    userdata = {}
    for i, pin in enumerate(args.gpio):
        userdata[f"fan{i+1}"] = pin

    client = mqtt_connect(args.host, args.topics, userdata)
    client.on_message = on_message
    atexit.register(cleanup, client)
    client.loop_forever()
