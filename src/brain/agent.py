import os
import json
from groq import Groq
from src.brain.prompt_builder import PromptBuilder

class IntelligentAgent:
    def __init__(self, prompt_builder: PromptBuilder):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.prompt_builder = prompt_builder

    def expand_query(self, user_query: str) -> list[str]:
        """
        Uses LLM to brainstorm 3 alternative search terms for the query.
        This bridges the gap between 'live' and 'stay', or 'hate' and 'dislike'.
        """
        print(f"🧠 Brainstorming better search terms for: '{user_query}'...")
        
        system_prompt = (
            "You are a Search Optimizer. "
            "The user is asking a question about their own personal memories. "
            "Generate 3 alternative short search phrases that might appear in their notes to answer this question. "
            "Focus on synonyms (e.g., 'live' -> 'stay', 'location', 'address'). "
            "Return ONLY the 3 phrases separated by newlines. No numbering."
        )

        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
            )
            
            # Extract the 3 lines
            raw_text = completion.choices[0].message.content.strip()
            variations = [line.strip().replace("- ", "") for line in raw_text.split('\n') if line.strip()]
            
            # Always include the original query too!
            variations.append(user_query)
            
            print(f"   -> Generated Variations: {variations}")
            return variations

        except Exception as e:
            print(f"⚠️ Query Expansion Failed: {e}")
            return [user_query]

    def _convert_tools(self, mcp_tools):
        """Converts MCP tool format to Groq/OpenAI tool format."""
        if not mcp_tools:
            return None
            
        groq_tools = []
        for t in mcp_tools:
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", "No description"),
                    "parameters": t.get("inputSchema", {})
                }
            })
        return groq_tools

    def think(self, user_message: str, rag_context: str, mcp_tools=None):
        """
        Decides whether to reply with text OR call a tool.
        """
        # 1. Get the Core Identity (Soul + User + Tools)
        base_prompt = self.prompt_builder.build_system_prompt()
        
        # 2. Add Critical Tool Instructions
        tool_instructions = ""
        if mcp_tools:
            tool_names = ", ".join([t["name"] for t in mcp_tools])
            tool_instructions = (
                f"\n\nAVAILABLE TOOLS: {tool_names}\n"
                "--------------------------------------------------\n"
                "RULES FOR USING TOOLS:\n"
                "1. ONLY use a tool if the user EXPLICITLY asks for an external action (e.g. 'search github', 'create issue').\n"
                "2. DO NOT use tools to answer personal questions about the user (e.g. 'who do i hate?', 'where do i live?').\n"
                "3. Use the provided 'Context from Memory' below to answer personal questions directly.\n"
                "4. If the answer is in the Context, just say it. Do not search for it externally.\n"
                "--------------------------------------------------"
            )

        if "No relevant" in rag_context:
            rag_context = "No specific recent conversation history found."

        # 3. Construct the Message Stack
        messages = [
            {
                "role": "system", 
                "content": base_prompt + tool_instructions
            },
            {
                "role": "user", 
                "content": f"""
                Context from Memory:
                ---
                {rag_context}
                ---

                User Question: {user_message}
                
                Respond naturally.
                """
            }
        ]

        # 4. Convert tools for Llama 3
        tools = self._convert_tools(mcp_tools)

        print("🤖 Agent is thinking (with Hands)...")
        try:
            # Call LLM with tools enabled
            completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                tools=tools, # Give it hands
                tool_choice="auto"
            )
            
            message = completion.choices[0].message
            
            # Check if it wants to use a tool
            if message.tool_calls:
                print(f"✋ Agent wants to use a tool: {message.tool_calls[0].function.name}")
                return {"type": "tool_call", "data": message.tool_calls[0]}
            
            # Otherwise, just return text
            return {"type": "text", "data": message.content}

        except Exception as e:
            return {"type": "error", "data": f"Brain Error: {str(e)}"}