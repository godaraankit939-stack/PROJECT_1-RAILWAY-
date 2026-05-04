import asyncio
import os
from datetime import datetime
import pytz # Indian Timezone handle karne ke liye
from telethon import events

async def setup(client):
    @client.on(events.NewMessage(pattern=r"\.snipe (\d{1,2}:\d{1,2}:\d{1,2}) (@?\w+|-\d+) (.*)", outgoing=True))
    async def ultra_sniper(event):
        # 1. Input Extraction
        target_time_str = event.pattern_match.group(1) # HH:MM:SS
        target_chat = event.pattern_match.group(2)
        message_text = event.pattern_match.group(3)

        # Indian Timezone setup
        ist = pytz.timezone('Asia/Kolkata')
        
        await event.edit(f"🎯 **Sniper Locked & Loaded!**\n\n**Time:** `{target_time_str}` (IST)\n**Target:** `{target_chat}`\n**Message:** `{message_text}`\n\n`Status: Waiting for the right millisecond...`")

        # Target time components
        t_h, t_m, t_s = map(int, target_time_str.split(':'))

        while True:
            # Current time in IST
            now = datetime.now(ist)
            
            # Phase 1: Jab target second se 1 second pehle ho (High Precision Mode)
            if now.hour == t_h and now.minute == t_m and now.second == (t_s - 1):
                
                # Phase 2: Millisecond Counting (The Kill Zone)
                while True:
                    milli_now = datetime.now(ist).microsecond // 1000
                    
                    # 935ms par fire: Taki server latency (65ms) cover ho jaye
                    # Ye tujhe manual ungli dabane se 100x fast banayega
                    if milli_now >= 935:
                        try:
                            # Direct Fire
                            await event.client.send_message(target_chat, message_text)
                            
                            # Success Log in Saved Messages
                            await event.client.send_message("me", f"✅ **SNIPER FIRED!**\nTime: `{target_time_str}`\nTarget: `{target_chat}`")
                        except Exception as e:
                            await event.client.send_message("me", f"❌ **SNIPER FAILED:** `{str(e)}`")
                        return # Task Complete
            
            # Low CPU Usage: Har 0.1s check karega jab tak target time paas na aaye
            await asyncio.sleep(0.1)

