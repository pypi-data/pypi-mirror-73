import ast
import re
from typing import List, Dict, Callable


def _cast_param(param):
    try:
        return ast.literal_eval(param)
    except:
        return param


def _find_shortcode_start(lines: List[str], handler_name: str):
    regex = re.compile("{%\\s*" + handler_name + "(\\s.*\\s)?\\s*%}")
    for idx, line in enumerate(lines):
        match = regex.match(line)
        if match:
            if match.group(1):
                params = [s.strip() for s in match.group(1).split("|")]
            else:
                params = []
            params = [_cast_param(param) for param in params]
            return idx, params
    return -1, None


def _find_shortcode_end(lines: List[str], handler_name: str):
    regex = re.compile("{%\\s*end" + handler_name + "(\\s.*\\s)?\\s*%}")
    for idx, line in enumerate(lines):
        match = regex.match(line)
        if match:
            return idx
    return -1


def make_process(
    handlers: Dict[str, Callable[..., str]] = {},
    block_handlers: Dict[str, Callable[..., str]] = {},
):
    def process(text: str):
        lines = text.splitlines()

        for handler_name, handler in handlers.items():
            while True:
                start_idx, params = _find_shortcode_start(lines, handler_name)
                if start_idx < 0:
                    break
                lines = lines[:start_idx] + [handler(*params)] + lines[start_idx + 1 :]

        for handler_name, handler in block_handlers.items():
            while True:
                start_idx, params = _find_shortcode_start(lines, handler_name)
                if start_idx < 0:
                    break
                end_idx = _find_shortcode_end(lines, handler_name)
                block = "\n".join(lines[start_idx + 1 : end_idx])
                lines = (
                    lines[:start_idx] + [handler(block, *params)] + lines[end_idx + 1 :]
                )

        return "\n".join(lines)

    return process
