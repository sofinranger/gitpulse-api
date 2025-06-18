@echo off
SETLOCAL

echo 📦 Menyiapkan virtual environment...
python -m venv venv

echo 📂 Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

echo ⬇️ Menginstall dependensi...
pip install -r requirements.txt

echo 📁 Membuat folder output jika belum ada...
if not exist output (
    mkdir output
)

echo 🚀 Menjalankan program GitPulse...
python app.py

echo ✅ Selesai. Lihat hasil di Telegram

ENDLOCAL
pause
