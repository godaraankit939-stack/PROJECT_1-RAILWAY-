import asyncio
import random
from telethon import events
from config import SRAID_F, SRAID_L, FLIRT, OWNER_ID, AURA_LINES
from database import is_sudo

# ALPHA style Raid Strings (Backup)
ALPHA_RAIDS = [
    "Beta reply de, dar gaya kya? 😂",
    "Tera baap aaya hai, niche jhuk ke reh!",
    "Aukat bhul gaya apni? Yaad dilau kya?",
    "Hawa nikal gayi? Itna hi dum tha?",
    "Chat chhod ke bhagne wale, tujhse na ho payega."
]

async def setup(client):
    
    # --- .raid command ---
    @client.on(events.NewMessage(pattern=r"\.raid (\d+)", outgoing=True))
    async def raid_handler(event):
        args = event.pattern_match.group(1)
        count = int(args)
        
        # Pehle raid.txt dhundega, nahi to ALPHA logic
        try:
            with open("raid.txt", "r") as f:
                raids = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            raids = ALPHA_RAIDS

        await event.delete()
        for _ in range(count):
            msg = random.choice(raids)
            await event.respond(msg)
            await asyncio.sleep(0.5) # ALPHA style flood protection

    # --- .sraid (Shayari Raid) ---
    @client.on(events.NewMessage(pattern=r"\.sraid (f|l) (\d+)", outgoing=True))
    async def sraid_handler(event):
        mode = event.pattern_match.group(1)
        count = int(event.pattern_match.group(2))
        
        # Jo lines tumne di thi (config.py se)
        pack = SRAID_F if mode == 'f' else SRAID_L
        
        await event.delete()
        for _ in range(count):
            msg = random.choice(pack)
            await event.respond(msg)
            await asyncio.sleep(0.8)

    # --- .flirt (Flirt Pack) ---
    @client.on(events.NewMessage(pattern=r"\.flirt (\d+)", outgoing=True))
    async def flirt_handler(event):
        count = int(event.pattern_match.group(1))
        await event.delete()
        for _ in range(count):
            msg = random.choice(FLIRT)
            await event.respond(msg)
            await asyncio.sleep(0.8)

    # --- OWNER AURA PROTECTION ---
    @client.on(events.NewMessage(incoming=True))
    async def aura_handler(event):
        # Agar koi owner ke PM mein .cmd try kare
        if event.is_private and event.sender_id != OWNER_ID:
            if event.text.startswith("."):
                # Tumhari Aura lines use hongi
                msg = random.choice(AURA_LINES)
                await event.reply(f"**{msg}**")
              
