import os
from telethon import events
from config import OWNER_ID

# --- PATH TO SUDOS FILE ---
SUDO_FILE = "DARK/sudos.py"

# --- HELPER: GET SUDO LIST ---
def get_sudo_list():
    try:
        from DARK.sudos import SUDO_USERS
        return SUDO_USERS
    except ImportError:
        return []

# --- HELPER: SAVE SUDO LIST ---
def save_sudo_list(sudo_list):
    # Removing duplicates and sorting
    sudo_list = list(set(sudo_list))
    with open(SUDO_FILE, "w") as f:
        f.write(f"SUDO_USERS = {sudo_list}")

# ================= 1. .sudo [Reply/Username] (Owner Only) =================
@events.register(events.NewMessage(pattern=r"\.sudo(?: (.*))?"))
async def add_sudo(event):
    if event.sender_id != OWNER_ID:
        return # Strictly Owner Only

    reply = await event.get_reply_message()
    target = event.pattern_match.group(1)

    try:
        if reply:
            user = await event.client.get_entity(reply.sender_id)
        elif target:
            user = await event.client.get_entity(target)
        else:
            return await event.edit("`Reply to someone or give @username!`")

        u_id = user.id
        sudo_users = get_sudo_list()

        if u_id in sudo_users:
            return await event.edit(f"👑 **{user.first_name}** is already in Sudo List.")

        sudo_users.append(u_id)
        save_sudo_list(sudo_users)
        await event.edit(f"✅ **{user.first_name}** [`{u_id}`] added to Sudo Empire!")
    except Exception as e:
        await event.edit(f"❌ `Error: {str(e)}`")

# ================= 2. .rsudo [Reply/Username] (Owner Only) =================
@events.register(events.NewMessage(pattern=r"\.rsudo(?: (.*))?"))
async def remove_sudo(event):
    if event.sender_id != OWNER_ID:
        return

    reply = await event.get_reply_message()
    target = event.pattern_match.group(1)

    try:
        if reply:
            user = await event.client.get_entity(reply.sender_id)
        elif target:
            user = await event.client.get_entity(target)
        else:
            return await event.edit("`Reply or give @username to remove!`")

        u_id = user.id
        sudo_users = get_sudo_list()

        if u_id not in sudo_users:
            return await event.edit("❌ This user is not a Sudo.")

        sudo_users.remove(u_id)
        save_sudo_list(sudo_users)
        await event.edit(f"🗑️ **{user.first_name}** removed from Sudo Empire.")
    except Exception as e:
        await event.edit(f"❌ `Error: {str(e)}`")

# ================= 3. .sudos (View List) =================
@events.register(events.NewMessage(pattern=r"\.sudos$"))
async def show_sudos(event):
    if event.sender_id != OWNER_ID:
        return

    sudo_users = get_sudo_list()
    if not sudo_users:
        return await event.edit("😔 **Empire is empty. No Sudos found.**")

    msg = "👑 **MSD EMPIRE SUDO LIST** 👑\n\n"
    for i, s_id in enumerate(sudo_users, 1):
        msg += f"{i}. ID: `{s_id}`\n"
    
    await event.edit(msg)

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(add_sudo)
    client.add_event_handler(remove_sudo)
    client.add_event_handler(show_sudos)
  
