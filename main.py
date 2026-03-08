# import sys
# import os
# import discord
# from discord.ext import commands
# import config
# from src.memory_system.file_manager import OpenClawFileManager
# from src.brain.prompt_builder import PromptBuilder
# from src.rag_engine.indexer import RAGController 
# from src.memory_system.extractor import IntelligentExtractor
# from src.brain.agent import IntelligentAgent
# from src.mcp.manager import MCPManager

# # Add the project root directory to Python's path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # 1. Initialize Systems
# print("Initializing OpenClaw Memory Core...")
# memory_manager = OpenClawFileManager(config.MEMORY_ROOT_DIR)
# prompt_builder = PromptBuilder(memory_manager)

# print("Initializing RAG Engine...")
# rag = RAGController()
# extractor = IntelligentExtractor(memory_manager) # <--- INIT EXTRACTOR

# print("Initializing agent...")
# agent = IntelligentAgent(prompt_builder)

# print("Initializing MCP Manager...")
# mcp_manager = MCPManager()

# # 2. Setup Discord Bot
# intents = discord.Intents.default()
# intents.message_content = True

# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
#     print(f"🧠 RAG Memory Size: {rag.vector_store.count()} memories stored.")
#     print("--------------------------------------------------")
#     print("Phase 2: Brain is ACTIVE.")

# @bot.event
# async def on_message(message):
#     # Don't let the bot talk to itself
#     if message.author == bot.user:
#         return

#     # --- 1. ANALYSIS & INDEXING ---
#     is_command = message.content.startswith("!")
#     is_mention = bot.user.mentioned_in(message)
#     is_question = "?" in message.content

#     # Only process statements (facts), NOT questions/commands
#     if not is_command and not is_mention and not is_question:
#         print(f"🤔 Analyzing: '{message.content[:30]}...'")
        
#         # A. Short-Term Memory (Vector DB)
#         rag.index_message(message)
        
#         # B. Long-Term Core Memory (OpenClaw Layers)
#         # This decides if it goes into 2_user.md or 3_memory.md
#         extractor.process_message(message.content)

#     # --- 2. RESPONSE GENERATION ---
#     if is_mention:
#         async with message.channel.typing():
#             clean_query = message.content.replace(f"<@{bot.user.id}>", "").strip()
            
#             # A. Gather Context
#             rag_context = rag.retrieve_context(clean_query)
            
#             # B. Let the Agent Think
#             # The Agent automatically reads the User/Memory layers via prompt_builder
#             response = agent.think(user_message=clean_query, rag_context=rag_context)
            
#             await message.channel.send(response)

#     await bot.process_commands(message)

# # Run
# if __name__ == "__main__":
#     bot.run(config.DISCORD_TOKEN)


# -----------------------------------------------------------------

# import sys
# import os
# import discord
# from discord.ext import commands
# import config

# # --- IMPORTS ---
# from src.memory_system.file_manager import OpenClawFileManager
# from src.brain.prompt_builder import PromptBuilder
# from src.rag_engine.indexer import RAGController
# from src.memory_system.extractor import IntelligentExtractor
# from src.brain.agent import IntelligentAgent
# from src.mcp.manager import MCPManager  # <--- PHASE 4: THE HANDS

# # --- INITIALIZATION ---
# print("Initializing OpenClaw Memory Core...")
# memory_manager = OpenClawFileManager(config.MEMORY_ROOT_DIR)
# prompt_builder = PromptBuilder(memory_manager)

# print("Initializing RAG Engine...")
# rag = RAGController()

# print("Initializing Intelligence Layer...")
# extractor = IntelligentExtractor(memory_manager)
# agent = IntelligentAgent(prompt_builder)

# print("Initializing MCP Manager...")
# mcp_manager = MCPManager()  # <--- PHASE 4 INIT

# # --- DISCORD SETUP ---
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    
#     # --- PHASE 4: CONNECT TO GITHUB (MCP) ---
#     print("🔌 Connecting to MCP Servers (GitHub)...")
#     await mcp_manager.start_all()
    
#     # Verify Connection
#     tools = await mcp_manager.list_available_tools()
#     print(f"🛠️  MCP Tools Active: {len(tools)} tools loaded.")
#     for t in tools[:3]: # Print first 3 to verify
#         print(f"   - [{t['server']}] {t['name']}")
#     # ----------------------------------------

#     print(f"🧠 RAG Memory Size: {rag.vector_store.count()} memories stored.")
#     print("--------------------------------------------------")
#     print("🚀 OpenClaw System Online.")

