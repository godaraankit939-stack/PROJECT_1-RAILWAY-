from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

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
        # 1. BAN CHECK
        if await is_banned(event.sender_id):
            return

        # 2. MAINTENANCE CHECK
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        cmd = event.pattern_match.group(1).lower()
        if not cmd:
            await event.edit(f"```{HELP_MENU}```")
        else:
            # Future logic for specific plugin help
            await event.edit(f"🔍 Searching help for `{cmd}`...")
      
