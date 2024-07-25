from flask import Flask, render_template
from flask_socketio import SocketIO
import threading, time, json

import openstream


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd$ehls'
socketio = SocketIO(app, async_mode = 'gevent') # async_mode = gevent , threading works, idk what they are - AVD


# TBR with DB
devices = [
    {'id': 1, 'name': 'Device 1', 'latitude': 13.0474, 'longitude': 77.562, 'status': 'Online'},
    {'id': 2, 'name': 'Device 2', 'latitude': 13.0476, 'longitude': 77.562, 'status': 'Offline'}
]
baseview = {"lat":13.0474, "long":77.562, "zoom":16}


def emit_frequently():
    while True:
        # print("thread heartbeat")
        devices[0]["latitude"] += 0.001
        socketio.emit('devices_response', devices)
        time.sleep(2)

@socketio.on('connect')
def handle_connect():
    print('Client connected********************')

@socketio.on('option_selected')
def handle_options(data):
    print(f"clicked {data['option']} in {data['deviceId']} ")
    if (data['deviceId'],data['option']) == (2,'A'):
        openstream.cam_popup("rtsp://admin:admin@192.168.1.111:554/snl/live/1/1")

@app.route('/')
def index():
    return render_template('index.html', data = baseview)

if __name__ == '__main__':
    # start emit data process, this emits to client at regular interval
    emit_thread = threading.Thread(target=emit_frequently)
    emit_thread.daemon = True
    emit_thread.start()
    
    socketio.run(app, debug=True)


    