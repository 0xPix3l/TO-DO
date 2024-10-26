from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, UTC
from functools import wraps
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' or 'you-will-never-guess'
CORS(app)

# Local storage paths
USER_DATA_FILE = 'users.json'
TODO_DATA_FILE = 'todos.json'

# Initialize local data storage
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(TODO_DATA_FILE):
    with open(TODO_DATA_FILE, 'w') as f:
        json.dump([], f)

def load_users():
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_todos():
    with open(TODO_DATA_FILE, 'r') as f:
        return json.load(f)

def save_todos(todos):
    with open(TODO_DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            # Handle 'Bearer token' format
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = next((user for user in load_users() if user['id'] == data['user_id']), None)
            
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
        
    hashed_password = generate_password_hash(data['password'], method='scrypt')
    
    users = load_users()
    if any(user['username'] == data['username'] for user in users):
        return jsonify({'message': 'Username already exists'}), 400
    
    new_user = {
        'id': len(users) + 1,
        'name': data.get('name', ''),
        'username': data['username'],
        'password': hashed_password
    }
    users.append(new_user)
    save_users(users)
    
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.get_json()
    
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Missing credentials'}), 401

    users = load_users()
    user = next((user for user in users if user['username'] == auth['username']), None)
    
    if not user or not check_password_hash(user['password'], auth['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode(
        {
            'user_id': user['id'],
            'exp': datetime.now(UTC) + timedelta(hours=24)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'name': user.get('name', '')
        }
    })

@app.route('/api/todos', methods=['GET', 'POST'])
@token_required
def todos(current_user):
    if request.method == 'GET':
        todos = load_todos()
        user_todos = [todo for todo in todos if todo['user_id'] == current_user['id']]
        return jsonify(user_todos)
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({'message': 'Missing content'}), 400
            
        todos = load_todos()
        new_todo = {
            'id': len(todos) + 1,
            'content': data['content'],
            'completed': False,
            'user_id': current_user['id'],
            'created_at': datetime.now(UTC).isoformat()
        }
        todos.append(new_todo)
        save_todos(todos)
        
        return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
@token_required
def todo(current_user, todo_id):
    todos = load_todos()
    todo = next((todo for todo in todos if todo['id'] == todo_id and todo['user_id'] == current_user['id']), None)
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        todo['content'] = data.get('content', todo['content'])
        todo['completed'] = data.get('completed', todo['completed'])
        save_todos(todos)
        return jsonify(todo)
    
    elif request.method == 'DELETE':
        todos.remove(todo)
        save_todos(todos)
        return jsonify({'message': 'Todo deleted'})

@app.route('/api/admin/users', methods=['GET'])
@token_required
def admin_users(current_user):
    if current_user['username'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    users = load_users()
    todos = load_todos()

    # Count todos for each user
    for user in users:
        user['todo_count'] = sum(1 for todo in todos if todo['user_id'] == user['id'])

    # Don't send password hashes
    safe_users = [{k: v for k, v in user.items() if k != 'password'} for user in users]
    return jsonify(safe_users)

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if current_user['username'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    users = load_users()
    user = next((user for user in users if user['id'] == user_id), None)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    users.remove(user)
    save_users(users)
    
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
