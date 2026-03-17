import asyncio
import os
from PIL import Image
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# ================= TINY CMD =================
@events.register(events.NewMessage(pattern=r"\.tiny$"))
async def tiny_handler(event):
    client = event.client

    # 🚫 BAN CHECK
    if await is_banned(event.sender_id):
        return

    # 🛠️ MAINTENANCE
    if await get_maintenance() and event.sender_id != OWNER_ID:
        return await event.edit("`System Status: Maintenance Mode Active.`")

    # 📩 REPLY CHECK
    if not event.is_reply:
        return await event.edit(
            "`Please reply to a photo or a static sticker to use this command professionally.`"
        )

    reply = await event.get_reply_message()

    # 🎯 VALIDATION
    if not reply.photo and not reply.sticker:
        return await event.edit(
            "`Please reply to a photo or a static sticker to use this command professionally.`"
        )

    # ❌ Animated Sticker Block
    if reply.sticker:
        if reply.sticker.mime_type != "image/webp":
            return await event.edit("`Only static stickers are supported.`")

    await event.edit("`⚡ Processing...`")

    input_path = None
    output_path = "tiny_output.png"

    try:
        # 📥 DOWNLOAD
        input_path = await reply.download_media()

        # 🖼️ OPEN IMAGE
        img = Image.open(input_path).convert("RGBA")

        # 📏 RESIZE (50%)
        width, height = img.size
        new_size = (max(1, width // 2), max(1, height // 2))
        img = img.resize(new_size, Image.LANCZOS)

        # 💾 SAVE
        img.save(output_path, "PNG")

        # 📤 SEND
        if reply.sticker:
            await client.send_file(
                event.chat_id,
                output_path,
                reply_to=event.reply_to_msg_id,
                force_document=False
            )
        else:
            await client.send_file(
                event.chat_id,
                output_path,
                reply_to=event.reply_to_msg_id
            )

        await event.delete()

    except Exception as e:
        await event.edit(f"`Error: {str(e)}`")

    finally:
        # 🧹 CLEANUP (NO SERVER JUNK)
        try:
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass


# ================= SETUP =================
async def setup(client):
    client.add_event_handler(tiny_handler)
