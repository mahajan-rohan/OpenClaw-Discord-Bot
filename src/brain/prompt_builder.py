from src.memory_system.file_manager import OpenClawFileManager

class PromptBuilder:
    def __init__(self, file_manager: OpenClawFileManager):
        self.memory = file_manager

    def build_system_prompt(self) -> str:
        """
        Compiles the Soul, User, and Tools layers into a master system prompt.
        """
        soul = self.memory.read_layer("soul")
        user = self.memory.read_layer("user")
        tools = self.memory.read_layer("tools")

        system_prompt = f"""
<<<< SYSTEM IDENTITY (LAYER 1: SOUL) >>>>
{soul}

<<<< USER CONTEXT (LAYER 2: USER) >>>>
{user}

<<<< ENVIRONMENT CONFIG (LAYER 5: TOOLS) >>>>
{tools}

You are running in a Discord environment. 
Always adhere to the persona defined in Layer 1.
Utilize the user preferences defined in Layer 2.
"""
        return system_prompt.strip()