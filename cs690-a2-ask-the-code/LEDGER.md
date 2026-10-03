# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates and numbers are made up.

```
## Entry 2
artifact:  askcode/split.py at commit 3f2a9c1
tool:      GitHub Copilot Chat in VS Code, model Claude Haiku 4.5, 2026-09-22
prompts:   asked for an ast loop that returns methods with class-qualified names;
           prompts/split-01.md
review:    read every line; rejected its use of ast.walk, which also returned nested
           functions and broke rule 1; rewrote the loop over tree.body and class bodies
           myself; kept its decorator handling after checking it against rule 3
checks:    pytest tests/test_split.py: 8 passed
evidence:  HANDOUT Step 2, split.py docstring rules 1 to 6
risk:      I did not test a file with Windows line endings

## Entry 5
artifact:  results/top3_words_five_part.csv at commit 8d41e07
tool:      askcode run_eval, anthropic claude-haiku-4-5-20251001, 2026-09-23
prompts:   the five-part prompt in askcode/prompt.py at commit 8d41e07;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part:
           valid JSON 10 of 10, right place 6 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit 51c0e2a; corpus requests v2.32.3
result:    correct 6 of 10, 24,113 input tokens; results/top3_words_five_part.csv
changed:   two misses were retrieval failures, so I looked at why word search missed
           them before touching the prompt
```

## My entries

## Entry 1

Provider:		OPENAI
Model:			gpt-5.6-luna
Prices per 1M tokens:
	Input:		$0.40
	Output:		$1.80
Pricing page:	https://developers.openai.com/api/docs/pricing

## Entry 2
artifact: questions/questions.json at commit [SHA: 3cbf584]
tool: Claude (claude.ai chat), Sonnet 5.5, 2026-10-02
prompts: asked the AI assistant to suggest ten questions about requests, checked
         against the corpus, and draft expected answers; prompts/questions-01.md

review:    The assistant proposed the ten questions, the target functions and
           draft expected answers. I read all eight target functions
           (utils.py: default_user_agent, get_encoding_from_headers,
           select_proxy; sessions.py: merge_setting, rebuild_method; auth.py:
           _basic_auth_str; models.py: raise_for_status; structures.py:
           __setitem__) and __version__.py, and compared each expected answer
           with the code; all eight matched, so I kept them. I reworded the
           two cannot-answer answers myself. I grepped the corpus to confirm
           q09 and q10 have no answer in the code.
checks:    sed -n on each function: all 8 found with the expected behavior;
           grep -rniE "async|await" corpus/requests --include=*.py: no matches;
           grep -rniE "cache|disk": only urllib3 pool docstrings, a comment at
           sessions.py:113, and atomic_open in utils.py, none a response cache;
           json.load of questions.json: ok;
           pytest tests/test_questions.py: not run yet, needs split.py
evidence:  HANDOUT Step 1; RUBRIC B1, B2; tests/test_questions.py
risk:      sessions.py:113 mentions caching a redirect location on the response
           object, which I judged unrelated to q10. Questions came from an
           assistant, so they may be easier or harder than my own would be.

## Entry 3
artifact:  askcode/split.py at commit [SHA: 2fe73b4]
tool:      Claude (claude.ai chat), Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to implement split_file and split_corpus
           from the starter docstring and tests; prompts/split-01.md
review:    The assistant drafted the implementation. I read it against rules 1
           to 6 in the split_file docstring: tree.body and each class body
           are looped directly, so nested functions and functions inside
           if/try blocks are never visited (rule 1); the start line is the
           smallest of the def line and the decorator lines (rule 3); the
           text is the lines from start_line - 1 to end_line joined with
           "\n" after splitting on "\n" (rule 4); the path comes from
           relative_to(root).as_posix() (rule 5). I removed the noqa comment
           on import ast because ast is now used. I did not change the logic.
checks:    pytest tests/test_split.py -v: 8 passed;
           pytest tests/test_questions.py -v: 4 passed;
           python -c "from askcode.split import split_corpus;
           print(len(split_corpus()))": 230
evidence:  HANDOUT Step 2, split.py docstring rules 1 to 6; RUBRIC A1, A6
risk:      The public tests do not cover files with Windows line endings,
           decorators spread over several lines, or async def inside a class.
           The hidden tests check the same rules on more cases, so a case I
           did not think of could still fail.
