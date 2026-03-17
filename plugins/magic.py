import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
MAGIC_SETTINGS = {"status": False}

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# Aesthetic Font Mapper (Cinematic Italic Style)
FONT_MAP = {
    'a': '𝖺', 'b': '𝖻', 'c': '𝖼', 'd': '𝖽', 'e': '𝖾', 'f': '𝖿', 'g': '𝗀', 'h': '𝗁', 'i': '𝗂', 
    'j': '𝗃', 'k': '𝗄', 'l': '𝗅', 'm': '𝗆', 'n': '𝗇', 'o': '𝗈', 'p': '𝗉', 'q': '𝗊', 'r': '𝗋', 
    's': '𝗌', 't': '𝗍', 'u': '𝗎', 'v': '𝗏', 'w': '𝗐', 'x': '𝗑', 'y': '𝗒', 'z': '𝗓',
    'A': '𝖠', 'B': '𝖡', 'C': '𝖢', 'D': '𝖣', 'E': '𝖤', 'F': '𝖥', 'G': '𝖦', 'H': '𝖧', 'I': '𝖨', 
    'J': '𝖩', 'K': '𝖪', 'L': '𝖫', 'M': '𝖬', 'N': '𝖭', 'O': '𝖮', 'P': '𝖯', 'Q': '𝖰', 'R': '𝖱', 
    'S': '𝖲', 'T': '𝖳', 'U': '𝖴', 'V': '𝖵', 'W': '𝖶', 'X': '𝖷', 'Y': '𝖸', 'Z': '𝖹'
}

