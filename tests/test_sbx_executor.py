import types

from evidence.runtime import validate_runtime_evidence
from executors.sbx import SBXExecutor


def test_sbx_executor_captures_success(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(command, capture_output, text, check):
        calls.append(command)
        if command[1] == "create":
            return types.SimpleNamespace(
                stdout="created\n",
                stderr="",
                returncode=0,
            )
        if command[1] == "exec":
            return types.SimpleNamespace(
                stdout="sandbox works\n",
                stderr="",
                returncode=0,
            )
        return types.SimpleNamespace(
            stdout="",
            stderr="",
            returncode=0,
        )

    monkeypatch.setattr("executors.sbx.subprocess.run", fake_run)

    evidence = SBXExecutor().execute(["echo", "hello"])

    validate_runtime_evidence(evidence)

    assert evidence["executor"] == "sbx"
    assert evidence["exit_code"] == 0
    assert evidence["stdout"] == "sandbox works\n"
    assert evidence["stderr"] == ""
    assert evidence["duration_ms"] >= 0
    assert calls[0][:3] == ["sbx", "create", "shell"]
    assert calls[1][:2] == ["sbx", "exec"]
    assert calls[2][:2] == ["sbx", "rm"]


def test_sbx_executor_captures_failure(monkeypatch) -> None:
    def fake_run(command, capture_output, text, check):
        if command[1] == "exec":
            return types.SimpleNamespace(
                stdout="",
                stderr="sandbox failed\n",
                returncode=3,
            )
        if command[1] == "create":
            return types.SimpleNamespace(stdout="", stderr="", returncode=0)
        return types.SimpleNamespace(stdout="", stderr="", returncode=0)

    monkeypatch.setattr("executors.sbx.subprocess.run", fake_run)

    evidence = SBXExecutor().execute(["python", "-c", "print('x')"])

    validate_runtime_evidence(evidence)

    assert evidence["executor"] == "sbx"
    assert evidence["exit_code"] == 3
    assert evidence["stdout"] == ""
    assert evidence["stderr"] == "sandbox failed\n"
