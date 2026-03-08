import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# --- DISCORD CONFIGURATION ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# --- MEMORY SYSTEM CONFIGURATION ---
# This tells the File Manager where to look for .md files
MEMORY_ROOT_DIR = "memory_core"

# --- VALIDATION ---
if not DISCORD_TOKEN:
    raise ValueError("❌ Error: DISCORD_TOKEN is missing from .env file!")

if not os.path.exists(MEMORY_ROOT_DIR):
    # Auto-create the directory if it doesn't exist
    try:
        os.makedirs(MEMORY_ROOT_DIR)
        print(f"📁 Created missing directory: {MEMORY_ROOT_DIR}")
    except OSError as e:
        print(f"⚠️ Warning: Could not create memory directory: {e}")