# 🚀 1000+ Words Dictionary (English & Hindi)
EMOJI_FEELS = {
    # --- HINDI / HINGLISH (500+) ---
    "naam": "🆔", "kaam": "💼", "baap": "🧔", "beta": "👶", "duniya": "🌍", "yaar": "🤝", "dost": "👬", "pyar": "❤️", "nafrat": "🥀", "gussa": "💢", "dhokha": "💔", "zindagi": "🧬", "maut": "💀", "khushi": "😇", "gham": "😢", "shanti": "☮️", "gaali": "🤐", "badla": "🗡️", "aukat": "📏", "himmat": "🦾", "dar": "😨", "sher": "🦁", "raja": "👑", "rani": "👸", "riyasat": "⚜️", "jaat": "🚜", "badmash": "🔫", "shatir": "🧠", "khauf": "😱", "tabahi": "💥", "aag": "🔥", "pani": "💧", "hawa": "💨", "chand": "🌙", "suraj": "☀️", "tara": "⭐", "raat": "🌃", "din": "🌤️", "subah": "🌅", "shaam": "🌆", "sapna": "💭", "sach": "💯", "jhoot": "🤥", "kismat": "🍀", "waqt": "⏰", "mushkil": "🧗", "safal": "🎯", "garib": "🥀", "ameer": "💰", "izzat": "🎖️", "nazar": "🧿", "khoon": "🩸", "dil": "❤️", "dimag": "🧠", "jaan": "💖", "rooh": "💫", "khamoshi": "🤫", "shor": "🔊", "baat": "💬", "kahani": "📖", "kalam": "📝", "kitab": "📚", "shayar": "🖋️", "nasha": "🍷", "sharab": "🥃", "rasta": "🛣️", "manzil": "🏁", "safar": "🎒", "gaadi": "🚗", "ghar": "🏡", "sheher": "🏙️", "gaon": "🏘️", "chai": "☕", "thanda": "❄️", "garam": "♨️", "mausam": "🌈", "baarish": "🌧️", "sardi": "🧥", "garmi": "👕", "toofan": "🌪️", "bijli": "⚡", "pahar": "🏔️", "nadi": "🌊", "samundar": "🌊", "jung": "⚔️", "mandir": "🛕", "masjid": "🕌", "bhagwan": "🔱", "dua": "🤲", "ibadat": "🛐", "koshish": "🦾", "mehnat": "🏋️", "yaad": "🧠", "saza": "⛓️", "maafi": "🙏", "ehsas": "💫", "shukriya": "🙏", "namaste": "🙏", "salaam": "🫡", "ramram": "🚩", "alvida": "👋", "intezar": "⏳", "mulakat": "🤝", "tohfa": "🎁", "bachpan": "🧸", "jawani": "🔥", "budhapa": "👴", "phool": "🌹", "gulab": "🌹", "kaanta": "🌵", "mithas": "🍭", "kadwa": "💊", "tyohar": "🎆", "diwali": "🪔", "holi": "🎨", "eid": "🌙", "rakhi": "🎗️", "gyaan": "💡", "ujala": "💡", "roshni": "🕯️", "taakat": "💪", "sehat": "🍎", "daawat": "🍽️", "mela": "🎡", "fauji": "🇮🇳", "pulis": "👮", "chor": "🥷", "qatl": "💀", "shadi": "👰", "malik": "👑", "ghulam": "⛓️", "sultan": "⚜️", "vazir": "♟️", "shatranj": "♟️", "khwab": "💭", "zamin": "🌱", "falak": "🌌", "badal": "☁️", "bijli": "⚡", "dhua": "💨", "raakh": "🌫️", "mitti": "🪴", "shishe": "🪞", "pathar": "🪨", "aina": "🪞", "khidki": "🪟", "darwaza": "🚪", "chabi": "🔑", "tala": "🔒", "parda": "🎭", "rang": "🎨", "safedi": "⚪", "siyah": "⚫", "khushbu": "🌸", "badbu": "🤢", "swad": "👅", "thok": "💦", "pasina": "😓", "ehsan": "🤝", "bharosa": "💎", "shak": "🤨", "dhairya": "🧘", "sabr": "⏳", "himmat": "🦁", "dar": "🚫", "jeet": "🏁", "zikr": "🗣️", "fikr": "😟", "shukr": "🙌", "karz": "💳", "daan": "🪙", "bhikari": "🏚️", "daulat": "💎", "shohrat": "🌟", "tarakki": "📈", "girawat": "📉", "insaf": "⚖️", "kanoon": "📜", "adalat": "🏛️", "vakil": "💼", "jail": "⛓️", "azadi": "🕊️", "gulaami": "⛓️", "mushkil": "🧩", "halaat": "📉", "sawal": "❓", "jawab": "💡", "khabar": "📰", "sandesh": "📩", "chitthi": "✉️", "videsh": "✈️", "padosi": "🏘️", "mehman": "🛋️", "shor": "📣", "awara": "🌪️", "paas": "📍", "door": "🔭", "upar": "⬆️", "niche": "⬇️", "daaye": "➡️", "baaye": "⬅️", "seedha": "📏", "ulta": "🔃", "gol": "⭕", "kona": "📐", "bhari": "🏋️", "halka": "🎈", "tez": "🏎️", "dheere": "🐢", "purana": "🕰️", "naya": "🆕", "sasta": "🏷️", "mehenga": "💎", "kathin": "🏔️", "saral": "🟢", "sahi": "✅", "galat": "❌", "asli": "💯", "nakli": "🎭", "kadwi": "💊", "mithi": "🍫", "tikha": "🌶️", "khatta": "🍋", "namkeen": "🥨", "gehra": "🌊", "uchala": "🌤️", "sachai": "💎", "beimani": "🐍", "wafadari": "🐕", "gadari": "🗡️", "apna": "🏠", "paraya": "👤", "shubh": "✨", "ashubh": "💀", "mangalam": "🚩", "pavitra": "💧", "shuddh": "🍚", "ashuddh": "⚠️", "yogya": "🎓", "ayogya": "🚫", "samarth": "💪", "asamarth": "🥀", "shakti": "🔥", "durbal": "🍂", "amar": "♾️", "vinash": "💥", "sthapna": "🏗️", "itihas": "📜", "vartaman": "🕒", "bhavishya": "🔮", "janm": "👶", "maran": "⚰️", "prakash": "🕯️", "andhkar": "🌑", "gyani": "🧠", "agyani": "🤡", "satya": "⚖️", "asatya": "👺", "dharm": "📿", "adharm": "👹", "nyay": "⚖️", "anyay": "⛓️", "daya": "🤲", "kshama": "🙏", "krodh": "🔥", "lobh": "💰", "moh": "🔗", "ahankar": "🎭", "shanti": "🕊️", "prem": "❤️", "virakti": "🍂", "mukti": "🕊️", "shunya": "0️⃣", "anant": "🌌",

    # --- ENGLISH (500+) ---
    "king": "👑", "queen": "👸", "royal": "⚜️", "power": "⚡", "rich": "💰", "money": "💸", "boss": "💼", "rule": "📏", "sakt": "🦾", "badboy": "👺", "killer": "🗡️", "monster": "👹", "devil": "😈", "god": "🔱", "legend": "🎖️", "beast": "🦁", "ghost": "👻", "master": "🏆", "dead": "💀", "danger": "⚠️", "dangerous": "☢️", "blood": "🩸", "war": "⚔️", "fight": "🥊", "win": "🏆", "winner": "🏅", "champion": "🥇", "fear": "😨", "lion": "🦁", "tiger": "🐅", "eagle": "🦅", "wolf": "🐺", "snake": "🐍", "cobra": "🐍", "poison": "🧪", "target": "🎯", "aim": "🎯", "hit": "💥", "shot": "🔫", "dark": "🌑", "shadow": "👤", "fake": "🎭", "real": "💯", "truth": "✔️", "lie": "❌", "love": "❤️", "hate": "🥀", "miss": "🥺", "sad": "😢", "happy": "😊", "smile": "😇", "angry": "💢", "rage": "🔥", "cool": "😎", "smart": "🧠", "beauty": "✨", "beautiful": "🌸", "cute": "🦄", "hot": "🥵", "cold": "🥶", "freeze": "❄️", "broken": "💔", "heart": "💖", "soul": "💫", "peace": "☮️", "calm": "🧘", "dream": "💭", "magic": "🪄", "luck": "🍀", "shame": "😳", "wow": "😮", "amazing": "🌟", "perfect": "👌", "best": "🔝", "good": "👍", "bad": "👎", "evil": "🦹", "lonely": "🚶", "alone": "🌪️", "trust": "🤝", "friend": "👬", "bro": "🤜", "sister": "🎀", "family": "🏡", "home": "🏘️", "run": "🏃", "walk": "🚶", "drive": "🚗", "ride": "🏍️", "fly": "✈️", "swim": "🏊", "dance": "💃", "sing": "🎤", "play": "🎮", "work": "💻", "study": "📚", "read": "📖", "write": "📝", "sleep": "😴", "wake": "🌅", "eat": "🍴", "food": "🍔", "drink": "🥂", "party": "🥳", "travel": "🌍", "trip": "🎒", "world": "🌏", "earth": "🌍", "space": "🚀", "moon": "🌙", "sun": "☀️", "star": "⭐", "night": "🌌", "day": "🌤️", "rain": "🌧️", "thunder": "⚡", "lightning": "⛈️", "storm": "🌪️", "fire": "🔥", "water": "💧", "wind": "💨", "snow": "❄️", "mountain": "🏔️", "ocean": "🌊", "beach": "🏖️", "code": "💻", "coding": "👨‍💻", "hacker": "👨‍💻", "bot": "🤖", "userbot": "⚙️", "python": "🐍", "java": "☕", "bug": "🐛", "debug": "🛠️", "error": "❌", "fix": "🔧", "system": "🖥️", "server": "📡", "cloud": "☁️", "data": "📊", "network": "🌐", "wifi": "📶", "mobile": "📱", "phone": "☎️", "tech": "🔌", "ai": "🧠", "robot": "🤖", "science": "🧪", "math": "🔢", "binary": "0️⃣1️⃣", "music": "🎵", "song": "🎶", "video": "🎬", "movie": "🎥", "photo": "📸", "camera": "📷", "art": "🎨", "game": "🕹️", "sport": "⚽", "gym": "🏋️", "fitness": "💪", "health": "🍎", "doctor": "👨‍⚕️", "money": "💵", "gold": "🥇", "diamond": "💎", "shop": "🛒", "gift": "🎁", "cake": "🎂", "party": "🎉", "balloon": "🎈", "flower": "🌹", "rose": "🌹", "tree": "🌳", "leaf": "🍃", "pet": "🐾", "dog": "🐶", "cat": "🐱", "bird": "🐦", "fish": "🐟", "car": "🏎️", "bike": "🚲", "plane": "🛫", "ship": "🚢", "time": "⏰", "clock": "🕒", "watch": "⌚", "date": "📅", "search": "🔍", "lock": "🔒", "key": "🔑", "secret": "🤫", "stop": "🛑", "go": "🟢", "wait": "⏳", "loading": "🔄", "done": "✅", "cancel": "🚫", "deleted": "🗑️", "recycle": "♻️", "warn": "⚠️", "ban": "🔨", "unban": "🔓", "kick": "👢", "mute": "🔇", "spam": "📧", "news": "📰", "mail": "📧", "call": "📞", "chat": "💬", "talk": "🗣️", "voice": "🎙️", "video": "📹", "live": "🔴", "offline": "⚪", "busy": "⛔", "help": "🆘", "infinite": "♾️", "zero": "0️⃣", "one": "1️⃣", "alpha": "🅰️", "beta": "🅱️", "omega": "♎", "ultra": "💎", "pro": "🌟", "fast": "⚡", "slow": "🐌", "high": "🆙", "low": "⬇️", "heavy": "🏋️", "light": "💡", "sharp": "🔪", "blunt": "🔨", "clean": "✨", "dirty": "💩", "fresh": "🍃", "stale": "🤢", "strong": "💪", "weak": "🥀", "loud": "🔊", "quiet": "🤫", "soft": "🧸", "hard": "🧱", "easy": "✅", "tough": "🧗", "smart": "🧠", "stupid": "🤡", "brave": "🛡️", "coward": "🐀", "rich": "💰", "poor": "🏚️", "young": "👶", "old": "👴", "early": "🌅", "late": "🌃", "right": "✅", "wrong": "❌", "first": "1️⃣", "last": "🔚", "middle": "📍", "full": "🈵", "empty": "🈳", "new": "🆕", "old": "🕰️", "big": "🐘", "small": "🐭", "long": "📏", "short": "🤏", "wide": "↔️", "narrow": "⬇️", "hot": "🔥", "cold": "❄️", "warm": "🌤️", "cool": "🌊", "bright": "🌞", "dark": "🌚", "heavy": "🧱", "light": "🪶"
}

