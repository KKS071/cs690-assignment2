"""Step 4, part A: the five-part prompt from the Week 3 slides.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_prompt.py
"""

from __future__ import annotations

from askcode.core import NO_CODE, Chunk, Prompt, format_chunk

# The stable part of the prompt. It is a constant, so it is the same text for every
# question and every set of chunks, and it goes first (slide 26). Each label starts
# its own line. The example is a made-up one, not one of my ten questions.
SYSTEM_PROMPT = """\
Goal:
You answer questions about a Python codebase. You are shown a few functions from the
code, each with numbered lines, and one question. Give a short answer to the question
and point to the file and line that support it.

Inputs and outputs:
Input: a "Code:" section with functions from the codebase, each starting with a header
line "### file, name, lines X to Y" and followed by numbered lines, then a
"Question:" section with the question.
Output: one JSON object with a short answer, the file that holds the evidence, and
the line number of the most relevant line.

Rules:
- Answer only from the code shown. Do not use outside knowledge about the library.
- Keep the answer short, one or two sentences, and name the concrete behavior.
- Take "file" from the header of the function you used, and "line" from the line
  numbers shown for that function.
- If the code shown does not answer the question, reply with the answer
  "not found in the code shown" and null for both file and line.
- Do not guess. If you are not sure the code answers the question, use the
  "not found in the code shown" reply.

Example:
Question: What does the function clamp return when the value is above the maximum?
Reply: {"answer": "It returns the maximum, because clamp uses min(value, high).", "file": "math_utils.py", "line": 12}

Reply format:
Reply with exactly one JSON object and nothing before or after it. No Markdown, no
explanation. The object has exactly these keys:
- "answer": a string
- "file": a string, or null
- "line": an integer, or null
"file" and "line" are both null or both set.
"""


def build_prompt_five_part(question: str, chunks: list[Chunk]) -> Prompt:
    """Build the prompt your pipeline sends to the AI.

    Requirements. The tests check each one.

    1. prompt.system holds the five parts from slide 6. Each part starts on its own
       line with its label, in this order:
           Goal:
           Inputs and outputs:
           Rules:
           Example:
           Reply format:
    2. Rules tell the model to answer only from the code shown, and, when that code
       does not answer the question, to reply with the answer
       "not found in the code shown" and null for both file and line.
    3. Example holds one sample question and its correct reply written as a JSON
       object with the keys "answer", "file" and "line". Do not use one of your own
       ten questions.
    4. Reply format asks for exactly one JSON object with the keys "answer" (a string),
       "file" (a string or null) and "line" (an integer or null), with nothing before
       or after it.
    5. prompt.system is the same text for every question and every set of chunks.
       It is the stable part of the prompt, so it goes first (slide 26).
    6. prompt.user is a line "Code:", then every chunk shown with format_chunk(chunk)
       in the order given, separated by blank lines, then a line "Question:", then
       the question. The question comes last. If chunks is empty, put NO_CODE under
       "Code:" instead.
    """
    code = "\n\n".join(format_chunk(chunk) for chunk in chunks) or NO_CODE
    user = f"Code:\n{code}\n\nQuestion:\n{question}"
    return Prompt(system=SYSTEM_PROMPT, user=user)