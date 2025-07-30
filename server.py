from flask import Flask
from flask_socketio import SocketIO, emit, disconnect
import subprocess
import json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
appConf = json.loads(Path("secret", "config.json").read_text())


@socketio.on('run_script')
def handle_run_script(payload):
    clientSecret = payload.get("token", "")
    cmdId = payload.get("cmdId", "")
    if clientSecret not in appConf["clients"]:
        # Send exit code and disconnect
        emit('script_output', {'data': "client token is invalid"})
        emit('script_exit', {'exit_code': -1})
        disconnect()

    if cmdId not in appConf["clients"][clientSecret]:
        # Send exit code and disconnect
        emit('script_output', {
             'data': "command access not provided to client"})
        emit('script_exit', {'exit_code': -1})
        disconnect()

    cmdObj = appConf["commands"][cmdId]
    cmd = cmdObj["cmd"]
    cwd = cmdObj["cwd"]
    try:
        # Start subprocess and stream output
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Read output line by line and send to client
        for line in iter(process.stdout.readline, ''):
            emit('script_output', {'data': line})

        process.stdout.close()
        return_code = process.wait()

        # Send exit code and disconnect
        emit('script_exit', {'exit_code': return_code})
        disconnect()
    except Exception as e:
        emit('script_output', {'data': f"Error: {str(e)}"})
        emit('script_exit', {'exit_code': -1})
        disconnect()


@app.route('/')
def index():
    return "WebSocket server is running. Connect via WebSocket to `/run_script`."


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True, allow_unsafe_werkzeug=True)