# @bot.event
# async def on_message(message):
#     # Don't let the bot talk to itself
#     if message.author == bot.user:
#         return

#     # --- 1. ANALYSIS & INDEXING ---
#     is_command = message.content.startswith("!")
#     is_mention = bot.user.mentioned_in(message)
#     is_question = "?" in message.content

#     # Only process statements (facts), NOT questions/commands
#     if not is_command and not is_mention and not is_question:
#         print(f"🤔 Analyzing: '{message.content[:30]}...'")
        
#         # A. Short-Term Memory (Vector DB)
#         rag.index_message(message)
        
#         # B. Long-Term Core Memory (OpenClaw Layers)
#         # This decides if it goes into 2_user.md or 3_memory.md
#         extractor.process_message(message.content)

#     # --- 2. RESPONSE GENERATION ---
#     if is_mention:
#         async with message.channel.typing():
#             clean_query = message.content.replace(f"<@{bot.user.id}>", "").strip()
            
#             # A. Gather Context
#             rag_context = rag.retrieve_context(clean_query)
            
#             # B. Let the Agent Think
#             # The Agent automatically reads the User/Memory layers via prompt_builder
#             response = agent.think(user_message=clean_query, rag_context=rag_context)
            
#             await message.channel.send(response)

#     await bot.process_commands(message)

# # Run
# if __name__ == "__main__":
#     bot.run(config.DISCORD_TOKEN)


# -----------------------------------------------------------------

# import sys
# import os
# import json
# import discord
# from discord.ext import commands
# import config

# # --- IMPORTS ---
# from src.memory_system.file_manager import OpenClawFileManager
# from src.brain.prompt_builder import PromptBuilder
# from src.rag_engine.indexer import RAGController
# from src.memory_system.extractor import IntelligentExtractor
# from src.brain.agent import IntelligentAgent
# from src.mcp.manager import MCPManager

# # --- INITIALIZATION ---
# print("Initializing OpenClaw Memory Core...")
# memory_manager = OpenClawFileManager(config.MEMORY_ROOT_DIR)
# prompt_builder = PromptBuilder(memory_manager)

# print("Initializing RAG Engine...")
# rag = RAGController()

# print("Initializing Intelligence Layer...")
# extractor = IntelligentExtractor(memory_manager)
# agent = IntelligentAgent(prompt_builder)

# print("Initializing MCP Manager...")
# mcp_manager = MCPManager()

# # --- DISCORD SETUP ---
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
#     print("🔌 Connecting to MCP Servers (GitHub)...")
#     await mcp_manager.start_all()
    
#     tools = await mcp_manager.list_available_tools()
#     print(f"🛠️  MCP Tools Active: {len(tools)} tools loaded.")
#     print("--------------------------------------------------")
#     print("🚀 OpenClaw System Online.")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     # --- 1. ANALYSIS & INDEXING ---
#     is_command = message.content.startswith("!")
#     is_mention = bot.user.mentioned_in(message)
#     is_question = "?" in message.content

#     if not is_command and not is_mention and not is_question:
#         print(f"🤔 Analyzing: '{message.content[:30]}...'")
#         rag.index_message(message)
#         extractor.process_message(message.content)

#     # --- 2. RESPONSE GENERATION ---
#     if is_mention:
#         async with message.channel.typing():
#             clean_query = message.content.replace(f"<@{bot.user.id}>", "").strip()
            
#             # A. Get Tools & Context
#             mcp_tools = await mcp_manager.list_available_tools()
#             rag_context = rag.retrieve_context(clean_query)
            
#             # B. Agent Decision
#             response = agent.think(
#                 user_message=clean_query, 
#                 rag_context=rag_context,
#                 mcp_tools=mcp_tools
#             )
            
#             # C. Handle Tool Usage
#             if response["type"] == "tool_call":
#                 tool_call = response["data"]
#                 tool_name = tool_call.function.name
#                 tool_args = json.loads(tool_call.function.arguments)
                
#                 await message.channel.send(f"🛠️ **Executing Tool:** `{tool_name}`...")
                
#                 # Execute the tool via MCP
#                 # (Note: We loop through clients to find who owns the tool)
#                 result = None
#                 for client_name, client in mcp_manager.clients.items():
#                     # Try to call it on every client (simple approach)
#                     try:
#                         result = await client.call_tool(tool_name, tool_args)
#                         if result: break
#                     except: continue
                
#                 # Show Result
#                 if result:
#                     # Simplify output for Discord
#                     output = str(result)[:1800] 
#                     await message.channel.send(f"✅ **Result:**\n```json\n{output}\n```")
#                 else:
#                     await message.channel.send("❌ Tool execution failed or returned no data.")

