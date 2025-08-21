from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = "mysecretkey"  # needed for sessions

# Employees stored in a JSON file
EMPLOYEE_FILE = "employees.json"

def load_employees():
    try:
        with open(EMPLOYEE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        employees = load_employees()

        if username in employees and employees[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    employees = load_employees()
    user_data = employees[username]

    return render_template("dashboard.html", username=username, user=user_data)

if __name__ == "__main__":
    app.run(debug=True)
