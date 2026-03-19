import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ ACCESS DENIED 🛡️**"]

# ================= FREE AI SYSTEM =================
@events.register(events.NewMessage(pattern=r"\.ask ?(.*)"))
async def ask_ai(event):
    client = event.client

    # 🛡️ NO ENTRY
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, min(3, len(aura))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ SECURITY
    if await is_banned(event.sender_id):
        return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode.`")

    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("`Ask something...`")

    await event.edit("`🤖 Thinking (Free AI Mode)...`")

    result = ""

    # 🚀 ENGINE 1: DUCKDUCKGO
    try:
        url = "https://api.duckduckgo.com/?q=" + query.replace(" ", "+") + "&format=json&no_html=1"
        data = requests.get(url, timeout=10).json()

        if data.get("Answer"):
            result = data["Answer"]

        elif data.get("AbstractText"):
            result = data["AbstractText"]

        elif data.get("RelatedTopics"):
            texts = []
            for t in data["RelatedTopics"][:5]:
                if "Text" in t:
                    texts.append(t["Text"])
            if texts:
                result = "\n\n".join(texts)

    except:
        pass

    # 🚀 ENGINE 2: WIKIPEDIA
    if not result:
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            data = requests.get(url, timeout=10).json()

            if data.get("extract"):
                result = data["extract"]
        except:
            pass

    # 🚀 FINAL FALLBACK (SMART MESSAGE)
    if not result:
        result = f"I couldn’t find exact info for '{query}', but try being more specific."

    # 🧠 FORMAT (AI style)
    final = (
        f"🤖 **AI Answer:**\n\n"
        f"{result}\n\n"
        f"**Powered By DARK-USERBOT 💀 (FREE AI)**"
    )

    if len(final) > 4095:
        final = final[:4090] + "..."

    await event.edit(final)


async def setup(client):
    client.add_event_handler(ask_ai)
