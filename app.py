from flask import Flask, request, Response, render_template, send_from_directory

app = Flask(__name__)

# ----------------------------
# CONSTANTS
# ----------------------------
USERNAME = "mark"
PASSWORD = "password1"        # password included inside rockyou wordlist
FLAG = "SDC{ADMIN_ZONE_GRANTED}"
ALLOWED_IP = "127.0.0.1"     # internal workstation IP


# ----------------------------
# HOME PAGE
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# GATEWAY PAGE
# ----------------------------
@app.route("/gateway")
def gateway():
    return render_template("gateway.html")


# ----------------------------
# ROBOTS FILE
# ----------------------------
@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(".", "robots.txt")


# ----------------------------
# NODE402 PAGE (glitch / distraction)
# ----------------------------
@app.route("/node402/")
def node402():
    return render_template("node402.html")


# ----------------------------
# LOG FILE (fake internal logs)
# ----------------------------
@app.route("/logs/system")
def system_logs():
    return send_from_directory("logs", "system.log")


# ----------------------------
# ADMIN PANEL
# Basic Auth + Internal IP Restriction
# ----------------------------
@app.route("/admin")
def admin_panel():

    # --- (1) Basic Auth check ---
    auth = request.authorization

    if not (auth and auth.username == USERNAME and auth.password == PASSWORD):
        return Response(
            render_template("unauthorized.html"),
            401,
            {"WWW-Authenticate": 'Basic realm=\"Neo-402\"'}
        )

    # --- (2) IP check with X-Forwarded-For bypass ---
    xff = request.headers.get("X-Forwarded-For", request.remote_addr)
    client_ip = xff.split(",")[0].strip()

    if client_ip != ALLOWED_IP:
        return Response(
            "Access blocked. Internal workstation required.",
            403
        )

    # --- (3) All good → show flag ---
    return render_template("admin.html", flag=FLAG)


# ----------------------------
# STATIC NOISE FILE (decoy)
# ----------------------------
@app.route("/static/notes")
def noise():
    return send_from_directory("static", "notes.txt")


# ----------------------------
# RUN
# ----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

