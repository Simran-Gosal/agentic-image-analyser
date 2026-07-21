# Testing

## Testing Strategy

Given the scope of this project, testing is structured in 3 layers:

1. Unit-level: each individual tools tested in isolation
2. Integration-level: the agent's decision making tested against the tools it calls
3. End-to-end: the full pipeline tested as a user would experience it


## 1. Unit-Level Testing

### 1.1 Vision Tool (PyTorch Captioning)

| Test ID | Test case | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| U1 | Caption a clear, simple image (single object) | e.g. photo of a dog | Coherent caption identifying the subject |  | |
| U2 | Caption a complex image (multiple objects/scene) | e.g. street scene | Caption covers the main elements without becoming incoherent |  |  |
| U3 | Caption a low-quality/blurry image | Blurry photo | Caption degrades gracefully (vague but not nonsensical), or system flags low confidence |  |  |
| U4 | Confirm no prompt-leakage bug | Any image, BLIP model | Caption does not contain literal prompt text (e.g. "contents of image:") |  |  |
| U5 | Confirm repetition penalty fix | Image with a repeated visual element (e.g. multiple identical objects) | Caption reads naturally, not forced/distorted wording |  |  |
| U6 | Confirm sampling parameters actually take effect | Same image, run twice with `do_sample=True` | Two runs produce *different* captions (proves temperature/top_p are active, not silently ignored) |  |  |

### 1.2 Web Search Tool

| Test ID | Test case | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| U7 | Search returns relevant results | A specific, well-formed query derived from a caption | Results are topically relevant to the query |  |  |
| U8 | Search handles a vague/ambiguous caption gracefully | A generic caption (e.g. "a picture of an object") | Tool does not error out; returns broad or no results without crashing |  |  |

### 1.3 Ollama LLM (Decision-Making)

| Test ID | Test case | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| U9 | LLM correctly identifies when a caption needs no further context | Caption of a simple, self-explanatory image (e.g. "a red apple on a table") | LLM decides "No — skip to report" |  |  |
| U10 | LLM correctly identifies when a caption warrants research | Caption naming something specific/notable (e.g. a landmark, named object) | LLM decides "Yes — search for more context" |  |  |
| U11 | LLM responds within reasonable local inference time | Any prompt | Response returned without excessive delay (define acceptable threshold once measured on your hardware) |  |  |

---

## 2. Integration-Level Testing

| Test ID | Test case | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| I1 | Agent correctly routes to "skip" branch | Given a simple image, no search tool is called, report generated directly from caption |  |  |
| I2 | Agent correctly routes to "search" branch | Given a research-worthy image, search tool is called and its output is incorporated into the final report |  |  |
| I3 | Agent handles a tool failure gracefully | If the web search tool errors (e.g. no internet), agent still returns a report using the caption alone, rather than crashing |  |  |
| I4 | LangGraph state passes correctly between steps | Caption generated in step 1 is the same caption the LLM reasons about in step 2 (no data loss/corruption between graph nodes) |  |  |

---

## 3. End-to-End Testing

Full pipeline tested by uploading a range of test images and confirming the complete flow works as intended.

| Image category | Purpose | Pass/Fail |
|---|---|---|
| Simple, single-subject photo | Baseline "happy path" test |  |
| Complex, multi-subject scene | Tests caption quality under complexity | |
| Recognisable landmark/notable object | Tests whether agent correctly triggers a search |  |
| Abstract/ambiguous image | Tests graceful degradation, not a crash |  |
| Very large file size | Tests the app doesn't break on realistic file sizes |  |
| Unsupported file type (e.g. .gif) | Tests input validation / error handling |  |

For each end-to-end run, confirm:
- Caption generated correctly
- Agent's routing decision (search vs. skip) is appropriate for the image
- Final report is coherent and reflects both caption and any additional context
- Streamlit interface displays the result without errors
- No unhandled exceptions in the terminal/logs during the run

---

## Known Limitations

- No automated `pytest` suite currently exists - all testing above is manual, run and recorded by hand
- Test image set is small and manually chosen, not a large or statistically representative sample
- LLM decision-making (search vs. skip) is inherently somewhat non-deterministic; the same image may not always produce identical routing decisions across runs

## What I'd Improve

- Convert the unit-level tests above into an automated `pytest` suite for the vision tool and agent logic
- Build a fixed, version-controlled set of test images with recorded expected outcomes, to catch regressions after future code changes
- Add basic logging/metrics (e.g. how often the agent chooses to search vs. skip) to monitor behaviour over more runs than manual testing alone would cover
