import asyncio
import random
import requests
from datetime import datetime
from telethon import events, functions, types
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG (Aura Lines) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

@events.register(events.NewMessage(pattern=r"\.create ?(.*)"))
async def create_handler(event):
    client = event.client
    me = await client.get_me()

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

    # Only Master/Self can trigger this
    if event.sender_id != me.id:
        return

    group_name = event.pattern_match.group(1).strip()
    if not group_name:
        return await event.edit("`Error: Group name provide karein. Ex: .create DarkGroup`")

    await event.edit(f"`🛠 Creating Group: {group_name}...`")

    try:
        # 🚀 𝖲𝖠𝖪𝖳𝖨 𝖫𝖮𝖦𝖨𝖢: Safe Group Creation
        result = await client(functions.messages.CreateChatRequest(
            users=[me.id], 
            title=group_name
        ))
        
        new_group_id = None
        
        # 🛠️ FIX: Direct Chat Attribute Check
        if hasattr(result, 'chats') and result.chats:
            new_group_id = result.chats[0].id
        
        # 🛠️ FIX: Updates Object Check (Iterable error handle karne ke liye)
        if not new_group_id and hasattr(result, 'updates'):
            # Check if it's a list or a single object
            updates = result.updates if isinstance(result.updates, list) else [result.updates]
            for upd in updates:
                if hasattr(upd, 'chat_id'):
                    new_group_id = upd.chat_id
                    break
        
        # 🛠️ ULTIMATE FAIL-SAFE: Sync check via Dialogs
        if not new_group_id:
            await asyncio.sleep(1)
            async for dialog in client.iter_dialogs(limit=5):
                if dialog.name == group_name:
                    new_group_id = dialog.id
                    break

        if not new_group_id:
            return await event.edit("❌ **Failure:** ID extraction failed.")

        # Sync Delay
        await asyncio.sleep(2.5)

        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d-%m-%Y")

        welcome_text = (
            f"✅ **Group Created Successfully!**\n\n"
            f"◈ **Name:** `{group_name}`\n"
            f"◈ **Date:** `{date_str}`\n"
            f"◈ **Time:** `{time_str}`\n\n"
            f"**Powered By DARK-USERBOT** 💀"
        )
        
        # 📤 Message sending to the new group
        await client.send_message(new_group_id, welcome_text)
        await event.edit(f"✅ **Group `{group_name}` Created!**\nID: `{new_group_id}`")

    except Exception as e:
        await event.edit(f"❌ **Error:** `{str(e)}`")

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(create_handler)
        
