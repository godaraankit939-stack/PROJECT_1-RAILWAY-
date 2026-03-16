import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG (Aura Lines) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️", "⌬ `System: God Mode Active` ✨"]

@events.register(events.NewMessage(pattern=r"\.bcast(?: |$)(.*)"))
async def broadcast_handler(event):
    me = await event.client.get_me()

    # 🛡️ 1. NO ENTRY LOGIC (Forceful Edit in Owner's Chat)
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. BAN CHECK
    if await is_banned(event.sender_id):
        return

    # 🛠️ 3. MAINTENANCE CHECK
    if await get_maintenance():
        if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
            return await event.edit("🛠 **Maintenance Mode is ON.**")

    # Command Execution (Only for Master/Client)
    if event.sender_id != me.id: return

    msg_content = event.pattern_match.group(1).strip()
    reply_to_msg = await event.get_reply_message()

    if not msg_content and not reply_to_msg:
        return await event.edit("`Bhulaaaa! Provide text or reply to a message.`")

    # ⚠️ STEP 1: HIGH RISK WARNING & CONFIRMATION
    # Text ko code block (`) mein dala hai taaki copy ho sake
    warning_msg = (
        "⚠️ **𝖧𝖨𝖦𝖧 𝖱𝖨𝖲𝖪 𝖶𝖠𝖱𝖭𝖨𝖭𝖦** ⚠️\n\n"
        "◈ `Ban Risk: 80-90% (Don't use without Emergency)`\n"
        "◈ `Are you sure you want to proceed?`\n\n"
        "👉 Click to Copy: `Yes, i am sure` \n"
        "👉 Click to Copy: `Cancel` \n\n"
        "⏳ **𝖳𝗂𝗆𝖾𝗈𝗎𝗍:** `1 Minute`"
    )
    await event.edit(warning_msg)

    # 🛠️ 4. NEW CONFIRMATION LOGIC
    def check(e):
        return e.chat_id == event.chat_id and e.text in ["Yes, i am sure", "Cancel"]

    try:
        async with event.client.conversation(event.chat_id) as conv:
            response_event = await conv.wait_event(events.NewMessage(chats=event.chat_id, func=check), timeout=60)
            
            if response_event.message.text == "Cancel":
                return await event.respond("❌ **Broadcast Cancelled by User.**")
            
            await event.respond("✅ **Confirmation Received. Starting...**")

            # 🚀 STEP 2: ACTUAL BROADCAST
            await event.respond("🚀 **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗂𝗇 𝗉𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**")
            
            count = 0
            error = 0
            async for dialog in event.client.iter_dialogs():
                try:
                    # 🛠️ 5. ANTI-BAN LOGIC (1.5s Sleep)
                    if reply_to_msg:
                        await event.client.send_message(dialog.id, reply_to_msg)
                    else:
                        await event.client.send_message(dialog.id, msg_content)
                    count += 1
                    await asyncio.sleep(1.5) 
                except Exception:
                    error += 1
                    continue

            await event.respond(f"✅ **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖥𝗂𝗇𝗂𝗌𝗁𝖾𝖽!**\n◈ **𝖲𝖾𝗇𝗍:** `{count}`\n◈ **𝖥𝖺𝗂𝗅𝖾𝖽:** `{error}`")

    except asyncio.TimeoutError:
        await event.respond("⏰ **Timeout! Auto-cancelled for safety.**")

async def setup(client):
    client.add_event_handler(broadcast_handler)
    
