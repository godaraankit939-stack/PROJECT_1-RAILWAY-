import random
import requests
from telethon import events

# ================= CONFIG =================

TENOR_API_KEY = "LIVDSRZULELA"

SEARCH_TERMS = [
    "indian meme",
    "babu rao meme",
    "bollywood reaction meme",
    "carryminati meme",
    "akshay kumar meme",
    "rajpal yadav meme",
    "funny indian reaction"
]

REDDIT_SUBS = [
    "IndianDankMemes",
    "dankinindia",
    "memes"
]

# ================= TENOR =================

def get_tenor_meme():
    try:
        query = random.choice(SEARCH_TERMS)
        url = f"https://tenor.googleapis.com/v2/search?q={query}&key={TENOR_API_KEY}&limit=20"

        res = requests.get(url, timeout=5).json()
        results = res.get("results", [])

        if results:
            gif = random.choice(results)
            return gif["media_formats"]["gif"]["url"]

    except Exception as e:
        print("Tenor Error:", e)

    return None

# ================= REDDIT =================

def get_reddit_meme():
    try:
        sub = random.choice(REDDIT_SUBS)
        url = f"https://meme-api.com/gimme/{sub}"

        res = requests.get(url, timeout=5).json()

        if res and "url" in res:
            return res["url"]

    except Exception as e:
        print("Reddit Error:", e)

    return None

# ================= COMMANDS =================

# 🔥 MIXED MEME
@events.register(events.NewMessage(pattern=r"\.meme"))
async def meme(event):
    await event.edit("`😂 Fetching Meme...`")

    meme_url = get_tenor_meme()

    # fallback to reddit
    if not meme_url:
        meme_url = get_reddit_meme()

    if meme_url:
        await event.delete()
        return await event.client.send_file(event.chat_id, meme_url)

    await event.edit("❌ No meme found")

# 😂 REDDIT ONLY
@events.register(events.NewMessage(pattern=r"\.rmeme"))
async def rmeme(event):
    await event.edit("`🔥 Fetching Reddit Meme...`")

    meme_url = get_reddit_meme()

    if meme_url:
        await event.delete()
        return await event.client.send_file(event.chat_id, meme_url)

    await event.edit("❌ No Reddit meme found")

# ================= SETUP =================

async def setup(client):
    client.add_event_handler(meme)
    client.add_event_handler(rmeme)
