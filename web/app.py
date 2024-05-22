from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import threading
import time
import socket

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# In-memory storage for simplicity
users = {}
messages = []


# Function to receive messages from the simulator
def receive_messages_from_simulator():
    while True:
        try:
            # Connect to the cleverhub_sim
            with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            ) as client_socket:
                client_socket.connect(
                    ("server", 12345)
                )  # Adjust host and port as needed
                client_socket.sendall(b"WEBAPP")
                rsp = client_socket.recv(1024).decode()
                print("Received response from the simulator:", rsp)
                # Send command to the cleverhub_sim to get device data
                client_socket.sendall(b"GS")

                # Receive response from the cleverhub_sim
                response = client_socket.recv(1024).decode()
                print("Received response from the simulator:", response)
                # Append the received response to the messages list
                messages.append(response)

                # Emit the response to all connected clients
                socketio.emit("message", {"msg": response}, namespace="/chat")
                client_socket.close()
        except Exception as e:
            print("Error communicating with the simulator:", e)
            time.sleep(5)


# Start receiving messages from the simulator in a separate thread
receive_thread = threading.Thread(target=receive_messages_from_simulator)
receive_thread.daemon = True
receive_thread.start()


# Handle user login
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        if username in users:
            return "Username already taken!"
        session["username"] = username
        return redirect(url_for("chat"))
    return render_template("index.html")


@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("chat.html", username=session["username"])


@socketio.on("connect", namespace="/chat")
def handle_connect():
    username = session.get("username", "Anonymous")
    users[username] = request.sid
    print("AYUDA QUIERO DORMIR")
    socketio.emit(
        "message",
        {"msg": f"{username} has joined the chat"},
        namespace="/chat",
    )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
