"""Step 3: find the chunks that share the most useful words with the question.

YOUR CODE. Read HANDOUT.md, Step 3, first.
Check your work with:  pytest tests/test_search_words.py
"""

from __future__ import annotations

import math

from askcode.core import STOPWORDS, Chunk, words


def search_words(question: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:
    """Return up to k chunks that best match the question by shared words.

    Scoring. The tests check the exact order this produces.

    1. Question words: the set of words(question), minus STOPWORDS.
    2. Chunk words: for each chunk, the set of words(chunk.name + "\\n" + chunk.text).
    3. For each question word w, df(w) is the number of chunks whose word set
       contains w, and N is len(chunks). Ignore question words no chunk contains.
    4. weight(w) = math.log(N / df(w)). A rare word weighs a lot; a word found in
       every chunk weighs 0.
    5. score(chunk) = the sum of weight(w) over the question words the chunk contains,
       rounded with round(score, 6). Rounding makes chunks that match the same words
       tie exactly, whatever order your code adds the weights in.
    6. Return the chunks whose score is greater than 0, highest score first, at most k
       of them. When two chunks have the same score, the one that comes first in
       `chunks` comes first.

    If the question has no words left after step 1, or chunks is empty, return [].

    This is the core idea of BM25, the standard keyword search (slide 45). BM25 adds
    adjustments for how often a word repeats and for chunk length.
    """
    if not chunks:
        return []

    # 1. Question words, without the stopwords.
    question_words = set(words(question)) - STOPWORDS
    if not question_words:
        return []

    # 2. The set of words in each chunk (its name counts too).
    chunk_words = [set(words(c.name + "\n" + c.text)) for c in chunks]

    # 3 and 4. Weight each question word by how rare it is across all chunks.
    n = len(chunks)
    weights: dict[str, float] = {}
    for w in question_words:
        df = sum(1 for cw in chunk_words if w in cw)
        if df > 0:  # ignore question words that no chunk contains
            weights[w] = math.log(n / df)

    # 5. Score each chunk: add up the weights of the question words it contains.
    scored = []
    for position, (chunk, cw) in enumerate(zip(chunks, chunk_words)):
        score = round(sum(weight for w, weight in weights.items() if w in cw), 6)
        if score > 0:
            scored.append((score, position, chunk))

    # 6. Highest score first; ties keep the original order (lower position first).
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in scored[:k]]