import os
import threading
import subprocess
import time
from flask import Flask

# 1. Flask App Setup
app = Flask(__name__)

@app.route('/')
def hello():
    # Render ko '200 OK' signal bhejne ke liye taaki service 'Live' rahe
    return "DARK USERBOT IS LIVE 🚀", 200

def run_flask():
    # Render ka port ya default 8080
    port = int(os.environ.get("PORT", 8080))
    print(f"LOG: Port binding on {port}...")
    # use_reloader=False zaroori hai taaki threads clash na karein
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# 2. Manager Bot (@BotFather wala) chalane ka function
def start_manager():
    print("LOG: Starting Manager Bot...")
    if os.path.exists("main.py"):
        # Popen background mein chalne ke liye best hai, ye code ko block nahi karta
        subprocess.Popen(["python3", "main.py"])
    else:
        print("ERROR: main.py not found in root folder!")

# 3. Userbot Engine chalane ka function
def start_userbot():
    print("LOG: Starting Userbot Engine...")
    if os.path.exists("userbot.py"):
        # Dono bots ko parallel chalane ke liye Popen zaroori hai
        subprocess.Popen(["python3", "userbot.py"])
    else:
        print("ERROR: userbot.py not found in root folder!")

# 4. Main Executive Block (Sabse Important)
if __name__ == "__main__":
    # Flask thread ko sabse pehle start karna taaki Render 'Port' detect kar le
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Chhota sa delay taaki Flask port ko pakad le
    time.sleep(1)

    # Manager Bot aur Userbot ko background mein fire karna
    start_manager()
    start_userbot()

    # Main thread ko block karke zinda rakhna (threading.Event se)
    # Iske bina script turant band ho jayegi
    print("LOG: DARK-USERBOT services are booting up...")
    threading.Event().wait()
    
