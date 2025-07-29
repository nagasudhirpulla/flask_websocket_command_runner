import socketio
import json
from pathlib import Path

appConf = json.loads(Path("secret", "config.json").read_text())

token = next(iter(appConf["clients"]))
cmdId = next(iter(appConf["commands"]))
serverUrl = "http://localhost:5000"

sio = socketio.Client()


@sio.event
def connect():
    print('✅ connection established')
    sio.emit('run_script', {"token": token, "cmdId": cmdId})


@sio.on('script_output')
def script_output(msg):
    print(msg['data'], end='')


@sio.on('script_exit')
def script_exit(msg):
    print(f'⚠️ exit msg received with {msg['exit_code']}')
    sio.disconnect()


@sio.event
def disconnect():
    print('❌ disconnected from server')

# Event handler for connection error


@sio.event
def connect_error(data):
    print("⚠️ Connection failed:", data)


if __name__ == "__main__":
    try:
        # Connect to the Flask-SocketIO server
        sio.connect(serverUrl)
        sio.wait()
    except Exception as e:
        print("❌ Could not connect:", e)
