from telethon import events
from database import get_maintenance, is_sudo
from config import OWNER_ID

# Final Symmetric Grid Design
# Note: Isko hamesha Triple Backticks (```) ke andar send karna hai
HELP_MENU = """
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃   ⌬ 𝗗𝗔𝗥𝗞 𝗫 𝗨𝗦𝗘𝗥𝗕𝗢𝗧 ⌬   ┃
┣━━━━━━━━━━┳━━━━━━━━━━━┫
┃ ◈ 𝖠𝗎𝗍𝗈𝗉𝗂𝖼 ┃ ◈ 𝖠𝖽𝗆𝗂𝗇    ┃
┃ ◈ 𝖠𝖿𝗄     ┃ ◈ 𝖠𝗇𝗂𝗆𝖺𝗍𝖾   ┃
┃ ◈ 𝖠𝗇𝗍𝗂𝗉𝗆  ┃ ◈ 𝖡-𝖢𝖺𝗌𝗍   ┃
┃ ◈ 𝖢𝗅𝗈𝗇𝖾   ┃ ◈ 𝖢𝗋𝖾𝖺𝗍𝖾    ┃
┃ ◈ 𝖣𝖾𝗌𝗍𝗋𝗎𝖼𝗍┃ ◈ 𝖣𝗂𝖼𝗍      ┃
┃ ◈ 𝖦𝗈𝗈𝗀𝗅𝖾  ┃ ◈ 𝖨𝗇𝖿𝗈      ┃
┃ ◈ 𝖫𝗒𝗋𝗂𝖼𝗌   ┃ ◈ 𝖬𝖾𝗆𝗂𝖿𝗒    ┃
┃ ◈ 𝖬𝖾𝗇𝗍𝗂𝗈𝗇 ┃ ◈ 𝖯𝗂𝗇𝗀      ┃
┃ ◈ 𝖰𝗎𝗈𝗍𝖾   ┃ ◈ 𝖱𝖺𝗂𝖽/𝖱𝗋𝖺𝗂𝖽 ┃
┃ ◈ 𝖳𝗂𝗇𝗒    ┃ ◈ 𝖳𝗋𝖺𝗇𝗌     ┃
┃ ◈ 𝖶𝖾𝖺𝗍𝗁𝖾𝗋 ┃ ◈ 𝖬𝖺𝗀𝗂𝖼     ┃
┣━━━━━━━━━━┻━━━━━━━━━━━┫
┃    𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 : 𝗠𝗦𝗗 👑   ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛
"""

async def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"\.help(?: |$)(.*)"))
    async def help_handler(event):
        # --- MAINTENANCE CHECK ---
        if await get_maintenance():
            # Owner aur Sudo ko maintenance affect nahi karegi
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**\nOnly Owner/Sudo can use commands.")

        # Logic for help menu
        cmd = event.pattern_match.group(1).lower()
        
        if not cmd:
            # Pura grid menu dikhane ke liye
            await event.edit(f"```{HELP_MENU}```")
            return

        # Yahan specific plugin ki details aayengi jab hum unhe banayenge
        if cmd == "ping":
            await event.edit("🏓 **𝖯𝖨𝖭𝖦**\nUse: `.ping` to check bot speed.")
        elif cmd == "raid":
            await event.edit("🔥 **𝖱𝖠𝖨𝖣**\nUse: `.raid <count> <user>`\nTarget user ko fast messages bhejta hai.")
        else:
            await event.edit(f"❌ Plugin `{cmd}` not found.")

