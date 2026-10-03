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
artifact:  .env settings for the AI provider, model and prices (the file itself is
           never committed)
tool:      none; I set this up by hand following README.md and HANDOUT Step 0
prompts:   none; no AI tool was used for this entry
review:    Provider openai, model gpt-5.6-luna. I looked up the prices on the
           provider's pricing page, https://developers.openai.com/api/docs/pricing:
           $0.40 per million input tokens and $1.80 per million output tokens, and
           put them in PRICE_INPUT_PER_MTOK and PRICE_OUTPUT_PER_MTOK. My first
           experiment runs recorded $0.20 and $1.20 because of a wrong value in
           .env; I corrected .env and reran from the saved replies (see the risk
           lines of Entries 8 to 11).
checks:    python -m askcode.check_setup: All checks passed, with the note
           "$0.4 in and $1.8 out per million tokens"
evidence:  HANDOUT Step 0; README Setup steps 1 to 5
risk:      Prices change, so the costs in this assignment are only valid for the
           prices above on the day I ran the experiments.

## Entry 2
artifact:  questions/questions.json at commit 3cbf584
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to suggest ten questions about requests, checked
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
           pytest tests/test_questions.py -v: 4 passed (run after split.py existed)
evidence:  HANDOUT Step 1; RUBRIC B1, B2; tests/test_questions.py
risk:      sessions.py:113 mentions caching a redirect location on the response
           object, which I judged unrelated to q10. Questions came from an
           assistant, so they may be easier or harder than my own would be.

## Entry 3
artifact:  askcode/split.py at commit 2fe73b4
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
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
changed:   No change to search_words.py. I recorded q03, q04, q06 and q08 as
           retrieval misses to label in the fault table in Step 5 and to
           compare against meaning search in Step 7.

## Entry 6
artifact:  askcode/prompt.py at commit cefb948
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
           input tokens for the whole run
evidence:  HANDOUT Step 4 part A, prompt.py requirements 1 to 6;
           RUBRIC A3, A6
risk:      The prompt had not been run against the model when I wrote this
           entry, so I did not yet know how well the rules and example work.
           The example uses a made-up file and line the model may imitate.

## Entry 7
artifact:  askcode/answer.py at commit cefb948
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

## Entry 8
artifact:  results/top3_words_five_part.csv at commit 3431323
tool:      askcode run_eval, openai gpt-5.6-luna, 2026-10-02
prompts:   the five-part prompt in askcode/prompt.py at commit cefb948;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against
           questions.json: yes for q01, q02, q07, q09 and q10; no for q03, q04,
           q05, q06 and q08
checks:    python -m askcode.run_eval --search words --context top3 --prompt
           five_part: valid JSON 10 of 10, right place 6 of 10,
           16,913 input tokens, 385 output tokens, $0.0075
evidence:  HANDOUT Step 5; RUBRIC B3, B5, C2
risk:      one run only; a fresh run may answer differently. My marks are
           judgment calls on partial answers, such as q05. The first commit of
           this run (df05f3a) recorded prices of $0.20 and $1.20 from a wrong
           .env. I corrected .env and reran from saved replies, so the
           submitted file (3431323) carries $0.40 and $1.80. No API call was
           repeated.
dataset:   questions/questions.json at commit 3cbf584; corpus requests v2.32.3
result:    correct 5 of 10, 16,913 input tokens; results/top3_words_five_part.csv
changed:   four of the five wrong answers (q03, q04, q06, q08) had the right
           function missing from the top 3, so I treated them as retrieval
           failures and did not reword the prompt; I will try meaning search
           in Step 7 instead

## Entry 9
artifact:  results/gold_five_part.csv at commit 3431323
tool:      askcode run_eval, openai gpt-5.6-luna, 2026-10-02
prompts:   the five-part prompt in askcode/prompt.py at commit cefb948;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against
           questions.json: no for q05 only
checks:    python -m askcode.run_eval --context gold --prompt five_part:
           valid JSON 10 of 10, right place 10 of 10, 6,075 input tokens,
           394 output tokens, $0.0031
evidence:  HANDOUT Step 5 item 3; RUBRIC B3, B5, C2
risk:      one run only. q06 left out the Latin-1 encoding step and I counted it
           as correct because the main behavior was right. The first commit of
           this run (df05f3a) recorded prices of $0.20 and $1.20 from a wrong
           .env. I corrected .env and reran from saved replies, so the
           submitted file (3431323) carries $0.40 and $1.80. No API call was
           repeated.
dataset:   questions/questions.json at commit 3cbf584; corpus requests v2.32.3
result:    correct 9 of 10, 6,075 input tokens; results/gold_five_part.csv
changed:   gold answered q03, q04, q06 and q08 correctly, which confirms those
           were retrieval failures in top3; q05 is still wrong with the right
           code, so it is a generation failure

## Entry 10
artifact:  results/whole_five_part.csv at commit 3431323
tool:      askcode run_eval, openai gpt-5.6-luna, 2026-10-02
prompts:   the five-part prompt in askcode/prompt.py at commit cefb948;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against
           questions.json: no for q05 only
checks:    python -m askcode.run_eval --context whole --prompt five_part --dry-run
           estimated about 544,346 input tokens for the whole run; the real
           run: valid JSON 10 of 10, right place 10 of 10, 549,048 input
           tokens, 400 output tokens, $0.2203
