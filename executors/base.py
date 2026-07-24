from abc import ABC, abstractmethod
from typing import Any


class Executor(ABC):
    @abstractmethod
    def execute(self, command: list[str]) -> dict[str, Any]:
        """Execute a command and return runtime evidence."""
