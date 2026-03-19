import asyncio
from telethon import events
from telethon.tl.functions.messages import DeleteHistoryRequest

# Target AI Bot Username
TARGET_BOT = "@ChatGPT_General_Bot"

@events.register(events.NewMessage(pattern=r"\.ask ?(.*)"))
async def ask_ai(event):
    client = event.client
    query = event.pattern_match.group(1).strip()
    
    if not query:
        return await event.edit("`Syntax: .ask <your query>`")

    # --- 🌀 DYNAMIC LOADING ANIMATION (Background Task) ---
    stop_loading = False
    async def loading_animation():
        # User ko bore nahi hone denge
        frames = [
            "🔍 Searching.", "🔍 Searching..", "🔍 Searching...",
            "🧠 Thinking.", "🧠 Thinking..", "🧠 Thinking...",
            "⚙️ Finalizing.", "⚙️ Finalizing..", "⚙️ Finalizing..."
        ]
        while not stop_loading:
            for frame in frames:
                if stop_loading: break
                try:
                    await event.edit(f"`{frame}`")
                    await asyncio.sleep(0.8) # Dot movement speed
                except:
                    break
    
    # Animation start kar rahe hain bina conversation block kiye
    loader_task = asyncio.create_task(loading_animation())

    try:
        # Start a hidden conversation
        async with client.conversation(TARGET_BOT, timeout=60) as conv:
            # Step 1: Start (Light Speed)
            await conv.send_message("/start")
            
            # Step 2: Gap for bot to breathe (2.1s as requested)
            await asyncio.sleep(2.1)
            await conv.send_message("/language en")
            
            # Step 3: Gap before query (2.1s as requested)
            await asyncio.sleep(2.1)
            await conv.send_message(query)
            
            # --- Step 4: SMART HOURGLASS SKIPPER ---
            # Pehla response uthao
            response = await conv.get_response()
            
            # Jab tak message mein ⌛️ ye emoji dikhega, bot rukega
            # Jaise hi bot asli result dega (jisme ⌛️ nahi hoga), loop toot jayega
            while "⌛" in response.text:
                response = await conv.get_response()
            
            # Ab hamare paas asli result hai
            answer = response.text
            
            # Animation roko
            stop_loading = True
            loader_task.cancel()

            # Final response (Speed of Light)
            final_output = f"🤖 **AI Response:**\n\n{answer}\n\n**DARK-USERBOT 💀**"
            await event.edit(final_output)

        # ================= CLEANUP (Gayab Mode) =================
        await asyncio.sleep(1) 
        entity = await client.get_input_entity(TARGET_BOT)
        await client(DeleteHistoryRequest(peer=entity, max_id=0, just_clear=False, revoke=True))
        await client.delete_dialog(TARGET_BOT)

    except asyncio.TimeoutError:
        stop_loading = True
        await event.edit("`❌ Error: AI Bot is dead or too slow!`")
    except Exception as e:
        stop_loading = True
        await event.edit(f"**Error:** `Something went wrong.`\n`Log: {str(e)}` ")
    finally:
        stop_loading = True

async def setup(client):
    client.add_event_handler(ask_ai)
    
