/* Aizentify CDF-F portal — practice question bank (Day 1 set).
   Extend this file as Days 2-5 are built. Each item:
   { id, day, domain, sub, style, stem, options:[{k,t}], answer:[k...], rationale } */
window.AIZ_QUESTIONS = [
  { id:"d1-01", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"Every Claude capability below goes through the same API call EXCEPT one. Which is a separate endpoint?",
    options:[{k:"A",t:"Tool use"},{k:"B",t:"Vision (image input)"},{k:"C",t:"Extended thinking"},{k:"D",t:"Counting tokens for a prompt"}],
    answer:["D"],
    rationale:"Token counting is its own endpoint (/v1/messages/count_tokens). Tools, vision and thinking are all parameters of POST /v1/messages — the 'one endpoint, many parameters' model.", ref:"code-snippets/messages_basics.py" },

  { id:"d1-02", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"response.content[0] on a normal text reply is:",
    options:[{k:"A",t:"a str"},{k:"B",t:'a dict {"type":"text","text":"..."}'},{k:"C",t:"a typed block object with .type and .text"},{k:"D",t:"the raw JSON string of the whole response"}],
    answer:["C"],
    rationale:"A typed block object. B is the input shape you send, not what you get back. content is a LIST — filter on block.type.", ref:"code-snippets/messages_basics.py" },

  { id:"d1-03", day:1, domain:"D2", sub:"API Mechanics", style:"MR",
    stem:"Which are valid stop_reason values? (choose TWO)",
    options:[{k:"A",t:"end_turn"},{k:"B",t:"tool_call"},{k:"C",t:"max_tokens"},{k:"D",t:"content_filter"},{k:"E",t:"token_limit"}],
    answer:["A","C"],
    rationale:"end_turn and max_tokens are real. tool_call/content_filter are OpenAI-isms (Claude uses tool_use / refusal). token_limit is invented. Bucket: 'wrong system'.", ref:"code-snippets/messages_basics.py" },

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
    rationale:"budget_tokens is deprecated and rejected on current models. Use adaptive thinking + output_config.effort. Classic 'stale API' distractor.", ref:"code-snippets/cot_structured.py" },

  { id:"d1-07", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"After a `with client.messages.stream(...) as stream:` block, get the complete message (usage, stop_reason, blocks) via:",
    options:[{k:"A",t:"concatenate stream.text_stream"},{k:"B",t:"stream.get_final_message()"},{k:"C",t:"stream.response.usage while streaming"},{k:"D",t:"a second non-streaming call"}],
    answer:["B"],
    rationale:"get_final_message() reconstructs the whole Message. A gives text only; C isn't final mid-stream; D wastes a call and re-bills.", ref:"code-snippets/streaming.py" },

  { id:"d1-08", day:1, domain:"D2", sub:"API Mechanics", style:"SCN",
    stem:"Which is the WEAKEST reason to stream?",
    options:[{k:"A",t:"Output may be several thousand tokens"},{k:"B",t:"Rendering the answer live in a chat UI"},{k:"C",t:"You need the full answer before parsing it as JSON, and latency doesn't matter"},{k:"D",t:"max_tokens is set to 64000"}],
    answer:["C"],
    rationale:"If you must have the whole answer before acting and latency is irrelevant, streaming buys little. A/B/D are strong reasons (timeout risk, live UI, huge max_tokens).", ref:"code-snippets/streaming.py" },

  { id:"d1-09", day:1, domain:"D4", sub:"Debugging & Error Handling", style:"MR",
    stem:"Which errors are worth RETRYING with backoff? (choose all)",
    options:[{k:"A",t:"RateLimitError (429)"},{k:"B",t:"AuthenticationError (401)"},{k:"C",t:"APIStatusError with status 503"},{k:"D",t:"BadRequestError (400)"},{k:"E",t:"APIConnectionError"}],
    answer:["A","C","E"],
    rationale:"Transient = 429 / >=500 / connection. 401 and 400 are caller errors — retrying can't fix a bad key or a malformed request.", ref:"code-snippets/retry_chain.py" },

  { id:"d1-10", day:1, domain:"D4", sub:"Debugging & Error Handling", style:"SBA",
    stem:"The Anthropic SDK, out of the box:",
    options:[{k:"A",t:"never retries — you must implement it"},{k:"B",t:"retries every error type indefinitely"},{k:"C",t:"retries 408/409/429/5xx + connection errors, exp backoff, max_retries=2"},{k:"D",t:"retries only 429, once"}],
    answer:["C"], rationale:"Built-in exponential backoff on transient failures; max_retries defaults to 2 and is configurable.", ref:"code-snippets/retry_chain.py" },

  { id:"d1-11", day:1, domain:"D4", sub:"Debugging & Error Handling", style:"SCN",
    stem:"HTTP 200, stop_reason == 'refusal'. Your code does response.content[0].text and crashes. Why / what to do?",
    options:[{k:"A",t:"The key is invalid; catch AuthenticationError"},{k:"B",t:"On a refusal content may have no text block; check stop_reason before reading content"},{k:"C",t:"Refusals raise APIStatusError; wrap in try/except"},{k:"D",t:"Add max_retries=5; refusals are transient"}],
    answer:["B"], rationale:"A refusal is HTTP 200 and never raises. Check stop_reason (and stop_details.category) first. Refusals are not transient." },

  { id:"d1-12", day:1, domain:"D1", sub:"Agent Construction", style:"SBA",
    stem:"In a manual tool loop, immediately after receiving ANY response you must:",
    options:[{k:"A",t:"check stop_reason and return if end_turn"},{k:"B",t:'append {"role":"assistant","content": response.content} to messages'},{k:"C",t:"append a tool_result user message"},{k:"D",t:"call response.model_dump() and log it"}],
    answer:["B"], rationale:"Append the whole content list as the assistant turn — the API is stateless and needs the full alternation. Then you branch on stop_reason.", ref:"code-snippets/agent_loop_react.py" },

  { id:"d1-13", day:1, domain:"D1", sub:"Agent Construction", style:"SCN",
    stem:"One assistant response has THREE tool_use blocks. To continue the loop you append:",
    options:[{k:"A",t:"three user messages, one tool_result each"},{k:"B",t:"one user message with a list of three tool_result blocks, ids matching"},{k:"C",t:"one user message with the outputs concatenated as a string"},{k:"D",t:"one assistant message with the tool outputs"}],
    answer:["B"], rationale:"One user message, list of tool_result blocks, each with the matching tool_use_id. Splitting across messages trains the model to stop parallelising.", ref:"code-snippets/agent_loop_react.py" },

  { id:"d1-14", day:1, domain:"D1", sub:"Agent Construction", style:"BUG",
    stem:"This loop sometimes 400s with 'roles must alternate': it appends only {'role':'user','content':results} after a tool_use response and continues. The bug is:",
    options:[{k:"A",t:"tools=TOOLS should only be passed on the first call"},{k:"B",t:"the assistant turn (r.content) is never appended before the tool_result user message"},{k:"C",t:"results should be a string, not a list"},{k:"D",t:"continue should be break"}],
    answer:["B"], rationale:"Without the assistant turn, messages goes user -> user(tool_result); roles don't alternate. Append the assistant content first, always.", ref:"code-snippets/agent_loop_react.py" },

  { id:"d1-15", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"client.messages.count_tokens(...) accepts:",
    options:[{k:"A",t:"model, system, messages, tools"},{k:"B",t:"model, max_tokens, messages"},{k:"C",t:"a single text string"},{k:"D",t:"the same args as messages.create, including max_tokens and temperature"}],
    answer:["A"], rationale:"It counts the full prompt including tool schemas; it does NOT take max_tokens or sampling params.", ref:"code-snippets/count_tokens.py" },

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
    answer:["C"], rationale:"Caching the stable prefix drops repeated input cost ~90% for the cached portion — free quality-wise, huge at 20k/day. B is a model-choice tradeoff (excluded); output is already short; batch adds latency and doesn't touch the repeated-prefix waste.", ref:"code-snippets/prompt_caching.py" },

  { id:"d1-19", day:1, domain:"D5", sub:"LLM Fundamentals", style:"SBA",
    stem:"Same prompt, run twice, different wording. This is:",
    options:[{k:"A",t:"a bug"},{k:"B",t:"expected — generation samples among plausible continuations"},{k:"C",t:"a cache miss"},{k:"D",t:"a rate-limit artefact"}],
    answer:["B"], rationale:"Design for variation: assert on structure and required content, not exact wording. temperature was never a guarantee and is removed on newest models.", ref:"code-snippets/cot_structured.py" },

  { id:"d1-20", day:1, domain:"D2", sub:"API Mechanics", style:"SBA",
    stem:"The Messages API is stateless. Practically that means:",
    options:[{k:"A",t:"it can't be used for chat"},{k:"B",t:"you resend the full conversation history every request"},{k:"C",t:"responses are not cached"},{k:"D",t:"you can't use tools"}],
    answer:["B"], rationale:"No server-side session. Multi-turn = you carry the history and resend it; the model reads it fresh each call.", ref:"code-snippets/messages_basics.py" },

  { id:"d1-21", day:1, domain:"D6", sub:"Reasoning patterns", style:"SBA",
    stem:"Chain-of-Thought vs ReAct — which is true?",
    options:[{k:"A",t:"They're the same thing"},{k:"B",t:"CoT is reasoning inside one turn; ReAct interleaves reasoning with tool calls across a loop"},{k:"C",t:"ReAct is a single API call"},{k:"D",t:"CoT requires the model to execute tools"}],
    answer:["B"], rationale:"CoT = reason-then-answer in one response. ReAct = Thought -> Action -> Observation repeated in a loop (the agentic loop). ReAct needs tool results fed back; it is not one call. The model emits tool_use — your code runs the tool.", ref:"code-snippets/agent_loop_react.py" },

  { id:"d1-22", day:1, domain:"D6", sub:"Reasoning patterns", style:"JDG",
    stem:"For a high-volume ticket-classification route, adding 'think step by step' to the prompt will:",
    options:[{k:"A",t:"always improve accuracy"},{k:"B",t:"add latency and cost with little or no benefit — CoT helps reasoning tasks, not fixed-set classification"},{k:"C",t:"cause a 400 error"},{k:"D",t:"disable the model's own thinking"}],
    answer:["B"], rationale:"'CoT always helps' is a distractor. It trades output tokens for accuracy on problems that need working-out; classification into a fixed set doesn't.", ref:"code-snippets/cot_structured.py" },

  { id:"d2-01", day:2, domain:"D6", sub:"Prompt Engineering", style:"SBA",
    stem:"A prototype in the chat product behaves well; the same instructions via the API behave differently. Best explanation?",
    options:[{k:"A",t:"the API serves a different model"},{k:"B",t:"the chat product adds its own system prompt that doesn't apply to the API"},{k:"C",t:"the default temperature differs"},{k:"D",t:"the API needs the instructions as a role:'system' message"}],
    answer:["B"], rationale:"Rule 1 — find the mechanism that differs between surfaces. A/C are 'reach for a knob'. D is right-word-wrong-place: no message has role:'system'.", ref:"code-snippets/prompt_structure.py" },

  { id:"d2-02", day:2, domain:"D8", sub:"Tool Implementation", style:"SCN",
    stem:"The model calls your refund tool at the wrong time. First thing to check?",
    options:[{k:"A",t:"the model tier"},{k:"B",t:"the tool's description — is it detailed about WHEN to use it and what the inputs mean"},{k:"C",t:"temperature"},{k:"D",t:"max_tokens"}],
    answer:["B"], rationale:"The description is the biggest factor in whether the model uses a tool correctly. The others are generic knobs.", ref:"code-snippets/strict_tool.py" },

  { id:"d2-03", day:2, domain:"D2", sub:"Structured output", style:"BUG",
    stem:"Your strict tool keeps failing validation on an 'optional' field you left out of `required`. Fix?",
    options:[{k:"A",t:"remove strict"},{k:"B",t:"keep it in `required` and allow null as a type — strict has no 'optional'"},{k:"C",t:"set additionalProperties:true"},{k:"D",t:"lower max_tokens"}],
    answer:["B"], rationale:"strict mode expresses optional as nullable. Everything stays in `required`; additionalProperties must be false.", ref:"code-snippets/strict_tool.py" },

  { id:"d2-04", day:2, domain:"D7", sub:"AI App Security", style:"SBA",
    stem:"Where does third-party content (a fetched page, a customer ticket) belong?",
    options:[{k:"A",t:"appended to the system field"},{k:"B",t:"in a tool_result block"},{k:"C",t:"in your user instruction text"},{k:"D",t:"anywhere — the model sorts it out"}],
    answer:["B"], rationale:"tool_result is the untrusted channel. And your own instructions must NOT go in a tool_result — the rule runs both ways.", ref:"code-snippets/blocking_hook.py" },

  { id:"d3-01", day:3, domain:"D1", sub:"Agent Construction", style:"SCN",
    stem:"You want the request->execute->loop handled for you, but only over YOUR tools, on YOUR infra. Which?",
    options:[{k:"A",t:"a manual while loop"},{k:"B",t:"the SDK Tool Runner"},{k:"C",t:"Managed Agents"},{k:"D",t:"the Claude Agent SDK"}],
    answer:["B"], rationale:"Tool Runner = harness only, your tools, you host. Managed Agents adds hosting; Agent SDK adds built-in tools; manual loop makes you write the harness.", ref:"code-snippets/blocking_hook.py" },

  { id:"d3-02", day:3, domain:"D7", sub:"Guardrails", style:"SCN",
    stem:"'Ticket text must NEVER be able to trigger the refund tool.' Which satisfies the requirement?",
    options:[{k:"A",t:"add a system-prompt line telling the model to ignore instructions inside tickets"},{k:"B",t:"switch to the most capable model tier"},{k:"C",t:"treat ticket text as untrusted, keep it out of the instruction channel, and put a blocking approval hook in front of refund"},{k:"D",t:"set temperature to 0"}],
    answer:["C"], rationale:"Rule 2 — 'must never' kills guidance (A). B/D are knobs, and a stronger model follows the injected instruction better too. Only C is a mechanism that stops it.", ref:"code-snippets/blocking_hook.py" },

  { id:"d3-03", day:3, domain:"D3", sub:"Claude Code", style:"SBA",
    stem:"A CLAUDE.md in a subfolder and one at the repo root both exist. Running Claude Code from the subfolder, which applies?",
    options:[{k:"A",t:"only the subfolder one"},{k:"B",t:"only the root one"},{k:"C",t:"both — discovered cwd upward"},{k:"D",t:"neither unless passed explicitly"}],
    answer:["C"], rationale:"Project config is discovered from the working directory up to the repo root; both load.", ref:"code-snippets/mcp_server.py" },

  { id:"d3-04", day:3, domain:"D8", sub:"MCP", style:"SBA",
    stem:".mcp.json for a local Python server you wrote uses which transport?",
    options:[{k:"A",t:"http"},{k:"B",t:"stdio with a command + args"},{k:"C",t:"sse with a url"},{k:"D",t:"websocket"}],
    answer:["B"], rationale:"A local server is just a program: type 'stdio', a command and args.", ref:"code-snippets/mcp_server.py" },

  { id:"d4-01", day:4, domain:"D2", sub:"Requirements", style:"SBA",
    stem:"'Any engineer must be able to deploy it and roll it back.' This requirement is:",
    options:[{k:"A",t:"functional"},{k:"B",t:"infrastructure"},{k:"C",t:"a bug"},{k:"D",t:"out of scope"}],
    answer:["B"], rationale:"Infrastructure = what it runs on AND what the team must be able to do to it. Functional = what the system does." },

  { id:"d4-02", day:4, domain:"D2", sub:"Systems Life Cycle", style:"SBA",
    stem:"In the systems life cycle, 'implement' means:",
    options:[{k:"A",t:"write the code"},{k:"B",t:"deploy the finished thing where users are"},{k:"C",t:"design the architecture"},{k:"D",t:"retire the system"}],
    answer:["B"], rationale:"Implement = stand it up in production. Production credit is earned in operate + maintain, never in develop." },

  { id:"d4-03", day:4, domain:"D2", sub:"Configuration Management", style:"SCN",
    stem:"Three engineers, one repo, different behaviour every run. The team requires every run use the same model version and rules. Best move?",
    options:[{k:"A",t:"rewrite it in a faster language"},{k:"B",t:"write a long setup document"},{k:"C",t:"pin the model version and commit the rules/config to version control"},{k:"D",t:"add the missing features first"}],
    answer:["C"], rationale:"Rule 2 — a doc is guidance. Committed, pinned config is the mechanism. Secrets stay out via .gitignore." },

  { id:"d4-04", day:4, domain:"D6", sub:"Context Engineering", style:"SBA",
    stem:"Compaction vs context-editing:",
    options:[{k:"A",t:"same thing"},{k:"B",t:"compaction summarises earlier context; context-editing CLEARS old tool-results / thinking"},{k:"C",t:"both delete messages permanently"},{k:"D",t:"only compaction is server-side"}],
    answer:["B"], rationale:"Different mechanisms: summarise vs clear. The memory tool is a third option (write to disk)." },

  { id:"d5-01", day:5, domain:"D5", sub:"Cost & Token Management", style:"SCN",
    stem:"A feature calls Claude 20,000x/day with an identical 12 KB system prompt. Biggest lever to cut cost, before touching model choice?",
    options:[{k:"A",t:"lower max_tokens"},{k:"B",t:"switch every call to Haiku"},{k:"C",t:"prompt caching on the stable system-prompt prefix"},{k:"D",t:"batch the requests"}],
    answer:["C"], rationale:"Caching the stable prefix drops repeated input cost ~90% — lever #1, before model choice. B is a quality trade; output is already short; batch adds latency.", ref:"code-snippets/prompt_caching.py" },

  { id:"d5-02", day:5, domain:"D5", sub:"Cost & Token Management", style:"SBA",
    stem:"usage.cache_read_input_tokens is 0 across repeated identical-prefix calls. Most likely:",
    options:[{k:"A",t:"caching isn't supported"},{k:"B",t:"a silent invalidator in the prefix (datetime.now(), unsorted JSON, varying tools)"},{k:"C",t:"the model is too small"},{k:"D",t:"you need a beta header"}],
    answer:["B"], rationale:"Any byte change in the prefix invalidates everything after it. datetime.now() in the system prompt is the classic one.", ref:"code-snippets/prompt_caching.py" },

  { id:"d5-03", day:5, domain:"D2", sub:"Batch", style:"SCN",
    stem:"10,000 documents, processed overnight, cost is the concern, nobody needs results until morning. Best approach?",
    options:[{k:"A",t:"run them in parallel with async"},{k:"B",t:"the Batch API"},{k:"C",t:"switch to Haiku"},{k:"D",t:"cap max_tokens"}],
    answer:["B"], rationale:"Rule 1 — the stem names the exact constraint Batch exists for. Results come back in any order — key by custom_id.", ref:"code-snippets/batch_custom_id.py" },

  { id:"d5-04", day:5, domain:"D5", sub:"Technical Fundamentals", style:"SBA",
    stem:"A PDF sent as a document block is billed:",
    options:[{k:"A",t:"once, as text"},{k:"B",t:"once, as an image"},{k:"C",t:"twice — as its text AND as each page rendered to an image"},{k:"D",t:"it's free"}],
    answer:["C"], rationale:"If you already have the text, send the text — an image (or a PDF's page images) is built-in tokens." },

  { id:"m-01", day:3, domain:"D1", sub:"Agents vs Workflows", style:"SCN",
    stem:"Triage: classify the ticket, look up the customer, draft a reply — same 3 steps, in order, every ticket. The team proposes an autonomous agent with a dozen tools. Best guidance?",
    options:[{k:"A",t:"Build the agent — it's more capable"},{k:"B",t:"Build a routed workflow — the path is fixed"},{k:"C",t:"Don't automate reply drafting"},{k:"D",t:"Use an agent-framework supervisor pattern"}],
    answer:["B"], rationale:"The path is scriptable → a workflow (cheaper, testable). A is the OVERBUILD — an agent buys flexibility you don't need. C is extremist. D is overbuild + true-but-irrelevant.", ref:"code-snippets/agent_loop_react.py" },

  { id:"m-02", day:4, domain:"D4", sub:"Debugging", style:"SCN",
    stem:"A batch pipeline's outputs are cut off mid-sentence on long documents. First move?",
    options:[{k:"A",t:"Rewrite the prompt to be more concise"},{k:"B",t:"Read stop_reason (it says max_tokens); raise the output limit for those docs"},{k:"C",t:"Switch to a bigger-context model"},{k:"D",t:"Add a second pass that stitches truncated outputs together"}],
    answer:["B"], rationale:"Evidence first — stop_reason names the cause; the fix is the smallest one. D is the OVERBUILD. A/C treat a symptom that isn't the cause.", ref:"code-snippets/messages_basics.py" },

  { id:"m-03", day:5, domain:"D8", sub:"MCP", style:"SCN",
    stem:"Three teams each hand-wired the same internal customer-lookup integration, with three different bugs. Best move?",
    options:[{k:"A",t:"One shared MCP server for customer lookup"},{k:"B",t:"Copy the least-buggy version to the other two"},{k:"C",t:"Each team keeps its own for independence"},{k:"D",t:"Build an agent to manage the three integrations"}],
    answer:["A"], rationale:"A capability that crosses apps/teams → an MCP server. B is symptom-treater (3 copies still). C is true-but-irrelevant. D is the OVERBUILD.", ref:"code-snippets/mcp_server.py" },

  { id:"m-04", day:5, domain:"D7", sub:"AI App Security", style:"SCN",
    stem:"A support agent summarises incoming emails. A crafted email makes it call the refund tool. Choose TWO defences.",
    options:[{k:"A",t:"Remove the refund tool from the summarisation path (least privilege)"},{k:"B",t:"Treat email content as untrusted data; validate model output before any tool acts"},{k:"C",t:"Add a system-prompt line: 'ignore malicious instructions'"},{k:"D",t:"Stop processing email entirely"}],
    answer:["A","B"], rationale:"Mechanisms: an agent that only reads shouldn't hold a tool that writes; outputs that become actions get validated. C is guidance/symptom-treater. D is extremist.", ref:"code-snippets/blocking_hook.py" },

  { id:"m-05", day:5, domain:"D5", sub:"Model Selection", style:"SCN",
    stem:"A classifier handles 1,000,000 requests/day. Which tier?",
    options:[{k:"A",t:"Fast tier for everything"},{k:"B",t:"Fast tier, and route the hard cases up a tier (cascade)"},{k:"C",t:"Top tier for everything"},{k:"D",t:"Workhorse tier for everything"}],
    answer:["B"], rationale:"Volume + mostly-easy → the fast tier PLUS the engineering move: cascading beats paying premium for every request. C is cost blowout; A leaves accuracy on the hard inputs.", ref:"code-snippets/count_tokens.py" }
];
