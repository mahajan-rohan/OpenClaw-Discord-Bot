import asyncio
import json
import os
from typing import Dict, List, Any, Optional

class MCPClient:
    def __init__(self, name: str, command: str, args: List[str], env: Dict[str, str] = None):
        self.name = name
        self.command = command
        self.args = args
        self.env = env if env else os.environ.copy()
        self.process: Optional[asyncio.subprocess.Process] = None
        self.request_id = 0
        self.pending_futures: Dict[int, asyncio.Future] = {}

    async def start(self):
        # Log exactly what we are running
        print(f"🔌 MCP [{self.name}]: Executing '{self.command}'...")
        
        try:
            # STANDARD MODE (No Shell) - Most stable for 'node'
            self.process = await asyncio.create_subprocess_exec(
                self.command, *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self.env
            )
            
            asyncio.create_task(self._listen_stdout())
            asyncio.create_task(self._listen_stderr())
            
            print(f"⏳ MCP [{self.name}]: Waiting 2s for boot...")
            await asyncio.sleep(2)

            print(f"⚡ MCP [{self.name}]: Sending Handshake...")
            await self.send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "openclaw-discord", "version": "1.0"}
            })
            await self.send_notification("notifications/initialized")
            print(f"✅ MCP [{self.name}]: Connected & Ready.")
            
        except Exception as e:
            print(f"❌ MCP [{self.name}] Startup Failed: {e}")

    async def list_tools(self):
        return await self.send_request("tools/list")

    async def call_tool(self, tool_name: str, arguments: Dict):
        return await self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })

    async def send_request(self, method: str, params: Any = None):
        self.request_id += 1
        req_id = self.request_id
        payload = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params: payload["params"] = params

        future = asyncio.get_running_loop().create_future()
        self.pending_futures[req_id] = future

        if self.process and self.process.stdin:
            try:
                self.process.stdin.write((json.dumps(payload) + "\n").encode())
                await self.process.stdin.drain()
            except Exception as e:
                print(f"❌ MCP [{self.name}] Write Error: {e}")
                return None

        try:
            return await asyncio.wait_for(future, timeout=10.0)
        except asyncio.TimeoutError:
            print(f"❌ MCP [{self.name}] Timeout: {method}")
            return None

    async def send_notification(self, method: str, params: Any = None):
        payload = {"jsonrpc": "2.0", "method": method}
        if params: payload["params"] = params
        if self.process and self.process.stdin:
            try:
                self.process.stdin.write((json.dumps(payload) + "\n").encode())
                await self.process.stdin.drain()
            except: pass

    async def _listen_stdout(self):
        if not self.process or not self.process.stdout: return
        while True:
            line = await self.process.stdout.readline()
            if not line: break
            try:
                decoded = line.decode().strip()
                if not decoded: continue
                
                # Check if it's JSON
                if not decoded.startswith("{"):
                    print(f"📝 MCP [LOG]: {decoded}")
                    continue

                msg = json.loads(decoded)
                if "id" in msg and msg["id"] in self.pending_futures:
                    future = self.pending_futures.pop(msg["id"])
                    if "error" in msg: future.set_exception(Exception(msg["error"]["message"]))
                    else: future.set_result(msg.get("result"))
            except: continue

    async def _listen_stderr(self):
        if not self.process or not self.process.stderr: return
        while True:
            line = await self.process.stderr.readline()
            if not line: break
            print(f"⚠️ MCP [STDERR]: {line.decode().strip()}")