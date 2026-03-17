import asyncio
import random
import requests
from bs4 import BeautifulSoup
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
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

@events.register(events.NewMessage(pattern=r"\.google ?(.*)"))
async def google_search(event):
    client = event.client
    me = await client.get_me()

    # 🛡️ 1. NO ENTRY LOGIC
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. BAN & MAINTENANCE CHECK
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode Active.`")

    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("`Error: Please provide a search query.`")

    await event.edit(f"`🔍 Multi-Engine Search: {query}...`")
    final_info = ""

    # 🚀 ENGINE 1: GOOGLE DEEP SCRAPE
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        g_url = f"https://www.google.com/search?q={query}&hl=en"
        g_res = requests.get(g_url, headers=headers, timeout=10)
        soup = BeautifulSoup(g_res.text, "html.parser")
        
        g_results = []
        for g in soup.find_all("div", class_="VwiC3b"):
            g_results.append(g.get_text().strip())
        
        if len(g_results) > 0:
            final_info = "\n\n".join(g_results[:4])
    except:
        pass

    # 🚀 ENGINE 2: WIKIPEDIA (If Google fails or short results)
    if len(final_info) < 100:
        try:
            w_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            w_res = requests.get(w_url, timeout=10).json()
            if "extract" in w_res:
                final_info = w_res["extract"]
        except:
            pass

    # 🚀 ENGINE 3: DUCKDUCKGO API (Final Fallback)
    if len(final_info) < 50:
        try:
            ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
            ddg_res = requests.get(ddg_url, timeout=10).json()
            if ddg_res.get("AbstractText"):
                final_info = ddg_res["AbstractText"]
        except:
            pass

    # --- FINAL RESPONSE ---
    if not final_info or len(final_info) < 10:
        return await event.edit("`Error: No results found on all search engines.`")

    response_msg = (
        f"🧐 **Search Results for:** `{query.upper()}`\n\n"
        f"📝 {final_info}\n\n"
        f"**Powered By DARK-USERBOT** 💀"
    )

    # Character limit adjustment
    if len(response_msg) > 4095:
        response_msg = response_msg[:4090] + "..."

    await event.edit(response_msg)

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(google_search)
        
