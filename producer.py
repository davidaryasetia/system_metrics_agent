import os
import json
import time
import psutil
from dotenv import load_dotenv
from kafka import KafkaProducer
import socketio
import time 
import urllib3

# Load .env
load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")
EMIT_INTERVAL = float(os.getenv("EMIT_INTERVAL_EVERY_SECONDS"))
SOCKETIO_SERVER = os.getenv("SOCKETIO_SERVER", "http://localhost:5000")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Socket.IO client
sio = socketio.Client()
connected = False

while not connected:
    try:
        print("Connecting to SocketIO server...")
        sio.connect(SOCKETIO_SERVER) 
        connected = True
        print("Connected to SocketIO Server ✅")
    except (socketio.exceptions.ConnectionError, urllib3.exceptions.NewConnectionError) as e:
        print(f"Connection failed: {e}. Retrying in 5 seconds...")
        time.sleep(5)

print("Connected to SocketIO server ✔")

def get_cpu_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.3),
        "cpu_count": psutil.cpu_count(),
        "load_avg": psutil.getloadavg(),
        "memory_percent": psutil.virtual_memory().percent,
        "timestamp": time.time(),
    }

if __name__ == "__main__":
    print("Starting CPU metrics producer...")

    while True:
        data = get_cpu_metrics()
        print("Metrics data")
        # Send to Kafka
        producer.send(TOPIC, data)
        producer.flush()

        # Emit to Socket.io realtime
        sio.emit("cpu_data", data)

        print("Sent:", data)
        time.sleep(EMIT_INTERVAL)
