import asyncio
from telethon import events
from deep_translator import GoogleTranslator
from database import get_maintenance, is_banned
from config import OWNER_ID

# --- GLOBAL SETTINGS ---
# Dict to store user_id: target_lang
AUTO_TR_USERS = {}

# ================= 1. .autotr [lang] (Toggle Mode) =================
@events.register(events.NewMessage(pattern=r"\.autotr(?: (.*))?"))
async def autotr_toggle(event):
    # 🛡️ NO-ENTRY (OWNER DM PROTECTION)
    if event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        await event.edit("**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️")
        return

    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    user_id = event.sender_id
    input_lang = event.pattern_match.group(1)

    # Turn OFF Logic
    if user_id in AUTO_TR_USERS and not input_lang:
        del AUTO_TR_USERS[user_id]
        await event.edit("🔄 **Auto-Translate Mode: OFF**")
        await asyncio.sleep(2)
        return await event.delete()

    # Validation Logic
    if not input_lang:
        return await event.edit("`❌ Language code bhi dalo! Example: .autotr hi`")

    # Turn ON Logic
    try:
        # Testing if language code is valid
        GoogleTranslator(source='auto', target=input_lang.strip())
        AUTO_TR_USERS[user_id] = input_lang.strip()
        await event.edit(f"🚀 **Auto-Translate ACTIVE: [{input_lang.upper()}]**\n`Ab jo bhi likhoge wo auto-translate hoga!`")
        await asyncio.sleep(2)
        await event.delete()
    except Exception:
        await event.edit("`❌ Invalid Language Code! Use 'hi', 'en', 'pb', etc.`")

# ================= 2. THE GHOST WORKER (Auto Edit) =================
@events.register(events.NewMessage(outgoing=True))
async def translator_worker(event):
    user_id = event.sender_id
    
    # Check if user has active Auto-TR and message is not a command
    if user_id in AUTO_TR_USERS and not event.text.startswith("."):
        target_lang = AUTO_TR_USERS[user_id]
        original_text = event.text
        
        try:
            # Speed of Light Translation
            translated = GoogleTranslator(source='auto', target=target_lang).translate(original_text)
            
            # Agar translation original se alag hai, tabhi edit karo
            if translated.strip().lower() != original_text.strip().lower():
                await event.edit(translated)
        except:
            pass # Silent fail to keep it ghost mode

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(autotr_toggle)
    client.add_event_handler(translator_worker)
  
