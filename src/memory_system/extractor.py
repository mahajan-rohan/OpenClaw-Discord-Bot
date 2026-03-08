import re
from src.memory_system.file_manager import OpenClawFileManager

class IntelligentExtractor:
    def __init__(self, file_manager: OpenClawFileManager):
        self.memory = file_manager

    def process_message(self, message_content: str):
        """
        Analyzes the message and routes it to the correct memory layer.
        """
        clean_text = message_content.strip()
        lower_text = clean_text.lower()
        
        # Log the attempt
        print(f"🧠 Intelligence Active: Routing '{clean_text}'...")

        # --- ROUTING LOGIC ---
        
        # RULE A: User Preferences / Personality (Layer 2)
        # Added: "hate", "dislike", "passion", "obsessed", "fan of"
        user_triggers = [
            "i like", "i love", "i prefer", "my favorite", "i use", 
            "i hate", "i dislike", "i detest", "cant stand", "can't stand",
            "passion", "hobby", "obsessed", "fan of", "i am a", "i'm a"
        ]
        
        if any(x in lower_text for x in user_triggers):
            print("   -> Detected User Preference/Trait. Updating Layer 2 (User).")
            self.memory.update_layer("user", f"* {clean_text}")
            return "User Layer Updated"

        # RULE B: Tasks/Schedule (Layer 4)
        task_triggers = ["remind", "schedule", "todo", "must do", "deadline"]
        if any(x in lower_text for x in task_triggers):
            print("   -> Detected Task. Updating Layer 4 (Heartbeat).")
            self.memory.update_layer("heartbeat", f"* [ ] {clean_text}")
            return "Heartbeat Layer Updated"

        # RULE C: General Facts / Status (Layer 3)
        # Added: "currently", "working on", "fellowship"
        fact_triggers = [
            "i live", "i stay", "i work", "i study", "my location", 
            "currently", "doing my", "fellowship"
        ]
        if any(x in lower_text for x in fact_triggers):
            print("   -> Detected Fact. Updating Layer 3 (Memory).")
            self.memory.update_layer("memory", f"* {clean_text}")
            return "Memory Layer Updated"

        # RULE D: Default
        print("   -> No specific layer match. Keeping in Short-Term RAG only.")
        return "RAG Only"