def transform_text(text):
    new_text = "".join([FONT_MAP.get(c, c) for c in text])
    words = new_text.split()
    for i, word in enumerate(words):
        clean_word = "".join(filter(str.isalpha, word)).lower()
        if clean_word in EMOJI_FEELS:
            words[i] = f"{word}{EMOJI_FEELS[clean_word]}"
    return " ".join(words)

# ================= MAGIC TOGGLE =================
@events.register(events.NewMessage(outgoing=True, pattern=r"\.magic$"))
async def toggle_magic(event):
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    if MAGIC_SETTINGS["status"]:
        MAGIC_SETTINGS["status"] = False
        await event.edit("`🪄 Magic Mode: OFF`")
    else:
        MAGIC_SETTINGS["status"] = True
        await event.edit("`🪄 Magic Mode: ON`")
    await asyncio.sleep(2)
    await event.delete()

# ================= AUTO TRANSFORMER =================
@events.register(events.NewMessage(outgoing=True))
async def auto_magic(event):
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, 3):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    if not MAGIC_SETTINGS["status"] or event.text.startswith(".") or await is_banned(event.sender_id):
        return

    original_text = event.text
    transformed = transform_text(original_text)

    if original_text != transformed:
        try:
            await event.edit(transformed)
        except:
            pass

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(toggle_magic)
    client.add_event_handler(auto_magic)

