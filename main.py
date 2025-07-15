# @title <font color=red> 🖥️ Main Colab Leech Code

# @markdown <div><center><img src="https://user-images.githubusercontent.com/125879861/255391401-371f3a64-732d-4954-ac0f-4f093a6605e1.png" height=80></center></div>
# @markdown <center><h4><a href="https://github.com/XronTrix10/Telegram-Leecher/wiki/INSTRUCTIONS">READ</a><b> How to use</h4></b></center>
# @markdown <br><center><h2><font color=lime><strong>Fill all Credentials, Run The Cell and Start The Bot</strong></h2></center>
# @markdown <br><br>

API_ID = 0  # @param {type: "integer"}
API_HASH = ""  # @param {type: "string"}
BOT_TOKEN = ""  # @param {type: "string"}
USER_ID = 0  # @param {type: "integer"}
DUMP_ID = 0  # @param {type: "integer"}

import subprocess, json, shutil, os
from IPython.display import clear_output

def log(msg, icon="🔧"):
    print(f"{icon} {msg}")

log("Initializing setup...")

# Format DUMP_ID if necessary
if len(str(DUMP_ID)) == 10 and "-100" not in str(DUMP_ID):
    DUMP_ID = int("-100" + str(DUMP_ID))

# Remove default Colab sample data
if os.path.exists("/content/sample_data"):
    log("Removing /content/sample_data")
    shutil.rmtree("/content/sample_data")

# Clone the Telegram-Leecher repository
log("Cloning Telegram-Leecher repository...")
subprocess.run(["git", "clone", "https://github.com/XronTrix10/Telegram-Leecher"])

# Install system dependencies
log("Installing ffmpeg and aria2...")
subprocess.run("apt update && apt install ffmpeg aria2 -y", shell=True)

# Install Python dependencies with live output
log("Installing Python dependencies from requirements.txt...", icon="📦")
req_path = "/content/Telegram-Leecher/requirements.txt"
process = subprocess.Popen(
    ["pip3", "install", "-r", req_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

# Display pip output live
for line in process.stdout:
    log(line.strip(), icon="🔹")

process.wait()

# Save credentials to JSON
log("Saving credentials to credentials.json...")
credentials = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID,
}

with open('/content/Telegram-Leecher/credentials.json', 'w') as file:
    json.dump(credentials, file)

# Remove previous bot session if exists
session_path = "/content/Telegram-Leecher/my_bot.session"
if os.path.exists(session_path):
    log("Removing previous bot session...")
    os.remove(session_path)

clear_output()
log("Launching bot...", icon="🚀")

# Run the bot
!cd /content/Telegram-Leecher/ && python3 -m colab_leecher  # type: ignore
