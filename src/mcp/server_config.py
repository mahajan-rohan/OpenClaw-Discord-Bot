import os
import subprocess
import sys

def get_server_config():
    print("🔍 DEBUG: Checking MCP Requirements...")
    
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        print("   ❌ GitHub Token MISSING in .env")
        return {}

    print("   ✅ GitHub Token found.")
    
    # 1. FIND THE GLOBAL INSTALL PATH
    try:
        npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
        npm_root = subprocess.check_output([npm_cmd, "root", "-g"], text=True).strip()
        
        # Path: <root>/@modelcontextprotocol/server-github/dist/index.js
        server_path = os.path.join(npm_root, "@modelcontextprotocol", "server-github", "dist", "index.js")
        
        if not os.path.exists(server_path):
            print(f"   ❌ File not found at: {server_path}")
            print("   👉 YOU MUST RUN: npm install -g @modelcontextprotocol/server-github")
            return {}
            
        print(f"   ✅ Found Server Script: {server_path}")

    except Exception as e:
        print(f"   ❌ Failed to find npm root: {e}")
        return {}

    config = {}

    # 2. PREPARE ENVIRONMENT (The Fix)
    # We must copy the FULL environment, otherwise Node crashes on Windows
    full_env = os.environ.copy()
    full_env["GITHUB_PERSONAL_ACCESS_TOKEN"] = token

    # 3. RUN USING 'node' DIRECTLY
    config["github"] = {
        "command": "node",
        "args": [server_path],
        "env": full_env  # <--- Passing full env prevents the CSPRNG crash
    }
    
    return config