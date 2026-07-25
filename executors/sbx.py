import subprocess
import time
import uuid

from executors.base import Executor


class SBXExecutor(Executor):
    def execute(self, command: list[str]) -> dict:
        start = time.perf_counter()
        unique_name = f"eval-{uuid.uuid4().hex[:8]}"

        create_command = [
            "sbx",
            "create",
            "shell",
            ".",
            "--name",
            unique_name,
        ]
        exec_args = list(command)
        if exec_args and exec_args[0] == "python":
            exec_args[0] = "python3"

        exec_command = [
            "sbx",
            "exec",
            unique_name,
            *exec_args,
        ]
        cleanup_command = ["sbx", "rm", "--force", unique_name]

        create_result = subprocess.run(
            create_command,
            capture_output=True,
            text=True,
            check=False,
        )

        exec_result = None
        try:
            if create_result.returncode == 0:
                exec_result = subprocess.run(
                    exec_command,
                    capture_output=True,
                    text=True,
                    check=False,
                )
        finally:
            cleanup_result = subprocess.run(
                cleanup_command,
                capture_output=True,
                text=True,
                check=False,
            )

        duration_ms = round(
            (time.perf_counter() - start) * 1000,
            3,
        )

        if create_result.returncode != 0:
            return {
                "executor": "sbx",
                "command": command,
                "stdout": create_result.stdout,
                "stderr": create_result.stderr,
                "exit_code": create_result.returncode,
                "duration_ms": duration_ms,
            }

        if exec_result is None:
            exec_result = create_result

        return {
            "executor": "sbx",
            "command": command,
            "stdout": exec_result.stdout,
            "stderr": exec_result.stderr,
            "exit_code": exec_result.returncode,
            "duration_ms": duration_ms,
        }
