import asyncio
import tempfile
import os
import sys
import json

class Executor:
    async def run(self, code: str, data: dict):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "solve.py")

            with open(path, "w") as f:
                f.write(code)

            proc = await asyncio.create_subprocess_exec(
                sys.executable, path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                out, err = await asyncio.wait_for(proc.communicate(), timeout=60)
            except asyncio.TimeoutError:
                return None

            if proc.returncode != 0:
                return None

            try:
                return json.loads(out.decode())
            except:
                return out.decode().strip()
