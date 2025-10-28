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
CLIENT_ID = "testpi"

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

print("Connecting to {} with client '{}'...".format(ENDPOINT, CLIENT_ID))
connect_future = mqtt_connection.connect()

connect_future.result()
print("Connected Successfully!")

try:
    led_status = False
    while True:
        led_status = not led_status
        if led_status:
            status = "ON"
        else:
            status = "OFF"

        message = {
            "status": status
        }

        publish_future, packet_id = mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(message),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

        print("Published message to topic '{}': {}".format(TOPIC, message))

        time.sleep(3)

except KeyboardInterrupt:
    print("Disconnecting from AWS...")

finally:
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
    sys.exit(0)


