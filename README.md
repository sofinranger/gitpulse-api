# 📡 GitPulse Logger

GitPulse Logger adalah tool Python sederhana yang digunakan untuk memantau commit terakhir dan branch aktif dari beberapa repository Git di dalam sistem lokal, lalu mengirimkan hasilnya ke Telegram.

---

## 📦 Fitur

- ✅ Membaca daftar folder dari file `.env`
- ✅ Deteksi commit terakhir dan branch aktif tiap repo
- ✅ Simpan log hasil ke `last_commit.json`
- ✅ Kirim log ke Telegram sebagai:
  - 📝 Pesan teks
  - 📄 File `.json`
  - 📤 Keduanya (opsional)
- ✅ Interaktif: pilih mode kirim saat dijalankan

---

## 🧰 Kebutuhan

- Python 3.7+
- `pip install`:
  - `requests`
  - `python-dotenv`
- Bot Telegram aktif (lihat panduan di bawah)

---

## 🛠️ Instalasi

1. **Clone project:**

   ```bash
   git clone https://github.com/namamu/gitpulse-logger.git
   cd gitpulse-logger
# GitPulse
# gitpulse-api
