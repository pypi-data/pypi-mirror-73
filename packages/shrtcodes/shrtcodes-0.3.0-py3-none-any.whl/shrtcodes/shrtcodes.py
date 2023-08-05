import ast
import re
from typing import List, Dict, Callable, Tuple, Optional


class Shrtcodes:
    def __init__(self):
        self.handlers: Dict[str, Callable[..., str]] = {}
        self.block_handlers: Dict[str, Callable[..., str]] = {}

    def register(self, name: str):
        def decorator(handler: Callable[..., str]):
            self.handlers = {**self.handlers, name: handler}
            return handler

        return decorator

    def register_paired(self, name: str):
        def decorator(handler: Callable[..., str]):
            self.block_handlers = {**self.block_handlers, name: handler}
            return handler

        return decorator

    @staticmethod
    def _find_shortcode_start(lines: List[str], handler_name: str) -> Tuple[int, List]:
        regex = re.compile(r"{%\s*" + handler_name + r"(\s.*\s)?\s*%}")
        for idx, line in enumerate(lines):
            match = regex.match(line)
            if match:
                params = (
                    ast.literal_eval(f"[{match.group(1)}]") if match.group(1) else []
                )
                return idx, params
        return -1, []

    @staticmethod
    def _find_shortcode_end(lines: List[str], handler_name: str) -> int:
        regex = re.compile(r"{%\s*end" + handler_name + r"(\s.*\s)?\s*%}")
        for idx, line in enumerate(lines):
            match = regex.match(line)
            if match:
                return idx
        return -1

    def process(self, text: str) -> str:
        lines = text.splitlines()

        for handler_name, handler in self.handlers.items():
            while True:
                start_idx, params = self._find_shortcode_start(lines, handler_name)
                if start_idx < 0:
                    break
                lines = lines[:start_idx] + [handler(*params)] + lines[start_idx + 1 :]

        for handler_name, handler in self.block_handlers.items():
            while True:
                start_idx, params = self._find_shortcode_start(lines, handler_name)
                if start_idx < 0:
                    break
                end_idx = self._find_shortcode_end(lines, handler_name)
                block = "\n".join(lines[start_idx + 1 : end_idx])
                lines = (
                    lines[:start_idx] + [handler(block, *params)] + lines[end_idx + 1 :]
                )

        return "\n".join(lines)
