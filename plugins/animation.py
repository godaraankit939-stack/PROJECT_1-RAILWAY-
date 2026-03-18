import asyncio
import random
from telethon import events
from database import is_banned, get_maintenance, is_sudo
from config import OWNER_ID

# --- ANIMATION HANDLER ---
# FIXED: Added proper closing brackets and simplified regex
@events.register(events.NewMessage(pattern=r"^\.(kill|ghost|earth|error|server|rain|love|hack|nuke|cyber|brain|slap|shoot|moon|heart|toss|virus|bdsm|horny|blow|cum|pounding|climax|sexmsg)$", outgoing=True))
async def animation_handler(event):
    cmd = event.pattern_match.group(1).lower()
    
    # 🛡️ SECURITY CHECKS
    if await is_banned(event.sender_id): 
        return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`🛠️ Maintenance Mode Active.`")

    try:
        if cmd == "kill":
            for s in ["⌬ `Target Locked...` 🎯", "⌬ `Sharpening Blade...` 🔪", "⌬ `Savouring Fear...` 👅", "💀 `Target Executed.`"]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "ghost":
            for s in ["⌬ `Scanning Area...` 🕵️", " ( ) ", " (•_•) ", " (•_•) 💨", "👻 `GHOST IS HERE!`"]:
                await event.edit(s); await asyncio.sleep(1.2)

        elif cmd == "earth":
            for e in ["🌍", "🌎", "🌏", "🌍", "🌎", "🌏"]:
                await event.edit(f"**⌬ 𝖶𝖮𝖱𝖫𝖣 𝖲𝖯𝖨𝖭**\n{e}"); await asyncio.sleep(0.8)

        elif cmd == "error":
            for s in ["⌬ `System Check...` 🔍", "⌬ `Err#r Found!` ⚠️", "⌬ `Critical Failure!` 🛑", "💀 `ACCESS DENIED.`"]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "server":
            for s in ["⌬ `Voltage High!` ⚡", "⌬ `System Overheating!` 🔥", "⌬ `Cooling Failed...` ❄️", "🛑 `SERVER CRASHED.`"]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "rain":
            for _ in range(3):
                for r in [" . ☁️ . ", " , . | . , ", " | . | | | "]:
                    await event.edit(f"**⌬ 𝖱𝖠𝖨𝖭𝖨𝖦 𝖵𝖨𝖡𝖤**\n{r}"); await asyncio.sleep(0.6)
            await event.edit("🌧️ `Relax, it's raining.`")

        elif cmd == "love":
            colors = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]
            for _ in range(2):
                for h in colors:
                    shape = f" {h}{h}     {h}{h} \n{h}{h}{h}{h}{h}{h}{h}\n {h}{h}{h}{h}{h}{h} \n  {h}{h}{h}{h}{h}  \n    {h}{h}{h}    \n      {h}      "
                    await event.edit(f"**⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖨𝖭 𝖫𝖮𝖵𝖤**\n\n{shape}"); await asyncio.sleep(0.3)

        elif cmd == "hack":
            for s in ["⌬ `Connecting...` 📡", "⌬ `Bypassing Firewall...` 🛡️", "⌬ `Fetching Data...` 📂", "**⌬ 𝖲𝖸▵▤𝖬 𝖧𝖠𝖢𝖪𝖤𝖣** 💀"]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "nuke":
            for i in range(3,0,-1): 
                await event.edit(f"🚀 **𝖭𝖴𝖪𝖤 𝖨𝖭: `{i}`**"); await asyncio.sleep(1.0)
            await event.edit("💥 **𝖡𝖮𝖮𝖮▵▵▬!** \n`Area Erased.`")

        elif cmd == "cyber":
            for i in range(0,101,20): 
                bar = "■" * (i // 10) + "□" * (10 - (i // 10))
                await event.edit(f"**⌬ 𝖲𝖸▵𝖳▵𝖬 𝖫▮𝖠𝖣▨𝖭𝖦**\n`[{bar}] {i}%` ⚙️"); await asyncio.sleep(1.2)
            await event.edit("⚡ **𝖢𝖸𝖡𝖤𝖱-𝖲𝖸𝖲𝖳𝖤𝖬 𝖮𝖭𝖫𝖨𝖭𝖤**")

        elif cmd == "brain":
            res = random.choice(["100% Psycho detected.", "Deep Love.", "Pure Evil Mind.", "Master of Shadows.", "High IQ."])
            await event.edit("⌬ `Scanning Brain...` 🧠"); await asyncio.sleep(1.5); await event.edit(f"**Result:** `{res}`")

        elif cmd == "slap":
            await event.edit("( •_•)"); await asyncio.sleep(0.8)
            await event.edit("( •_•)>⌐■-■"); await asyncio.sleep(0.8)
            await event.edit("(⌐■_■) 👋 *SLAP!*")

        elif cmd == "shoot":
            for s in ["Loading... 🔫", "Aiming... 🎯", "⌬ `PEW PEW!` 💥", "💀 `Target Terminated.`"]:
                await event.edit(s); await asyncio.sleep(1.2)

        elif cmd == "moon":
            for m in ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌑"]:
                await event.edit(f"**⌬ 𝖬𝖮𝖮𝖭 𝖢𝖸𝖢𝖫𝖤** \n{m}"); await asyncio.sleep(0.8)

        elif cmd == "heart":
            for b in ["───", "──√v──", "──√v^√v──", "──√v^√v^√v──", "❤️"]:
                await event.edit(f"`{b}`"); await asyncio.sleep(1)

        elif cmd == "toss":
            res = random.choice(["Heads 🪙", "Tails 🪙"])
            await event.edit("🌪️ `Flipping...` "); await asyncio.sleep(1.5); await event.edit(f"**Result:** `{res}`")

        elif cmd == "virus":
            for s in ["👾 `Injecting Virus-X...` ", "🔓 `Stripping Security...` ", "💀 `System Overridden.` "]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "bdsm":
            for s in ["1. `On your knees, slave.` 🧎", "2. `Tightening the chains...` ⛓️", "3. `No mercy, only pleasure...` 🩸", "4. `Obey the Master.` 👑", "**⌬ 𝖲𝖨𝖫𝖤𝖭𝖢𝖤 𝖨𝖲 𝖸𝖮𝖴▵ 𝖮𝖭𝖫𝖸 𝖲𝖠𝖥𝖤 𝖶𝖮𝖱𝖣.** 💀"]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "horny":
            for s in ["1. `Vibrating at 100%...` ⚡", "2. `Getting wet... with blood?` 🩸", "3. `Harder... Faster... Better.` 🌀", "4. **⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖨𝖲 𝖥𝖴*𝖪𝖨𝖭𝖦 𝖧𝖮𝖳!** 🔥", "**⌬ 𝖳▵𝖬𝖤 𝖳𝖮 𝖤𝖷𝖯𝖫𝖮𝖣𝖤.** 💦"]:
                await event.edit(s); await asyncio.sleep(1.5)

        elif cmd == "blow":
            for s in ["8=D", "8==D", "8===D", "8====D💦👅"]:
                await event.edit(f"**{s}**"); await asyncio.sleep(0.8)

        elif cmd == "cum":
            for s in ["8=D", "8=D💦", "8=D 💦 💦", "8=D  💦  💦  💦"]:
                await event.edit(f"`{s}`"); await asyncio.sleep(0.8)

        elif cmd == "pounding":
            for s in ["εつ💦(‿ˠ‿)", "εつ🔥(‿ˠ‿)", "εつ🌊(‿ˠ‿)"]:
                await event.edit(f"**{s}**"); await asyncio.sleep(0.7)

        elif cmd == "climax":
            await event.edit("( ͜. ㅅ ͜. )🥛 `yumy`")

        elif cmd == "sexmsg":
            await event.edit("𓀐𓂸🤰🏻 🤱🏻👨‍👩‍👧")

    except Exception as e:
        print(f"Error in animation: {e}")

# --- SETUP ---
async def setup(client):
    client.add_event_handler(animation_handler)
