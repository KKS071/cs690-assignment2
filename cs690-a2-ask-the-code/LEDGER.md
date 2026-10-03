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
prompts: asked the assistant to suggest ten questions about requests, checked
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

## Entry 4
artifact:  askcode/search_words.py at commit 9bd684c
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to implement search_words from the starter
           docstring and tests; prompts/search-words-01.md
review:    The assistant drafted the implementation. I read it against steps 1
           to 6 in the docstring: question words minus STOPWORDS, a word set
           per chunk that includes the chunk name, weight log(N / df) with
           words found in no chunk skipped, score rounded to 6 places, and a
           sort on (-score, original position) so ties keep file order. I
           removed the noqa comments on the imports because they are now
           used. I did not change the logic.
checks:    pytest tests/test_search_words.py -v: 7 passed
evidence:  HANDOUT Step 3, search_words.py docstring steps 1 to 6; RUBRIC A2, A6
risk:      This is the simple version without BM25's length and repetition
           adjustments. Hidden tests could cover edge cases I did not test,
           such as repeated question words or an empty chunk list.

## Entry 5
artifact:  results/retrieval_words.csv at commit 9bd684c
tool:      askcode run_eval (no AI call), 2026-10-02
prompts:   none sent to the program; the assistant helped me read the misses;
           prompts/search-words-01.md
review:    I read every row of the CSV. hit and hit_rank are computed by
           run_eval, so there was nothing to mark by hand. q09 and q10 are
           n/a because the code cannot answer them. The right function was
           retrieved for q01, q02, q05 and q07 (all at rank 1) and missed for
           q03, q04, q06 and q08.
checks:    python -m askcode.run_eval --search words --no-ai: right function
           in the top 3 for 4 of 8 answerable questions;
           python -m askcode.check_freeze: PASS, questions last changed in
           3cbf584 before the first results commit 9bd684c
evidence:  HANDOUT Step 3; RUBRIC B2, B3
risk:      Only eight answerable questions, so one question moves the rate by
           12.5 points. The misses are not yet explained in my own words.
dataset:   questions/questions.json at commit 3cbf584; corpus requests v2.32.3
result:    right function in the top 3 for 4 of 8 answerable questions (50%);
           results/retrieval_words.csv
changed:   No change to search_words.py. I recorded q03, q04, q06 and q08 as retrieval
           misses to label in the fault table in Step 5 and to compare against meaning 
           search in Step 7.

## Entry 6
artifact:  askcode/prompt.py at commit [SHA: cefb948]
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to write build_prompt_five_part from the starter
           docstring and tests; prompts/five-part-v1.md
review:    The assistant drafted the system prompt and the builder. I read the
           printed prompt from the dry run and checked it against requirements
           1 to 6: the five labels each start a line in the required order; the
           Rules say to answer only from the code shown and to reply "not found
           in the code shown" with null file and line; the Example is a made-up
           clamp function, not one of my ten questions; the Reply format names
           answer, file and line. The system text is a module constant, so it is
           identical for every question.
checks:    pytest tests/test_prompt.py tests/test_answer.py -v: 22 passed;
           python -m askcode.run_eval --search words --context top3 --prompt
           five_part --dry-run: prompt printed for q01, estimate about 17,763
           input tokens, about $0.0036 with openai gpt-5.6-luna
evidence:  HANDOUT Step 4 part A, prompt.py requirements 1 to 6;
           RUBRIC A3, A6
risk:      The prompt has not been run against the model yet, so I do not know
           how well the rules and example work. The example uses a made-up file
           and line the model may imitate.

## Entry 7
artifact:  askcode/answer.py at commit [SHA: cefb948]
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to write parse_reply from the starter docstring
           and tests; prompts/five-part-v1.md
review:    The assistant drafted parse_reply. I read it against rules 1 to 5:
           one optional code fence whose first line is ``` or ```json and last
           line is ```; json.loads on the rest; an exact key set check; answer
           must be a non-empty string; file a non-empty string or null; line an
           int of at least 1 or null, with bool excluded because bool is an int
           in Python; file and line both null or both set. Every failure raises
           BadReply. I did not change the logic.
checks:    pytest tests/test_answer.py -v: 15 passed (the full run of
           tests/test_prompt.py and tests/test_answer.py shows 22 passed)
evidence:  HANDOUT Step 4 part B, answer.py rules 1 to 5; RUBRIC A4, A6
risk:      Replies the public tests do not cover, such as a fence that is
           indented or a duplicate key, may be handled differently by the hidden
           tests.