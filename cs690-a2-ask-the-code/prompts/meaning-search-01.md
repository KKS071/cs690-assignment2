cat > prompts/meaning-search-01.md <<'EOF'
# Prompts for Entries 12 and 13: askcode/search_meaning.py and retrieval_meaning.csv
Tool: Claude (claude.ai chat), Claude Sonnet 5.5, 2026-10-02

1. Pasted the output of python -m askcode.check_setup (all checks passed, prices
   $0.4 in and $1.8 out) and of the first run_eval rerun after fixing the prices.
   No other text. The assistant then read search_meaning.py, embed.py and
   tests/test_search_meaning.py and wrote the implementation of cosine and
   MeaningIndex.

2. Pasted the output of python -m askcode.summary, showing retrieval_meaning
   as "not run yet". No other text. The assistant told me to put the code in
   place, run the tests, and run the meaning search.

3. Pasted the output of python -m askcode.run_eval --search meaning --no-ai
   (7 of 8), the full python -m askcode.summary output with Table 4, and the
   contents of results/retrieval_meaning.csv. The assistant explained which
   questions each search ranked higher and drafted ledger entries 12 and 13.

4. Pasted the output of pytest tests/test_search_meaning.py -v: 6 passed.
