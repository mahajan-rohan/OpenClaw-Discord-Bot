from src.mcp.client import MCPClient
from src.mcp.server_config import get_server_config

class MCPManager:
    def __init__(self):
        self.clients = {}

    async def start_all(self):
        """Starts all servers defined in server_config."""
        configs = get_server_config()
        
        if not configs:
            print("⚠️ No MCP servers configured (Check .env for tokens)")
            return

        for name, cfg in configs.items():
            client = MCPClient(
                name=name,
                command=cfg["command"],
                args=cfg["args"],
                env=cfg.get("env")
            )
            await client.start()
            self.clients[name] = client

    async def list_available_tools(self):
        """Aggregates tools from all connected servers."""
        all_tools = []
        for name, client in self.clients.items():
            try:
                result = await client.list_tools()
                if result and "tools" in result:
                    for t in result["tools"]:
                        t["server"] = name  # Tag the source
                        all_tools.append(t)
            except Exception as e:
                print(f"❌ Failed to list tools for {name}: {e}")
        return all_tools