#             # D. Handle Normal Text
#             elif response["type"] == "text":
#                 await message.channel.send(response["data"])
            
#             else:
#                 await message.channel.send(f"⚠️ Error: {response['data']}")

#     await bot.process_commands(message)

# if __name__ == "__main__":
#     bot.run(config.DISCORD_TOKEN)


# ---------------------------------------------------------------


import sys
import os
import json
import discord
from discord.ext import commands
import config

# --- IMPORTS ---
from src.memory_system.file_manager import OpenClawFileManager
from src.brain.prompt_builder import PromptBuilder
from src.memory_system.extractor import IntelligentExtractor
from src.brain.agent import IntelligentAgent
from src.mcp.manager import MCPManager
from src.rag_engine.indexer import RAGController
from src.memory_system.scheduler import HeartbeatSystem

# --- 1. INITIALIZE MEMORY & BRAIN ---
print("Initializing OpenClaw Memory Core...")
memory_manager = OpenClawFileManager(config.MEMORY_ROOT_DIR)
prompt_builder = PromptBuilder(memory_manager)

print("Initializing RAG Engine...")
rag = RAGController()

print("Initializing Intelligence Layer...")
extractor = IntelligentExtractor(memory_manager)

print("Initializing Agent...")
agent = IntelligentAgent(prompt_builder)

print("Initializing MCP Manager...")
mcp_manager = MCPManager()

# --- 2. INITIALIZE DISCORD BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. INITIALIZE HEARTBEAT (Requires 'bot') ---
print("Initializing Heartbeat...")
heartbeat = HeartbeatSystem(memory_manager, bot)


# --- 4. EVENTS ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    
    # Start MCP Services
    print("🔌 Connecting to MCP Servers (GitHub)...")
    await mcp_manager.start_all()
    
    tools = await mcp_manager.list_available_tools()
    print(f"🛠️  MCP Tools Active: {len(tools)} tools loaded.")

    # Start Autonomy Loop
    print("💓 Starting Autonomy Loop...")
    bot.loop.create_task(heartbeat.start_pulse())

    print("--------------------------------------------------")
    print("🚀 OpenClaw System Online.")

@bot.event
async def on_message(message):
    # Don't let the bot talk to itself
    if message.author == bot.user:
        return

    # --- 1. ANALYSIS & INDEXING ---
    is_command = message.content.startswith("!")
    is_mention = bot.user.mentioned_in(message)
    is_question = "?" in message.content

    # Only process statements (facts), NOT questions/commands
    if not is_command and not is_mention and not is_question:
        print(f"🤔 Analyzing: '{message.content[:30]}...'")
        
        # A. Short-Term Memory (Vector DB)
        rag.index_message(message)
        
        # B. Long-Term Core Memory (OpenClaw Layers)
        extractor.process_message(message.content)

    # --- 2. RESPONSE GENERATION ---
    if is_mention:
        async with message.channel.typing():
            clean_query = message.content.replace(f"<@{bot.user.id}>", "").strip()
            
            # --- A. INTELLIGENT SEARCH (Smart Search) ---
            # 1. Ask Brain to generate synonyms (e.g. "live" -> "stay")
            search_variations = agent.expand_query(clean_query)
            
            # 2. Search DB with ALL variations
            rag_context = rag.retrieve_context(search_variations)
            
            # 3. Get Tools
            mcp_tools = await mcp_manager.list_available_tools()
            
            # --- B. AGENT THINKING ---
            response = agent.think(
                user_message=clean_query, 
                rag_context=rag_context,
                mcp_tools=mcp_tools
            )
            
            # --- C. HANDLE ACTION (Tool Usage) ---
            if response["type"] == "tool_call":
                tool_call = response["data"]
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}
                
                await message.channel.send(f"🛠️ **Executing Tool:** `{tool_name}`...")
                
                # Execute the tool via MCP
                result = None
                for client_name, client in mcp_manager.clients.items():
                    try:
                        result = await client.call_tool(tool_name, tool_args)
                        if result: break
                    except: continue
                
                # Show Result
                if result:
                    output = str(result)[:1800] # Truncate for Discord limit
                    await message.channel.send(f"✅ **Result:**\n```json\n{output}\n```")
                else:
                    await message.channel.send("❌ Tool execution failed or returned no data.")

            # --- D. HANDLE TEXT RESPONSE ---
            elif response["type"] == "text":
                await message.channel.send(response["data"])
            
            else:
                await message.channel.send(f"⚠️ Error: {response['data']}")

    await bot.process_commands(message)

# Run
if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)