import sys
import os
from awscrt import mqtt
from awsiot import mqtt_connection_builder
import time
import json
from dotenv import load_dotenv

load_dotenv(".env")

ENDPOINT = os.getenv("ENDPOINT")
TOPIC = "led/testpi"
CLIENT_ID = "receiver"

CERT = os.getenv("CERT_PATH")
KEY = os.getenv("PRIKEY_PATH")
ROOT = os.getenv("ROOT_PATH")

def on_connection_successful(connection):
    print("Connected to AWS IoT!")

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERT,
    pri_key_filepath=KEY,
    ca_filepath=ROOT,
    on_connection_interrupted=on_connection_interrupted,
    on_connection_resumed=on_connection_resumed,
    on_connection_successful=on_connection_successful,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=8
)

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("\n--- Message Received ---")
    print("Topic: {}".format(topic))
    msg = json.loads(payload)
    print("Device LED Status: {}".format(msg["status"]))
    print("--- End Message ---")

print("Connecting to {} with client '{}'...".format(ENDPOINT, CLIENT_ID))
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected Successfully!")

print("Subscribing to topic '{}'...".format(TOPIC))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_future.result()
print(f"Subscribed to: {TOPIC}\n")
print("Waiting for messages... (Press Ctrl+C to exit)\n")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDisconnecting from AWS...")

finally:
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
    sys.exit(0)