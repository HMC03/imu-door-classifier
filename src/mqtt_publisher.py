import time
import json
from pathlib import Path
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# Configuration for AWS IoT
ENDPOINT = "a23t95b48l3151-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "imu_door_publisher"
CERT_DIR = Path(__file__).parent.parent / "certs"
PATH_TO_CERT = CERT_DIR / "door-certificate.pem.crt"
PATH_TO_KEY = CERT_DIR / "door-private.pem.key"
PATH_TO_ROOT = CERT_DIR / "AmazonRootCA1.pem"
TOPIC = "door/status"

def connect_mqtt():
    """Create and return an AWS IoT MQTT connection."""
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=str(PATH_TO_CERT),
        pri_key_filepath=str(PATH_TO_KEY),
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30,
        ca_filepath=str(PATH_TO_ROOT)
    )
    print("Connecting to AWS IoT...")
    connect_future = mqtt_connection.connect()
    connect_future.result()  # Wait for connection
    print("Connected!")
    return mqtt_connection

def publish_door_state(mqtt_connection, state):
    """Publish door state to MQTT topic."""
    message = json.dumps({"door_state": state, "timestamp": time.time()})
    mqtt_connection.publish(
        topic=TOPIC,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print(f"Published: {message}")