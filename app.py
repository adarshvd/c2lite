from flask import Flask, render_template
from flask_socketio import SocketIO
import threading, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Example data (replace with actual data or simulated data)
devices = [
    {'id': 1, 'name': 'Device 1', 'latitude': 51.505, 'longitude': -0.09, 'status': 'Online'},
    {'id': 2, 'name': 'Device 2', 'latitude': 51.51, 'longitude': -0.1, 'status': 'Offline'}
]

# SocketIO event to emit device updates
@socketio.on('get_devices')
def send_devices():
    socketio.emit('devices_response', devices)


def emit_frequently():
    global devices
    cnt = 0
    while True:
        cnt += 1
        print(f"{cnt} : emitting...")
        devices[0]['latitude']+=0.02
        print(devices[0])
        socketio.emit('devices_response', devices)
        time.sleep(5)

        cnt += 1
        print(f"{cnt} : emitting...")
        devices[0]['latitude']-=0.02
        print(devices[0])
        socketio.emit('devices_response', devices)
        time.sleep(5)

@socketio.on('connect')
def handle_connect():
    print('Client connected********************')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # start emit data process, this emits to client at regular interval
    emit_thread = threading.Thread(target=emit_frequently)
    emit_thread.daemon = True
    emit_thread.start()
    
    
    socketio.run(app, debug=True)


    