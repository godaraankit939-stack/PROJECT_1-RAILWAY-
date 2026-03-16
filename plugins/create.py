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

    # 🛡️ 1. NO ENTRY LOGIC (Owner's Chat Protection)
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

    # Only Master/Client can create groups
    if event.sender_id != me.id:
        return

    group_name = event.pattern_match.group(1).strip()
    if not group_name:
        return await event.edit("`Bhulaaaa! Group ka naam toh batao? Ex: .create MyGroup`")

    await event.edit(f"`🛠 Creating Group: {group_name}...`")

    try:
        # 🚀 𝖲𝖠𝖪𝖳𝖨 𝖫𝖮𝖦𝖨𝖢: 100% ID Extraction
        result = await client(functions.messages.CreateChatRequest(
            users=[me.id], 
            title=group_name
        ))
        
        # Multiple checks taaki 'InvitedUsers' wala error na aaye
        new_group_id = None
        
        # Check 1: Direct chats attribute
        if hasattr(result, 'chats') and result.chats:
            new_group_id = result.chats[0].id
        # Check 2: Updates list ke andar se
        elif hasattr(result, 'updates'):
            for upd in result.updates:
                if hasattr(upd, 'chats') and upd.chats:
                    new_group_id = upd.chats[0].id
                    break
                if hasattr(upd, 'chat_id'):
                    new_group_id = upd.chat_id
                    break
        
        # Agar fir bhi na mile toh last created chat uthana (Ultimate Fail-safe)
        if not new_group_id:
            async for dialog in client.iter_dialogs(limit=5):
                if dialog.name == group_name:
                    new_group_id = dialog.id
                    break

        if not new_group_id:
            return await event.edit("❌ **Failure:** Group ban gaya par ID nahi mili.")

        # 𝖲𝖠𝖪𝖳𝖨: Sync ke liye wait
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
        
        # 𝖲𝖠𝖪𝖳𝖨: Naye group mein message bhejna
        await client.send_message(new_group_id, welcome_text)

        await event.edit(f"✅ **Group `{group_name}` Created!**\nID: `{new_group_id}`")

    except Exception as e:
        await event.edit(f"❌ **Error while creating group:** `{e}`")

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(create_handler)
                
