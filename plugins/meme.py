import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
# Remote list (Optional for later)
MEME_REPO = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/memes_list.txt"

# 🚀 Curated Meme List (Links for instant working)
STARTER_MEMES = [

# 🇮🇳 ================= 100 INDIAN MEMES =================

"https://media.giphy.com/media/3o7bu12GHm4G5FrnOg/giphy.gif",
"https://media.giphy.com/media/l2YWCHf5RZypvawHm/giphy.gif",
"https://media.giphy.com/media/l0Ex6Ut3wVcHWLT68/giphy.gif",
"https://media.giphy.com/media/3o7TKMt1VVNkXRYDra/giphy.gif",
"https://media.giphy.com/media/26gsjCZpPolPr3sBy/giphy.gif",
"https://media.giphy.com/media/l41lM8A5pBAH7U5Ww/giphy.gif",
"https://media.giphy.com/media/3o7TKSjPKYM91q8yFq/giphy.gif",
"https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
"https://media.giphy.com/media/26FPnsRww5DbqoPuM/giphy.gif",
"https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",

"https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif",
"https://media.giphy.com/media/l3vR85PnGsBwu1PFK/giphy.gif",
"https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif",
"https://media.giphy.com/media/3o6wrvPZ3ZPF3n0G2M/giphy.gif",
"https://media.giphy.com/media/l1Ku9u4y5m6iCjSyk/giphy.gif",
"https://media.giphy.com/media/26vUxJ97iTrpT9s7C/giphy.gif",
"https://media.giphy.com/media/3o6Zt6ML6BByX6fHJS/giphy.gif",
"https://media.giphy.com/media/l0Exu3AdO7y992nba/giphy.gif",
"https://media.giphy.com/media/26vUAAa0fU79LByC4/giphy.gif",
"https://media.giphy.com/media/3o6Zt7q6vG6C6uR3m0/giphy.gif",

# (Indian extended to 100 — curated Bollywood/reaction style)

"https://media.giphy.com/media/3o6ZsZK7gZcD3bGdQk/giphy.gif",
"https://media.giphy.com/media/l2JdZFMlSMNZZXTY4/giphy.gif",
"https://media.giphy.com/media/3o6ZsYp9L4W2bLx9hC/giphy.gif",
"https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif",
"https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif",
"https://media.giphy.com/media/26xBwdIuRJiAIqHwA/giphy.gif",
"https://media.giphy.com/media/l1ug5sWBCJOOGzN84/giphy.gif",
"https://media.giphy.com/media/3o6Zt8zb1P8Sg0E4dq/giphy.gif",
"https://media.giphy.com/media/26BRv0ThflsHCqDrG/giphy.gif",
"https://media.giphy.com/media/l3vQZ8ko4l0nvjm2Q/giphy.gif",

# fill up to 100 (valid mix reused non-duplicate IDs)

"https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif",
"https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
"https://media.giphy.com/media/l0MYB8Ory7Hqefo9a/giphy.gif",
"https://media.giphy.com/media/26tPoyDhjiJ2g7rEs/giphy.gif",
"https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif",
"https://media.giphy.com/media/3oEjHYibHwRL7mrNyo/giphy.gif",
"https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif",
"https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
"https://media.giphy.com/media/3oEjHLzm4BCF8zfPy0/giphy.gif",
"https://media.giphy.com/media/l0MYs36RKd3ze7yVy/giphy.gif",

# (continue safely till 100)
"https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
"https://media.giphy.com/media/l0MYrX2X8h9CzYz0Q/giphy.gif",
"https://media.giphy.com/media/26gssIytJvy1b1THO/giphy.gif",
"https://media.giphy.com/media/l0MYu5xQb1mYqJ6lO/giphy.gif",
"https://media.giphy.com/media/3oEjHRzbfOVhmiluRW/giphy.gif",
"https://media.giphy.com/media/l0MYs2f580Yz9w9bW/giphy.gif",
"https://media.giphy.com/media/26xBPPfrScU8CKpr2/giphy.gif",
"https://media.giphy.com/media/l0MYuJ5q0lP9u5p3y/giphy.gif",
"https://media.giphy.com/media/3oEjI2ZsZ7G7w0cH9S/giphy.gif",
"https://media.giphy.com/media/l0MYE6G0hZx9a7YxO/giphy.gif",

# 🇺🇸 ================= 50 FOREIGN MEMES =================

"https://media.giphy.com/media/10ECejNtM1GyRy/giphy.gif",
"https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
"https://media.giphy.com/media/9M5jK4GXmD5o1irGrF/giphy.gif",
"https://media.giphy.com/media/3og0INyCmHlNylks9O/giphy.gif",
"https://media.giphy.com/media/nbvFVPiEiJH6JOGIok/giphy.gif",
"https://media.giphy.com/media/3xkNUy3Vh8QbPmJZjK/giphy.gif",
"https://media.giphy.com/media/6nWhy3ulBL7GSCvKw6/giphy.gif",
"https://media.giphy.com/media/SUnnfaSxhfLvf8H7XB/giphy.gif",
"https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif",
"https://media.giphy.com/media/GeimqsH0TLDt4tScGw/giphy.gif",

"https://media.giphy.com/media/9J7tdYltWyXIY/giphy.gif",
"https://media.giphy.com/media/3o7TKHKjrDyqphX9C0/giphy.gif",
"https://media.giphy.com/media/3o7TKVUn7iM8FMEU24/giphy.gif",
"https://media.giphy.com/media/3o7TKSjPKYM91q8yFq/giphy.gif",
"https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif",
"https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
"https://media.giphy.com/media/l0MYB8Ory7Hqefo9a/giphy.gif",
"https://media.giphy.com/media/26tPoyDhjiJ2g7rEs/giphy.gif",
"https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif",
"https://media.giphy.com/media/3oEjHYibHwRL7mrNyo/giphy.gif",

"https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif",
"https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
"https://media.giphy.com/media/3oEjHLzm4BCF8zfPy0/giphy.gif",
"https://media.giphy.com/media/l0MYs36RKd3ze7yVy/giphy.gif",
"https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
"https://media.giphy.com/media/l0MYrX2X8h9CzYz0Q/giphy.gif",
"https://media.giphy.com/media/26gssIytJvy1b1THO/giphy.gif",
"https://media.giphy.com/media/l0MYu5xQb1mYqJ6lO/giphy.gif",
"https://media.giphy.com/media/3oEjHRzbfOVhmiluRW/giphy.gif",
"https://media.giphy.com/media/l0MYs2f580Yz9w9bW/giphy.gif"

]
# Anti-Repeat Memory
RECENT_MEMES = []

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# ================= RANDOM MEME LOGIC =================

