from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json, os

app = Flask(__name__)
app.secret_key = "change_this_secret"

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")
USERS_PATH = os.path.join(os.path.dirname(__file__), "users.json")

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/schedule")
def schedule():
    data = read_json(DATA_PATH)
    return render_template("schedule.html", data=data)

@app.route("/lineup")
def lineup():
    # placeholder lineup - can be expanded
    data = read_json(DATA_PATH)
    lineup = data.get("lineup", {})
    return render_template("lineup.html", lineup=lineup)

@app.route("/standings")
def standings():
    data = read_json(DATA_PATH)
    teams = data.get("teams", [])
    # sort by points descending
    teams_sorted = sorted(teams, key=lambda x: x.get("points",0), reverse=True)
    return render_template("standings.html", teams=teams_sorted)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        username = request.form.get("username","")
        password = request.form.get("password","")
        mac = request.form.get("mac","")
        users = read_json(USERS_PATH).get("users", [])
        for u in users:
            if u["username"]==username and u["password"]==password and u["mac"].lower()==mac.lower():
                session["admin"] = username
                return redirect(url_for("admin_panel"))
        flash("بيانات الدخول أو MAC خاطئة.", "danger")
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html")

@app.route("/admin")
def admin_panel():
    if "admin" not in session:
        return redirect(url_for("dashboard"))
    data = read_json(DATA_PATH)
    return render_template("admin.html", data=data)

@app.route("/admin/update", methods=["POST"])
def admin_update():
    if "admin" not in session:
        return jsonify({"ok":False,"error":"unauthorized"}),401
    team_id = request.form.get("team_id")
    action = request.form.get("action")
    data = read_json(DATA_PATH)
    teams = data.get("teams", [])
    for t in teams:
        if t["id"] == team_id:
            if action == "add_win":
                t["wins"] += 1
                t["points"] += 3
            elif action == "add_loss":
                t["losses"] += 1
            elif action == "add_point":
                t["points"] += int(request.form.get("value",1))
            elif action == "set_points":
                t["points"] = int(request.form.get("value",0))
            elif action == "reset":
                t["points"] = 0
                t["wins"] = 0
                t["losses"] = 0
            break
    write_json(DATA_PATH, data)
    return redirect(url_for("admin_panel"))

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
