"""Step 2: split the codebase into chunks, one per function or method.

YOUR CODE. Read HANDOUT.md, Step 2, first.
Check your work with:  pytest tests/test_split.py
"""

from __future__ import annotations

import ast
from pathlib import Path

from askcode import CORPUS_DIR
from askcode.core import Chunk


def split_file(path: Path, root: Path) -> list[Chunk]:
    """Return one Chunk for every function and method in the Python file at `path`.

    Rules. The tests check every one.

    1. Make a chunk for each `def` or `async def` that sits directly in the module,
       and for each `def` or `async def` that sits directly in a class that sits
       directly in the module. Nothing else becomes a chunk: not code outside
       functions, not a class with no methods, not a function nested inside another
       function, not a class nested inside a class, and not a function defined inside
       an `if`, `try`, `for`, `while` or `with` block at module level.
    2. name is the function name, or "ClassName.method_name" for a method.
    3. start_line is the line of the `def`, or the line of the first decorator if the
       function has decorators. end_line is the last line of the function.
       Both count from 1.
    4. text is exactly the source lines start_line to end_line, joined with "\\n".
       Split the file's text on "\\n" (not with str.splitlines) so your line numbers
       agree with the ones ast reports.
    5. file is the path of `path` relative to `root`, written with forward slashes,
       e.g. "sessions.py" or "sub/module.py".
    6. Return the chunks in the order they appear in the file.

    Hint: ast.parse(source) gives you a tree. tree.body lists the top-level
    statements. A function node has .name, .lineno, .end_lineno and .decorator_list,
    and each decorator node has its own .lineno. A class node has .name and .body.
    Read the file with encoding="utf-8".
    """
    source = path.read_text(encoding="utf-8")
    lines = source.split("\n")
    tree = ast.parse(source)
    file_name = path.relative_to(root).as_posix()

    def make_chunk(node, name: str) -> Chunk:
        # A decorated function starts at its first decorator, not at the def line.
        start = min([node.lineno] + [d.lineno for d in node.decorator_list])
        end = node.end_lineno
        return Chunk(
            file=file_name,
            name=name,
            start_line=start,
            end_line=end,
            text="\n".join(lines[start - 1 : end]),
        )

    chunks: list[Chunk] = []
    for node in tree.body:  # only top-level statements, so nested code is skipped
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            chunks.append(make_chunk(node, node.name))
        elif isinstance(node, ast.ClassDef):
            for item in node.body:  # only directly inside the class
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    chunks.append(make_chunk(item, f"{node.name}.{item.name}"))
    return chunks


def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:
    """Return the chunks of every .py file under `root`, including subfolders.

    Process the files in order of their relative path, written with forward slashes
    and sorted as plain strings. Keep each file's chunks in file order.
    For the requests codebase this returns 230 chunks.
    """
    paths = sorted(root.rglob("*.py"), key=lambda p: p.relative_to(root).as_posix())
    chunks: list[Chunk] = []
    for path in paths:
        chunks.extend(split_file(path, root))
    return chunks