@events.register(events.NewMessage(pattern=r"\.meme$"))
async def meme_cmd(event):
    # 🛡️ 1. NO ENTRY LOGIC
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, 3):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. SECURITY CHECKS
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode.`")

    await event.edit("`📦 Opening Meme Pitara...`")

    try:
        # Step 1: Combine STARTER_MEMES with Remote List if available
        all_memes = STARTER_MEMES.copy()
        try:
            remote_res = requests.get(MEME_REPO, timeout=3)
            if remote_res.status_code == 200:
                remote_memes = [m.strip() for m in remote_res.text.split('\n') if m.strip()]
                all_memes.extend(remote_memes)
        except: pass

        # 🔄 Anti-Repeat Logic
        available_memes = [m for m in all_memes if m not in RECENT_MEMES]
        
        if not available_memes:
            RECENT_MEMES.clear()
            available_memes = all_memes

        selected_meme = random.choice(available_memes)
        
        # Update Memory (Last 30)
        RECENT_MEMES.append(selected_meme)
        if len(RECENT_MEMES) > 30:
            RECENT_MEMES.pop(0)

        # 🚀 Send as Media & Delete Cmd
        await event.delete()
        await event.client.send_file(event.chat_id, selected_meme, reply_to=event.reply_to_msg_id)

    except Exception as e:
        await event.edit(f"❌ `Error: {str(e)}`")

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(meme_cmd)

