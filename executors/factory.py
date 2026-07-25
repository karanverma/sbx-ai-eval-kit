from executors.local import LocalExecutor
from executors.sbx import SBXExecutor


def get_executor(name="local"):
    if name == "sbx":
        return SBXExecutor()
    return LocalExecutor()
