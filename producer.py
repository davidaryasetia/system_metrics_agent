import os
import json
import time
import psutil
from dotenv import load_dotenv
from kafka import KafkaProducer
import socketio

# Load .env
load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")
EMIT_INTERVAL = float(os.getenv("EMIT_INTERVAL_SEC", 0.001))
SOCKETIO_SERVER = os.getenv("SOCKETIO_SERVER", "http://localhost:5000")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Socket.IO client (connect to internal realtime server)
sio = socketio.Client()

print("Connecting to SocketIO server...")
sio.connect(SOCKETIO_SERVER)  # Sesuaikan port jika beda
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

        # Send to Kafka
        producer.send(TOPIC, data)
        producer.flush()

        # Emit to Socket.io realtime
        sio.emit("cpu_data", data)

        print("Sent:", data)
        time.sleep(EMIT_INTERVAL)
