import asyncio
from telethon import events
from telethon.tl.functions.messages import DeleteMessagesRequest
from database import get_maintenance, is_banned
from config import OWNER_ID

# --- HELPER: DELETE FOR ALL LOGIC ---
async def delete_messages(event, msg_ids):
    try:
        # 'revoke=True' means delete for everyone
        await event.client(DeleteMessagesRequest(msg_ids, revoke=True))
    except Exception:
        pass

# ================= 1. .purge (Reply or Count Mode) =================
@events.register(events.NewMessage(pattern=r"\.purge(?: (\d+))?"))
async def purge_cmd(event):
    # 🛡️ NO-ENTRY LOGIC (OWNER DM PROTECTION)
    if event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        await event.edit("**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️")
        return

    # 🛡️ BAN & MAINTENANCE LOGIC
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    reply = await event.get_reply_message()
    count = event.pattern_match.group(1)
    
    # Mode A: Reply + Count or Just Reply
    if reply:
        msg_ids = []
        limit = int(count) if count else None
        # Iterates from the replied message upwards
        async for msg in event.client.iter_messages(event.chat_id, min_id=reply.id - 1, limit=limit):
            msg_ids.append(msg.id)
        await delete_messages(event, msg_ids)
    
    # Mode B: Just Count based (.purge 10) - Mix Delete
    elif count:
        num = int(count)
        msg_ids = []
        # +1 to include the command message itself
        async for msg in event.client.iter_messages(event.chat_id, limit=num + 1):
            msg_ids.append(msg.id)
        await delete_messages(event, msg_ids)
    
    else:
        return await event.edit("`Reply to a message or provide count: .purge 10`")

# ================= 2. .purgemy [Count] =================
@events.register(events.NewMessage(pattern=r"\.purgemy (\d+)"))
async def purgemy_cmd(event):
    # 🛡️ NO-ENTRY LOGIC (OWNER DM PROTECTION)
    if event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        await event.edit("**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️")
        return

    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    count = int(event.pattern_match.group(1))
    msg_ids = []
    
    # Iterates only through messages sent by the user who gave the command
    async for msg in event.client.iter_messages(event.chat_id, from_user="me"):
        if len(msg_ids) >= count:
            break
        msg_ids.append(msg.id)
    
    # Adding the command message id to delete it too
    if event.id not in msg_ids:
        msg_ids.append(event.id)
        
    await delete_messages(event, msg_ids)

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(purge_cmd)
    client.add_event_handler(purgemy_cmd)
        
