import os
import threading
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Render ko '200 OK' signal bhejne ke liye
    return "DARK USERBOT IS LIVE 🚀", 200

def run_flask():
    # Render ka port ya default 8080
    port = int(os.environ.get("PORT", 8080))
    print(f"LOG: Port binding on {port}...")
    # use_reloader=False zaroori hai threads ke liye
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def start_manager():
    print("LOG: Starting Manager Bot...")
    if os.path.exists("main.py"):
        # Popen use kiya hai taaki ye background mein chale aur loop block na ho
        subprocess.Popen(["python3", "main.py"])
    else:
        print("ERROR: main.py not found in root folder!")

def start_userbot():
    print("LOG: Starting Userbot Engine...")
    if os.path.exists("userbot.py"):
        # Popen use kiya hai background process ke liye
        subprocess.Popen(["python3", "userbot.py"])
    else:
        print("ERROR: userbot.py not found in root folder!")

if __name__ == "__main__":
    # 1. Sabse pehle Flask thread taaki Port turant open ho jaye
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 2. Manager Bot (@BotFather wala) ko start karna
    start_manager()

    # 3. Userbot (Engine) ko start karna
    start_userbot()

    # Main thread ko zinda rakhne ke liye taaki Render bot band na kare
    print("LOG: DARK-USERBOT services are booting up...")
    threading.Event().wait()
            
