from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import date

app = Flask(__name__)
app.secret_key = 'very_secret_key'

USERS_FILE = 'users.json'

# Load users or initialize empty
if os.path.exists(USERS_FILE):
    with open(USERS_FILE) as f:
        users = json.load(f)
else:
    users = {}

# Mock Food Data
foods = [
    {
        "name": "Doro Wot",
        "ingredients": ["chicken", "berbere", "onion"],
        "nutrition": {"protein": 30, "fat": 10, "calories": 350}
    },
    {
        "name": "Misir Wot",
        "ingredients": ["lentils", "onion", "berbere"],
        "nutrition": {"protein": 20, "fat": 5, "calories": 250}
    },
    {
        "name": "Shiro",
        "ingredients": ["chickpeas", "onion"],
        "nutrition": {"protein": 15, "fat": 6, "calories": 280}
    }
]

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"].lower()
        filter_type = request.form["filter"]
        results = []

        for food in foods:
            if filter_type == "name" and query in food["name"].lower():
                results.append(food)
            elif filter_type == "ingredient":
                if any(query in ingredient for ingredient in food["ingredients"]):
                    results.append(food)
            elif filter_type == "nutrition":
                if "high protein" in query and food["nutrition"]["protein"] >= 20:
                    results.append(food)
                elif "low fat" in query and food["nutrition"]["fat"] <= 7:
                    results.append(food)
                elif "under" in query and "calories" in query:
                    try:
                        number = int(query.split("under")[1].split()[0])
                        if food["nutrition"]["calories"] <= number:
                            results.append(food)
                    except:
                        continue
        return render_template("home.html", results=results)
    return redirect(url_for("home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        if username in users:
            return "Username exists. Go back."
        users[username] = {"meals": {}}
        save_users()
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        if username in users:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "Username not found. Go back."
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    username = session["user"]
    today = str(date.today())
    meals = users[username]["meals"].get(today, [])

    if request.method == "POST":
        food_name = request.form["food_name"]
        users[username]["meals"].setdefault(today, []).append(food_name)
        save_users()
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", meals=meals, today=today, username=username)

@app.route('/share')
def share():
    if "user" not in session:
        return redirect(url_for("login"))
    username = session["user"]
    meal_log = users[username]["meals"]
    return render_template("share.html", username=username, meal_log=meal_log)

if __name__ == "__main__":
    app.run(debug=True)