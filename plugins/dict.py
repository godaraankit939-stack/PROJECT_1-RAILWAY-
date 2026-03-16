import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG (Aura Lines) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤▣** 🛡️"]

@events.register(events.NewMessage(pattern=r"\.dic ?(.*)"))
async def dictionary_handler(event):
    client = event.client
    me = await client.get_me()

    # 🛡️ 1. NO ENTRY LOGIC (Professional Style)
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        for line in random.sample(aura_list, min(3, len(aura_list))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. BAN & MAINTENANCE CHECK
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("🚧 **Maintenance Mode Active.**")

    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await event.edit("`Usage:`\n`.dic <word>` - Meaning dhundne ke liye\n`.dic <letter> <length> <count>` - Words generate karne ke liye")

    await event.edit("`🔍 Processing request...`")
    args = input_str.split()

    # --- LOGIC A: WORD GENERATOR (.dic a 4 5) ---
    if len(args) == 3 and len(args[0]) == 1 and args[1].isdigit() and args[2].isdigit():
        letter = args[0].lower()
        length = int(args[1])
        count = min(int(args[2]), 20)
        
        try:
            # Datamuse API for word generation
            url = f"https://api.datamuse.com/words?sp={letter}{'?' * (length-1)}&max=50"
            response = requests.get(url).json()
            words = [w['word'] for w in response if len(w['word']) == length]
            
            if not words:
                return await event.edit(f"❌ No {length}-letter words found starting with '{letter}'.")
            
            selected = random.sample(words, min(count, len(words)))
            result = f"📚 **Words starting with '{letter}' ({length} letters):**\n\n"
            for i, word in enumerate(selected, 1):
                result += f"{i}. `{word}`\n"
            
            await event.edit(result)
        except Exception as e:
            await event.edit(f"❌ **Generator Error:** `{e}`")

    # --- LOGIC B: WORD MEANING (.dic success) ---
    else:
        word = args[0]
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return await event.edit(f"❌ Word `{word}` nahi mila.")
            
            data = response.json()[0]
            meaning = data['meanings'][0]['definitions'][0]['definition']
            part_of_speech = data['meanings'][0]['partOfSpeech']
            example = data['meanings'][0]['definitions'][0].get('example', 'N/A')
            
            res_msg = (
                f"📖 **Dictionary: `{word.upper()}`**\n\n"
                f"◈ **Type:** `{part_of_speech}`\n"
                f"◈ **Meaning:** `{meaning}`\n\n"
                f"◈ **Example:** *{example}*\n\n"
                f"**Powered By DARK-USERBOT** 💀"
            )
            await event.edit(res_msg)
        except Exception as e:
            await event.edit(f"❌ **Meaning Error:** `{e}`")

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(dictionary_handler)
  
