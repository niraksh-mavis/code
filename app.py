import os
import subprocess
from flask import Flask, render_template, request, redirect, session, url_for, send_file, Response
from config import Config
import database

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database tables on launch
database.init_db()

STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))

# Vulnerability: Insecure CORS configuration with wildcard (Low)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# 1. Main Feed Route (renders Stored XSS from database)
@app.route("/")
def index():
    comments = database.get_all_comments()
    return render_template("index.html", comments=comments)

# 2. Login Route (Vulnerable to SQL Injection)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Authenticate with SQL Injection vulnerable query in database.py
        user = database.authenticate_user(username, password)
        if user:
            # Set user session
            session["user"] = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# 3. Post Comment Route
@app.route("/comment", methods=["POST"])
def post_comment():
    if "user" not in session:
        return redirect(url_for("login"))

    content = request.form.get("content", "")
    author = session["user"]["username"]
    user_id = session["user"]["id"]

    database.add_comment(user_id, author, content)
    return redirect(url_for("index"))

# 4. Search Route (Vulnerable to SQL Injection)
@app.route("/search")
def search():
    query = request.args.get("q", "")
    users = []
    if query:
        # SQL Injection vulnerable search
        users = database.search_users(query)
    return render_template("search.html", users=users, query=query)

# 5. Profile Route (Vulnerable to IDOR and Reflected XSS)
@app.route("/profile")
def profile():
    user_id = request.args.get("id", type=int)
    greeting = request.args.get("greeting", "Welcome back!")

    if not user_id and "user" in session:
        user_id = session["user"]["id"]

    # Vulnerability: IDOR - Any authenticated or unauthenticated user can fetch anyone's profile
    user = database.get_user_by_id(user_id) if user_id else None

    # Vulnerability: Reflected XSS (banner_html returned unsanitized)
    banner_html = f"<span>{greeting}</span>"

    return render_template("profile.html", user=user, banner_html=banner_html)

# 6. File Download Route (Vulnerable to Path Traversal / Arbitrary File Read - Medium)
@app.route("/download")
def download_file():
    filename = request.args.get("file", "")
    if not filename:
        return "Filename parameter 'file' is required", 400

    # Vulnerability: Path traversal via unsanitized file path (e.g. ?file=../../schema.sql)
    target_path = os.path.join(STORAGE_DIR, filename)

    try:
        return send_file(target_path, as_attachment=True)
    except Exception as e:
        # Vulnerability: Information disclosure in error response (Low)
        return f"File read error: {str(e)}", 500

# 7. Diagnostic Ping API (Vulnerable to OS Command Injection - High/Critical)
@app.route("/api/ping", methods=["POST"])
def ping_host():
    host = request.form.get("host", "127.0.0.1")
    # Vulnerability: Command injection via shell=True with user input
    try:
        output = subprocess.check_output(f"ping -c 1 {host}", shell=True, stderr=subprocess.STDOUT)
        return Response(output, mimetype="text/plain")
    except subprocess.CalledProcessError as e:
        return Response(e.output, mimetype="text/plain", status=500)

if __name__ == "__main__":
    # Vulnerability: Flask Debug Mode enabled in production (Low/Medium)
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
