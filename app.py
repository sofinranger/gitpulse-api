from flask import Flask, jsonify, request
import subprocess
from send_gitlog import collect_commits, save_to_file, send_as_text, send_as_file

app = Flask(__name__)

@app.route("/")
def home():
    return "GitPulse Logger API aktif!"

@app.route("/trigger", methods=["POST"])
def trigger():
    mode = request.json.get("mode", "text")
    logs = collect_commits()
    if not logs:
        return jsonify({"status": "error", "message": "No valid repos found."}), 400

    save_to_file(logs)

    if mode == "text":
        send_as_text(logs)
    elif mode == "file":
        send_as_file()
    elif mode == "both":
        send_as_text(logs)
        send_as_file()
    else:
        return jsonify({"status": "error", "message": "Mode tidak valid"}), 400

    return jsonify({"status": "success", "sent_mode": mode})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
