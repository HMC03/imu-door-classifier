import json
import time
from collections import deque
from pathlib import Path
from flask import Flask, render_template, Response
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# MQTT Config (update these to match your AWS IoT setup)
ENDPOINT = "a23t95b48l3151-ats.iot.us-east-2.amazonaws.com"  # Your AWS IoT endpoint
CLIENT_ID = "door_dashboard"  # Unique client ID for the dashboard
CERT_DIR = Path(__file__).parent.parent / "certs"
PATH_TO_CERT = CERT_DIR / "door-certificate.pem.crt"
PATH_TO_KEY = CERT_DIR / "door-private.pem.key"
PATH_TO_ROOT = CERT_DIR / "AmazonRootCA1.pem"
TOPIC = "door/status"

app = Flask(__name__)

# In-memory state
current_state = "unknown"
last_timestamp = None
event_log = deque(maxlen=5)  # Last 5 events

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    """Callback for MQTT messages."""
    global current_state, last_timestamp
    message = json.loads(payload)
    state = message.get("door_state")
    timestamp = message.get("timestamp")
    if state:
        current_state = state
        last_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        event_log.append(f"{last_timestamp}: Door {state}")
        print(f"Received update: {state} at {last_timestamp}")

# Set up MQTT connection
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=str(PATH_TO_CERT),
    pri_key_filepath=str(PATH_TO_KEY),
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30,
    ca_filepath=str(PATH_TO_ROOT)
)
connect_future = mqtt_connection.connect()
connect_future.result()
print("Dashboard MQTT connected!")

# Subscribe to topic
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_result = subscribe_future.result()
print(f"Subscribed to {TOPIC}")

@app.route("/")
def index():
    return render_template("index.html", state=current_state, timestamp=last_timestamp, log=list(event_log))

@app.route("/events")
def events():
    """SSE endpoint for real-time updates."""
    def generate():
        prev_state = current_state
        prev_log = list(event_log)
        while True:
            if current_state != prev_state or list(event_log) != prev_log:
                yield f"data: {json.dumps({'state': current_state, 'timestamp': last_timestamp, 'log': list(event_log)})}\n\n"
                prev_state = current_state
                prev_log = list(event_log)
            time.sleep(1)
    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)