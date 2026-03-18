import asyncio
import random
from telethon import events, functions
from database import (
    is_banned, get_maintenance, get_antipm_status,
    is_warned_in_db, set_warned_in_db, delete_warned_user,
    is_sudo
)
from config import OWNER_ID

# --- NO ENTRY HELPER ---
def get_remote_aura():
    try:
        import requests
        AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ ACCESS DENIED 🛡️**"]

# ================= AUTO-GUARD =================
@events.register(events.NewMessage(incoming=True))
async def antipm_handler(event):
    client = event.client
    sender_id = event.sender_id

    # ❌ sirf private msgs pe kaam kare
    if not event.is_private:
        return

    # 🛡️ NO ENTRY (OWNER DM PROTECTION)
    if sender_id != OWNER_ID and event.chat_id == OWNER_ID:
        aura_list = get_remote_aura()
        for line in random.sample(aura_list, min(3, len(aura_list))):
            await event.reply(line)
            await asyncio.sleep(1.5)
        return

    # 🚫 BAN CHECK
    if await is_banned(sender_id):
        return

    # 🔧 MAINTENANCE
    if await get_maintenance() and sender_id != OWNER_ID and not await is_sudo(sender_id):
        return

    # ❌ ANTIPM OFF
    if not await get_antipm_status():
        return

    # 👑 APG LOGIC (OWNER RESPECT)
    if sender_id == OWNER_ID:
        from config import APG_RESPECT
        await event.reply(random.choice(APG_RESPECT))
        return

    # ✅ ALLOW: BOT / SUDO
    if event.is_bot or await is_sudo(sender_id):
        return

    # ✅ CONTACT CHECK (FIXED)
    try:
        contacts = await client.get_contacts()
        contact_ids = [user.id for user in contacts]

        if sender_id in contact_ids:
            return
    except:
        pass

    # ================= WARN / BLOCK =================

    # ⚠️ FIRST WARNING
    if not await is_warned_in_db(sender_id):
        warn_msg = (
            "**⌬ ANTI-PM SECURITY 🛡️**\n\n"
            "⚠️ Unauthorized DM detected!\n"
            "Do not message without permission.\n\n"
            "**Next message = BLOCK 🚫**"
        )
        await event.reply(warn_msg)
        await set_warned_in_db(sender_id)

    # 🚫 SECOND MESSAGE → BLOCK
    else:
        try:
            await event.reply("`Policy Violation: BLOCKED 🚫`")
            await asyncio.sleep(1)

            await client(functions.contacts.BlockRequest(id=sender_id))

            await delete_warned_user(sender_id)

        except:
            pass


# ================= COMMAND =================
@events.register(events.NewMessage(outgoing=True, pattern=r"^\.antipm (on|off)$"))
async def antipm_cmd(event):

    if await is_banned(event.sender_id):
        return await event.edit("`YOU WERE BANNED BY OWNER!`")

    from database import set_antipm_status

    mode = event.pattern_match.group(1).lower()

    if mode == "on":
        await set_antipm_status(True)
        await event.edit("🛡️ Anti-PM: ON")

    else:
        await set_antipm_status(False)
        await event.edit("🔓 Anti-PM: OFF")


# ================= SETUP =================
async def setup(client):
    client.add_event_handler(antipm_handler)
    client.add_event_handler(antipm_cmd)
