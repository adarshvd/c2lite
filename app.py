from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading, time
from flask_cors import CORS

import utils_streaming
import config
import requests

################################### Init

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.config['SECRET_KEY'] = 'd$ehls'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode = 'gevent') # async_mode = gevent , threading works, idk what they are - AVD

# fetch from db once
devices = requests.get('http://127.0.0.1:5005/get_devices').json()
baseview = requests.get('http://127.0.0.1:5005/get_baseview').json()

################################### Threads

# refreshing the display
def update_display():
    cnt = 0
    while True:
        cnt += 1
        # print(f"{cnt}:updating...")
        devices = requests.get('http://127.0.0.1:5005/get_devices').json()
        # print(devices)
        socketio.emit('update', devices)
        time.sleep(config.REFRESH_RATE)



################################### Socket functions

@socketio.on('connect')
def handle_connect():
    print('Client connected********************')

    # Listen for 'feature-right-clicked' event
    @socketio.on('feature-right-clicked')
    def handle_feature_right_click(data):
        print(f"Client right-clicked on feature: {data['name']} {data['type']}")


@socketio.on('init')
def handle_connect():
    baseview = requests.get('http://127.0.0.1:5005/get_baseview').json()
    # print(baseview)
    devices_types_raw = requests.get('http://localhost:5005/get_devices_types').json()
    
    devices_types = dict()
    for dev in devices_types_raw:
        devices_types[dev[0]] = dev[1]

    # print(devices_types)

    socketio.emit('initialize', {'baseview':baseview, 'devices_types':devices_types})
    print('Initializing client********************')

# @socketio.on('option_selected')
# def handle_options(data):
#     print(f"clicked {data['option']} in {data['deviceId']} ")
#     if (data['deviceId'],data['option']) == (2,'A'):
#         print("streaming A 2")
#         # utils_streaming.cam_popup("rtsp://admin:admin@192.168.1.111:554/snl/live/1/1")



################################### flask routes

@app.route('/')
def index():
    print("C2 is running...")
    return 'C2 is running on 5173'
    # return render_template('index.html', data = baseview)



################################### driver

if __name__ == '__main__':
    # start emit data process, this emits to client at regular interval
    emit_thread = threading.Thread(target=update_display)
    emit_thread.daemon = True
    emit_thread.start()
    
    socketio.run(app, debug=True)


    