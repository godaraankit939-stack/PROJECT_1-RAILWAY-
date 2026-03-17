import asyncio
import io
import random
import requests
from telethon import events
from PIL import Image
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# ================= TINY IMAGE LOGIC =================

@events.register(events.NewMessage(pattern=r"\.tiny$"))
async def tiny_image_cmd(event):
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

    reply = await event.get_reply_message()
    if not reply or not (reply.sticker or reply.photo):
        return await event.edit("`Error: Reply to a sticker or photo!`")

    await event.edit("`🖌️ Making it tiny...`")

    try:
        # 📂 Step 1: Download media to memory
        media_bytes = await event.client.download_media(reply, file=io.BytesIO())
        media_bytes.seek(0)
        
        # 🛠️ Step 2: Load with Pillow
        img = Image.open(media_bytes)
        width, height = img.size
        
        # 📉 Step 3: Resize (Reduce by 50%)
        # Tiny logic: Current size / 2
        new_width = int(width / 2)
        new_height = int(height / 2)
        
        # Prevent image from becoming 0x0
        if new_width == 0 or new_height == 0:
            return await event.edit("`Error: Image is already too tiny!`")
            
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        
        # 💾 Step 4: Save resized image to memory
        output_bytes = io.BytesIO()
        
        # Handle Sticker (WEBP) vs Photo (JPEG/PNG)
        if reply.sticker:
            resized_img.save(output_bytes, format="WEBP")
            output_bytes.seek(0)
            # Send as sticker
            await event.client.send_file(event.chat_id, output_bytes, reply_to=reply, force_document=False)
        else:
            resized_img.save(output_bytes, format="PNG")
            output_bytes.seek(0)
            # Send as photo
            await event.client.send_file(event.chat_id, output_bytes, reply_to=reply, force_document=False)

        await event.delete() # Delete command msg

    except Exception as e:
        await event.edit(f"❌ `Error: {str(e)}`")

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(tiny_image_cmd)
                 
