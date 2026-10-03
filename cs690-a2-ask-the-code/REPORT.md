# Assignment 2 Report: Ask the Code

Name: Kundan Singh  
Provider and model: OpenAI, gpt-5.6-luna  
Prices used (per million tokens, input and output), and the page you found them on:  
$0.40 input and $1.80 output, from https://developers.openai.com/api/docs/pricing

## Table 1. Finding the right function

| Run | Right function in top 3 |
| --- | --- |
| retrieval_words | 4 of 8 |
| retrieval_meaning | 7 of 8 |

## Table 2. Answers

| Run | Valid JSON | Right place | Correct (your marks) | Input tokens | Output tokens | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| top3_words_five_part | 10 of 10 | 6 of 10 | 5 of 10 | 16,913 | 385 | 0.0075 |
| whole_five_part | 10 of 10 | 10 of 10 | 9 of 10 | 549,048 | 400 | 0.2203 |
| gold_five_part | 10 of 10 | 10 of 10 | 9 of 10 | 6,075 | 394 | 0.0031 |
| top3_words_minimal | 3 of 10 | 1 of 10 | 1 of 10 | 13,123 | 2,498 | 0.0097 |

## 1. Whose fault is it? (Step 5)

| Question | Hit in top 3 | Correct with gold context | Fault | Evidence |
| --- | --- | --- | --- | --- |
| q03 | no | yes | retrieval | The top 3 were three HTTPAdapter methods and did not include select_proxy, so the reply only said the proxy is passed to select_proxy and never explained how it is chosen; with gold it gave the correct key order. |
| q04 | no | yes | retrieval | The top 3 were HTTPAdapter.send, resolve_redirects and build_connection_pool_key_attributes, so the model replied "not found in the code shown"; with merge_setting in front of it, it answered correctly. |
| q05 | yes | no | generation | rebuild_method was ranked first, yet the reply said only that a 301 turns a POST into a GET and left out 302 and 303, and the gold run gave the same incomplete answer. |
| q06 | no | yes | retrieval | The top 3 were rebuild_proxies, proxy_headers and HTTPBasicAuth.__call__, so the reply said that _basic_auth_str is called but not how the string is built; the gold run described the colon join, Base64 and the "Basic " prefix. |
| q08 | no | yes | retrieval | The top 3 were build_response, Session.__init__ and Response.__init__, so the reply named CaseInsensitiveDict but never said that keys are stored in lowercase; the gold run said so. |

## 2. Paste everything or search? (Step 5)

Searching with word search (top3_words_five_part) got 5 of 10 correct using 16,913 input tokens for $0.0075. Pasting the whole codebase (whole_five_part) got 9 of 10 correct using 549,048 input tokens for $0.2203, which is about 32 times the tokens and about 29 times the cost. Pasting gave clearly better answers because the four extra correct answers (q03, q04, q06 and q08) were all questions where word search had not found the right function. For ten questions the extra cost was only about 21 cents, so here it was worth it.

## 3. Minimal prompt against five-part prompt (Step 6)

The five-part prompt did better on both measures. On right place it scored 6 of 10 against 1 of 10 for the minimal prompt, and on correct it scored 5 of 10 against 1 of 10. It also produced valid JSON for 10 of 10 questions, against 3 of 10 for the minimal prompt. The replies differed on q05: the minimal prompt's answer listed 303, 302 and 301, which is the full answer, but it wrote the line as the text "340-351", so it failed the check and was marked wrong. The five-part prompt gave a valid reply with line 350, but its answer mentioned only 301.

## 4. Word search against meaning search (Step 7)

Meaning search ranked q04 higher: word search did not find merge_setting in its top 3, and meaning search ranked it 1. Word search ranked q02 higher: it put get_encoding_from_headers at rank 1 and meaning search put it at rank 2. I think meaning search won q04 because the question describes combining two sets of options in everyday words, and merge_setting does that, while word search was pulled toward longer functions that mention "request" and "session" many times. I think word search won q02 because the question uses "Content-Type", "charset" and "encoding", which appear almost literally in that function, whereas meaning search ranked Response.text, a function on the same topic, just above it.

## 5. Your decision rule (Step 8)

For this codebase I would paste everything, because it is only about 55,000 tokens and pasting got 9 of 10 correct for $0.2203, against 5 of 10 for $0.0075 with word search. I would switch to searching when the code no longer fits comfortably in one prompt, or when I would ask many questions, because pasting costs about $0.022 per question against about $0.00075 per question for searching, and that difference grows with every question (about $22 against $0.75 for a thousand questions). When I do search, I would use meaning search, which found the right function for 7 of 8 questions against 4 of 8 for word search, though I did not test it with the AI.