from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
SocketIO = SocketIO(app, cors_allowed_origins="*")

@SocketIO.on("cpu_data")
def cpu_data(data):
    SocketIO.emit("cpu_broadcast", data)

@app.get("/")
def home(): 
    return "Socket.IO Server is running"

if __name__ == "__main__":
    SocketIO.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)