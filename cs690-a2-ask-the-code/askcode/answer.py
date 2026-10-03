"""Step 4, part B: check the AI's reply before your program trusts it.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_answer.py
"""

from __future__ import annotations

import json

from askcode.core import BadReply

KEYS = {"answer", "file", "line"}


def parse_reply(text: str) -> dict:
    """Check the model's reply and return {"answer": ..., "file": ..., "line": ...}.

    Accept the reply only if every rule holds. Otherwise raise BadReply with a short
    message that says which rule failed. Never let a different exception escape.

    1. After stripping whitespace, the reply is one JSON object. The only thing
       allowed around it is a single Markdown code fence: a first line of ``` or
```json, and a last line of ```. Any other text before or after the object
       makes the reply bad.
    2. The object has exactly the keys "answer", "file" and "line": none missing,
       none extra.
    3. "answer" is a string that is not empty or only whitespace.
    4. "file" is a non-empty string or null. "line" is an integer or null; true and
       false do not count as integers, and an integer line must be at least 1.
    5. "file" and "line" are both null, or both set.

    Return a new dict with exactly the three keys and the values from the reply.
    """
    if not isinstance(text, str):
        raise BadReply("reply is not text")

    body = text.strip()

    # Rule 1: allow one Markdown code fence around the object, and nothing else.
    if body.startswith("```"):
        lines = body.split("\n")
        if len(lines) < 3 or lines[0].strip() not in ("```", "```json"):
            raise BadReply("code fence must start with ``` or ```json on its own line")
        if lines[-1].strip() != "```":
            raise BadReply("code fence must end with ``` on its own line")
        body = "\n".join(lines[1:-1]).strip()

    try:
        data = json.loads(body)
    except (ValueError, RecursionError):
        raise BadReply("reply is not a single valid JSON object") from None

    if not isinstance(data, dict):
        raise BadReply("reply is JSON, but not an object")

    # Rule 2: exactly the three keys.
    if set(data) != KEYS:
        raise BadReply(f"keys must be exactly answer, file and line; got {sorted(data)}")

    answer, file, line = data["answer"], data["file"], data["line"]

    # Rule 3: answer is a real string.
    if not isinstance(answer, str) or not answer.strip():
        raise BadReply("answer must be a non-empty string")

    # Rule 4: file is a non-empty string or null; line is an int >= 1 or null.
    if file is not None and (not isinstance(file, str) or not file.strip()):
        raise BadReply("file must be a non-empty string or null")
    if line is not None:
        if isinstance(line, bool) or not isinstance(line, int):
            raise BadReply("line must be an integer or null")
        if line < 1:
            raise BadReply("line must be at least 1")

    # Rule 5: file and line are both null or both set.
    if (file is None) != (line is None):
        raise BadReply("file and line must both be null or both be set")

    return {"answer": answer, "file": file, "line": line}
