import os
from pathlib import Path
from typing import Dict, Optional

class OpenClawFileManager:
    """
    Manages the 6-layer OpenClaw memory system stored in Markdown files.
    """
    
    LAYERS = {
        "soul": "1_soul.md",
        "user": "2_user.md",
        "memory": "3_memory.md",
        "heartbeat": "4_heartbeat.md",
        "tools": "5_tools.md",
        "cron": "6_cron.md"
    }

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        self._initialize_storage()

    def _initialize_storage(self):
        """Creates the memory directory and empty layer files if they don't exist."""
        self.root.mkdir(parents=True, exist_ok=True)
        
        # Default templates for each layer
        templates = {
            "soul": "# 1. Soul\n\n**Persona:** You are OpenClaw, a helpful AI assistant.\n**Operational Limits:** Be kind and concise.",
            "user": "# 2. User\n\n**Identity:** The user is the Admin.\n**Preferences:** Likes Python.",
            "memory": "# 3. Memory\n\n* [2023-10-01] System initialized.",
            "heartbeat": "# 4. Heartbeat\n\n* [ ] Daily Check at 09:00",
            "tools": "# 5. Tools\n\n**Environment:** Discord\n**Device:** Server-1",
            "cron": "# 6. Cron Jobs\n\n* No active jobs."
        }

        for key, filename in self.LAYERS.items():
            file_path = self.root / filename
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(templates.get(key, f"# {key.capitalize()}"))
                print(f"Created new memory layer: {filename}")

    def read_layer(self, layer: str) -> str:
        """Reads content from a specific memory layer."""
        if layer not in self.LAYERS:
            raise ValueError(f"Unknown layer: {layer}. Valid layers: {list(self.LAYERS.keys())}")
        
        file_path = self.root / self.LAYERS[layer]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def update_layer(self, layer: str, content: str, mode: str = "append"):
        """Updates a specific memory layer."""
        if layer not in self.LAYERS:
            raise ValueError(f"Unknown layer: {layer}")
            
        file_path = self.root / self.LAYERS[layer]
        write_mode = "a" if mode == "append" else "w"
        
        with open(file_path, write_mode, encoding="utf-8") as f:
            if mode == "append":
                f.write(f"\n{content}")
            else:
                f.write(content)