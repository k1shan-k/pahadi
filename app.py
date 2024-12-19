from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app) 
#app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Store users
users = {}

# Serve the chat page
@app.route('/')
def index():
    return render_template('index.html')

# Handle message sending
@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    user = data['user']
    timestamp = data['timestamp']
    
    # Broadcast message to all clients
    emit('new_message', {'user': user, 'message': message, 'timestamp': timestamp}, broadcast=True)

# Handle typing indicator
@socketio.on('typing')
def handle_typing(data):
    user = data['user']
    emit('typing', {'user': user}, broadcast=True)

# Handle stop typing indicator
@socketio.on('stop_typing')
def handle_stop_typing(data):
    user = data['user']
    emit('stop_typing', {'user': user}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
