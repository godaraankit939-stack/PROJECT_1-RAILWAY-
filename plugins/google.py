import asyncio
import random
import requests
from bs4 import BeautifulSoup
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID
import os

AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ ACCESS DENIED 🛡️**"]


# ================= GOOGLE CMD =================
@events.register(events.NewMessage(pattern=r"\.google ?(.*)"))
async def google_search(event):
    client = event.client
    me = await client.get_me()

    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        for line in random.sample(aura_list, min(3, len(aura_list))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    if await is_banned(event.sender_id):
        return

    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode Active.`")

    if event.sender_id != me.id and not await is_sudo(event.sender_id):
        return

    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("`Give something to search...`")

    await event.edit(f"`🔍 Searching: {query}...`")

    final_info = ""

    # DUCKDUCKGO
    try:
        d_url = "https://api.duckduckgo.com/?q=" + query.replace(' ', '+') + "&format=json"
        d_res = requests.get(d_url, timeout=10).json()

        if d_res.get("Answer"):
            final_info = d_res["Answer"]
        elif d_res.get("AbstractText"):
            final_info = d_res["AbstractText"]
    except:
        pass

    # WIKIPEDIA
    if not final_info:
        try:
            w_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(' ', '_')
            w_res = requests.get(w_url, timeout=10).json()

            if w_res.get("extract"):
                final_info = w_res["extract"]
        except:
            pass

    # GOOGLE SCRAPE
    if not final_info:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            url = "https://www.google.com/search?q=" + query.replace(" ", "+")
            res = requests.get(url, headers=headers, timeout=10)

            soup = BeautifulSoup(res.text, "html.parser")

            results = []
            for g in soup.find_all("div"):
                text = g.get_text()
                if len(text) > 50 and text not in results:
                    results.append(text)

            if results:
                final_info = "\n\n".join(results[:3])
        except:
            pass

    if not final_info:
        final_info = "Try refining your query."

    msg = "🧐 **Search:** `" + query.upper() + "`\n\n" + final_info
    await event.edit(msg[:4095])


# ================= ASK CMD =================
@events.register(events.NewMessage(pattern=r"\.ask ?(.*)"))
async def ask_ai(event):
    client = event.client
    me = await client.get_me()

    if await is_banned(event.sender_id):
        return

    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`Maintenance Mode.`")

    if event.sender_id != me.id and not await is_sudo(event.sender_id):
        return

    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("`Ask something...`")

    await event.edit("`🤖 Thinking...`")

    response_text = ""

    # OPENAI
    if OPENAI_API_KEY:
        try:
            res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": query}],
                    "temperature": 0.7
                },
                timeout=15
            )

            data = res.json()

            if "choices" in data:
                response_text = data["choices"][0]["message"]["content"]

        except Exception as e:
            print("OPENAI ERROR:", e)

    # GEMINI
    if not response_text and GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

            res = requests.post(
                url,
                json={"contents": [{"parts": [{"text": query}]}]},
                timeout=15
            )

            data = res.json()

            if "candidates" in data:
                response_text = data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print("GEMINI ERROR:", e)

    if not response_text:
        response_text = "⚠️ AI not responding.\nCheck API keys or limits."

    if len(response_text) > 4095:
        response_text = response_text[:4090] + "..."

    await event.edit(response_text)


async def setup(client):
    client.add_event_handler(google_search)
    client.add_event_handler(ask_ai)
