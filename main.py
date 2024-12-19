from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory storage for online users' status and messages
users_status = {}
messages = []

@app.route('/')
def index():
    return render_template('index.html')

# User connects to the WebSocket
@socketio.on('connect')
def handle_connect():
    users_status[request.sid] = {'status': 'online'}
    emit('user_status', {'status': 'online', 'user': request.sid}, broadcast=True)
    print(f"User {request.sid} connected.")

# User disconnects from the WebSocket
@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users_status:
        users_status[request.sid] = {'status': 'offline'}
        emit('user_status', {'status': 'offline', 'user': request.sid}, broadcast=True)
        print(f"User {request.sid} disconnected.")

# Sending messages
@socketio.on('send_message')
def handle_message(data):
    message = {
        'user': data['user'],
        'message': data['message'],
        'status': 'delivered',
        'timestamp': str(datetime.now())
    }
    messages.append(message)
    emit('new_message', message, broadcast=True)

# Handling message read status
@socketio.on('message_read')
def handle_message_read(data):
    message_id = data['message_id']
    if 0 <= message_id < len(messages):
        messages[message_id]['status'] = 'read'
        emit('message_status', {'message_id': message_id, 'status': 'read'}, broadcast=True)

# Handling typing status
@socketio.on('typing')
def handle_typing(data):
    emit('show_typing', {'user': data['user']}, broadcast=True)

@socketio.on('stop_typing')
def handle_stop_typing(data):
    emit('stop_typing', {'user': data['user']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

