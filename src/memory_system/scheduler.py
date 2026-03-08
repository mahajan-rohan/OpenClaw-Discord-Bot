import asyncio
import os
import discord
import dateparser
from datetime import datetime
from src.memory_system.file_manager import OpenClawFileManager

class HeartbeatSystem:
    def __init__(self, memory_manager: OpenClawFileManager, bot):
        self.memory = memory_manager
        self.bot = bot
        try:
            self.channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
            print(f"💓 Heartbeat: Target Channel ID = {self.channel_id}")
        except (TypeError, ValueError):
            self.channel_id = None
            print("⚠️ Heartbeat Warning: DISCORD_CHANNEL_ID not set in .env")

    async def start_pulse(self):
        """Main loop: Checks tasks every 60 seconds."""
        print("💓 Heartbeat System: Started.")
        while True:
            try:
                # Run the check
                await self.check_tasks()
                
                # Wait 60 seconds (Debug: reduced to 10s for faster testing)
                await asyncio.sleep(10) 
            except Exception as e:
                print(f"💔 Heartbeat Loop Error: {e}")
                await asyncio.sleep(10)

    async def check_tasks(self):
        """Parses 4_heartbeat.md and alerts on due tasks."""
        # 1. READ FILE
        content = self.memory.read_layer("heartbeat")
        if not content:
            print("💓 Heartbeat: File '4_heartbeat.md' is empty or missing.")
            return

        lines = content.split('\n')
        updated_lines = []
        alerts = []
        dirty = False
        now = datetime.now()

        # 2. SCAN LINES
        for line in lines:
            if line.strip().startswith("* [ ]"):
                task_text = line.replace("* [ ]", "").strip()
                
                # DEBUG: Print what we found
                print(f"🔍 Checking Task: '{task_text}'")
                
                # 3. PARSE TIME
                # Force 'past' settings so "1 min ago" triggers immediately
                dt = dateparser.parse(task_text, settings={'PREFER_DATES_FROM': 'past'})
                
                if dt:
                    print(f"   -> Parsed Time: {dt} | Current Time: {now}")
                    
                    if dt <= now:
                        print(f"   ✅ DUE! triggering alert.")
                        alerts.append(task_text)
                        line = line.replace("* [ ]", "* [x]")
                        dirty = True
                    else:
                        print(f"   ⏳ Not due yet.")
                else:
                    print(f"   ❌ Could not parse time from text.")
            
            updated_lines.append(line)

        # 4. SAVE & ALERT
        if dirty:
            self.memory.write_layer("heartbeat", "\n".join(updated_lines))
        
        if alerts and self.channel_id:
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                for alert in alerts:
                    await channel.send(f"⏰ **REMINDER:** {alert}")
            else:
                print(f"❌ Heartbeat Error: Could not find channel {self.channel_id}")