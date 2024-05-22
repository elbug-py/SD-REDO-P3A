from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
import socketio

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode="eventlet")

# In-memory storage for simplicity
users = {}
messages = []


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


@socketio.on("message")
def handle_message(msg):
    username = session["username"]
    messages.append(f"{username}: {msg}")
    emit("message", {"msg": f"{username}: {msg}"}, broadcast=True)


@socketio.on("connect")
def handle_connect():
    username = session.get("username")
    if username:
        users[username] = request.sid
        emit(
            "message",
            {"msg": f"{username} has joined the chat"},
            broadcast=True,
        )


@socketio.on("disconnect")
def handle_disconnect():
    username = session.get("username")
    if username:
        users.pop(username, None)
        emit(
            "message", {"msg": f"{username} has left the chat"}, broadcast=True
        )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
