* Websocket server and client example for running commands remotely
* The command execution console output is streamed via websocket in real time from server to client

## secret/config.json
```json
{
    "clients":
    {
        "r73rG457zjkgf": ["ping_server"]
    },
    "commands":
    {
        "ping_server": {
            "cmd":["ping", "-n", "5", "8.8.8.8"],
            "cwd": null
        }
    }
}
```

## References
* https://me.micahrl.com/blog/magicrun/
* python-socketio[client] docs - https://python-socketio.readthedocs.io/en/stable/intro.html#client-examples
* flask-socketio docs - https://flask-socketio.readthedocs.io/en/latest/getting_started.html#receiving-messages
