import asyncio
import random
from telethon import events, functions, types
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- NO ENTRY HELPER ---
def get_remote_aura():
    try:
        import requests
        AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

@events.register(events.NewMessage(pattern=r"\.purge(?: |$)(.*)"))
async def fast_purge(event):
    client = event.client
    me = await client.get_me()

    # 🛡️ 1. NO ENTRY LOGIC
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        for line in random.sample(aura_list, min(3, len(aura_list))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. SECURITY CHECKS
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`🛠️ Maintenance Mode Active.`")

    # Only Owner/Sudo can trigger purge
    if event.sender_id != me.id and not await is_sudo(event.sender_id):
        return

    input_str = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()

    try:
        # --- CASE 1: Reply + Count (.purge 10) ---
        if reply and input_str.isdigit():
            count = int(input_str)
            messages = []
            async for msg in client.iter_messages(event.chat_id, limit=count, offset_id=reply.id - 1, reverse=True):
                messages.append(msg.id)
            
            # Khud ka trigger message bhi add karo delete ke liye
            messages.append(event.id)
            
            # Batch Delete (Fastest)
            await client.delete_messages(event.chat_id, messages)
            status = await event.respond(f"🧹 **Purged `{len(messages)-1}` messages starting from reply!**")
            await asyncio.sleep(2)
            await status.delete()

        # --- CASE 2: Only Reply (.purge) ---
        elif reply:
            messages = []
            async for msg in client.iter_messages(event.chat_id, min_id=reply.id - 1):
                messages.append(msg.id)
            
            await client.delete_messages(event.chat_id, messages)
            status = await event.respond(f"🧹 **Purged `{len(messages)}` messages successfully!**")
            await asyncio.sleep(2)
            await status.delete()

        # --- CASE 3: No Reply, Only Count (.purge 20) ---
        elif input_str.isdigit():
            count = int(input_str)
            messages = []
            async for msg in client.iter_messages(event.chat_id, limit=count):
                messages.append(msg.id)
            
            await client.delete_messages(event.chat_id, messages)
            status = await event.respond(f"🧹 **Fast Purge `{len(messages)}` messages done!**")
            await asyncio.sleep(2)
            await status.delete()

        else:
            await event.edit("`Reply to a message or provide a count! (.purge 10)`")

    except Exception as e:
        await event.edit(f"❌ **Purge Error:** `{str(e)}`")

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(fast_purge)
    
