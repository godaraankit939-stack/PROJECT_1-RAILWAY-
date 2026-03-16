from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

ALIVE_TEXT = (
    "**⌬ 𝖣𝖠𝖱𝖪-𝖴𝖲𝖤𝖱𝖡𝖮𝖳 𝖨𝖲 𝖠𝖫𝖨𝖵𝖤 ⚡**\n\n"
    "◈ **𝖵𝖾𝗋𝗌𝗂𝗈𝗇:** `𝟩.𝟢 (𝖳𝗁𝖺𝗅𝖺 𝖥𝗈𝗋 𝖠 𝖱𝖾𝖺𝗌𝗈𝗇)`\n"
    "◈ **𝖲𝗍𝖺𝗍𝗎𝗌:** `𝖱𝖾𝖺𝖽𝗒 𝗍𝗈 𝖣𝖾𝗌𝗍𝗋𝗈𝗒` 💀"
)

async def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
    async def alive_handler(event):
        # 1. BAN CHECK
        if await is_banned(event.sender_id):
            return

        # 2. MAINTENANCE CHECK
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        await event.edit(ALIVE_TEXT)
              