evidence:  HANDOUT Step 5; RUBRIC B3, B5, C5
risk:      one run only; the codebase is about 55,000 tokens, so this result may
           not hold for a codebase too large to paste. The first commit of this
           run (df05f3a) recorded prices of $0.20 and $1.20 from a wrong .env.
           I corrected .env and reran from saved replies, so the submitted file
           (3431323) carries $0.40 and $1.80. No API call was repeated.
dataset:   questions/questions.json at commit 3cbf584; corpus requests v2.32.3
result:    correct 9 of 10, 549,048 input tokens, $0.2203;
           results/whole_five_part.csv
changed:   whole matched gold's 9 of 10 at about 90 times the input tokens, and
           beat top3's 5 of 10 at about 32 times; I kept the prompt unchanged
           and will use these numbers for the paste-or-search decision in the
           report

## Entry 11
artifact:  results/top3_words_minimal.csv at commit 3431323
tool:      askcode run_eval, openai gpt-5.6-luna, 2026-10-02
prompts:   the given minimal prompt (build_prompt_minimal in askcode/core.py);
           no prompt of mine; prompts/five-part-v1.md covers the session
review:    read all ten replies and marked the correct column: yes for q01
           only. q02 to q08 are no because valid_json is no (line given as a
           string such as "340-351"). q09 and q10 are no because they fill in
           file and line instead of nulls, which my answer key requires.
checks:    python -m askcode.run_eval --search words --context top3 --prompt
           minimal: valid JSON 3 of 10, right place 1 of 10, 13,123 input
           tokens, 2,498 output tokens, $0.0097
evidence:  HANDOUT Step 6; RUBRIC B3, B5, C3
risk:      one run only. My marking of q09 and q10 is strict; under a lenient
           reading the correct count would be 3 of 10. The terminal output of
           the first run showed $0.0056 because of the wrong prices in .env; I
           corrected .env and reran from saved replies before committing, so
           the committed file carries $0.40 and $1.80.
dataset:   questions/questions.json at commit 3cbf584; corpus requests v2.32.3
result:    correct 1 of 10, 13,123 input tokens, $0.0097;
           results/top3_words_minimal.csv
changed:   the five-part prompt beat the minimal one on valid JSON (10 against
           3), right place (6 against 1) and correct (5 against 1), at a lower
           cost, so I kept the five-part prompt for the other runs

## Entry 12
artifact:  askcode/search_meaning.py at commit ef56fed
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to implement cosine and MeaningIndex from the
           starter docstring and tests; prompts/meaning-search-01.md
review:    The assistant drafted the code. I read it against the docstring
           rules: cosine raises ValueError when the lengths differ and returns
           0.0 for a zero-length vector; MeaningIndex embeds every chunk once,
           as name + "\n" + text, in the order of chunks; search embeds only
           the question and sorts by (-score, position) so ties keep the chunk
           order; it always returns k chunks. I removed the noqa comment on
           import math because it is now used. I did not change the logic.
checks:    pytest tests/test_search_meaning.py -v: 6 passed;
           python -m askcode.run_eval --search meaning --no-ai: ran with the
           real local model, right function in the top 3 for 7 of 8 answerable
           questions
evidence:  HANDOUT Step 7, search_meaning.py docstring; RUBRIC A5, A6
risk:      The public tests use fake vectors, so only the real run exercised
           the embedding model. Hidden tests may check edge cases such as an
           empty chunk list or k larger than the number of chunks.

## Entry 13
artifact:  results/retrieval_meaning.csv at commit ef56fed
tool:      askcode run_eval (no AI call; local model BAAI/bge-small-en-v1.5),
           2026-10-02
prompts:   none sent to a program; prompts/meaning-search-01.md
review:    read every row of the CSV. hit and hit_rank are computed by
           run_eval. The right function was in the top 3 for q01 to q07
           (ranks 1, 2, 2, 1, 1, 3, 1) and missed for q08. q09 and q10 are n/a
           and still returned three unrelated chunks each.
checks:    python -m askcode.run_eval --search meaning --no-ai: right function
           in the top 3 for 7 of 8 answerable questions;
           python -m askcode.summary: Table 4 shows meaning search ranking
           q03, q04 and q06 where word search did not, and word search ranking
           q02 higher (1 against 2)
evidence:  HANDOUT Step 7; RUBRIC B3, C4
risk:      only eight answerable questions, so one question moves the rate by
           12.5 points. I did not run the AI on the meaning search results, so
           I do not know whether 7 of 8 retrieval turns into more correct
           answers.
dataset:   questions/questions.json at commit 3cbf584; corpus requests v2.32.3
result:    right function in the top 3 for 7 of 8 answerable questions (88%)
           against 4 of 8 for word search; results/retrieval_meaning.csv
changed:   none to the code or prompt. Meaning search recovered q03, q04 and
           q06, which were retrieval failures under word search, but q08 was
           missed by both.

## Entry 14
artifact:  REPORT.md at commit b97cb0f
tool:      Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02
prompts:   asked the assistant to draft the report from my results;
           prompts/report-01.md
review:    The assistant drafted all five sections. I compared Tables 1 and 2
           with python -m askcode.summary, checked each Section 1 evidence
           sentence against the rows in results/top3_words_five_part.csv and
           results/gold_five_part.csv, and checked the Section 4 ranks against
           Table 4. Rewrote Sections 2 to 5 in my own words, kept the tables as printed.
checks:    python -m askcode.summary: Tables 1 and 2 in REPORT.md match the
           output row for row
evidence:  HANDOUT Step 8; RUBRIC C1 to C5
risk:      The explanations of why each search won in Section 4 are my
           interpretation and were not tested.