# if __name__ == "__main__":
#     conn = connect_to_db()
#     print(float(get_data(conn)[0][1]))

import config

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

# example
def get_data(conn):
    conn = connect_to_db()
    cur = conn.cursor() 
    cur.execute("SELECT * FROM csl.config WHERE key = 'BASE_LATITUDE'")
    rows = cur.fetchall()
    conn.close()
    return rows


########################################################################################

from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)


todos = [
    {'id': 1, 'text': 'Buy groceries'},
    {'id': 2, 'text': 'Learn Python'},
    {'id': 3, 'text': 'Build a Flask API'}
]

@app.route('/get_baseview', methods=['GET'])
def get_baseview():
    if request.method == 'GET':
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM csl.config WHERE key = 'BASE_LATITUDE'")
        rows = cur.fetchall()
        return jsonify(todos)


@app.route('/todos', methods=['GET', 'POST'])
def get_or_create_todos():
    if request.method == 'GET':
        return jsonify(todos)
    elif request.method == 'POST':
        todo = request.get_json()
        todos.append(todo)
        return jsonify(todo), 201

@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_todo(todo_id):
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    if request.method == 'GET':
        return jsonify(todo)
    elif request.method == 'PUT':
        updated_todo = request.get_json()
        todo.update(updated_todo)
        return jsonify(todo)
    elif request.method == 'DELETE':
        todos.remove(todo)
        return jsonify({'message': 'Todo deleted'}), 204

if __name__ == '__main__':

    get_data()
    # app.run(debug=True, port=5005)


