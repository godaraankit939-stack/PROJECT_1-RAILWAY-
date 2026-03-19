import asyncio
import random
import requests
import os
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

HF_API_KEY = os.getenv("HF_API_KEY")

AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ ACCESS DENIED 🛡️**"]

# ================= MULTI FREE AI =================
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

    await event.edit("`🤖 AI Thinking...`")

    answer = ""

    # ================= 1️⃣ HUGGINGFACE =================
    if HF_API_KEY:
        try:
            API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": query}

            res = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            data = res.json()

            if isinstance(data, list) and "generated_text" in data[0]:
                answer = data[0]["generated_text"]

        except:
            pass

    # ================= 2️⃣ DUCKDUCKGO =================
    if not answer:
        try:
            url = "https://api.duckduckgo.com/?q=" + query.replace(" ", "+") + "&format=json&no_html=1"
            data = requests.get(url, timeout=10).json()

            if data.get("Answer"):
                answer = data["Answer"]

            elif data.get("AbstractText"):
                answer = data["AbstractText"]

            elif data.get("RelatedTopics"):
                texts = []
                for t in data["RelatedTopics"][:5]:
                    if "Text" in t:
                        texts.append(t["Text"])
                if texts:
                    answer = "\n\n".join(texts)

        except:
            pass

    # ================= 3️⃣ WIKIPEDIA =================
    if not answer:
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            data = requests.get(url, timeout=10).json()

            if data.get("extract"):
                answer = data["extract"]

        except:
            pass

    # ================= FINAL =================
    if not answer:
        answer = "I couldn’t find proper info. Try refining your query."

    final = f"🤖 **AI Response:**\n\n{answer}\n\n**DARK-USERBOT 💀 (FREE AI SYSTEM)**"

    if len(final) > 4095:
        final = final[:4090] + "..."

    await event.edit(final)


async def setup(client):
    client.add_event_handler(ask_ai)
