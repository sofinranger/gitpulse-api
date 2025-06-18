import os
import subprocess
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# Load konfigurasi dari .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT_PATH = os.getenv("REPO_PATH")
LOG_FILE = os.path.join(BASE_DIR, "last_commit.json")

def get_git_info(repo_path):
    try:
        # Ambil nama branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path
        ).decode().strip()

        # Ambil hash commit
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_path
        ).decode().strip()

        # Ambil author dan tanggal
        author = subprocess.check_output(
            ["git", "show", "-s", "--format=%an <%ae>", "HEAD"], cwd=repo_path
        ).decode().strip()

        date = subprocess.check_output(
            ["git", "show", "-s", "--format=%ci", "HEAD"], cwd=repo_path
        ).decode().strip()

        # Ambil pesan commit
        message = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"], cwd=repo_path
        ).decode().strip()

        return {
            "name": os.path.basename(repo_path),
            "path": repo_path,
            "branch": branch,
            "commit": commit,
            "author": author,
            "date": date,
            "message": message
        }
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Gagal membaca repo: {repo_path} ({e})")
        return None

def collect_commits():
    results = []
    if not REPO_ROOT_PATH or not os.path.isdir(REPO_ROOT_PATH):
        print(f"[ERROR] Direktori repo '{REPO_ROOT_PATH}' tidak valid.")
        return results

    for root, dirs, files in os.walk(REPO_ROOT_PATH):
        if ".git" in dirs:
            print(f"[OK] Ditemukan repo Git: {root}")
            info = get_git_info(root)
            if info:
                results.append(info)
            else:
                results.append({
                    "name": os.path.basename(root),
                    "path": root,
                    "error": "Gagal membaca commit"
                })
            dirs[:] = []  # Hindari masuk ke subfolder .git
    return results

def save_to_file(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Log JSON ditulis ke {LOG_FILE}")

def send_as_file():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(LOG_FILE, "rb") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caption = f"📄 JSON Log Commit\n_{now}_"
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "caption": caption,
            "parse_mode": "Markdown"
        }, files={"document": file})
    if res.status_code == 200:
        print("[INFO] File JSON berhasil dikirim ke Telegram.")
    else:
        print(f"[ERROR] Gagal kirim file JSON: {res.text}")


def send_as_text(logs):
    lines = []
    for item in logs:
        line = (
            f"[{item['project']}]\n"
            f"Branch: {item['branch']}\n"
            f"Commit: {item['commit']}\n"
            f"Author: {item['author']} <{item['email']}>\n"
            f"Date: {item['date']}\n"
            f"Message: {item['message']}\n"
        )
        lines.append(line)

    message = "📌 *Last Git Commit Log:*\n\n" + "\n\n".join(lines)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    res = requests.post(url, data=payload)
    if res.status_code == 200:
        print("[INFO] Pesan berhasil dikirim ke Telegram.")
    else:
        print(f"[ERROR] Gagal kirim pesan: {res.text}")