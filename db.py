import config
from flask import Flask, jsonify, request
import psycopg2


######################################################################################## DB utility functions

#connect and return CONN
def connect_to_db():
    conn = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    return conn

# get data
def get_data(command):
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute(command)
        rows = cur.fetchall()
        conn.close()
        return rows
    except psycopg2.Error as e:
        print(f"Error updating device status: {e}")

def put_data(command):
    print(command)
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute(command)
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error updating device status: {e}")




######################################################################################## Flask 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd$ehls'



# Flask Routes

@app.route('/get_baseview', methods=['GET'])
def get_baseview():
    if request.method == 'GET':
        baseview = dict()
        baseview["latitude"] = float(get_data("SELECT * FROM csl.config WHERE key = 'BASE_LATITUDE'")[0][1])
        baseview["longitude"] = float(get_data("SELECT * FROM csl.config WHERE key = 'BASE_LONGITUDE'")[0][1])
        baseview["zoom"] = int(get_data("SELECT * FROM csl.config WHERE key = 'BASE_ZOOM'")[0][1])
        return jsonify(baseview), 200


@app.route('/get_devices', methods=['GET'])
def get_devices():
    if request.method == 'GET':
        result = []
        data = get_data("SELECT * FROM csl.devices")
        for i in data:
            device = dict()
            device["id"] = i[0]
            device["name"] = i[1]
            device["latitude"] = i[2]
            device["longitude"] = i[3]
            device["status"] = i[4]
            device["type"]=i[5]

            result.append(device)
        # print(result)
        return jsonify(result), 200
    
@app.route('/get_devices_types', methods=['GET'])
def get_devices_types():
    if request.method == 'GET':
        # result = []
        data = get_data("SELECT * FROM csl.device_types")
        # print(data)
        return jsonify(data), 200
        


# driver
if __name__ == '__main__':
    app.run(debug=True, port=5005)
    












# todos = [
#     {'id': 1, 'text': 'Buy groceries'},
#     {'id': 2, 'text': 'Learn Python'},
#     {'id': 3, 'text': 'Build a Flask API'}
# ]

# @app.route('/todos', methods=['GET', 'POST'])
# def get_or_create_todos():
#     if request.method == 'GET':
#         return jsonify(todos)
#     elif request.method == 'POST':
#         todo = request.get_json()
#         todos.append(todo)
#         return jsonify(todo), 201

# @app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
# def get_update_delete_todo(todo_id):
#     todo = next((item for item in todos if item['id'] == todo_id), None)
#     if not todo:
#         return jsonify({'error': 'Todo not found'}), 404

#     if request.method == 'GET':
#         return jsonify(todo)
#     elif request.method == 'PUT':
#         updated_todo = request.get_json()
#         todo.update(updated_todo)
#         return jsonify(todo)
#     elif request.method == 'DELETE':
#         todos.remove(todo)
#         return jsonify({'message': 'Todo deleted'}), 204


