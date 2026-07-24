import subprocess
import time

from executors.base import Executor


class LocalExecutor(Executor):
    def execute(self, command: list[str]) -> dict:
        start = time.perf_counter()

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        duration_ms = round(
            (time.perf_counter() - start) * 1000,
            3,
        )

        return {
            "executor": "local",
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "duration_ms": duration_ms,
        }
