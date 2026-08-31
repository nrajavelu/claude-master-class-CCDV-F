/* Aizentify CDF-F portal — practice question bank (Day 1 set).
   Extend this file as Days 2-5 are built. Each item:
   { id, day, domain, sub, style, stem, options:[{k,t}], answer:[k...], rationale } */
window.AIZ_QUESTIONS = [
  { id:"d1-01", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"Every Claude capability below goes through the same API call EXCEPT one. Which is a separate endpoint?",
    options:[{k:"A",t:"Tool use"},{k:"B",t:"Vision (image input)"},{k:"C",t:"Extended thinking"},{k:"D",t:"Counting tokens for a prompt"}],
    answer:["D"],
    rationale:"Token counting is its own endpoint (/v1/messages/count_tokens). Tools, vision and thinking are all parameters of POST /v1/messages — the 'one endpoint, many parameters' model." },

  { id:"d1-02", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"response.content[0] on a normal text reply is:",
    options:[{k:"A",t:"a str"},{k:"B",t:'a dict {"type":"text","text":"..."}'},{k:"C",t:"a typed block object with .type and .text"},{k:"D",t:"the raw JSON string of the whole response"}],
    answer:["C"],
    rationale:"A typed block object. B is the input shape you send, not what you get back. content is a LIST — filter on block.type." },

  { id:"d1-03", day:1, domain:"D2", sub:"API Mechanics", style:"MR",
    stem:"Which are valid stop_reason values? (choose TWO)",
    options:[{k:"A",t:"end_turn"},{k:"B",t:"tool_call"},{k:"C",t:"max_tokens"},{k:"D",t:"content_filter"},{k:"E",t:"token_limit"}],
    answer:["A","C"],
    rationale:"end_turn and max_tokens are real. tool_call/content_filter are OpenAI-isms (Claude uses tool_use / refusal). token_limit is invented. Bucket: 'wrong system'." },

  { id:"d1-04", day:1, domain:"D2", sub:"API Mechanics", style:"SCN",
    stem:"Your call returns stop_reason == 'max_tokens' and the answer is cut off. Best fix for a long report feature?",
    options:[{k:"A",t:"Retry the same request"},{k:"B",t:"Stream with a higher max_tokens"},{k:"C",t:"Lower max_tokens so it stops cleanly"},{k:"D",t:'Set stop_sequences to ["\\n\\n"]'}],
    answer:["B"],
    rationale:"Rule 1: the constraint is 'long output must complete'. Streaming + more room is the mechanism. Retrying truncates again; lowering the ceiling still delivers an incomplete report; a stop sequence cuts it off sooner." },

  { id:"d1-05", day:1, domain:"D6", sub:"Prompt Engineering", style:"SBA",
    stem:"The most reliable place to put 'always answer in exactly three bullets' is:",
    options:[{k:"A",t:"the last line of every user message"},{k:"B",t:"the system field"},{k:"C",t:'an assistant message prefilled with "- "'},{k:"D",t:'output_config={"style":"bullets"}'}],
    answer:["B"],
    rationale:"The system field is the durable, every-turn contract. Prefill is removed on current models (400). output_config has no 'style' key." },

  { id:"d1-06", day:1, domain:"D6", sub:"Prompt Engineering", style:"BUG",
    stem:"thinking={'type':'enabled','budget_tokens':8000} on claude-sonnet-5 returns HTTP 400. Cause?",
    options:[{k:"A",t:"max_tokens must be >= 4096 when thinking is on"},{k:"B",t:"budget_tokens must be < max_tokens"},{k:"C",t:"budget_tokens thinking is not accepted on this model; use {'type':'adaptive'}"},{k:"D",t:"thinking must be a top-level sibling of model, not a dict"}],
    answer:["C"],
    rationale:"budget_tokens is deprecated and rejected on current models. Use adaptive thinking + output_config.effort. Classic 'stale API' distractor." },

  { id:"d1-07", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"After a `with client.messages.stream(...) as stream:` block, get the complete message (usage, stop_reason, blocks) via:",
    options:[{k:"A",t:"concatenate stream.text_stream"},{k:"B",t:"stream.get_final_message()"},{k:"C",t:"stream.response.usage while streaming"},{k:"D",t:"a second non-streaming call"}],
    answer:["B"],
    rationale:"get_final_message() reconstructs the whole Message. A gives text only; C isn't final mid-stream; D wastes a call and re-bills." },

  { id:"d1-08", day:1, domain:"D2", sub:"API Mechanics", style:"SCN",
    stem:"Which is the WEAKEST reason to stream?",
    options:[{k:"A",t:"Output may be several thousand tokens"},{k:"B",t:"Rendering the answer live in a chat UI"},{k:"C",t:"You need the full answer before parsing it as JSON, and latency doesn't matter"},{k:"D",t:"max_tokens is set to 64000"}],
    answer:["C"],
    rationale:"If you must have the whole answer before acting and latency is irrelevant, streaming buys little. A/B/D are strong reasons (timeout risk, live UI, huge max_tokens)." },

  { id:"d1-09", day:1, domain:"D4", sub:"Debugging & Error Handling", style:"MR",
    stem:"Which errors are worth RETRYING with backoff? (choose all)",
    options:[{k:"A",t:"RateLimitError (429)"},{k:"B",t:"AuthenticationError (401)"},{k:"C",t:"APIStatusError with status 503"},{k:"D",t:"BadRequestError (400)"},{k:"E",t:"APIConnectionError"}],
    answer:["A","C","E"],
    rationale:"Transient = 429 / >=500 / connection. 401 and 400 are caller errors — retrying can't fix a bad key or a malformed request." },

  { id:"d1-10", day:1, domain:"D4", sub:"Debugging & Error Handling", style:"SBA",
    stem:"The Anthropic SDK, out of the box:",
    options:[{k:"A",t:"never retries — you must implement it"},{k:"B",t:"retries every error type indefinitely"},{k:"C",t:"retries 408/409/429/5xx + connection errors, exp backoff, max_retries=2"},{k:"D",t:"retries only 429, once"}],
    answer:["C"], rationale:"Built-in exponential backoff on transient failures; max_retries defaults to 2 and is configurable." },

  { id:"d1-11", day:1, domain:"D4", sub:"Debugging & Error Handling", style:"SCN",
    stem:"HTTP 200, stop_reason == 'refusal'. Your code does response.content[0].text and crashes. Why / what to do?",
    options:[{k:"A",t:"The key is invalid; catch AuthenticationError"},{k:"B",t:"On a refusal content may have no text block; check stop_reason before reading content"},{k:"C",t:"Refusals raise APIStatusError; wrap in try/except"},{k:"D",t:"Add max_retries=5; refusals are transient"}],
    answer:["B"], rationale:"A refusal is HTTP 200 and never raises. Check stop_reason (and stop_details.category) first. Refusals are not transient." },

  { id:"d1-12", day:1, domain:"D1", sub:"Agent Construction", style:"SBA",
    stem:"In a manual tool loop, immediately after receiving ANY response you must:",
    options:[{k:"A",t:"check stop_reason and return if end_turn"},{k:"B",t:'append {"role":"assistant","content": response.content} to messages'},{k:"C",t:"append a tool_result user message"},{k:"D",t:"call response.model_dump() and log it"}],
    answer:["B"], rationale:"Append the whole content list as the assistant turn — the API is stateless and needs the full alternation. Then you branch on stop_reason." },

  { id:"d1-13", day:1, domain:"D1", sub:"Agent Construction", style:"SCN",
    stem:"One assistant response has THREE tool_use blocks. To continue the loop you append:",
    options:[{k:"A",t:"three user messages, one tool_result each"},{k:"B",t:"one user message with a list of three tool_result blocks, ids matching"},{k:"C",t:"one user message with the outputs concatenated as a string"},{k:"D",t:"one assistant message with the tool outputs"}],
    answer:["B"], rationale:"One user message, list of tool_result blocks, each with the matching tool_use_id. Splitting across messages trains the model to stop parallelising." },

  { id:"d1-14", day:1, domain:"D1", sub:"Agent Construction", style:"BUG",
    stem:"This loop sometimes 400s with 'roles must alternate': it appends only {'role':'user','content':results} after a tool_use response and continues. The bug is:",
    options:[{k:"A",t:"tools=TOOLS should only be passed on the first call"},{k:"B",t:"the assistant turn (r.content) is never appended before the tool_result user message"},{k:"C",t:"results should be a string, not a list"},{k:"D",t:"continue should be break"}],
    answer:["B"], rationale:"Without the assistant turn, messages goes user -> user(tool_result); roles don't alternate. Append the assistant content first, always." },

  { id:"d1-15", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"client.messages.count_tokens(...) accepts:",
    options:[{k:"A",t:"model, system, messages, tools"},{k:"B",t:"model, max_tokens, messages"},{k:"C",t:"a single text string"},{k:"D",t:"the same args as messages.create, including max_tokens and temperature"}],
    answer:["A"], rationale:"It counts the full prompt including tool schemas; it does NOT take max_tokens or sampling params." },

  { id:"d1-16", day:1, domain:"D2", sub:"API Mechanics", style:"OUT",
    stem:"messages=[{'role':'assistant','content':'Hi'}] as the first and only message. Result?",
    options:[{k:"A",t:"Works — Claude continues from 'Hi'"},{k:"B",t:"HTTP 400 — the first message must have role user"},{k:"C",t:"Works, but stop_reason is refusal"},{k:"D",t:"The SDK inserts an empty user message"}],
    answer:["B"], rationale:"The conversation must begin with a user turn. No silent fix-up." },

  { id:"d1-17", day:1, domain:"D6", sub:"Output Handling", style:"JDG",
    stem:"Two prompts both produce correct answers. A: 400-word system prompt, five rules. B: 60-word system prompt + one worked example. For a format-following task the exam's preferred answer is usually:",
    options:[{k:"A",t:"A — more explicit rules is always safer"},{k:"B",t:"B — a concrete example steers format better and costs fewer tokens"},{k:"C",t:"whichever has lower latency, regardless of quality"},{k:"D",t:"neither — use output_config"}],
    answer:["B"], rationale:"An example usually steers format better than piling on rules, and it's cheaper. The exam rewards simpler/cheaper/example-driven when quality is equal. 'Always' is the tell of a wrong option." },

  { id:"d1-18", day:1, domain:"D5", sub:"Cost & Token Management", style:"SCN",
    stem:"A feature calls Claude 20,000x/day with an identical 12 KB system prompt and a short varying question. Biggest single lever to cut cost, before touching model choice?",
    options:[{k:"A",t:"lower max_tokens"},{k:"B",t:"switch every call to Haiku"},{k:"C",t:"prompt caching on the stable system-prompt prefix"},{k:"D",t:"batch the requests"}],
    answer:["C"], rationale:"Caching the stable prefix drops repeated input cost ~90% for the cached portion — free quality-wise, huge at 20k/day. B is a model-choice tradeoff (excluded); output is already short; batch adds latency and doesn't touch the repeated-prefix waste." },

  { id:"d1-19", day:1, domain:"D5", sub:"LLM Fundamentals", style:"SBA",
    stem:"Same prompt, run twice, different wording. This is:",
    options:[{k:"A",t:"a bug"},{k:"B",t:"expected — generation samples among plausible continuations"},{k:"C",t:"a cache miss"},{k:"D",t:"a rate-limit artefact"}],
    answer:["B"], rationale:"Design for variation: assert on structure and required content, not exact wording. temperature was never a guarantee and is removed on newest models." },

  { id:"d1-20", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"The Messages API is stateless. Practically that means:",
    options:[{k:"A",t:"it can't be used for chat"},{k:"B",t:"you resend the full conversation history every request"},{k:"C",t:"responses are not cached"},{k:"D",t:"you can't use tools"}],
    answer:["B"], rationale:"No server-side session. Multi-turn = you carry the history and resend it; the model reads it fresh each call." }
];
