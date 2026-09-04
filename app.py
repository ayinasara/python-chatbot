from flask import Flask, render_template, request, redirect, url_for,session
from chatbot_engine import get_response
import json
import os

app = Flask(__name__)
app.secret_key="mysecretkey"

chat_history = {}


def load_users():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as file:
            json.dump([], file)

    with open("users.json", "r") as file:
        return json.load(file)


def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["username"] == username:
                message = "Username already exists"
                return render_template(
                    "register.html",
                    message=message
                )

        users.append({
            "username": username,
            "password": password
        })

        save_users(users)

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        message=message
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"]=username
                return redirect(url_for("chatbot"))

        message = "Invalid username or password"

    return render_template(
        "login.html",
        message=message
    )
@app.route("/logout")
    
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/clear_chat")
def clear_chat():
    username = session.get("username")

    if username in chat_history:
        chat_history[username] = []

    return redirect(url_for("chatbot"))
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    username=session.get("username")
    if username not in chat_history:
        chat_history[username]=[]

    if request.method == "POST":

        user_message = request.form["message"]

        bot_response = get_response(user_message)

        chat_history[username].append({
            "user": user_message,
            "bot": bot_response
        })

    return render_template(
        "index.html",
        chats=chat_history[username],
        username=username
    )


if __name__ == "__main__":
    app.run(debug=True)