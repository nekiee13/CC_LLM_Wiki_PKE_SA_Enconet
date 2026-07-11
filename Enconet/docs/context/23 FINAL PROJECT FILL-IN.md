# Conversation Export — LLM Wiki Project Planning

**Export date:** 2026-06-20  
**Format:** Markdown  
**Scope:** User-visible conversation only. System instructions, developer instructions, internal reasoning, and tool-call payloads are excluded. Uploaded Markdown files are embedded in full at the points where they were supplied.

---

## User

Adopt a **strictly objective narrative**. Use **third-person perspective** only. Avoid personal pronouns (no 'I', 'me', 'you', or 'your'). Focus exclusively on the **objects**. Use passive voice where appropriate to maintain a de-personalized tone. Make it easy to read and keep it beginner-friendly (Flesch‑Kincaid ≤9).

You may process multiple-steps that does not involve user interaction. But, when you need user to perform some action, always provide user with a single step instructions and then you will wait for user confirmation on that step resolution (and possible feedback).

I will provide you a multi-part context. Perform user input analysis and wait for further user input.

"""
<see appended text>

"""
Inspect provided links.
Let me know when you're ready to continue.

### Attached file: `Pasted markdown(19).md`

# Original Project Concept
- [ ] [X tweet](https://x.com/karpathy/status/2039805659525644595)
   * [Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

----
# Original Project Concept - LLM Wiki

A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts. A few examples:

- **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like [Tolkien Gateway](https://tolkiengateway.net/wiki/Main_Page) — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
- **Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered.

## Architecture

There are three layers:

**Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.

**The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain.

## Operations

**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

**index.md** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. Organized by category (entities, concepts, sources, etc.). The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure.

**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently.

## Optional: CLI tools

At some point you may want to build small tools that help the LLM operate on the wiki more efficiently. A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. [qmd](https://github.com/tobi/qmd) is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool). You could also build something simpler yourself — the LLM can help you vibe-code a naive search script as the need arises.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `raw/assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Dataview** is an Obsidian plugin that runs queries over page frontmatter. If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists.
- The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.


## Note

This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't. For example: your sources might be text-only, so you don't need image handling at all. Your wiki might be small enough that the index file is all you need, no search engine required. You might not care about slide decks and just want markdown pages. You might want a completely different set of output formats. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.

---

## Assistant

*Progress update*

The attached context will be reviewed, all embedded links will be opened, and only readiness status plus any access limits will be reported.

---

## Assistant

The multi-part context has been analyzed. The attached document, X post, GitHub Gist, Tolkien Gateway example, and qmd repository have been inspected.

No blocking access issue remains. **Ready to continue.**

---

## User

here is more context:

"""
# THE OBSIDIAN + CLAUDE CODE CODEBOOK

12 commands to build for your second brain

*Vin (Internet Vin) uses Obsidian and Claude Code together as a personal operating system. He built custom slash commands that let Claude Code read his entire vault, surface patterns across years of notes, and generate ideas he would never see on his own.*

*This guide breaks down 12 commands Vin demonstrated. Each one turns your notes into a different kind of thinking tool. You can build all of them yourself.*

*Inside: the core setup, how to create commands, and 12 slash commands with example prompts.*

## Tools Referenced

*   <u>Claude Code</u>
*   <u>Obsidian</u>
*   <u>Obsidian CLI</u>

## The Setup

Claude Code can control your computer through natural language. Obsidian stores your notes as interlinked markdown files. Obsidian CLI connects them.

Once connected, Claude Code can see both your files AND the relationships between them. It knows that your note on filmmaking links to your note on world building. It can trace how an idea evolved over months. It can find patterns you missed.

The key insight: the quality of context you feed the agent determines what it can do for you. Your vault is that context.

## <mark>How to Build These Commands</mark>

You don't need to code. You ask Claude Code to create the command for you.

**Example:**

```
None
Create a slash command called /trace that tracks how a specific
idea has evolved over time across my Obsidian vault. It should:
1. Take a topic as input
2. Search the vault for all mentions of that topic
3. Use Obsidian CLI to follow backlinks and find related notes
4. Output a timeline showing when the idea first appeared, how it
evolved, and what it's connected to now
```

Claude Code will generate the command and save it. Then you just type `/trace` to run it.

Start with one command. Test it. Refine the prompt if needed. Then build the next one.

## <mark>The Commands</mark>

Each command is a different way to use your vault as a thinking partner.

### 1. <mark>/context</mark>

**What it does:** Loads your full life and work state into Claude Code. Projects, preferences, priorities, current focus.

**When to use it:** At the start of any session where you want the agent to know everything relevant about you.

```
None
Read my vault and summarize my current context. Include active
projects, recent reflections, and any priorities I've mentioned
in the last 7 days.
```

## 2. <mark>/today</mark>

**What it does:** Pulls your calendar, tasks, and daily notes into a prioritized plan for the day.

**When to use it:** Morning planning. When you're overwhelmed and need clarity on what matters.

![Screenshot of a prompt box containing text: "Read my daily note, calendar, and task list. Generate a prioritized plan for today based on what I've said is important this week."](page_3_image_1_v2.jpg)

## 3. <mark>/trace</mark>

**What it does:** Tracks how a specific idea has evolved over time across your notes.

**When to use it:** When you want to see the arc of your thinking. When an idea keeps coming up and you want to understand why.

```
None
Trace the idea of [topic] across my vault. Show me when it first
appeared, how it evolved, and what it's connected to now.
```

## 4. <mark>/connect</mark>

**What it does:** Bridges two domains using the link graph in your vault. Finds unexpected connections between topics.

**When to use it:** When you're stuck. When you suspect two ideas are related but can't see how.

> None
> <mark>Find connections between [topic A] and [topic B] in my vault. Show me the notes that link them and any patterns you see.</mark>

***

### 5. <mark>/ghost</mark>

**What it does:** Answers a question the way you would, based on your writing and stated beliefs.

**When to use it:** When you want to externalize your own thinking. When you need a draft response that sounds like you.

> None
> <mark>Based on my vault, how would I answer this question: [question]? Use my voice and reference specific notes where relevant.</mark>

***

### 6. <mark>/challenge</mark>

**What it does:** Pressure-tests your current beliefs. Finds contradictions or weak points in your thinking.

**When to use it:** Before making a big decision. When you want to stress-test an idea.

> None
> <mark>Review my notes on [topic]. Where am I contradicting myself? What assumptions am I making that might be wrong?</mark>

***

### 7. <mark>/ideas</mark>

**What it does:** Scans your vault and generates a full idea report. Tools to build, people to meet, subjects to investigate, things to write.

**When to use it:** When you want fresh ideas grounded in your actual interests and patterns.

```text
None
Scan my vault for emerging patterns. Generate ideas for: tools I
should build, people I should reach out to, topics I should
investigate, and things I should write.
```

---

# 8. <mark>/graduate</mark>

**What it does:** Extracts undeveloped ideas from daily notes and promotes them into standalone files.

**When to use it:** Weekly review. When your daily notes are full of half-formed thoughts that deserve their own space.

```text
None
Scan my daily notes from the past 14 days. Find ideas that
deserve their own note. For each one, create a standalone file
with the core claim, context, and connections to other notes.
```

---

# 9. <mark>/closeday</mark>

**What it does:** Captures what happened today and what you learned. The counterpart to /today.

**When to use it:** End of day. When you want to log progress and clear your head before tomorrow.

```text
None
Review what I worked on today. Summarize progress, capture any
new ideas that came up, and note anything unfinished that should
carry over to tomorrow.
```

---

## 10. <mark>/drift</mark>

**What it does:** Surfaces loosely connected ideas that keep appearing across your notes without a clear thread.

**When to use it:** When you sense something emerging but can't name it. When you want to see what your subconscious is circling.

> > None
>
> > `Scan my vault for recurring themes or phrases that appear across unrelated notes. What ideas am I drifting toward without realizing it?`

***

## 11. <mark>/emerge</mark>

**What it does:** Identifies patterns that are starting to coalesce into something bigger.

**When to use it:** When you want to see what ideas are ready to become projects. When scattered thoughts are starting to cluster.

> > None
>
> > `Find clusters of related ideas in my vault that could become a project, essay, or product. Show me what's emerging and what notes connect to it.`

***

## 12. <mark>/schedule</mark>

**What it does:** Reads your priorities and calendar, then suggests how to allocate your time.

**When to use it:** Weekly planning. When you need to map your stated priorities to actual time blocks.

> None
> Based on my current projects and priorities, suggest a schedule for this week. Flag any conflicts between what I say matters and how I'm spending time.

# <mark>Final Note</mark>

Start by writing daily. The commands only work if your vault has context. Pick one command from this list. Ask Claude Code to build it. Run it. See what surfaces. Refine the prompt if needed, then build the next one.

The more you write, the more the agent can do for you.

# <mark>Want To Learn More?</mark>

Follow Vin on <u>X</u> and <u>YouTube</u>. Explore his site at <u>internetvin.com</u>.

> **"The quality of information that the agent has entirely determines what it can do for you. If it doesn't know a lot about you, it's not going to be able to do a lot for you."**

> — Vin
"""

Let me know when you're ready to continue.

---

## Assistant

The additional context has been analyzed.

The 12-command model, command structure, Obsidian vault role, Claude Code integration, Obsidian CLI dependency, and proposed workflows have been incorporated into the working context.

**Ready to continue.**

---

## User

Inspect following repos and links:

# Karpathy’s LLM Wiki (open source) - Github repos

- [ ] [LLM-wiki](https://github.com/Ss1024sS/LLM-wiki)
- [ ] [obsidian-llm-wiki-local](https://github.com/kytmanov/obsidian-llm-wiki-local)
- [ ] [OmegaWiki](https://github.com/skyllwt/OmegaWiki)
- [ ] [OpenKB](https://www.reddit.com/r/learnmachinelearning/s/TXBiN5tPUE)
   * [Github repo](https://github.com/VectifyAI/OpenKB)
- [ ] [BrainDB](https://www.reddit.com/r/LocalLLaMA/s/DmA95OtibF)
   * [Github repo](https://github.com/dimknaf/braindb)
- [ ] [DeepWiki - LLM-Wiki-compiler](https://deepwiki.com/atomicmemory/llm-wiki-compiler)
   * [Github repo](https://github.com/atomicmemory/llm-wiki-compiler)
- [ ] [llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent)

---
# Karpathy’s LLM Wiki (open source) - Web links

- [ ] [LLM Wiki knowledge-base - Guide](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide)
- [ ] [The Complete Guide to Karpathy’s LLM Wiki (Build a Self-Updating AI Knowledge System)](https://growwithaiguide.substack.com/p/the-complete-guide-to-karpathys-llm)
- [ ] [How to Implement Karpathy's LLM Knowledge Base. Full Guide](https://www.reddit.com/r/AskVibecoders/s/HaiZlSWyYC)
- [ ] [How I Built a Self-Maintaining Knowledge Base for 6 Projects Using Claude Code & Karpathy's LLM Wiki](https://hackernoon.com/how-i-built-a-self-maintaining-knowledge-base-for-6-projects-using-claude-code-and-karpathys-llm-wiki)

------

Let me know when you're ready to continue.

---

## Assistant

*Progress update*

The repositories and articles will be checked for scope, architecture, maintenance status, dependencies, and practical fit with the LLM Wiki concept. Any inaccessible or incomplete sources will be identified.

---

## Assistant

*Progress update*

Initial inspection shows several distinct implementation classes: lightweight agent templates, local Ollama pipelines, database-backed systems, and full compiler platforms. Redirects and renamed repositories are also being verified.

---

## Assistant

Inspection is complete.

Notable source changes and limits:

- **OmegaWiki** redirects to the renamed **AutoSci** repository.
- **atomicmemory/llm-wiki-compiler** redirects to **atomicstrata/llm-wiki-compiler**.
- **obsidian-llm-wiki-local** is now in maintenance mode; active development has moved to its successor, **Synto**.
- The Reddit post titled *How to Implement Karpathy’s LLM Knowledge Base. Full Guide* was removed by Reddit’s filters. Only the remaining discussion was available.
- The HackerNoon page exposed limited article text. Its metadata, available summaries, and associated open-source implementation were inspected.

The architecture, installation model, storage format, LLM dependencies, local-processing options, query methods, provenance controls, maintenance mechanisms, and project maturity of the listed implementations have been incorporated into the working context.

**Ready to continue.**

---

## User

Enrich overview of repo and links inspection.

"""
### GitHub repositories

* **LLM-wiki** is a platform-agnostic implementation of Karpathy’s LLM Wiki pattern. It emphasizes compile-first workflows, mandatory writeback, markdown-first storage, and support for tools such as Claude Code and Codex. [\[github.com\]](https://github.com/Ss1024sS/LLM-wiki)
* **obsidian-llm-wiki-local** is a local-first Obsidian wiki compiler. It uses local or OpenAI-compatible LLM endpoints, extracts concepts from markdown notes, and updates interlinked wiki articles. The project is marked as being in maintenance mode, with newer work moving to Synto. [\[github.com\]](https://github.com/kytmanov/obsidian-llm-wiki-local)
* **OmegaWiki** appears to have evolved into **AutoSci**. The linked repository resolves to AutoSci, described as a wiki-centric research agent with compounding memory and full scientific-lifecycle workflows. [\[github.com\]](https://github.com/skyllwt/AutoSci)
* **OpenKB** is a CLI-based open knowledge-base system. It compiles raw documents into a structured, interlinked wiki and uses PageIndex for vectorless long-document retrieval. [\[github.com\]](https://github.com/VectifyAI/OpenKB)
* **BrainDB** extends the LLM Wiki idea into a database system with typed entities, graph relations, REST APIs, fuzzy and semantic search, temporal decay, and agent-oriented memory. [\[github.com\]](https://github.com/dimknaf/braindb)
* **llm-wiki-compiler** is a CLI knowledge compiler that converts URLs, files, and papers into an interlinked markdown wiki. The DeepWiki page describes ingestion, compilation, concept extraction, link resolution, and query-saving workflows. [\[deepwiki.com\]](https://deepwiki.com/atomicmemory/llm-wiki-compiler)
* The GitHub repository for **llm-wiki-compiler** resolves under **atomicstrata/llm-wiki-compiler** and describes support for citation-traceable markdown, linting, export, MCP access, and SDK use. [\[github.com\]](https://github.com/atomicstrata/llm-wiki-compiler)
* **llm-wiki-agent** is an agent skill for Claude Code, Codex, Gemini CLI, and similar tools. It builds a persistent wiki from files placed in `raw/`, with `index.md`, `log.md`, source summaries, entities, concepts, syntheses, and graph outputs. [\[github.com\]](https://github.com/SamurAIGPT/llm-wiki-agent)

### Web links

* The **Starmorph guide** presents Karpathy’s LLM Wiki as a pattern rather than a product. It describes the three-layer architecture: `raw/`, `wiki/`, and `CLAUDE.md`, plus the three main operations: ingest, query, and lint. [\[blog.starmorph.com\]](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide)
* The **HackerNoon article** presents a practical account of using Claude Code and Karpathy’s LLM Wiki pattern to maintain project knowledge across multiple projects. [\[hackernoon.com\]](https://hackernoon.com/how-i-built-a-self-maintaining-knowledge-base-for-6-projects-using-claude-code-and-karpathys-llm-wiki)
* Some short-form links, especially Reddit and Substack entries, did not expose readable page content through the inspection tool. The linked GitHub targets were still inspected where available.

## Preliminary Synthesis

The inspected material points to four main implementation families:

1. **Markdown-first wiki agents**
   * `LLM-wiki`
   * `llm-wiki-agent`
   * `llm-wiki-compiler`

2. **Obsidian-local compilers**
   * `obsidian-llm-wiki-local`

3. **Research lifecycle systems**
   * `AutoSci` / former `OmegaWiki`

4. **Database-backed knowledge systems**
   * `OpenKB`
   * `BrainDB`

The shared object across all inspected sources is a **persistent compiled knowledge layer**. Raw files are treated as source material. Markdown pages, indexes, logs, citations, graph links, and query outputs become the durable working knowledge base.
"""
Let me know when you're ready to continue.

---

## Assistant

The enriched repository and link overview has been analyzed and incorporated into the working context.

The following distinctions are now established:

- implementation family and architectural scope;
- markdown-first, Obsidian-local, research-agent, and database-backed models;
- compile-first and mandatory-writeback principles;
- source provenance, citation, indexing, logging, linting, and graph-link functions;
- redirects from OmegaWiki to AutoSci and from the former Atomic Memory repository to Atomic Strata;
- maintenance status of `obsidian-llm-wiki-local`;
- limitations affecting Reddit, Substack, and HackerNoon content inspection.

The preliminary synthesis is consistent with the original LLM Wiki concept: raw sources remain stable, while a persistent compiled knowledge layer is continuously updated and reused.

**Ready to continue.**

---

## User

Now, here is some context on the project:

LLM Wiki including Claude Code will operate inside VM.

Facts:
1. VM is operational (Ubuntu 26.04 LTS, VM is Gen 2)
2. Claude Code is installed inside VM
3. Obsidian is installed inside VM
4. Obsidian Web Clipper is installed inside VM in Firefox

-----

`/home/nekiee`


```
# Global level - LLM_Wiki
/home/nekiee/LLL_Wiki/
                |- CLAUDE.md
                |- index.md
                |- log.md

# Project level - Travel guide
/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan
                                     |- raw/
                                     |- wiki/
                                     |- CLAUDE.md
                                     |- index.md
                                     |- log.md

# Project level - Procedure review
/home/nekiee/LLL_Wiki/Project02_Internal_procedure/Procedure_A
                                                       |- raw/
                                                       |- wiki/
                                                       |- CLAUDE.md
                                                       |- index.md
                                                       |- log.md

# Project level - Procedure review
/home/nekiee/LLL_Wiki/Project02_Internal_procedure/Procedure_B
                                                       |- raw/
                                                       |- wiki/
                                                       |- CLAUDE.md
                                                       |- index.md
                                                       |- log.md

# Project level - NQA Supplier Audit
/home/nekiee/LLL_Wiki/Project03_NQA_Enconet/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - NQA Supplier Audit
/home/nekiee/LLL_Wiki/Project03_NQA_Tekol/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - NQA Internal Audit
/home/nekiee/LLL_Wiki/Project04_NQA_IA-ING-DOV/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - NQA Internal Audit
/home/nekiee/LLL_Wiki/Project04_NQA_IA-ING-MOD/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - NQA Internal Audit
/home/nekiee/LLL_Wiki/Project04_NQA_IA-TOVZ-GR/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Internal Audit
/home/nekiee/LLL_Wiki/Project04_NQA_IA-TOVZ-SKL/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Software Development
/home/nekiee/LLL_Wiki/Project05_SW_FIN/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Software Development
/home/nekiee/LLL_Wiki/Project05-SW_LOTO/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Software Development
/home/nekiee/LLL_Wiki/Project05-SW_Games/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Legal
/home/nekiee/LLL_Wiki/Project06-LEG_01/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md
# Project level - Legal
/home/nekiee/LLL_Wiki/Project06-LEG_02/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Legal
/home/nekiee/LLL_Wiki/Project06-LEG_03/
                                  |- raw/
                                  |- wiki/
                                  |- CLAUDE.md
                                  |- index.md
                                  |- log.md

# Project level - Prompt
/home/nekiee/LLL_Wiki/Project07/AXIOM_Report_Review
                                     |- raw/
                                     |- wiki/
                                     |- CLAUDE.md
                                     |- index.md
                                     |- log.md
# Project level - Prompt
/home/nekiee/LLL_Wiki/Project07/AXIOM_JSON_Sieve
                                     |- raw/
                                     |- wiki/
                                     |- CLAUDE.md
                                     |- index.md
                                     |- log.md
# Project level - Prompt
/home/nekiee/LLL_Wiki/Project07/AXIOM_Report_Sentiment
                                     |- raw/
                                     |- wiki/
                                     |- CLAUDE.md
                                     |- index.md
                                     |- log.md

.....
(LATER)
# Project level - ISO 9001
# Project level - ISO 17025
# Project level - ISO 45001

```

Let me know when you're ready to continue.

---

## Assistant

The VM environment and proposed directory hierarchy have been analyzed.

The working context now includes:

- Ubuntu 26.04 LTS Generation 2 VM
- Claude Code, Obsidian, Firefox, and Obsidian Web Clipper
- global LLM Wiki control files under `/home/nekiee/LLL_Wiki/`
- isolated project workspaces with separate `raw/`, `wiki/`, `CLAUDE.md`, `index.md`, and `log.md`
- project groups for travel, procedure review, supplier audits, internal audits, software development, legal work, prompt engineering, and later ISO standards
- the requirement for project-specific knowledge isolation under one global governance layer

One naming detail has been retained for later review: the root directory uses `LLL_Wiki`, with three `L` characters.

**Ready to continue.**

---

## User

Here is master plan of the 1st Wiki project. Inspect it.

Let me know when you're ready to continue.

### Attached file: `Pasted markdown(20).md`

# MASTER PLAN — Travel Guide LLM Wiki (v2)
## Project01 / Trip_to_Japan
### Implementation Plan for Claude Code Execution — Revised

---

## CHANGE LOG (v1 → v2)

This revision addresses every must-fix item raised in the v1 critique and a subset of the should-fix items. The structural changes are summarized below; the body of the document contains the full corrected content.

| Area | v1 state | v2 state |
|------|----------|----------|
| Frontmatter parser | Broken (started after closing fence) | Fixed; shared parser in `scripts/_yaml_util.py`; uses PyYAML |
| `cost_level=n-a` | Rejected by validator | Allowed; `n-a` added to controlled vocabularies |
| `time_required=n-a` | Allowed but enum unused | `n-a` added; enum now enforced |
| `best_season` multi-value | Rejected by validator | Supported; comma-separated and YAML-list values accepted |
| `itinerary` in DECISION_TYPES | Caused valid itineraries to fail | Removed; itinerary has its own section-based check |
| `_source-list.md` location | Inside immutable `raw/` | Moved to `sources/_source-list.md` |
| Capture staging | None — Web Clipper writes to `raw/` directly | New `incoming/` staging folder; promoted to `raw/` after review |
| Raw immutability check | File write bits only | File and directory write bits |
| `validate_links.py` planned-stems | Comment lines treated as valid stems | Blank lines and `#` comments ignored |
| `validate_links.py` folder links | Folder-qualified links failed | Both stems and relative paths supported |
| Stale data | No enforcement | New `validate_staleness.py` script |
| `run_all_validations.py` IDs | Second-resolution collisions | Microsecond resolution; per-run group ID |
| Permission deny rules | Path format uncertain | Relative and absolute patterns both listed |
| Bash deny rules framing | Implied comprehensive | Explicitly labeled advisory |
| Slash command enforcement | Markdown only | Backed by `scripts/trip_ingest.py` state machine |
| Git init position | Phase 8 (after EPIC 7) | Phase 4 (after skeleton, before templates) |
| Phase numbering | Inconsistent (Phase 12 mention missing in EPIC list) | Reconciled |
| EPIC 0 framing | Called "stubs" but contained real logic | Renamed "Initial Validation Layer"; behavior documented |
| YAML dependency | Manual parser | PyYAML required; installation step added |
| Source-existence check | Not validated | New check in `validate_frontmatter.py` |
| Date format check | Not validated | New check in `validate_frontmatter.py` |
| Manifest row values | Header-only check | Header plus row-value sanity check |

---

## SYSTEM IDENTITY

```
System name  : Travel Guide LLM Wiki
Project      : Project01 / Trip_to_Japan
Project root : /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan
Global root  : /home/nekiee/LLL_Wiki
Executor     : Claude Code (running inside Ubuntu 26.04 Hyper-V guest VM)
Interface    : Obsidian (GUI, running inside VM)
Capture tool : Firefox + Obsidian Web Clipper (running inside VM)
Host OS      : Windows 11 Pro (host only — no Claude Code activity on host)
Python       : 3.9+ with PyYAML installed (pip install pyyaml)
```

All file operations, script execution, git commands, and validation runs are performed by Claude Code inside the VM. The host Windows machine is irrelevant to the implementation. Claude Code has full filesystem freedom within the VM, subject to the permission rules in `.claude/settings.json` and the OS-level chmod protections applied to `raw/`.

---

## ARCHITECTURE OVERVIEW

```
/home/nekiee/LLL_Wiki/              ← Global root (multi-project workspace)
    CLAUDE.md                        ← Global wiki rules (inherited by all projects)
    index.md                         ← Cross-project index
    log.md                           ← Global operation log

/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/    ← Project root (Obsidian vault)
    CLAUDE.md                        ← Project-specific rules
    CLAUDE.local.md                  ← Machine-local notes (gitignored)
    README.md                        ← Human-readable project description
    .gitignore

    incoming/                        ← Capture staging (writable)
                                       Web Clipper saves here first.
                                       Human reviews and edits metadata here.
                                       Files are promoted to raw/ after validation.

    raw/                             ← Immutable source documents
        assets/                      ← Downloaded images

    sources/                         ← Source registry (writable, human-maintained)
        _source-list.md              ← URL planning and capture status tracker

    wiki/                            ← LLM-maintained knowledge pages
        index.md                     ← Page catalog (Claude reads this first)
        log.md                       ← Append-only operation record
        current-status.md            ← Session continuity file
        cities/
        districts/
        food/
        restaurants/
        attractions/
        hotels/
        transport/
        budget/
        itineraries/
        day-trips/
        practical/
        decisions/

    manifests/                       ← CSV tracking files
        raw_sources.csv
        wiki_pages.csv
        ingest_runs.csv
        decisions.csv
        validation_runs.csv
        planned_pages.txt

    .claude/                         ← Claude Code configuration
        settings.json
        commands/                    ← Slash command definitions

    templates/                       ← Page templates for Claude to use

    scripts/                         ← Validation scripts and the ingest state machine
        _yaml_util.py                ← Shared frontmatter parser
        trip_ingest.py               ← Ingest state machine (approval gate)
        validate_*.py                ← Ten validation scripts
        run_all_validations.py       ← Aggregator
```

### Key architectural decisions in v2

The `incoming/` directory exists so that the canonical `raw/` directory never needs its chmod lock broken. Web Clipper captures land in `incoming/` first. After a human reviews and corrects frontmatter, the file is moved into `raw/` and the lock is re-applied. This avoids the v1 problem where every new capture required temporarily exposing the immutable source-of-truth folder.

The `sources/_source-list.md` registry lives outside `raw/`. It is human-maintained and updated as sources move through their lifecycle. Moving it out of `raw/` eliminates the v1 contradiction where the immutability check would conflict with the registry's natural update cadence.

The `manifests/planned_pages.txt` file is now an explicit required artifact, listed in `validate_structure.py` REQUIRED_FILES. Its parser ignores blank lines and `#` comment lines.

---

## TDD PHILOSOPHY

**Test-first rule — strictly enforced:**

```
Phase 0 runs before any other phase.
Phase 0 creates the initial validation layer (10 scripts + shared parser).
No epic beyond Phase 0 may begin until run_all_validations.py runs successfully,
producing the expected mix of PASS (content validators on empty input) and
FAIL (structural validators with no structure yet built).

Every task in every epic must name its verification command.
Every ingest, every write, every structural change ends with:
  python3 scripts/run_all_validations.py
```

**Note on terminology change**

The v1 plan called these "stubs." This was misleading. The scripts contain real validation logic from day one. Some return PASS on empty input by design (a content validator over zero content has nothing to fail). Some return FAIL by design until the structure they validate exists (the structural validator fails until the project skeleton is built).

This is the correct behavior for a TDD layer. The framing has been corrected: the scripts are real validators, not stubs.

**TDD cycle per task:**

```
1. Identify expected behavior.
2. Write or update the validation script (test exists before structure).
3. Run the script → confirm the expected result for the current state.
4. Implement the minimal structure or file.
5. Run the script → confirm it now returns PASS.
6. Record result in manifests/validation_runs.csv and wiki/log.md.
```

---

## PHASE EXECUTION ORDER (v2)

```
Phase 0  — Initial Validation Layer (write all tests, run baseline)
Phase 1  — Global LLM Wiki root setup
Phase 2  — Project directory structure
Phase 3  — Git initialization (moved earlier for rollback safety)
Phase 4  — Permission and immutability layer
Phase 5  — Wiki schema: frontmatter + templates
Phase 6  — Travel ontology and domain model
Phase 7  — Manifest tracking system
Phase 8  — CLAUDE.md: complete project control schema
Phase 9  — Source capture preparation (incoming/ + sources/)
Phase 10 — Ingest pipeline (trip_ingest.py + workflow)
Phase 11 — Claude Code command system
Phase 12 — Obsidian integration
Phase 13 — Travel outputs: itinerary, budget, decisions
Phase 14 — Session management and context continuity
Phase 15 — Iterative expansion (deferred)
```

The phase order matches the EPIC numbering exactly in v2. There is no "Full validation script implementation" phase, since validation scripts are written in EPIC 0 and refined inside the relevant EPIC when a new check is added.

---

# EPIC 0 — Initial Validation Layer

## What & Why

The TDD layer is the foundation. Every later phase depends on these scripts existing and producing predictable results. This epic creates the shared frontmatter parser, ten validation scripts, the ingest state machine, and the aggregator. All scripts use UTF-8, all rely on the shared parser, and all return clear PASS or FAIL messages.

PyYAML is a hard dependency. The installation step is documented before the first script is written.

## Task 0.1 — Install PyYAML and create scripts directory

### Commands

```bash
# Install PyYAML inside the VM Python environment used by Claude Code:
pip install pyyaml
# Or, if conda is used:
conda install -c conda-forge pyyaml

# Verify:
python3 -c "import yaml; print(yaml.__version__)"

# Create the scripts directory:
mkdir -p /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/scripts
```

## Task 0.2 — Create scripts/_yaml_util.py (shared parser)

### File: scripts/_yaml_util.py

```python
#!/usr/bin/env python3
"""Shared YAML frontmatter parser for all validation scripts.

This module is the single source of truth for how Markdown frontmatter
is read across the validation layer. All validators import parse_frontmatter
from this file so that a fix here propagates everywhere.

PyYAML is required. Install with: pip install pyyaml
"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a Markdown file.

    Returns a tuple (fields, body) where:
      fields is a dict of parsed YAML, or None if no valid frontmatter exists.
      body is the Markdown content after the closing fence.

    A valid frontmatter block starts with --- on the first line and ends
    with --- on a later line. Everything between is parsed as YAML.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Normalize line endings to LF.
    content = content.replace("\r\n", "\n")

    # Must start with --- on the very first line.
    if not content.startswith("---\n"):
        return None, content

    # Skip the opening fence.
    rest = content[4:]

    # Find the closing fence on its own line.
    end_idx = rest.find("\n---\n")
    if end_idx == -1:
        # Allow file to end with ---\n (no trailing newline).
        if rest.endswith("\n---"):
            end_idx = len(rest) - 4
            fm_text = rest[:end_idx]
            body = ""
        else:
            return None, content
    else:
        fm_text = rest[:end_idx]
        body = rest[end_idx + 5:]

    try:
        fields = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        print(f"YAML parse error in {filepath}: {exc}", file=sys.stderr)
        return None, body

    if fields is None:
        fields = {}
    if not isinstance(fields, dict):
        return None, body

    return fields, body


def is_valid_date(value):
    """Return True if value matches YYYY-MM-DD. Accepts placeholder text."""
    if value is None:
        return False
    s = str(value).strip()
    # Accept template placeholder; templates use 'YYYY-MM-DD' as literal text.
    if s == "YYYY-MM-DD":
        return True
    return bool(DATE_RE.match(s))


def normalize_value(value):
    """Convert any YAML-parsed scalar to a comparable string."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def normalize_list(value):
    """Return a list view of value. Scalars become single-element lists."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # Allow comma-separated strings.
        if "," in value:
            return [v.strip() for v in value.split(",") if v.strip()]
        if value.strip() == "":
            return []
        return [value.strip()]
    return [value]


if __name__ == "__main__":
    # Self-test: parse own header to confirm PyYAML works.
    print("PASS: _yaml_util.py loaded; PyYAML available.")
```

## Task 0.3 — Create scripts/validate_structure.py

### File: scripts/validate_structure.py

```python
#!/usr/bin/env python3
"""Validate required project directory and file structure."""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_DIRS = [
    "incoming",
    "raw", "raw/assets",
    "sources",
    "wiki", "wiki/cities", "wiki/districts", "wiki/food",
    "wiki/restaurants", "wiki/attractions", "wiki/hotels",
    "wiki/transport", "wiki/budget", "wiki/itineraries",
    "wiki/day-trips", "wiki/practical", "wiki/decisions",
    "manifests", ".claude", ".claude/commands",
    "templates", "scripts",
]

REQUIRED_FILES = [
    "CLAUDE.md", "CLAUDE.local.md", "README.md", ".gitignore",
    "wiki/index.md", "wiki/log.md", "wiki/current-status.md",
    "sources/_source-list.md",
    "manifests/raw_sources.csv", "manifests/wiki_pages.csv",
    "manifests/ingest_runs.csv", "manifests/decisions.csv",
    "manifests/validation_runs.csv", "manifests/planned_pages.txt",
    ".claude/settings.json",
    "scripts/_yaml_util.py",
]


def main():
    failures = []
    for d in REQUIRED_DIRS:
        path = os.path.join(PROJECT_ROOT, d)
        if not os.path.isdir(path):
            failures.append(f"MISSING DIR : {d}")
    for f in REQUIRED_FILES:
        path = os.path.join(PROJECT_ROOT, f)
        if not os.path.isfile(path):
            failures.append(f"MISSING FILE: {f}")
    if failures:
        print("FAIL: validate_structure.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print("PASS: validate_structure.py — required structure exists")


if __name__ == "__main__":
    main()
```

## Task 0.4 — Create scripts/validate_frontmatter.py

### File: scripts/validate_frontmatter.py

```python
#!/usr/bin/env python3
"""Validate YAML frontmatter in all wiki pages.

Uses scripts/_yaml_util.py for robust parsing. Checks include:
  - Frontmatter block is present and parseable.
  - All required fields are present.
  - Controlled-vocabulary fields hold allowed values.
  - Date fields use YYYY-MM-DD format.
  - sources: entries point to existing files.
  - best_season supports multiple values (list or comma string).
"""
import os
import sys
import glob

# Allow import of sibling utility module.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _yaml_util import parse_frontmatter, is_valid_date, normalize_value, normalize_list

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WIKI_DIR = os.path.join(PROJECT_ROOT, "wiki")

REQUIRED_FIELDS = [
    "title", "type", "city", "district", "category",
    "created", "updated", "last_verified",
    "sources", "source_urls", "confidence", "status",
    "cost_level", "time_required", "best_for",
    "best_season", "related_pages",
]

VALID_TYPES = {
    "city", "district", "food", "restaurant", "attraction",
    "hotel", "transport", "budget", "itinerary", "day-trip",
    "practical-tip", "seasonal-update", "decision",
    "source-summary", "seasonal-event", "calendar",
}

VALID_CONFIDENCE = {"high", "medium", "low", "unknown"}
VALID_STATUS = {"draft", "active", "needs-review", "outdated", "rejected", "superseded"}
VALID_COST = {"free", "low", "medium", "high", "luxury", "unknown", "n-a"}
VALID_TIME = {"short", "half-day", "full-day", "multi-day", "unknown", "n-a"}
VALID_SEASON = {"spring", "summer", "autumn", "winter", "all", "unknown", "n-a"}

DATE_FIELDS = ["created", "updated", "last_verified"]

SKIP_FILES = {"index.md", "log.md", "current-status.md"}


def main():
    md_files = glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True)
    pages = [f for f in md_files if os.path.basename(f) not in SKIP_FILES]

    if not pages:
        print("PASS: validate_frontmatter.py — no wiki pages yet (expected at start)")
        sys.exit(0)

    failures = []
    for fp in pages:
        rel = os.path.relpath(fp, PROJECT_ROOT)
        fm, _ = parse_frontmatter(fp)
        if fm is None:
            failures.append(f"{rel}: missing or invalid frontmatter block")
            continue

        for field in REQUIRED_FIELDS:
            if field not in fm:
                failures.append(f"{rel}: missing field '{field}'")

        if "type" in fm:
            val = normalize_value(fm["type"])
            if val and val not in VALID_TYPES:
                failures.append(f"{rel}: invalid type '{val}'")

        if "confidence" in fm:
            val = normalize_value(fm["confidence"])
            if val and val not in VALID_CONFIDENCE:
                failures.append(f"{rel}: invalid confidence '{val}'")

        if "status" in fm:
            val = normalize_value(fm["status"])
            if val and val not in VALID_STATUS:
                failures.append(f"{rel}: invalid status '{val}'")

        if "cost_level" in fm:
            val = normalize_value(fm["cost_level"])
            if val and val not in VALID_COST:
                failures.append(f"{rel}: invalid cost_level '{val}'")

        if "time_required" in fm:
            val = normalize_value(fm["time_required"])
            if val and val not in VALID_TIME:
                failures.append(f"{rel}: invalid time_required '{val}'")

        if "best_season" in fm:
            seasons = normalize_list(fm["best_season"])
            for s in seasons:
                sv = normalize_value(s)
                if sv and sv not in VALID_SEASON:
                    failures.append(f"{rel}: invalid best_season value '{sv}'")

        for df in DATE_FIELDS:
            if df in fm:
                val = normalize_value(fm[df])
                if val and not is_valid_date(val):
                    failures.append(f"{rel}: invalid {df} format '{val}' (expected YYYY-MM-DD)")

        if "sources" in fm:
            for src in normalize_list(fm["sources"]):
                sv = normalize_value(src)
                if not sv:
                    continue
                src_path = os.path.join(PROJECT_ROOT, sv)
                if not os.path.isfile(src_path):
                    failures.append(f"{rel}: source file does not exist: {sv}")

    if failures:
        print("FAIL: validate_frontmatter.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print(f"PASS: validate_frontmatter.py — {len(pages)} pages valid")


if __name__ == "__main__":
    main()
```

## Task 0.5 — Create scripts/validate_raw_immutability.py

### File: scripts/validate_raw_immutability.py

```python
#!/usr/bin/env python3
"""Validate raw/ directory protection at multiple layers.

Layer 1: .claude/settings.json deny rules are present.
Layer 2: All files under raw/ have no write bits set.
Layer 3: All directories under raw/ have no group/other write bits set.
         (The owner directory bit must remain readable for traversal.)

Layer 3 is enforced because, on POSIX, the ability to delete or rename
a file depends primarily on the parent directory's write permission, not
the file's own write bit.
"""
import json
import os
import stat
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "raw")
SETTINGS = os.path.join(PROJECT_ROOT, ".claude", "settings.json")

REQUIRED_DENY = [
    "Edit(raw/**)",
    "Write(raw/**)",
    "Edit(/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/raw/**)",
    "Write(/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/raw/**)",
]


def main():
    failures = []

    if not os.path.isfile(SETTINGS):
        failures.append("MISSING: .claude/settings.json")
    else:
        with open(SETTINGS, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                failures.append(f"INVALID JSON in settings.json: {e}")
                data = {}
        deny_rules = data.get("permissions", {}).get("deny", [])
        for rule in REQUIRED_DENY:
            if rule not in deny_rules:
                failures.append(f"MISSING deny rule: {rule}")

    if os.path.isdir(RAW_DIR):
        for root, dirs, files in os.walk(RAW_DIR):
            # Directory permissions: no group or other write.
            dir_stat = os.stat(root)
            if dir_stat.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
                rel = os.path.relpath(root, PROJECT_ROOT)
                failures.append(f"DIR WRITABLE by group or other: {rel}")

            # File permissions: no write bits at all.
            for fname in files:
                fpath = os.path.join(root, fname)
                s = os.stat(fpath)
                if s.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
                    rel = os.path.relpath(fpath, PROJECT_ROOT)
                    failures.append(f"FILE WRITABLE: {rel} (should be read-only)")

    if failures:
        print("FAIL: validate_raw_immutability.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print("PASS: validate_raw_immutability.py — raw/ is protected")


if __name__ == "__main__":
    main()
```

## Task 0.6 — Create scripts/validate_manifests.py

### File: scripts/validate_manifests.py

```python
#!/usr/bin/env python3
"""Validate CSV manifest files: required columns plus row-value sanity."""
import csv
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTS_DIR = os.path.join(PROJECT_ROOT, "manifests")

REQUIRED_COLUMNS = {
    "raw_sources.csv": [
        "source_id", "filename", "title", "source_url", "captured_date",
        "source_type", "city", "district", "topic", "status",
        "ingested_date", "notes",
    ],
    "wiki_pages.csv": [
        "page_id", "filename", "title", "type", "city", "district",
        "category", "status", "created", "updated", "sources", "confidence",
    ],
    "ingest_runs.csv": [
        "run_id", "date", "source_filename", "mode", "preview_status",
        "pages_created", "pages_updated", "conflicts_found", "result", "notes",
    ],
    "decisions.csv": [
        "decision_id", "date", "decision_topic", "selected_option",
        "rejected_options", "reasoning", "sources", "confidence", "status",
    ],
    "validation_runs.csv": [
        "run_id", "date", "script", "result", "failures", "notes",
    ],
}

VALID_INGEST_MODE = {"preview", "apply"}
VALID_INGEST_PREVIEW_STATUS = {"pending", "applying", "applied", "failed", "rejected"}
VALID_INGEST_RESULT = {
    "pending-approval", "in-progress", "completed",
    "failed", "rejected", "recovered",
}
VALID_RAW_SOURCE_STATUS = {
    "planned", "captured", "ingest-previewed",
    "ingested", "rejected", "needs-recapture",
}
VALID_DECISION_STATUS = {"draft", "active", "superseded", "rejected"}


def check_row_values(csv_path, csv_name, failures):
    """Inspect data rows for sanity. Header presence already verified."""
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row_num = 1
        for row in reader:
            row_num += 1
            if csv_name == "ingest_runs.csv":
                m = (row.get("mode") or "").strip()
                if m and m not in VALID_INGEST_MODE:
                    failures.append(f"{csv_name}:row {row_num}: invalid mode '{m}'")
                ps = (row.get("preview_status") or "").strip()
                if ps and ps not in VALID_INGEST_PREVIEW_STATUS:
                    failures.append(f"{csv_name}:row {row_num}: invalid preview_status '{ps}'")
                rs = (row.get("result") or "").strip()
                if rs and rs not in VALID_INGEST_RESULT:
                    failures.append(f"{csv_name}:row {row_num}: invalid result '{rs}'")
            elif csv_name == "raw_sources.csv":
                s = (row.get("status") or "").strip()
                if s and s not in VALID_RAW_SOURCE_STATUS:
                    failures.append(f"{csv_name}:row {row_num}: invalid status '{s}'")
            elif csv_name == "decisions.csv":
                s = (row.get("status") or "").strip()
                if s and s not in VALID_DECISION_STATUS:
                    failures.append(f"{csv_name}:row {row_num}: invalid status '{s}'")


def main():
    failures = []
    for csv_name, required_cols in REQUIRED_COLUMNS.items():
        csv_path = os.path.join(MANIFESTS_DIR, csv_name)
        if not os.path.isfile(csv_path):
            failures.append(f"MISSING: manifests/{csv_name}")
            continue
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                failures.append(f"EMPTY or no header: manifests/{csv_name}")
                continue
            actual = set(reader.fieldnames)
            for col in required_cols:
                if col not in actual:
                    failures.append(f"manifests/{csv_name}: missing column '{col}'")
        # Row-value pass.
        if not failures or all("missing column" not in fa for fa in failures
                               if fa.startswith(f"manifests/{csv_name}")):
            try:
                check_row_values(csv_path, csv_name, failures)
            except Exception as exc:
                failures.append(f"manifests/{csv_name}: row scan error: {exc}")
    if failures:
        print("FAIL: validate_manifests.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print("PASS: validate_manifests.py — all manifests valid")


if __name__ == "__main__":
    main()
```

## Task 0.7 — Create scripts/validate_index.py

### File: scripts/validate_index.py

```python
#!/usr/bin/env python3
"""Validate wiki/index.md references every active wiki page.

A reference must be an Obsidian wikilink [[stem]] or [[folder/stem]],
or a Markdown link with the relative path. Plain prose mentions of the
stem are not sufficient to count as an index reference.
"""
import glob
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_DIR = os.path.join(PROJECT_ROOT, "wiki")
INDEX_FILE = os.path.join(WIKI_DIR, "index.md")
SKIP_FILES = {"index.md", "log.md", "current-status.md"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\]\(([^)]+\.md)\)")


def collect_references(index_content):
    """Return a set of normalized references found in index.md."""
    refs = set()
    for m in WIKILINK_RE.finditer(index_content):
        target = m.group(1).strip().lower()
        # Wikilinks may include folder prefix; track both forms.
        refs.add(target)
        refs.add(target.split("/")[-1])
    for m in MDLINK_RE.finditer(index_content):
        path = m.group(1).strip().lower()
        # Drop leading ./ or wiki/ if present.
        path = path.lstrip("./")
        if path.startswith("wiki/"):
            path = path[5:]
        stem = os.path.splitext(os.path.basename(path))[0]
        refs.add(stem)
        refs.add(path[:-3] if path.endswith(".md") else path)
    return refs


def main():
    if not os.path.isfile(INDEX_FILE):
        print("FAIL: validate_index.py — wiki/index.md does not exist")
        sys.exit(1)

    with open(INDEX_FILE, encoding="utf-8") as f:
        index_content = f.read()

    refs = collect_references(index_content)

    md_files = glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True)
    failures = []
    for fp in md_files:
        fname = os.path.basename(fp)
        if fname in SKIP_FILES:
            continue
        stem = os.path.splitext(fname)[0].lower()
        rel = os.path.relpath(fp, WIKI_DIR).replace("\\", "/")
        rel_noext = rel[:-3] if rel.endswith(".md") else rel
        if stem not in refs and rel_noext.lower() not in refs:
            failures.append(f"NOT INDEXED: {rel} (expected [[{stem}]] or [[{rel_noext}]])")

    if failures:
        print("FAIL: validate_index.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print(f"PASS: validate_index.py — {len(md_files)} files checked")


if __name__ == "__main__":
    main()
```

## Task 0.8 — Create scripts/validate_links.py

### File: scripts/validate_links.py

```python
#!/usr/bin/env python3
"""Validate all [[wikilinks]] in wiki pages resolve to existing files.

Allowed targets:
  - The stem of any existing wiki/*.md file.
  - The relative path (without extension) of any existing wiki/*.md file.
  - Any stem listed in manifests/planned_pages.txt (planned but not yet built).

planned_pages.txt parsing rules:
  - One stem per line.
  - Blank lines are ignored.
  - Lines beginning with # are ignored as comments.

Duplicate stem detection:
  If two wiki files share the same basename stem (different folders), the
  script reports a duplicate-stem warning so the human can disambiguate.
"""
import glob
import os
import re
import sys
from collections import defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_DIR = os.path.join(PROJECT_ROOT, "wiki")
PLANNED_LINKS_FILE = os.path.join(PROJECT_ROOT, "manifests", "planned_pages.txt")

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")


def collect_allowed_targets():
    stems = set()
    rel_paths = set()
    stem_to_files = defaultdict(list)
    for fp in glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True):
        stem = os.path.splitext(os.path.basename(fp))[0].lower()
        rel = os.path.relpath(fp, WIKI_DIR).replace("\\", "/")
        rel_no_ext = rel[:-3] if rel.endswith(".md") else rel
        stems.add(stem)
        rel_paths.add(rel_no_ext.lower())
        stem_to_files[stem].append(rel)
    return stems, rel_paths, stem_to_files


def collect_planned_stems():
    if not os.path.isfile(PLANNED_LINKS_FILE):
        return set()
    planned = set()
    with open(PLANNED_LINKS_FILE, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            planned.add(line.lower())
    return planned


def main():
    stems, rel_paths, stem_to_files = collect_allowed_targets()
    planned = collect_planned_stems()
    allowed = stems | rel_paths | planned

    failures = []
    warnings = []

    # Duplicate-stem warnings (informational).
    for stem, files in stem_to_files.items():
        if len(files) > 1:
            warnings.append(f"DUPLICATE STEM '{stem}': {', '.join(files)}")

    for fp in glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True):
        rel = os.path.relpath(fp, PROJECT_ROOT)
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        for match in WIKILINK_RE.finditer(content):
            target = match.group(1).strip().lower()
            if target not in allowed:
                failures.append(f"{rel}: broken link [[{target}]]")

    if warnings:
        print("WARNINGS: validate_links.py")
        for w in warnings:
            print(f"  {w}")

    if failures:
        print("FAIL: validate_links.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print("PASS: validate_links.py — all wiki links resolve")


if __name__ == "__main__":
    main()
```

## Task 0.9 — Create scripts/validate_source_metadata.py

### File: scripts/validate_source_metadata.py

```python
#!/usr/bin/env python3
"""Validate captured raw source files for required frontmatter and naming."""
import glob
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _yaml_util import parse_frontmatter, is_valid_date, normalize_value

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(PROJECT_ROOT, "raw")

REQUIRED_SOURCE_FIELDS = [
    "source_url", "captured_date", "source_type",
    "city", "district", "topic", "language",
    "capture_method", "status",
]

VALID_SOURCE_STATUS = {
    "planned", "captured", "ingest-previewed",
    "ingested", "rejected", "needs-recapture",
}

FILENAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")


def main():
    md_files = [
        f for f in glob.glob(os.path.join(RAW_DIR, "*.md"))
    ]

    if not md_files:
        print("PASS: validate_source_metadata.py — no sources yet (expected at start)")
        sys.exit(0)

    failures = []
    for fp in md_files:
        fname = os.path.basename(fp)
        rel = os.path.relpath(fp, PROJECT_ROOT)

        if not FILENAME_RE.match(fname):
            failures.append(f"{rel}: filename not lowercase kebab-case")

        fm, _ = parse_frontmatter(fp)
        if fm is None:
            failures.append(f"{rel}: missing or invalid frontmatter block")
            continue

        for field in REQUIRED_SOURCE_FIELDS:
            val = fm.get(field)
            if val is None or normalize_value(val) == "":
                failures.append(f"{rel}: missing or empty field '{field}'")

        if "status" in fm:
            s = normalize_value(fm["status"])
            if s and s not in VALID_SOURCE_STATUS:
                failures.append(f"{rel}: invalid status '{s}'")

        if "captured_date" in fm:
            d = normalize_value(fm["captured_date"])
            if d and not is_valid_date(d):
                failures.append(f"{rel}: invalid captured_date '{d}' (expected YYYY-MM-DD)")

    if failures:
        print("FAIL: validate_source_metadata.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print(f"PASS: validate_source_metadata.py — {len(md_files)} sources valid")


if __name__ == "__main__":
    main()
```

## Task 0.10 — Create scripts/validate_travel_schema.py

### File: scripts/validate_travel_schema.py

```python
#!/usr/bin/env python3
"""Validate travel-specific fields on relevant wiki page types.

Decision-quality fields are required on attraction, restaurant, hotel,
and transport pages. Itinerary pages are NOT in this list (they have
their own structural section requirements instead).
"""
import glob
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _yaml_util import parse_frontmatter, normalize_value

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WIKI_DIR = os.path.join(PROJECT_ROOT, "wiki")
SKIP_FILES = {"index.md", "log.md", "current-status.md"}

DECISION_TYPES = {
    "attraction", "restaurant", "hotel", "transport",
}

DECISION_FIELDS = [
    "location", "nearest_station", "opening_hours",
    "reservation_required", "estimated_cost", "estimated_duration",
    "transport_time", "weather_sensitivity", "crowd_risk",
    "best_time_to_visit",
]

ITINERARY_SECTIONS = [
    "## Summary", "## Assumptions", "## Day-by-day plan",
    "## Transport notes", "## Food plan", "## Budget estimate",
    "## Risks", "## Alternatives", "## Open questions", "## Sources",
]


def main():
    md_files = glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True)
    relevant = [f for f in md_files if os.path.basename(f) not in SKIP_FILES]
    if not relevant:
        print("PASS: validate_travel_schema.py — no wiki pages yet")
        sys.exit(0)

    failures = []
    for fp in relevant:
        rel = os.path.relpath(fp, PROJECT_ROOT)
        fm, body = parse_frontmatter(fp)
        if fm is None:
            continue  # frontmatter validator reports this

        page_type = normalize_value(fm.get("type", ""))

        if page_type in DECISION_TYPES:
            for field in DECISION_FIELDS:
                if field not in fm:
                    failures.append(
                        f"{rel}: [{page_type}] missing decision field '{field}'"
                    )

        if page_type == "itinerary":
            for section in ITINERARY_SECTIONS:
                if section not in body:
                    failures.append(f"{rel}: itinerary missing section '{section}'")

    if failures:
        print("FAIL: validate_travel_schema.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print("PASS: validate_travel_schema.py — travel schema valid")


if __name__ == "__main__":
    main()
```

## Task 0.11 — Create scripts/validate_command_names.py

### File: scripts/validate_command_names.py

```python
#!/usr/bin/env python3
"""Validate .claude/commands/ files use trip-* naming and avoid built-in conflicts.

The BUILTIN_COMMANDS list mirrors known Claude Code reserved command names
as of the v2 plan date. This list should be reviewed when Claude Code is
upgraded, since new built-in commands could collide silently otherwise.
"""
import glob
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMANDS_DIR = os.path.join(PROJECT_ROOT, ".claude", "commands")

BUILTIN_COMMANDS = {
    "context", "schedule", "help", "clear", "compact", "cost",
    "doctor", "init", "login", "logout", "memory", "model",
    "pr_comments", "quit", "release-notes", "review", "status",
    "terminal", "vim", "config", "permissions",
}

REQUIRED_COMMANDS = [
    "trip-context.md", "trip-capture-review.md", "trip-ingest.md",
    "trip-query.md", "trip-challenge.md", "trip-schedule.md",
    "trip-budget.md", "trip-lint.md", "trip-closeday.md",
]


def main():
    failures = []
    if not os.path.isdir(COMMANDS_DIR):
        print("FAIL: validate_command_names.py — .claude/commands/ does not exist")
        sys.exit(1)
    for req in REQUIRED_COMMANDS:
        if not os.path.isfile(os.path.join(COMMANDS_DIR, req)):
            failures.append(f"MISSING command: {req}")
    for fp in glob.glob(os.path.join(COMMANDS_DIR, "*.md")):
        stem = os.path.splitext(os.path.basename(fp))[0]
        if not stem.startswith("trip-"):
            failures.append(f"BAD NAME: {stem}.md — must start with 'trip-'")
        bare = stem.replace("trip-", "", 1)
        if bare in BUILTIN_COMMANDS:
            failures.append(f"COLLISION: {stem} conflicts with built-in /{bare}")
    if failures:
        print("FAIL: validate_command_names.py")
        for msg in failures:
            print(f"  {msg}")
        sys.exit(1)
    print("PASS: validate_command_names.py — command names valid")


if __name__ == "__main__":
    main()
```

## Task 0.12 — Create scripts/validate_staleness.py (NEW)

### File: scripts/validate_staleness.py

```python
#!/usr/bin/env python3
"""Flag wiki pages with stale last_verified dates.

Thresholds (defaults; override via STALE_DAYS env var):
  - price-related pages (any with cost_level != n-a): 365 days
  - exchange-rate page                              : 30 days
  - other pages                                     : 540 days

The script reports stale pages as warnings, not failures. It exits 0
unless severely stale pages are present (more than 2x the threshold).
"""
import glob
import os
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _yaml_util import parse_frontmatter, is_valid_date, normalize_value

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WIKI_DIR = os.path.join(PROJECT_ROOT, "wiki")
SKIP_FILES = {"index.md", "log.md", "current-status.md"}

DEFAULT_THRESHOLDS = {
    "exchange-rate": 30,
    "price": 365,
    "other": 540,
}


def classify(rel_path, fm):
    """Return the threshold key for a page."""
    base = os.path.splitext(os.path.basename(rel_path))[0]
    if base == "exchange-rate":
        return "exchange-rate"
    cost = normalize_value(fm.get("cost_level", ""))
    if cost and cost not in ("n-a", "unknown"):
        return "price"
    return "other"


def main():
    md_files = glob.glob(os.path.join(WIKI_DIR, "**", "*.md"), recursive=True)
    relevant = [f for f in md_files if os.path.basename(f) not in SKIP_FILES]
    if not relevant:
        print("PASS: validate_staleness.py — no wiki pages yet")
        sys.exit(0)

    today = datetime.now().date()
    warnings = []
    severe = []

    for fp in relevant:
        rel = os.path.relpath(fp, PROJECT_ROOT)
        fm, _ = parse_frontmatter(fp)
        if fm is None:
            continue
        lv = normalize_value(fm.get("last_verified", ""))
        if not lv or lv == "YYYY-MM-DD":
            continue
        if not is_valid_date(lv):
            continue
        try:
            lv_date = datetime.strptime(lv, "%Y-%m-%d").date()
        except ValueError:
            continue
        age = (today - lv_date).days
        key = classify(rel, fm)
        threshold = DEFAULT_THRESHOLDS[key]
        if age > threshold * 2:
            severe.append(f"{rel}: last_verified {lv} ({age} days; threshold {threshold})")
        elif age > threshold:
            warnings.append(f"{rel}: last_verified {lv} ({age} days; threshold {threshold})")

    if warnings:
        print("WARNINGS: validate_staleness.py")
        for w in warnings:
            print(f"  {w}")

    if severe:
        print("FAIL: validate_staleness.py — severely stale pages present")
        for s in severe:
            print(f"  {s}")
        sys.exit(1)

    print(f"PASS: validate_staleness.py — {len(relevant)} pages checked")


if __name__ == "__main__":
    main()
```

## Task 0.13 — Create scripts/run_all_validations.py

### File: scripts/run_all_validations.py

```python
#!/usr/bin/env python3
"""Run all validation scripts and log results to manifests/validation_runs.csv."""
import csv
import os
import subprocess
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
VALIDATION_LOG = os.path.join(PROJECT_ROOT, "manifests", "validation_runs.csv")

SCRIPTS = [
    "validate_structure.py",
    "validate_frontmatter.py",
    "validate_raw_immutability.py",
    "validate_manifests.py",
    "validate_index.py",
    "validate_links.py",
    "validate_source_metadata.py",
    "validate_travel_schema.py",
    "validate_command_names.py",
    "validate_staleness.py",
]


def make_run_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def append_validation_log(group_id, script, result, failures_summary):
    if not os.path.isfile(VALIDATION_LOG):
        return
    row = {
        "run_id": f"{group_id}-{script}",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "script": script,
        "result": result,
        "failures": (failures_summary or "")[:200],
        "notes": f"group={group_id}",
    }
    with open(VALIDATION_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)


def main():
    group_id = make_run_id()
    total = passed = failed = 0
    for script in SCRIPTS:
        script_path = os.path.join(SCRIPTS_DIR, script)
        if not os.path.isfile(script_path):
            print(f"  SKIP (not found): {script}")
            continue
        total += 1
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        if result.returncode == 0:
            passed += 1
            print(f"  PASS : {script}")
            append_validation_log(group_id, script, "PASS", "")
        else:
            failed += 1
            print(f"  FAIL : {script}")
            for line in output.splitlines():
                print(f"         {line}")
            append_validation_log(group_id, script, "FAIL", output[:200])

    print(f"\n{'=' * 50}")
    print(f"  Total: {total}  Passed: {passed}  Failed: {failed}")
    if failed > 0:
        print("RESULT: FAIL — see failures above")
        sys.exit(1)
    print("RESULT: PASS — all validations passed")


if __name__ == "__main__":
    main()
```

## Task 0.14 — Create scripts/trip_ingest.py (state machine)

### File: scripts/trip_ingest.py

```python
#!/usr/bin/env python3
"""Trip ingest state machine.

This script enforces the preview / apply approval gate for source ingestion.
It does NOT perform content extraction — that is Claude's responsibility.
It manages the state transitions, locks, and audit log in ingest_runs.csv.

Usage:
    python3 scripts/trip_ingest.py SOURCE preview
    python3 scripts/trip_ingest.py SOURCE apply
    python3 scripts/trip_ingest.py SOURCE complete [pages_created] [pages_updated] [conflicts]
    python3 scripts/trip_ingest.py SOURCE fail "reason"
    python3 scripts/trip_ingest.py SOURCE status

SOURCE is the relative path to the raw source file, e.g. raw/tokyo-food.md
"""
import csv
import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INGEST_LOG = os.path.join(PROJECT_ROOT, "manifests", "ingest_runs.csv")

FIELDS = [
    "run_id", "date", "source_filename", "mode", "preview_status",
    "pages_created", "pages_updated", "conflicts_found", "result", "notes",
]


def make_run_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def append_record(record):
    with open(INGEST_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({k: record.get(k, "") for k in FIELDS})


def read_latest_for_source(source_filename):
    if not os.path.isfile(INGEST_LOG):
        return None
    rows_for_source = []
    with open(INGEST_LOG, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("source_filename") == source_filename:
                rows_for_source.append(row)
    return rows_for_source[-1] if rows_for_source else None


def cmd_preview(source_filename):
    source_path = os.path.join(PROJECT_ROOT, source_filename)
    if not os.path.isfile(source_path):
        print(f"FAIL: Source file does not exist: {source_filename}")
        return 1
    record = {
        "run_id": make_run_id(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_filename": source_filename,
        "mode": "preview",
        "preview_status": "pending",
        "pages_created": "0",
        "pages_updated": "0",
        "conflicts_found": "0",
        "result": "pending-approval",
        "notes": "Preview opened. Claude must now produce the preview report.",
    }
    append_record(record)
    print(f"PASS: Preview opened for {source_filename}")
    print(f"  run_id: {record['run_id']}")
    return 0


def cmd_apply(source_filename):
    latest = read_latest_for_source(source_filename)
    if latest is None:
        print(f"FAIL: No preview record found for {source_filename}.")
        print("  Run preview first.")
        return 1
    if latest.get("preview_status") != "pending":
        print(f"FAIL: No pending preview for {source_filename}.")
        print(f"  Latest preview_status: {latest.get('preview_status')}")
        print(f"  Latest result        : {latest.get('result')}")
        return 1
    record = {
        "run_id": make_run_id(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_filename": source_filename,
        "mode": "apply",
        "preview_status": "applying",
        "pages_created": "0",
        "pages_updated": "0",
        "conflicts_found": "0",
        "result": "in-progress",
        "notes": "Apply started. Claude performs writes; run complete or fail at end.",
    }
    append_record(record)
    print(f"PASS: Apply opened for {source_filename}")
    print(f"  run_id: {record['run_id']}")
    return 0


def cmd_complete(source_filename, pc=0, pu=0, cf=0):
    record = {
        "run_id": make_run_id(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_filename": source_filename,
        "mode": "apply",
        "preview_status": "applied",
        "pages_created": str(pc),
        "pages_updated": str(pu),
        "conflicts_found": str(cf),
        "result": "completed",
        "notes": "Apply completed successfully.",
    }
    append_record(record)
    print(f"PASS: Ingest completed for {source_filename}")
    return 0


def cmd_fail(source_filename, reason=""):
    record = {
        "run_id": make_run_id(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_filename": source_filename,
        "mode": "apply",
        "preview_status": "failed",
        "pages_created": "0",
        "pages_updated": "0",
        "conflicts_found": "0",
        "result": "failed",
        "notes": reason or "Apply failed mid-write.",
    }
    append_record(record)
    print(f"FAIL: Ingest marked failed for {source_filename}")
    return 1


def cmd_status(source_filename):
    latest = read_latest_for_source(source_filename)
    if latest is None:
        print(f"No records for {source_filename}")
        return 0
    print(f"Latest record for {source_filename}:")
    for k, v in latest.items():
        print(f"  {k}: {v}")
    return 0


def main():
    if len(sys.argv) < 3:
        print("Usage: trip_ingest.py SOURCE {preview|apply|complete|fail|status}")
        return 2
    source = sys.argv[1]
    cmd = sys.argv[2]
    if cmd == "preview":
        return cmd_preview(source)
    if cmd == "apply":
        return cmd_apply(source)
    if cmd == "complete":
        pc = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        pu = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        cf = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        return cmd_complete(source, pc, pu, cf)
    if cmd == "fail":
        reason = sys.argv[3] if len(sys.argv) > 3 else ""
        return cmd_fail(source, reason)
    if cmd == "status":
        return cmd_status(source)
    print(f"Unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
```

### Acceptance Criteria — EPIC 0

```
Command:
  cd /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan
  python3 scripts/run_all_validations.py

Expected at this stage (before any other EPIC has run):
  validate_structure.py        → FAIL (structure not yet built)
  validate_frontmatter.py      → PASS (no pages yet — empty pass)
  validate_raw_immutability.py → FAIL (settings.json absent)
  validate_manifests.py        → FAIL (manifests absent)
  validate_index.py            → FAIL (index.md absent)
  validate_links.py            → PASS (no pages yet — empty pass)
  validate_source_metadata.py  → PASS (no sources yet — empty pass)
  validate_travel_schema.py    → PASS (no pages yet — empty pass)
  validate_command_names.py    → FAIL (commands/ absent)
  validate_staleness.py        → PASS (no pages yet — empty pass)
  RESULT: FAIL  ← correct; the test layer is live and reports missing structure.
```

---

# EPIC 1 — Global LLM Wiki Root Setup

## What & Why

The global root `/home/nekiee/LLL_Wiki/` is the parent workspace for all projects. It holds a global `CLAUDE.md` (shared base rules) and a cross-project index. Project-level `CLAUDE.md` files inherit from and extend the global rules.

## Task 1.1 — Create global directory and files

### Commands

```bash
mkdir -p /home/nekiee/LLL_Wiki
```

### File: /home/nekiee/LLL_Wiki/CLAUDE.md

```markdown
# LLM Wiki — Global Rules

This file defines shared rules for all LLM Wiki projects under this workspace.
Project-level CLAUDE.md files extend these rules. On conflict, the project
file takes precedence.

## Core principle

The LLM Wiki is a persistent, compounding knowledge base maintained by Claude.
Raw sources are immutable. Wiki pages are owned by Claude. The human curates
sources, asks questions, and guides the analysis.

## Universal rules — apply to all projects

- Never modify any file inside a raw/ directory under any project.
- Always update the project's wiki/index.md after writing or changing pages.
- Always append to wiki/log.md after any write operation.
- Always update wiki/current-status.md at session end.
- Page filenames: lowercase, hyphens only, .md extension (e.g. shibuya.md).
- Use [[wikilinks]] for all internal references.
- Every factual claim must cite a source file: (source: raw/filename.md)
- Unsourced claims: mark as (needs verification)
- Conflicting sources: mark as (conflict: raw/a.md vs raw/b.md)
- When uncertain how to categorize something, ask the user before writing.
- Run python3 scripts/run_all_validations.py after any significant change.

## Multi-project workspace

Projects live under /home/nekiee/LLL_Wiki/ProjectXX/ProjectName/
Each project has its own raw/, wiki/, manifests/, .claude/, templates/, scripts/.
Each project is an independent git repository.
Do not cross-reference wiki pages between projects.

## Session start protocol

1. Read the project CLAUDE.md.
2. Read wiki/current-status.md.
3. Read wiki/index.md.
4. Confirm understanding with a one-paragraph project state summary.
```

### File: /home/nekiee/LLL_Wiki/index.md

```markdown
# LLM Wiki — Global Project Index

| Project | Path | Status | Description |
|---------|------|--------|-------------|
| Trip_to_Japan | Project01/Trip_to_Japan | active | Travel guide wiki for Japan trip planning |

---

*Updated manually or by project session summary.*
```

### File: /home/nekiee/LLL_Wiki/log.md

```markdown
# LLM Wiki — Global Log

Append-only record of cross-project events.

## [2026-05-26] init | Global LLM Wiki workspace initialized
```

### Acceptance Criteria

```
ls /home/nekiee/LLL_Wiki/
→ CLAUDE.md  index.md  log.md
```

---

# EPIC 2 — Project Directory Structure

## What & Why

This epic creates the full physical skeleton of the project, including the new `incoming/` staging directory and the relocated `sources/` directory. All required directories and skeleton files are created so that `validate_structure.py` returns PASS immediately afterward.

## Task 2.1 — Create all required directories

### Commands

```bash
PROJECT=/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan

mkdir -p $PROJECT/incoming
mkdir -p $PROJECT/raw/assets
mkdir -p $PROJECT/sources
mkdir -p $PROJECT/wiki/cities
mkdir -p $PROJECT/wiki/districts
mkdir -p $PROJECT/wiki/food
mkdir -p $PROJECT/wiki/restaurants
mkdir -p $PROJECT/wiki/attractions
mkdir -p $PROJECT/wiki/hotels
mkdir -p $PROJECT/wiki/transport
mkdir -p $PROJECT/wiki/budget
mkdir -p $PROJECT/wiki/itineraries
mkdir -p $PROJECT/wiki/day-trips
mkdir -p $PROJECT/wiki/practical
mkdir -p $PROJECT/wiki/decisions
mkdir -p $PROJECT/manifests
mkdir -p $PROJECT/.claude/commands
mkdir -p $PROJECT/templates
# scripts/ already created in EPIC 0
```

## Task 2.2 — Create required skeleton files

### File: wiki/index.md

```markdown
# Trip_to_Japan Wiki — Index

*This file is maintained by Claude. Updated after every ingest or write operation.*

## Cities

## Districts

## Food & Restaurants

## Attractions

## Hotels

## Transport

## Budget

## Itineraries

## Day Trips

## Practical Tips

## Decisions

## Source Summaries
```

### File: wiki/log.md

```markdown
# Trip_to_Japan — Operation Log

Append-only. Format: ## [YYYY-MM-DD] operation | description

## [2026-05-26] init | Project log initialized
```

### File: wiki/current-status.md

```markdown
# Current Session Status

## Last updated
<!-- Claude writes the date here at session end -->

## Project purpose
Japan trip planning wiki. Accumulates knowledge from web articles into
structured, interlinked wiki pages for itinerary, budget, and district planning.

## Source capture status
- Total planned sources: 0
- Total captured sources: 0
- Total ingested sources: 0
- Pending ingest queue: none

## Wiki page count
- Total active pages: 0

## Last ingest run
None yet.

## Last lint run
None yet.

## Last validation run
None yet.

## Open decisions
None yet.

## Next recommended action
Begin EPIC 3 (git init), then EPIC 4 (permissions). Capture sources after EPIC 9.
```

### File: README.md

````markdown
# Travel Guide LLM Wiki — Trip to Japan

A persistent, LLM-maintained knowledge base for Japan trip planning.
Built using the Karpathy LLM Wiki pattern with Claude Code + Obsidian.

## Quick start

1. Open this folder as an Obsidian vault.
2. Launch Claude Code: `cd /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan && claude`
3. Run: `/trip-context`

## Folder layout

| Folder | Purpose |
|--------|---------|
| incoming/ | Capture staging (Web Clipper writes here first) |
| raw/ | Immutable source documents (chmod -R a-w) |
| sources/ | Source registry (writable, human-maintained) |
| wiki/ | LLM-maintained knowledge pages |
| manifests/ | CSV tracking files |
| .claude/ | Claude Code configuration and commands |
| templates/ | Page templates |
| scripts/ | Validation scripts and ingest state machine |

## Dependencies

PyYAML is required by the validation scripts:
```
pip install pyyaml
```

## Validation

```bash
python3 scripts/run_all_validations.py
```

## Git

Each ingest is committed. See git log for full history.
````

### File: CLAUDE.local.md

```markdown
# Local Machine Notes (gitignored)

Add machine-specific notes here.
This file is never committed to git.

## VM-specific notes
- VM display: [add your display method here, e.g. xrdp on port 3389]
- Claude Code launch: cd /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan && claude
- Obsidian vault: open this project root folder in Obsidian
```

### File: .gitignore

```
CLAUDE.local.md
.claude/settings.local.json
__pycache__/
*.pyc
*.pyo
.DS_Store
Thumbs.db
.tmp/
.cache/
*.swp
*~
incoming/
```

Note: `incoming/` is gitignored because it is a staging area for in-progress captures. Once a file is promoted to `raw/`, it enters version control.

### File: manifests/planned_pages.txt

```
# Planned wiki page stems (one per line, lowercase, no extension)
# validate_links.py treats these as valid link targets even before pages exist
# Blank lines and lines starting with # are ignored.

tokyo
shibuya
shinjuku
asakusa
akihabara
harajuku
shimokitazawa
ueno
ginza
roppongi
ikebukuro
yanaka
nakameguro
koenji
transport-overview
budget-overview
exchange-rate
itinerary-draft-v1
```

### File: sources/_source-list.md

(See EPIC 9 for full content. Create as empty placeholder for now to satisfy `validate_structure.py`.)

```markdown
# Trip_to_Japan — Source Registry

This file is populated in EPIC 9.
```

## Task 2.3 — Create manifest CSV files with headers

### File: manifests/raw_sources.csv

```csv
source_id,filename,title,source_url,captured_date,source_type,city,district,topic,status,ingested_date,notes
```

### File: manifests/wiki_pages.csv

```csv
page_id,filename,title,type,city,district,category,status,created,updated,sources,confidence
```

### File: manifests/ingest_runs.csv

```csv
run_id,date,source_filename,mode,preview_status,pages_created,pages_updated,conflicts_found,result,notes
```

### File: manifests/decisions.csv

```csv
decision_id,date,decision_topic,selected_option,rejected_options,reasoning,sources,confidence,status
```

### File: manifests/validation_runs.csv

```csv
run_id,date,script,result,failures,notes
```

### Acceptance Criteria — EPIC 2

```
python3 scripts/validate_structure.py
→ PASS: validate_structure.py — required structure exists

python3 scripts/validate_manifests.py
→ PASS: validate_manifests.py — all manifests valid
```

---

# EPIC 3 — Git Version Control (moved earlier in v2)

## What & Why

Git is initialized immediately after the skeleton exists so that every later phase can be rolled back if a mistake is made. Without this earlier git position, any mishap during the templates or CLAUDE.md authoring phases would require manual filesystem cleanup.

## Task 3.1 — Initialize git repository

### Commands

```bash
cd /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan
git init
git config user.name "LLM Wiki"
git config user.email "wiki@trip-to-japan.local"

git add .gitignore
git commit -m "[init] add .gitignore"

git add .
git commit -m "[init] project skeleton, manifests, scripts (EPIC 0–2)"
```

## Task 3.2 — Verify .gitignore excludes private files and incoming/

```bash
git status
# Confirm none of the following appear as tracked files:
#   CLAUDE.local.md
#   __pycache__/
#   incoming/ (only the directory itself may show as empty; no contents)
```

## Task 3.3 — Define commit convention (enforced in CLAUDE.md)

```
Format: [tag] description

Tags:
  [init]    — initial project setup
  [ingest]  — source ingested (e.g. [ingest] tokyo-food-jw-webmagazine.md)
  [update]  — wiki page updated outside of ingest
  [lint]    — post-lint fixes applied
  [schema]  — CLAUDE.md or template update
  [scripts] — validation script update
  [fix]     — error correction
  [session] — session closeday commit
  [expand]  — new command or feature added
  [promote] — file promoted from incoming/ to raw/

Claude Code always uses this format. Never use "Update files" or similar.
```

## Task 3.4 — Optional remote backup

```bash
# If a remote (private GitHub, Gitea, etc.) is available:
git remote add origin [remote-url]
git push -u origin main
# Document the remote URL in CLAUDE.local.md if configured.
```

### Acceptance Criteria — EPIC 3

```
git log --oneline
→ at least 2 commits:
   [init] project skeleton, manifests, scripts (EPIC 0–2)
   [init] add .gitignore
git status
→ "nothing to commit, working tree clean"
```

---

# EPIC 4 — Permission and Immutability Layer

## What & Why

`raw/` is the source-of-truth layer. It must never be modified by Claude Code during normal operation. Two protection layers are applied: Claude Code deny rules (in `settings.json`) and OS chmod on `raw/` files and directories.

**Important framing change in v2**: the Claude Code deny rules are advisory guardrails — they block tool-level operations matching the configured patterns but cannot block every possible bypass (e.g. Python file writes, shell redirection, `truncate`, `perl -pi`). The actual protection comes from filesystem permissions and git review. The plan does not pretend otherwise.

## Task 4.1 — Create .claude/settings.json with deny rules

### File: .claude/settings.json

```json
{
  "permissions": {
    "deny": [
      "Edit(raw/**)",
      "Write(raw/**)",
      "Edit(/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/raw/**)",
      "Write(/home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/raw/**)",
      "Bash(rm*raw/*)",
      "Bash(mv*raw/*)",
      "Bash(cp*raw/*)",
      "Bash(sed*raw/*)",
      "Bash(truncate*raw/*)",
      "Bash(perl*raw/*)"
    ]
  },
  "env": {},
  "model": "claude-sonnet-4-5",
  "cleanupPeriodDays": 30
}
```

### Notes on deny rule scope (advisory framing)

The deny rules block Claude Code file-tool operations that match the listed patterns. They are **not comprehensive**:

- They do not block Python subprocess writes (`python3 -c 'open("raw/x", "w")...'`).
- They do not block shell redirection (`cat > raw/x`).
- They do not block arbitrary binaries or scripts.

Real protection comes from:

1. **Filesystem permissions** — `chmod -R a-w raw/` removes write bits from files and parent directories.
2. **Git review** — every `[ingest]` commit is auditable. Unexpected raw/ modifications appear in `git diff`.

Use both layers together. Treat the deny rules as visible documentation of intent.

## Task 4.2 — Define OS chmod protocol

### Protocol — when raw/ is empty (initial state)

```bash
# Nothing to lock yet. The directory will be locked when the first
# file is promoted from incoming/ to raw/ (see EPIC 9).
```

### Protocol — after files are promoted to raw/

```bash
# Lock files (no write bits at all):
find /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/raw -type f \
     -exec chmod a-w {} \;

# Lock directories (remove group/other write, keep owner read+execute):
find /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan/raw -type d \
     -exec chmod go-w {} \;
```

### Why directory permissions matter

On POSIX systems, the ability to delete or rename a file depends on the **parent directory's** write permission, not the file's own write bit. A read-only file inside a writable directory can still be unlinked. The chmod protocol above locks both layers.

### Acceptance Criteria

```
python3 scripts/validate_raw_immutability.py
Expected (before any files are in raw/):
  PASS — settings.json deny rules present; raw/ contents empty.

After files are promoted to raw/:
  PASS — all files read-only, parent dirs not group/other writable.
```

---

# EPIC 5 — Wiki Schema: Frontmatter, Templates, Citations

## What & Why

Every wiki page must be machine-readable (for validation scripts and Obsidian Dataview) and human-readable. This epic defines the frontmatter specification, the page body format, citation syntax, and all page templates. The v1 templates contained `n-a` values that the v1 validator rejected; v2 templates remain unchanged in shape, and the validator now accepts `n-a` for the affected fields.

## Task 5.1 — Universal page template

### File: templates/wiki-page-template.md

```markdown
---
title: Page Title
type: city
city: tokyo
district: unknown
category: free-form category tag
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: unknown
status: draft
cost_level: unknown
time_required: unknown
best_for: []
best_season: all
related_pages: []
---

# Page Title

*Japanese: 日本語名 (rōmaji)*

## Summary

One to two sentences describing the page content.

## Key facts

- Fact. (source: raw/filename.md)
- Fact. (source: raw/filename.md)
- Uncertain claim. (needs verification)
- Conflicting data. (conflict: raw/source-a.md vs raw/source-b.md)

## Planning relevance

How this information affects the Japan trip.

## Open questions

- Question or gap requiring more research.

## Related pages

- [[related-page-name]]
```

Field reference (use only these values where indicated):

```
type            : city | district | food | restaurant | attraction | hotel |
                  transport | budget | itinerary | day-trip | practical-tip |
                  seasonal-update | decision | source-summary |
                  seasonal-event | calendar
confidence      : high | medium | low | unknown
status          : draft | active | needs-review | outdated | rejected | superseded
cost_level      : free | low | medium | high | luxury | unknown | n-a
time_required   : short | half-day | full-day | multi-day | unknown | n-a
best_season     : spring | summer | autumn | winter | all | unknown | n-a
                  (multiple values allowed: YAML list or comma-separated)
```

## Task 5.2 — District template

### File: templates/district-page-template.md

```markdown
---
title: District Name
type: district
city: tokyo
district: district-name
category: neighbourhood
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: unknown
status: draft
cost_level: unknown
time_required: unknown
best_for: []
best_season: all
related_pages: []
---

# District Name

*Japanese: 名前 (Rōmaji)*

## Summary

## Character and vibe

## Best for

## Getting there

Nearest station: [[station-name]] (source: raw/filename.md)

## Key attractions

- [[attraction-name]] (source: raw/filename.md)

## Food options

- [[restaurant-name]] (source: raw/filename.md)

## Budget level

## Crowd notes

## Seasonal notes

## Planning relevance

## Open questions

## Related pages
```

## Task 5.3 — Attraction template

### File: templates/attraction-page-template.md

```markdown
---
title: Attraction Name
type: attraction
city: tokyo
district: unknown
category: temple
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: unknown
status: draft
cost_level: unknown
time_required: unknown
best_for: []
best_season: all
location: ""
nearest_station: ""
opening_hours: ""
reservation_required: "unknown"
estimated_cost: ""
estimated_duration: ""
transport_time: ""
weather_sensitivity: unknown
crowd_risk: unknown
best_time_to_visit: ""
related_pages: []
---

# Attraction Name

*Japanese: 名前 (Rōmaji)*

## Summary

## What to expect

## Admission and hours

- Cost: (source: raw/filename.md)
- Hours: (source: raw/filename.md)
- Reservation: (source: raw/filename.md)

## Getting there

## Best time to visit

## Crowd risk

## Tips

## Planning relevance

## Open questions

## Related pages
```

Category values for attractions: `temple | shrine | museum | park | market | viewpoint | entertainment | shopping | other`

## Task 5.4 — Restaurant template

### File: templates/restaurant-page-template.md

```markdown
---
title: Restaurant Name
type: restaurant
city: tokyo
district: unknown
category: ramen
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: unknown
status: draft
cost_level: unknown
time_required: short
best_for: []
best_season: all
location: ""
nearest_station: ""
opening_hours: ""
reservation_required: "unknown"
estimated_cost: ""
estimated_duration: "1h"
transport_time: ""
weather_sensitivity: low
crowd_risk: unknown
best_time_to_visit: ""
related_pages: []
---

# Restaurant Name

*Japanese: 名前 (Rōmaji)*
*Category: (e.g. ramen, sushi)*

## Summary

## Signature dishes

## Cost estimate

Estimated cost per person: ¥XXXX–¥XXXX (source: raw/filename.md)

*Note: Prices in JPY. See [[exchange-rate]] for current rate.*

## Hours and reservation

## Getting there

## Tips and notes

## Planning relevance

## Open questions

## Related pages
```

Category values for restaurants: `ramen | sushi | tempura | yakitori | izakaya | kaiseki | conveyor-sushi | street-food | cafe | other`

## Task 5.5 — Source-note template

### File: templates/source-note-template.md

```markdown
---
title: Source Summary — Source Title
type: source-summary
city: unknown
district: n-a
category: source-summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources:
  - raw/filename.md
source_urls:
  - https://original-url.com
confidence: medium
status: active
cost_level: n-a
time_required: n-a
best_for: []
best_season: all
related_pages: []
---

# Source Summary — Source Title

## Source metadata

- **Filename**: raw/filename.md
- **Original URL**: https://original-url.com
- **Captured**: YYYY-MM-DD
- **Language**: English
- **Source type**: article

## Key facts extracted

- Fact 1.
- Fact 2.

## Pages updated by this source

- [[page-name]] — what was added or changed

## Contradictions found

None.

## Quality assessment

Confidence: medium
Reason: (brief justification)

## Related pages

- [[related-page]]
```

## Task 5.6 — Itinerary template

### File: templates/itinerary-template.md

```markdown
---
title: Itinerary — Name
type: itinerary
city: tokyo
district: n-a
category: itinerary
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: medium
status: draft
cost_level: unknown
time_required: multi-day
best_for: []
best_season: unknown
related_pages: []
---

# Itinerary — Name

## Summary

## Assumptions

- Travel dates: [dates or season]
- Base: [neighbourhood]
- Budget level: [low / medium / high]
- Party: [solo / couple / family]
- Trip length: [N days]
- Currency: Japanese Yen (¥). See [[exchange-rate]] for current rate.

## Day-by-day plan

### Day 1 — Theme

**District**: [[district-name]]
**Morning**: ...
**Afternoon**: ...
**Evening**: ...
**Meals**: [[restaurant-name]], [[restaurant-name]]
**Transport**: [[transport-overview]] — estimated ¥XXX
**Estimated cost**: ¥XXXX
**Confidence**: high

### Day 2 — Theme

...

## Transport notes

## Food plan

## Budget estimate

| Category | Low ¥ | High ¥ | Notes |
|----------|--------|--------|-------|
| Accommodation | | | |
| Food | | | |
| Transport | | | |
| Attractions | | | |
| Shopping | | | |
| Buffer (10%) | | | |
| **Total** | | | |

*Currency: JPY. Exchange rate as of [date]: [rate]. Source: [[exchange-rate]]*

## Risks

- Risk 1. (source: raw/filename.md)

## Alternatives

- Alternative if [[attraction]] is closed or too crowded.

## Open questions

- Question requiring more research.

## Sources

- [[source-summary-name]]
```

The itinerary template does **not** include the decision-quality fields (`location`, `nearest_station`, etc.) because itineraries are multi-day plans, not single locations. The travel-schema validator in v2 does not require those fields on itinerary pages — only the section headers above.

## Task 5.7 — Decision-record template

### File: templates/decision-record-template.md

```markdown
---
title: Decision — Topic
type: decision
city: unknown
district: n-a
category: decision
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: medium
status: draft
cost_level: n-a
time_required: n-a
best_for: []
best_season: all
related_pages: []
---

# Decision — Topic

## Decision

[State the chosen option clearly.]

## Options considered

| Option | Pros | Cons | Confidence |
|--------|------|------|------------|
| Option A | | | |
| Option B | | | |

## Reasoning

Why this option was selected over the alternatives.

## Risks

Known risks with the chosen option.

## Sources

- (source: raw/filename.md)

## Confidence

medium — [reason]

## Review trigger

This decision should be revisited if: [condition].
```

### Acceptance Criteria — EPIC 5

```
ls templates/
→ wiki-page-template.md
→ district-page-template.md
→ attraction-page-template.md
→ restaurant-page-template.md
→ source-note-template.md
→ itinerary-template.md
→ decision-record-template.md
All 7 files present = PASS.
```

---

# EPIC 6 — Travel Ontology and Domain Model

## What & Why

Japan trip planning requires domain-specific understanding. This epic documents the controlled vocabulary (entity types, confidence rules, seasonal model, language/encoding policy, currency policy). The ontology is referenced by templates, validators, and CLAUDE.md. No new files are created in this epic; the ontology is documentation that drives later EPICs.

## Task 6.1 — Entity type controlled vocabulary

```
city             — city-level overview page
district         — neighbourhood or district page
food             — food category or cuisine overview (not a specific restaurant)
restaurant       — specific restaurant or food establishment
attraction       — specific place to visit: temple, shrine, museum, park, market
hotel            — specific accommodation
transport        — transport method, route, pass, or station
budget           — budget overview or cost breakdown page
itinerary        — day-by-day trip plan
day-trip         — day trip destination from Tokyo
practical-tip    — visa, health, safety, currency, SIM, language tips
seasonal-update  — time-sensitive event or seasonal condition
decision         — recorded trip planning decision
source-summary   — summary of a raw source document
seasonal-event   — cherry blossom, festival, Golden Week, etc.
calendar         — monthly overview of what to expect
```

## Task 6.2 — Confidence model

```
high    — Confirmed by an official source (government, establishment website)
          OR confirmed by at least two independent non-affiliated sources.
medium  — Confirmed by one credible non-official source.
low     — Weak, old, or unverified source. Single-source or undated.
unknown — Not enough information to assess. Default for new pages.
```

## Task 6.3 — Seasonal model

```
spring  — March, April, May (cherry blossom peak: late March–early April)
summer  — June, July, August (rainy season June; hot and humid July–August)
autumn  — September, October, November (typhoon risk Sept; foliage Oct–Nov)
winter  — December, January, February (cold, quieter, winter illuminations)
all     — No seasonal restriction
n-a     — Field structurally required but semantically irrelevant
unknown — Seasonal data not yet researched
```

Multiple seasons may be expressed two ways:

```yaml
# YAML list form (preferred):
best_season:
  - spring
  - autumn

# Comma-separated string form (also accepted):
best_season: spring, autumn
```

Critical Japan-specific seasonal flags that must be noted on affected pages:

```
Golden Week     : late April to early May — extremely crowded everywhere
Cherry blossom  : late March to early April — peak tourist season, book early
Obon            : mid-August — domestic travel rush, Shinkansen busy
New Year        : late December to January 3 — many sites closed or very crowded
Rainy season    : June — outdoor attractions affected, plan indoor alternatives
Typhoon season  : September — outdoor day trips may be disrupted
```

## Task 6.4 — Language and encoding policy

```
Filenames       : Romaji, lowercase, hyphens only (e.g. shibuya.md).
                  Never use kanji, hiragana, or katakana in filenames.
Page titles     : English in the H1 heading, Japanese in italic below.
                  Example:
                    # Shibuya
                    *Japanese: 渋谷 (Shibuya)*
Wikilinks       : Always use romaji stems: [[shibuya]], [[senso-ji]], [[ramen]]
Japanese text   : Include in page body where useful (for search and accuracy).
                  Always pair kanji with romaji on first use per page.
File encoding   : UTF-8 for all files. PyYAML reads UTF-8 by default.
Source language : Sources may be English or Japanese. Japanese-language sources
                  are summarized in English in the wiki. Note original
                  language in the source-note frontmatter field 'language'.
```

## Task 6.5 — Currency and budget policy

```
Primary currency  : Japanese Yen (¥, JPY)
                    All prices in wiki pages use ¥ and JPY values.
Exchange rate     : wiki/budget/exchange-rate.md must exist before itinerary
                    generation. It records the reference rate used for planning,
                    its source, and its date. Stale rates (> 30 days) trigger
                    a warning from validate_staleness.py.
Budget note rule  : Any page with cost_level or estimated_cost must add:
                    *Note: Prices in JPY. See [[exchange-rate]] for current rate.*
Price dates       : Record the source date of any price claim. Pages older than
                    365 days (cost-bearing) or 540 days (others) trigger
                    staleness warnings.
Budget categories : flights | accommodation | local-transport | food |
                    paid-attractions | day-trips | shopping | buffer
```

### Acceptance Criteria — EPIC 6

This epic is documentation-driven. Acceptance is verified once EPIC 8 has embedded the ontology in CLAUDE.md and after the first pages exist:

```
python3 scripts/validate_frontmatter.py
→ PASS (or empty-pass if no pages yet)
```

---

# EPIC 7 — Manifest Tracking System

## What & Why

Manifests provide provenance, traceability, and duplicate prevention. CSV headers were created in EPIC 2. This epic defines the data entry protocols and additionally documents the new `planned_pages.txt` parsing rules.

## Task 7.1 — raw_sources.csv update protocol

```
When to update: After each source is captured and after each ingest.

Status lifecycle:
  planned          → URL added to sources/_source-list.md; not yet clipped
  captured         → Markdown file exists in raw/ with valid frontmatter
  ingest-previewed → /trip-ingest preview has been run
  ingested         → /trip-ingest apply has been run successfully
  rejected         → Source deemed irrelevant or low quality; not ingested
  needs-recapture  → Source file is incomplete or corrupt; must be re-clipped

Who updates: Claude updates status during ingest.
             Human updates planned→captured after promoting from incoming/ to raw/.
```

## Task 7.2 — ingest_runs.csv approval lock mechanism

This mechanism enforces the preview→apply approval gate, now backed by `scripts/trip_ingest.py`.

```
Preview mode (trip_ingest.py preview) writes:
  run_id          : auto (YYYYMMDDHHMMSSffffff — microsecond resolution)
  date            : timestamp
  source_filename : the raw source file path (e.g. raw/tokyo-food.md)
  mode            : preview
  preview_status  : pending
  pages_created   : 0 (not yet known)
  pages_updated   : 0 (not yet known)
  conflicts_found : 0 (not yet known)
  result          : pending-approval
  notes           : "Preview opened. Claude must now produce the preview report."

Apply mode (trip_ingest.py apply) checks:
  1. Read the latest ingest_runs.csv entry for this source.
  2. If preview_status is not 'pending', REFUSE apply and exit non-zero.
  3. If preview_status is 'pending', write a new record:
     mode='apply', preview_status='applying', result='in-progress'
  4. Claude performs writes.
  5. On success, Claude calls trip_ingest.py SOURCE complete <counts>:
     preview_status='applied', result='completed'
  6. On failure, Claude calls trip_ingest.py SOURCE fail "reason":
     preview_status='failed', result='failed'

Session interruption recovery:
  If a record has result='in-progress' at session start, /trip-context
  surfaces it as: "WARNING: incomplete ingest detected for [filename]."
  Claude must resolve this before starting new ingests.
```

## Task 7.3 — decisions.csv update protocol

```
When to update: After any /trip-closeday run where a decision was made.
Who updates: Claude writes the row. Human confirms.

Status values:
  draft      → Decision proposed, not yet confirmed
  active     → Decision confirmed and in effect
  superseded → A newer decision replaced this one
  rejected   → Decision was considered but not taken
```

## Task 7.4 — planned_pages.txt parsing rules

```
- One stem per line, lowercase, no .md extension.
- Blank lines are ignored.
- Lines beginning with '#' are ignored as comments.
- Stems may include folder prefix (e.g. 'districts/shibuya').
```

### Acceptance Criteria — EPIC 7

```
python3 scripts/validate_manifests.py
→ PASS: validate_manifests.py — all manifests valid
```

---

# EPIC 8 — CLAUDE.md: Complete Project Control Schema

## What & Why

`CLAUDE.md` is the single most critical file in the system. Claude Code reads it at session start. All operational behavior is defined here. The v2 content includes the updated directory layout (`incoming/`, `sources/`), the new ingest-script integration, the strengthened permission framing, and the `n-a` enum additions.

## Task 8.1 — Write complete project CLAUDE.md

### File: CLAUDE.md

```markdown
# LLM Wiki — Project Control Schema

## Project: Trip_to_Japan

*This file is the authoritative instruction set for Claude Code in this project.
It extends the global CLAUDE.md at /home/nekiee/LLL_Wiki/CLAUDE.md.
On conflict, this file takes precedence.*

---

## Project identity

- **Project name**: Trip_to_Japan
- **Project root**: /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan
- **Purpose**: Japan trip planning. Build a structured, interlinked wiki from
  travel articles, guides, and restaurant reviews. Produce actionable itinerary,
  budget, and district recommendations.
- **Primary city**: Tokyo (expand to Kyoto, Osaka, etc. as sources are added)
- **Executor**: Claude Code (inside Ubuntu 26.04 VM)
- **Human interface**: Obsidian (open project root as vault)
- **Capture tool**: Firefox + Obsidian Web Clipper (saves to incoming/)

---

## Session start protocol

Every session MUST begin with these steps in order:

1. Read this file (CLAUDE.md) fully.
2. Read wiki/current-status.md.
3. Read wiki/index.md.
4. Check manifests/ingest_runs.csv for any result='in-progress' records.
   If found: surface a WARNING and resolve before proceeding.
5. Output a one-paragraph project state summary covering:
   - Source count (planned, captured, ingested, rejected)
   - Wiki page count
   - Last operation date
   - Next recommended action

---

## Directory layout

```text
incoming/     ← Capture staging. Web Clipper writes here. NOT immutable.
raw/          ← IMMUTABLE. Never modify. Contains promoted source captures.
raw/assets/   ← Downloaded images (immutable).
sources/      ← Source registry (writable, human-maintained).
wiki/         ← LLM-maintained knowledge pages.
wiki/index.md ← Read this first when answering questions.
wiki/log.md   ← Append-only operation record.
wiki/current-status.md ← Session continuity file. Update at session end.
manifests/    ← CSV tracking files. Update after every operation.
.claude/      ← Claude Code configuration and commands.
templates/    ← Page templates. Always follow these formats.
scripts/      ← Validation scripts + trip_ingest.py state machine.
```

---

## Core rules (non-negotiable)

1. **Never modify any file in raw/ or raw/assets/.**
   This includes reads that trigger writes (e.g. accidentally overwriting).
   If unsure, ask before touching raw/.

2. **Wiki-first rule.** Always read wiki/index.md and relevant wiki pages
   before reading raw/ sources. Raw sources are for ingestion, not querying.

3. **Index and log must be updated after every write.**
   No wiki page may be created or modified without updating wiki/index.md
   and appending to wiki/log.md.

4. **No write without preview.** Never apply ingest changes without first
   producing a preview and confirming with the user. The preview must list
   proposed new pages, proposed updates, and detected conflicts.

5. **Approval gate via trip_ingest.py.** Before any apply-mode writes:
   - Call: `python3 scripts/trip_ingest.py raw/SOURCE preview`
     This opens a record with preview_status=pending.
   - Produce the preview report for the user.
   - On user APPROVAL, call: `python3 scripts/trip_ingest.py raw/SOURCE apply`
     This refuses unless a pending preview exists. It then opens an
     in-progress record.
   - After writes succeed: `python3 scripts/trip_ingest.py raw/SOURCE complete N M K`
   - On failure: `python3 scripts/trip_ingest.py raw/SOURCE fail "reason"`

6. **Run validations after major changes.**
   After any ingest apply, after any structural changes, run:
   `python3 scripts/run_all_validations.py`

7. **Commit after successful ingest.**
   After validation returns PASS, run:
   `git add -A && git commit -m "[ingest] SOURCE_FILENAME"`

8. **Citation in every factual claim.**
   `(source: raw/filename.md)` — for supported claims
   `(needs verification)` — for unsupported claims
   `(conflict: raw/a.md vs raw/b.md)` — for contradictions

9. **Romaji filenames.** All wiki page filenames use lowercase romaji with
   hyphens. Never use kanji or spaces in filenames.

10. **Templates are mandatory.** When creating any wiki page, start from the
    matching template in templates/. Do not invent new page formats.

11. **n-a is a valid value.** For fields that are structurally required but
    semantically irrelevant on a given page (e.g. cost_level on a decision
    page), use `n-a`. The validator accepts this value.

---

## Ingest workflow (detailed)

### Step 1 — Pre-ingest check

```
a. Confirm source file exists in raw/.
b. Confirm source file has required frontmatter (validate_source_metadata.py).
c. Confirm source file is read-only (chmod check).
d. Check ingest_runs.csv — has this source been ingested before?
   If yes: confirm with user before re-ingesting.
e. Run: python3 scripts/trip_ingest.py raw/FILENAME preview
   This opens a preview record.
```

### Step 2 — Source read and preview (DRY RUN — no writes)

```
a. Read the full source file.
b. Identify: source type, city, district, topic category.
c. Produce a preview report containing:
   - Source classification
   - List of proposed NEW wiki pages (filename, type, summary)
   - List of proposed UPDATED wiki pages (filename, what changes)
   - Possible duplicate pages
   - Detected conflicts with existing wiki content
   - Missing metadata flags
   - Recommended ingest action: PROCEED | PROCEED WITH CAUTION | DO NOT INGEST
d. Present the preview to the user.
e. Wait for explicit 'APPLY' confirmation. Do not proceed without it.
```

### Step 3 — Approved ingest (write operations)

```
1. Run: python3 scripts/trip_ingest.py raw/FILENAME apply
   This refuses if no pending preview exists.
2. Create new source-summary page from templates/source-note-template.md.
3. Create or update entity/concept/district pages.
4. Add or update [[wikilinks]] within affected pages.
5. Update wiki/index.md — add new pages, update one-line descriptions.
6. Append to wiki/log.md:
   ## [YYYY-MM-DD] ingest | raw/filename.md — N pages created, M pages updated
7. Update manifests/raw_sources.csv: ingested_date, status=ingested.
8. Update manifests/wiki_pages.csv: add new rows, update existing rows.
9. Run: python3 scripts/run_all_validations.py
10. If PASS:
    python3 scripts/trip_ingest.py raw/FILENAME complete N M K
    git add -A && git commit -m "[ingest] FILENAME"
11. If FAIL:
    python3 scripts/trip_ingest.py raw/FILENAME fail "reason"
    Stop. Report to user. Do not attempt silent recovery.
12. Update wiki/current-status.md (source counts, page counts).
```

---

## Query workflow (wiki-first)

When the user asks a travel question:

```
1. Read wiki/current-status.md (get project state).
2. Read wiki/index.md (find relevant pages).
3. Read the 2–5 most relevant wiki pages.
4. Synthesize an answer citing wiki pages by [[wikilink]].
5. If the wiki lacks sufficient information, say so explicitly and list
   the specific sources that should be ingested for a better answer.
6. If the answer is valuable as a reusable page, offer to save it.
7. Do NOT read raw/ source files when answering queries unless the wiki
   explicitly lacks relevant content AND the gap has been flagged.
```

---

## Linting rules (/trip-lint)

When linting is requested, check and report:

```
Structural checks (verified by scripts):
  - Missing or invalid frontmatter fields
  - Broken [[wikilinks]] (target page does not exist)
  - Orphan pages (no inbound links from other pages)
  - Duplicate page titles or filenames (stem collisions)
  - Pages missing from wiki/index.md
  - Pages missing from manifests/wiki_pages.csv
  - Sources cited but not present on disk
  - Date fields not in YYYY-MM-DD format

Semantic checks (Claude reasoning required):
  - Factual claims without source citations
  - Claims marked (needs verification) older than 14 days
  - Contradictions between pages
  - Confidence=high claims with only one source
  - Seasonal warnings missing from time-sensitive pages
  - Price data older than 12 months (validate_staleness.py)
  - Pages with status=draft that have enough sources to be finalized

Output format:
  Numbered list. Each item: [severity: HIGH/MEDIUM/LOW] — page — issue — fix.
```

---

## Travel ontology

Allowed type values:
city, district, food, restaurant, attraction, hotel, transport, budget,
itinerary, day-trip, practical-tip, seasonal-update, decision,
source-summary, seasonal-event, calendar

See templates/ for the template matching each type.

---

## Confidence model

```
high    — Official source OR 2+ independent sources agree.
medium  — One credible non-official source.
low     — Weak, old, or single-source-only claim.
unknown — Not yet researched. Default for new pages.
```

Every page's confidence value must be justified in prose or in a comment
on the Summary section. Do not assign 'high' without citing 2+ sources.

---

## Seasonal model

Allowed values: spring | summer | autumn | winter | all | unknown | n-a
Multiple values: YAML list or comma-separated string.

Japan-critical flags (must be noted on affected pages):
- Golden Week (late April–early May)
- Cherry blossom (late March–early April)
- Obon (mid-August)
- New Year (Dec 28–Jan 3)
- Rainy season (June)
- Typhoon season (September)

---

## Language and encoding policy

```
Filenames     : Romaji, lowercase, hyphens (e.g. senso-ji.md)
Page titles   : English H1, Japanese italic below.
Wikilinks     : Romaji stems only: [[senso-ji]], [[shibuya]]
In-body text  : Kanji + romaji on first use per page: 天ぷら (tempura)
Source lang   : Record in source frontmatter 'language' field.
Encoding      : UTF-8 everywhere. PyYAML reads UTF-8 by default.
```

---

## Currency and budget policy

```
Primary currency : JPY (¥)
All prices use ¥ and JPY values.
Exchange rate reference: [[exchange-rate]]
Any price older than 12 months: flagged by validate_staleness.py.
Budget note: Any cost estimate must include:
  *Note: Prices in JPY. See [[exchange-rate]] for current rate.*
```

---

## Permission model (advisory framing)

`.claude/settings.json` deny rules block Claude Code tool-level edits to
raw/. They are advisory: arbitrary scripts, Python writes, or shell
redirection can bypass them. Real protection comes from:

1. Filesystem permissions (chmod -R a-w raw/) — applied after each promote.
2. Git review — every ingest is a commit; unexpected raw/ changes show.

Treat the deny rules as visible documentation of intent.

---

## Command reference

| Command | Purpose |
|---------|---------|
| /trip-context | Load project state. Run at start of every session. |
| /trip-capture-review | Review source capture status. |
| /trip-ingest | Ingest raw source: preview or apply mode (calls trip_ingest.py). |
| /trip-query | Answer a question using wiki-first rule. |
| /trip-challenge | Stress-test a plan or itinerary. |
| /trip-schedule | Generate day-by-day itinerary. |
| /trip-budget | Estimate trip cost from wiki data. |
| /trip-lint | Run wiki health checks. |
| /trip-closeday | End-of-session summary and state save. |

Command files are in .claude/commands/.

---

## Git commit convention

```
[init]    — initial project setup
[ingest]  — source ingested (e.g. [ingest] tokyo-food-jw-webmagazine.md)
[update]  — wiki page updated outside of ingest
[lint]    — post-lint fixes applied
[schema]  — CLAUDE.md or template update
[scripts] — validation script update
[fix]     — error correction
[session] — session closeday commit
[expand]  — new command or feature added
[promote] — file promoted from incoming/ to raw/
```

---

## Session end protocol (/trip-closeday)

Before ending any session, update wiki/current-status.md with:
  - Date of session
  - Sources promoted from incoming/ to raw/ this session
  - Sources ingested this session
  - Pages created and updated this session
  - Decisions made this session
  - Open issues or gaps discovered
  - Next recommended action

Then append a summary line to wiki/log.md.
Then run python3 scripts/run_all_validations.py.
Then git commit if validation passes.
```

### Acceptance Criteria — EPIC 8

```
wc -l CLAUDE.md
→ more than 250 lines (complete v2 content present)

Functional check:
  Start a new Claude Code session.
  Type: "what is this project?"
  Expected: response references the v2 directory layout (incoming/, sources/),
  the trip_ingest.py approval gate, and the advisory permission framing.
```

---

# EPIC 9 — Source Capture Preparation

## What & Why

The base dataset is a list of URLs, not raw files. The ingest pipeline operates on local Markdown files inside `raw/`. The v2 capture workflow uses `incoming/` as a staging area so that `raw/` immutability never needs to be broken. The source registry lives in `sources/_source-list.md` (moved out of `raw/`).

## Task 9.1 — Populate sources/_source-list.md

### File: sources/_source-list.md (full content)

```markdown
# Trip_to_Japan — Source Registry

Status values: planned | captured | ingest-previewed | ingested | rejected | needs-recapture

## Flights

| Status | Filename | Title | URL | Category | Notes |
|--------|----------|-------|-----|----------|-------|
| planned | — | Skysonar flight search | https://skysonar.com | flights | Check for Tokyo routes |

## Hotels

| Status | Filename | Title | URL | Category | Notes |
|--------|----------|-------|-----|----------|-------|
| planned | — | Klook Tokyo hotels | https://www.klook.com/hotels/searchresult/?stype=city&svalue=28 | hotels | Filter by neighbourhood later |

## Food

| Status | Filename | Title | URL | Category | Notes |
|--------|----------|-------|-----|----------|-------|
| planned | tokyo-food-jw-webmagazine.md | What to Eat in Tokyo 2026 | https://jw-webmagazine.com/tips/what-to-eat-in-tokyo/ | food | Main food guide |
| planned | tokyo-restaurants-willflyforfood.md | 25 Restaurants in Tokyo | https://www.willflyforfood.net/tokyo-restaurants/ | food | Restaurant list |

## Things to do — Tokyo general

| Status | Filename | Title | URL | Category | Notes |
|--------|----------|-------|-----|----------|-------|
| planned | tokyo-things-to-do-skysonar.md | Things to do in Tokyo (Skysonar) | https://skysonar.com/en-us/guides/city-guides/things-to-do-in-tokyo | attractions | General overview |
| planned | tokyo-attractions-tripadvisor.md | Tokyo Attractions (TripAdvisor) | https://www.tripadvisor.com/Attractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html | attractions | Top-rated list |
| planned | tokyo-attractions-travelbabbo.md | What to do in Tokyo | https://travelbabbo.com/what-to-do-in-tokyo/ | attractions | Blog guide |
| planned | tokyo-budget-lonelyplanet.md | Tokyo on a Budget | https://www.lonelyplanet.com/articles/tokyo-on-a-budget | budget | Budget planning |
| planned | tokyo-itineraries-trulytokyo.md | Tokyo Itineraries | https://trulytokyo.com/tokyo-itineraries/ | itinerary | Suggested routes |
| planned | tokyo-day-trips-girlwithbigbag.md | Budget Day Trips from Tokyo | https://thegirlwithabigbag.com/budget-day-trips-from-tokyo/ | day-trips | Day trip options |
| planned | tokyo-transport-gotokyo.md | Getting Around Tokyo | https://www.gotokyo.org/en/plan/getting-around/index.html | transport | Official transport guide |
| planned | tokyo-tips-brightnomad.md | Tokyo Travel Tips | https://brightnomad.net/tokyo-travel-tips/ | practical | Practical tips |
| planned | tokyo-updates-2026.md | Tokyo 2026 Updates | https://www.tokyoupdates.metro.tokyo.lg.jp/en/brochure2026/ | seasonal-update | 2026 official updates |

## Neighbourhoods — Tokyo

| Status | Filename | Title | URL | Category | Notes |
|--------|----------|-------|-----|----------|-------|
| planned | tokyo-neighborhoods-trulytokyo.md | Tokyo Districts Guide | https://trulytokyo.com/tokyo-districts/ | district | District overview |
| planned | shibuya-tripadvisor.md | Shibuya Attractions | https://www.tripadvisor.com/Attractions-g1066456-Activities-Shibuya_Tokyo_Tokyo_Prefecture_Kanto.html | district | Shibuya guide |
| planned | shinjuku-globewelltravelled.md | Best Things in Shinjuku | https://aglobewelltravelled.com/2025/06/20/best-things-to-do-in-shinjuku-tokyo/ | district | Shinjuku guide |
| planned | asakusa-gotokyo.md | Asakusa Guide | https://www.gotokyo.org/en/destinations/eastern-tokyo/asakusa/index.html | district | Official Asakusa guide |
| planned | akihabara-tokyocheapo.md | Akihabara Guide | https://tokyocheapo.com/locations/central-tokyo/akihabara-central-tokyo/ | district | Akihabara guide |
| planned | harajuku-neverendingfootsteps.md | Harajuku Guide | https://www.neverendingfootsteps.com/harajuku-tokyo/ | district | Harajuku guide |
| planned | shimokitazawa-tripadvisor.md | Shimokitazawa | https://www.tripadvisor.com/Attraction_Review-g1066455-d1200230-Reviews-Shimokitazawa-Setagaya_Tokyo_Tokyo_Prefecture_Kanto.html | district | Shimokitazawa |

---

*Total planned: 20 | Captured: 0 | Ingested: 0*
*Last updated: 2026-05-26*
```

## Task 9.2 — Web Clipper configuration (writes to incoming/)

### Web Clipper configuration steps (human-performed, one-time)

```
1. Open Firefox inside the VM.
2. Open the Obsidian Web Clipper extension settings.
3. Set target vault: Trip_to_Japan
4. Set target folder: incoming
   (NOTE: incoming/, not raw/. Files are promoted to raw/ after review.)
5. Create a clip template named "LLM Wiki Source" with this content:
---
source_url: {{url}}
captured_date: {{date}}
source_type: article
city: tokyo
district: unknown
topic: unknown
language: english
capture_method: obsidian-web-clipper
status: captured
---
# {{title}}

{{content}}

---
*Clipped from: {{url}}*
*Clipped on: {{date}}*

6. Set this as the default template.
7. Test: clip one URL. Verify the file appears in incoming/ (not raw/).
```

## Task 9.3 — Promotion workflow (incoming/ → raw/)

```
After a batch of clips lands in incoming/:

1. Review each file in incoming/ for completeness.
2. Edit frontmatter: correct 'city', 'district', 'topic', 'source_type'.
3. Confirm filename matches city-topic-source.md pattern.
4. Validate metadata locally:
   python3 scripts/validate_source_metadata.py
   (Run with RAW_DIR temporarily pointed at incoming/, OR copy file
    into raw/ and re-run.)
5. Promote each validated file:
   mv incoming/FILENAME.md raw/FILENAME.md
6. Update sources/_source-list.md: change row status from planned to captured.
7. Update manifests/raw_sources.csv: append a row for each captured source.
8. Re-apply lock to raw/:
   find raw -type f -exec chmod a-w {} \;
   find raw -type d -exec chmod go-w {} \;
9. Commit the promotion:
   git add -A && git commit -m "[promote] N sources from incoming/ to raw/"
10. Run: python3 scripts/run_all_validations.py
```

## Task 9.4 — Source naming validation rules

Source filenames must follow the pattern `city-topic-source.md`:

```
Correct examples:
  tokyo-food-jw-webmagazine.md
  shibuya-tripadvisor.md
  tokyo-transport-gotokyo.md
  tokyo-budget-lonelyplanet.md

Rule: lowercase, hyphens only, no underscores, no spaces, .md extension.
Rule: must start with a city or neighbourhood name.
Rule: no Japanese characters in filename (romaji only).

The validator enforces: ^[a-z0-9]+(-[a-z0-9]+)*\.md$
```

### Acceptance Criteria — EPIC 9

```
After at least one file is promoted to raw/:

python3 scripts/validate_source_metadata.py
→ PASS: N sources valid

python3 scripts/validate_raw_immutability.py
→ PASS: raw/ is protected (files locked, directories locked)

python3 scripts/validate_structure.py
→ PASS (sources/_source-list.md exists)
```

---

# EPIC 10 — Ingest Pipeline

## What & Why

Ingestion transforms captured source files into structured wiki knowledge. The pipeline has two mandatory stages: preview (dry run, no writes) and apply (guarded by `trip_ingest.py` state machine). This prevents accidental page creation, duplicate concepts, and conflicts from entering the wiki unreviewed. Error handling ensures a partial ingest is detectable and recoverable.

The v2 design backs the workflow with a real Python script — `scripts/trip_ingest.py` (defined in EPIC 0) — so the approval gate is enforced by code, not only by markdown instructions.

## Task 10.1 — Ingest preview implementation

When `/trip-ingest SOURCE preview` is invoked, Claude executes:

```
1. python3 scripts/trip_ingest.py raw/SOURCE preview
   → opens a preview record in ingest_runs.csv with preview_status=pending.
2. Read the source file.
3. Produce the preview report (format below).
4. Wait for user 'APPLY' or 'REJECT'.
```

### Preview report format

```markdown
## Ingest Preview: raw/SOURCE

**Source**: raw/SOURCE
**Source type**: [detected type]
**City**: [detected city]
**District**: [detected district or 'various']
**Topic**: [detected topic]

### Proposed new pages

| Filename | Type | Summary |
|----------|------|---------|
| wiki/districts/shibuya.md | district | Overview of Shibuya neighbourhood |
| wiki/food/ramen.md | food | Ramen overview: styles and recommendations |

### Proposed page updates

| Filename | Change |
|----------|--------|
| wiki/index.md | Add 2 new entries |
| wiki/cities/tokyo.md | Add Shibuya reference |

### Duplicate risk

No duplicates detected. | [OR] Possible duplicate: wiki/districts/shibuya.md already exists.

### Conflicts detected

None. | [OR] Conflict: Source claims X. wiki/page.md claims Y.
Action: flag both claims with (conflict: raw/a.md vs raw/b.md)

### Missing source metadata

[field]: [issue] | None detected.

### Recommended action

Ingest: PROCEED | PROCEED WITH CAUTION | DO NOT INGEST

---

*Waiting for approval. Type 'APPLY' to execute or 'REJECT' to cancel.*
```

## Task 10.2 — Ingest apply implementation

When the user types `APPLY` (or `/trip-ingest SOURCE apply`), Claude executes:

```
1. python3 scripts/trip_ingest.py raw/SOURCE apply
   → refuses if no pending preview exists.
   → otherwise opens a record with result=in-progress.
2. Execute the 11-step ingest write sequence from CLAUDE.md.
3. python3 scripts/run_all_validations.py
4. On PASS:
     python3 scripts/trip_ingest.py raw/SOURCE complete N M K
     git add -A && git commit -m "[ingest] SOURCE"
5. On FAIL:
     python3 scripts/trip_ingest.py raw/SOURCE fail "validation failed"
     Stop and report to user.
```

## Task 10.3 — Error recovery protocol

```
Before beginning any write in apply mode:
  trip_ingest.py apply has already recorded result='in-progress'.

If any step fails:
  1. Stop immediately.
  2. Call trip_ingest.py SOURCE fail "reason".
  3. Append to wiki/log.md:
     ## [DATE] ingest-failed | raw/SOURCE — failed at step N: [reason]
  4. Report to user:
     "Ingest failed at step N. Pages partially written: [list].
      Manual review required before next ingest."

Recovery:
  1. Inspect wiki/ for partial pages.
  2. Either complete the partial page or delete it.
  3. Run python3 scripts/run_all_validations.py.
  4. Commit the recovery state: git commit -m "[fix] recover SOURCE ingest"
  5. Re-ingest the source if appropriate.
```

## Task 10.4 — Post-ingest wiki/log.md entry format

```markdown
## [YYYY-MM-DD] ingest | raw/filename.md
- Pages created: N (list each: wiki/type/page.md)
- Pages updated: M (list each: wiki/type/page.md)
- Conflicts flagged: K
- Validation: PASS
- Commit: [git short hash]
```

### Acceptance Criteria — EPIC 10

```
After ingesting the first source:

python3 scripts/run_all_validations.py
→ RESULT: PASS

git log --oneline -3
→ [ingest] SOURCE_FILENAME
```

---

# EPIC 11 — Claude Code Command System

## What & Why

Slash commands provide repeatable, consistent workflows. Each command is a Markdown file in `.claude/commands/`. Claude Code reads the file and follows its instructions when the command is invoked. All command names use the `trip-` prefix to avoid collisions with built-in Claude Code commands.

The v2 commands invoke `scripts/trip_ingest.py` where appropriate, so the workflow has both a markdown contract (the command file) and a code enforcement layer (the script).

## Task 11.1 — /trip-context command

### File: .claude/commands/trip-context.md

```markdown
# /trip-context — Load Project State

## Purpose

Summarize the current project state at the start of a session.
Required entry point for every Claude Code session.

## Procedure

1. Read CLAUDE.md (this project's control schema).
2. Read wiki/current-status.md.
3. Read wiki/index.md.
4. Read manifests/ingest_runs.csv — find any result='in-progress' records.
5. Read manifests/raw_sources.csv — count by status.
6. Read manifests/wiki_pages.csv — count total and by type.

## Output format

```
=== Trip_to_Japan — Project State ===
Date: [today]

SOURCE STATUS
  Planned    : N
  Captured   : N
  Ingested   : N
  Rejected   : N
  Pending    : N (captured but not yet ingested)

WIKI STATUS
  Total pages: N
  By type: city(N) district(N) attraction(N) restaurant(N) ...

LAST OPERATIONS
  Last ingest : [date] — [source filename]
  Last lint   : [date]
  Last commit : [git log --oneline -1]

OPEN ISSUES
  In-progress ingests: [list or 'none']
  Orphan pages: [list or 'run /trip-lint to check']

NEXT RECOMMENDED ACTION
  [Single concrete next step]
```
```

## Task 11.2 — /trip-capture-review command

### File: .claude/commands/trip-capture-review.md

```markdown
# /trip-capture-review — Review Source Capture Status

## Purpose

Bridge between URL planning and ingest. Shows which sources are ready
for ingestion and which still need to be clipped or promoted.

## Procedure

1. Read sources/_source-list.md.
2. List files in incoming/ (pending review).
3. List files in raw/ (excluding assets/).
4. Run python3 scripts/validate_source_metadata.py — show result.
5. Cross-reference raw/ files with raw_sources.csv.

## Output format

```
=== Source Capture Status ===

IN INCOMING (needs review and promotion)
  incoming/FILENAME.md — [title] — [issue, if any]

READY FOR INGEST (in raw/, frontmatter valid, not yet ingested)
  raw/FILENAME.md — [title] — [topic]

NEEDS METADATA FIXES (in raw/ but frontmatter invalid)
  raw/FILENAME.md — [issue]

NOT YET CAPTURED (planned in _source-list.md, no file anywhere)
  [URL] — [title]

ALREADY INGESTED
  raw/FILENAME.md — ingested [date]

CAPTURE SUMMARY
  Total planned: N | In incoming: N | In raw/: N | Ingested: N
```
```

## Task 11.3 — /trip-ingest command

### File: .claude/commands/trip-ingest.md

```markdown
# /trip-ingest — Ingest Raw Source into Wiki

## Usage

/trip-ingest raw/FILENAME.md preview
/trip-ingest raw/FILENAME.md apply

## Preview mode procedure

1. Verify CLAUDE.md ingest rules are loaded.
2. Run: python3 scripts/trip_ingest.py raw/FILENAME.md preview
   → opens a pending record in ingest_runs.csv.
3. If the script reports an error, fix and retry.
4. Read the full source file.
5. Classify: source type, city, district, topic.
6. Identify proposed new pages and updates (do NOT write anything).
7. Detect duplicate risks and conflicts.
8. Output the Ingest Preview report (see CLAUDE.md format).
9. Wait for 'APPLY' or 'REJECT' from the user.

## Apply mode procedure

1. Run: python3 scripts/trip_ingest.py raw/FILENAME.md apply
   → refuses if no pending preview exists.
   → otherwise opens an in-progress record.
2. Execute the 11-step ingest write sequence from CLAUDE.md.
3. Run: python3 scripts/run_all_validations.py
4. On PASS:
   python3 scripts/trip_ingest.py raw/FILENAME.md complete N M K
   git add -A && git commit -m "[ingest] FILENAME.md"
5. On FAIL:
   python3 scripts/trip_ingest.py raw/FILENAME.md fail "reason"
   Stop and report.
6. Update wiki/current-status.md.

## Error handling

If apply fails at any step:
  Call trip_ingest.py fail with a clear reason.
  Do not attempt silent continuation.
  See CLAUDE.md error recovery protocol.
```

## Task 11.4 — /trip-query command

### File: .claude/commands/trip-query.md

```markdown
# /trip-query — Answer a Travel Question Using Wiki-First Rule

## Usage

/trip-query [question]

## Procedure

1. Read wiki/current-status.md.
2. Read wiki/index.md. Identify the 2–5 most relevant pages.
3. Read those pages.
4. Synthesize an answer citing pages by [[wikilink]].
5. If wiki lacks sufficient information:
   State the gap clearly. Name specific sources to ingest for a better answer.
6. If the answer would be valuable as a reusable wiki page, offer to save it.

## Output format

Answer text with [[wikilink]] citations throughout.

End with:
  Confidence: [overall answer confidence]
  Based on: [list of wiki pages consulted]
  Gap: [list any information missing from the wiki]
```

## Task 11.5 — /trip-challenge command

### File: .claude/commands/trip-challenge.md

```markdown
# /trip-challenge — Stress-Test a Plan, Itinerary, or Decision

## Usage

/trip-challenge [topic or page name]

## Procedure

1. Read the target itinerary, decision, or plan page.
2. Read related wiki pages (district, transport, practical tips).
3. Apply stress tests:
   a. Distance and logistics: are planned locations geographically clustered?
   b. Time realism: is the day plan achievable given transport times?
   c. Opening hours: are all attractions open on planned days/times?
   d. Reservation risk: what requires advance booking?
   e. Season risk: does the plan assume good weather in a risky season?
   f. Budget risk: are cost estimates current and realistic?
   g. Crowd risk: are planned times the busiest periods?
   h. Contingency: what if one element fails (closed, full, bad weather)?
   i. Source quality: are key decisions based on low-confidence data?

## Output format

```
=== Challenge Report: [topic] ===

HIGH RISK
  [Issue] — [source] — [suggested fix]

MEDIUM RISK
  [Issue] — [source] — [suggested fix]

LOW RISK / NOTES
  [Issue or observation]

MISSING INFORMATION
  [What needs to be researched before this plan is reliable]

OVERALL ASSESSMENT
  [One paragraph: is this plan ready to execute or not?]
```
```

## Task 11.6 — /trip-schedule command

### File: .claude/commands/trip-schedule.md

```markdown
# /trip-schedule — Generate Day-by-Day Itinerary

## Usage

/trip-schedule [number of days] [optional: focus area or constraint]

## Prerequisites (check before running)

- wiki/cities/tokyo.md exists (or relevant city page)
- At least 3 district pages exist
- At least 3 attraction pages exist
- wiki/transport/transport-overview.md exists
- wiki/budget/budget-overview.md exists
- wiki/budget/exchange-rate.md exists

If any prerequisite is missing: report gaps; do not generate an incomplete itinerary.

## Procedure

1. Read wiki/index.md, wiki/cities/tokyo.md, wiki/current-status.md.
2. Read all district pages. Group attractions and restaurants by district.
3. Build geographic clusters (minimize transit between stops).
4. Apply seasonal rules from CLAUDE.md.
5. Apply crowd and reservation warnings.
6. Draft day-by-day plan using templates/itinerary-template.md.
7. Add transport notes (nearest stations, IC card tips, estimated cost in ¥).
8. Add food plan (breakfast, lunch, dinner options per day).
9. Build budget table (¥ low / ¥ high per category).
10. List risks and alternatives.
11. Offer to save as wiki/itineraries/itinerary-[name].md.

## Output

Follows templates/itinerary-template.md exactly.
Currency: JPY (¥). Include [[exchange-rate]] reference.
Confidence rated per day based on source quality.
```

## Task 11.7 — /trip-budget command

### File: .claude/commands/trip-budget.md

```markdown
# /trip-budget — Estimate Trip Cost from Wiki Data

## Usage

/trip-budget [number of days] [optional: budget level low|medium|high]

## Procedure

1. Read wiki/budget/ pages.
2. Read wiki/budget/exchange-rate.md. If absent or stale (>30 days):
   Stop. Print: "exchange-rate.md missing or stale. Update first."
3. Gather cost data from attraction, restaurant, transport, hotel pages.
4. Build budget table by category.
5. Flag any cost data older than 12 months (check last_verified).
6. Calculate total ¥ range (low / high).
7. Add 10% buffer line.
8. Offer to save as wiki/budget/budget-estimate-[version].md.

## Output format

```
=== Budget Estimate: N-Day Tokyo Trip ===

Exchange rate reference: See [[exchange-rate]] ([date])

| Category | Low ¥ | High ¥ | Per day | Confidence | Notes |
|----------|--------|--------|---------|------------|-------|
| Flights (return) | | | shared | | |
| Accommodation | | | per night | | |
| Local transport | | | per day | | |
| Food | | | per day | | |
| Paid attractions | | | per day | | |
| Day trips | | | per trip | | |
| Shopping buffer | | | total | | |
| Buffer (10%) | | | | | |
| TOTAL | | | | | |

Unknowns: [list items with unknown cost]
Stale data warnings: [items older than 12 months]
```
```

## Task 11.8 — /trip-lint command

### File: .claude/commands/trip-lint.md

```markdown
# /trip-lint — Run Wiki Health Checks

## Usage

/trip-lint

## Procedure

Step 1 — Run script-based structural checks:
  python3 scripts/run_all_validations.py
  Report any failures as HIGH severity.

Step 2 — Run Claude semantic checks:
  a. Read wiki/index.md. Find pages with status=draft older than 7 days.
  b. Scan all wiki pages for claims without (source: ...) citations.
  c. Check for (needs verification) markers older than 14 days.
  d. Find orphan pages: pages not linked from any other page.
  e. Check confidence=high pages — confirm they cite 2+ sources.
  f. Check seasonal warnings on time-sensitive pages.
  g. Check price data last_verified dates (validate_staleness.py covers basics).
  h. Look for concepts mentioned in 3+ pages but lacking their own page.

## Output format

```
=== Wiki Lint Report ===
Date: [date]

SCRIPT RESULTS
  validate_structure.py        : PASS | FAIL
  validate_frontmatter.py      : PASS | FAIL (N issues)
  validate_raw_immutability.py : PASS | FAIL
  validate_manifests.py        : PASS | FAIL
  validate_index.py            : PASS | FAIL
  validate_links.py            : PASS | FAIL
  validate_source_metadata.py  : PASS | FAIL
  validate_travel_schema.py    : PASS | FAIL
  validate_command_names.py    : PASS | FAIL
  validate_staleness.py        : PASS (warnings: N)

SEMANTIC FINDINGS (Claude analysis)
[N]. [HIGH|MEDIUM|LOW] — [page] — [issue] — [suggested fix]

SUGGESTED NEW PAGES
  Concept '[name]' appears in N pages but has no dedicated page.
  Suggested: wiki/[type]/[name].md

SUMMARY
  Issues found: N (HIGH: N  MEDIUM: N  LOW: N)
  Suggested new pages: N
```

After linting: offer to apply fixes one by one, or save the lint report
as wiki/decisions/lint-report-[date].md.
```

## Task 11.9 — /trip-closeday command

### File: .claude/commands/trip-closeday.md

```markdown
# /trip-closeday — End-of-Session Summary and State Save

## Usage

/trip-closeday

## Procedure

1. Summarize work completed this session:
   - Sources promoted from incoming/ to raw/ (if any)
   - Sources ingested (if any)
   - Pages created (list)
   - Pages updated (list)
   - Decisions made (list)
   - Commands used
2. Update wiki/current-status.md with all current counts and next action.
3. Append to wiki/log.md:
   ## [DATE] session-end | summary of session work
4. Run python3 scripts/run_all_validations.py.
5. If PASS:
   git add -A && git commit -m "[session] closeday [date]"
6. Output:
   ```
   === Session closed: [date] ===
   Sources ingested this session: N
   Pages created: N
   Pages updated: N
   Validation: PASS | FAIL
   Git commit: [hash]
   Next action: [recommended next step]
   ```
```

### Acceptance Criteria — EPIC 11

```
python3 scripts/validate_command_names.py
→ PASS: command names valid

ls .claude/commands/
→ trip-context.md  trip-capture-review.md  trip-ingest.md  trip-query.md
  trip-challenge.md  trip-schedule.md  trip-budget.md  trip-lint.md
  trip-closeday.md
```

---

# EPIC 12 — Obsidian Integration

## What & Why

Obsidian is the human-facing interface for the wiki. The project root is opened as the Obsidian vault. This gives visibility into all subdirectories. Graph view shows wiki page connections. Dataview (optional, later) enables filtered tables.

## Task 12.1 — Open project root as Obsidian vault

```
1. Open Obsidian inside the VM.
2. Click "Open folder as vault".
3. Navigate to: /home/nekiee/LLL_Wiki/Project01/Trip_to_Japan
4. Click Open.
5. Verify file tree shows: CLAUDE.md, incoming/, raw/, sources/, wiki/,
   templates/, manifests/, scripts/, .claude/
```

## Task 12.2 — Configure graph view filters

In Obsidian graph view settings, add path-based filters to reduce noise:

```
Exclude:
  path:incoming
  path:raw
  path:sources
  path:manifests
  path:templates
  path:.claude
  path:scripts
  file:index
  file:log
  file:current-status
```

The graph then shows only the knowledge pages in `wiki/`, connected by `[[wikilinks]]`.

## Task 12.3 — Verify wikilinks resolve

```
python3 scripts/validate_links.py
→ PASS: all wiki links resolve
```

Add planned-but-not-yet-built page stems to `manifests/planned_pages.txt` to suppress false-positive broken-link warnings.

## Task 12.4 — Configure Obsidian attachment folder

```
In Obsidian Settings → Files and links:
  Set "Attachment folder path" to: incoming/assets
After promotion to raw/, assets are moved to raw/assets and locked.
```

### Acceptance Criteria — EPIC 12

```
Manual:
  Obsidian opens the vault. ✓
  Graph view shows wiki pages connected. ✓
  Click a [[wikilink]] → navigates correctly. ✓
  python3 scripts/validate_links.py → PASS
```

---

# EPIC 13 — Travel Outputs: Itinerary, Budget, Decisions

## What & Why

The final purpose of the wiki is actionable trip planning. This epic defines how itinerary, budget, and decision pages are created and maintained.

## Task 13.1 — Create wiki/budget/exchange-rate.md (required before /trip-budget)

### File: wiki/budget/exchange-rate.md

```markdown
---
title: Exchange Rate Reference
type: budget
city: unknown
district: n-a
category: exchange-rate
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources: []
source_urls: []
confidence: medium
status: active
cost_level: n-a
time_required: n-a
best_for: []
best_season: all
related_pages:
  - budget-overview
---

# Exchange Rate Reference

*This page must be updated before generating any budget estimate.*

## Reference rate

| Currency pair | Rate | Date | Source |
|--------------|------|------|--------|
| JPY / EUR | [rate] | [date] | [source URL] |
| JPY / USD | [rate] | [date] | [source URL] |
| JPY / GBP | [rate] | [date] | [source URL] |

## Usage note

All wiki budget figures use JPY (¥). When generating a budget estimate,
Claude reads this page to provide a conversion reference.

If `last_verified` is older than 30 days, `validate_staleness.py` will
emit a warning. Update the rate before generating a new budget estimate.

## Related pages

- [[budget-overview]]
```

## Task 13.2 — Itinerary validation rule

When `/trip-schedule` saves an itinerary page, `validate_travel_schema.py` checks for the required section headers. Required sections:

```
## Summary
## Assumptions
## Day-by-day plan
## Transport notes
## Food plan
## Budget estimate
## Risks
## Alternatives
## Open questions
## Sources
```

`itinerary` is no longer in `DECISION_TYPES` (v1 bug fixed in v2), so decision-quality fields are not required on itinerary pages.

## Task 13.3 — Decision-record workflow

```
When a major planning decision is made (e.g., "stay in Shinjuku, not Shibuya"):

1. Claude creates wiki/decisions/[decision-topic].md from decision-record-template.md.
2. Claude appends a row to manifests/decisions.csv.
3. Claude adds the decision page to wiki/index.md under the Decisions section.
4. Claude appends to wiki/log.md:
   ## [DATE] decision | [topic] — [one-line summary]
5. Claude updates wiki/current-status.md → Open decisions section.

Decisions are never deleted. If superseded, set status=superseded and
link to the replacement decision page.
```

### Acceptance Criteria — EPIC 13

```
After creating exchange-rate.md and at least one itinerary:

python3 scripts/validate_travel_schema.py
→ PASS: travel schema valid

python3 scripts/validate_manifests.py
→ PASS: all manifests valid
```

---

# EPIC 14 — Session Management and Context Continuity

## What & Why

Claude Code sessions have context limits. The wiki will grow. Without a defined continuity mechanism, Claude loses state between sessions. `wiki/current-status.md` is the state handoff file. `/trip-context` is the session entry command.

## Task 14.1 — Verify /trip-context session start

```
1. Close the Claude Code session.
2. Open a new Claude Code session in the project root.
3. Run: /trip-context
4. Verify output includes:
   - Correct source counts (matches raw_sources.csv)
   - Correct page counts (matches wiki_pages.csv)
   - Last operation date (matches wiki/log.md)
   - Next recommended action
   - Any in-progress ingest warnings
```

## Task 14.2 — Within-session context management

If a session becomes complex (many files read, many pages created), proactively run `/trip-closeday` before reaching context limits. Do not wait for the user to ask. A clean state save is always preferable to a truncated session.

Recommended limit: ingest no more than 3 sources per session.

### Acceptance Criteria — EPIC 14

```
Manual:
  New session → /trip-context → output matches current project state.
```

---

# EPIC 15 — Iterative Expansion (Deferred)

## What & Why

Advanced features are added only after core workflows pass validation with real data. This epic lists planned expansions without implementing them prematurely.

## Task 15.1 — Advanced commands (add after 10+ sources ingested)

```
/trip-trace    — trace how a concept evolved across ingested sources
/trip-connect  — find unexpected connections between two topics
/trip-ideas    — scan wiki and suggest unexplored angles
/trip-graduate — promote recurring raw mentions to standalone pages
/trip-drift    — find recurring themes without a dedicated page
```

Add these as command files in `.claude/commands/` when ready.

## Task 15.2 — Dataview integration (add after 50+ wiki pages)

```
Prerequisites:
  - Install Obsidian Dataview plugin.
  - Frontmatter is stable and consistent (validate_frontmatter.py passes).

Create wiki/dataview-tables.md with queries such as:
  - All restaurants by district and cost_level
  - All attractions by confidence and best_season
  - All pages with status=needs-review
  - Budget items ordered by estimated_cost
```

## Task 15.3 — Local search tooling (add after 100+ raw sources)

```
Prerequisites:
  - Wiki has 300+ pages OR index.md reading is noticeably slow.

Options:
  1. qmd (hybrid BM25/vector search, CLI + MCP server)
  2. Custom Python BM25 script using rank-bm25 library.

Add as scripts/search.py and document usage in README.md.
Threshold: when current_page_count exceeds 300, /trip-context surfaces:
"Consider adding search tooling."
```

## Task 15.4 — Hardened ingest extractor (after 5+ successful ingests)

`scripts/trip_ingest.py` currently manages state only. A future enhancement could add automated content extraction: identifying probable wiki pages from a source file using heuristics or LLM-as-extractor calls. This is deferred until the workflow proves stable in real use.

---

# FINAL SUCCESS CRITERIA

The system is implementation-complete when ALL of the following pass:

```
DEPENDENCIES
  [ ] python3 -c "import yaml" → succeeds (PyYAML installed)

STRUCTURAL
  [ ] python3 scripts/run_all_validations.py → RESULT: PASS

SOURCE CAPTURE
  [ ] At least 5 sources exist in raw/ with valid frontmatter
  [ ] raw/ files and parent dirs have correct chmod (read-only / no group-write)
  [ ] sources/_source-list.md has correct rows
  [ ] raw_sources.csv has matching rows

WIKI CONTENT
  [ ] wiki/cities/tokyo.md exists
  [ ] At least 3 district pages exist in wiki/districts/
  [ ] At least 2 food pages exist in wiki/food/
  [ ] wiki/transport/transport-overview.md exists
  [ ] wiki/budget/exchange-rate.md exists
  [ ] wiki/budget/budget-overview.md exists
  [ ] All wiki pages have valid frontmatter (PASS)
  [ ] All [[wikilinks]] resolve (PASS)
  [ ] All pages appear in wiki/index.md (PASS)

COMMANDS
  [ ] /trip-context runs and produces correct state summary
  [ ] /trip-ingest preview runs without writing any files
  [ ] /trip-ingest apply creates pages and commits
  [ ] /trip-lint produces a numbered findings report
  [ ] /trip-schedule produces a valid itinerary

GIT
  [ ] git log --oneline shows at least 3 commits
  [ ] git status → clean working tree after each session

TRAVEL OUTPUTS
  [ ] wiki/itineraries/ has at least one complete itinerary
  [ ] Itinerary passes validate_travel_schema.py
  [ ] Budget estimate exists with JPY values and exchange-rate reference
```

---

# EXECUTION ORDER SUMMARY (v2)

```
Phase 0  → EPIC 0   : Initial Validation Layer (PyYAML install + 10 scripts + state machine)
             Verify: run_all_validations.py → expected mix of PASS/FAIL

Phase 1  → EPIC 1   : Global LLM Wiki root files

Phase 2  → EPIC 2   : Project skeleton (incoming/, raw/, sources/, wiki/, manifests/, etc.)
             Verify: validate_structure.py → PASS
             Verify: validate_manifests.py → PASS

Phase 3  → EPIC 3   : Git init + initial commits (MOVED EARLIER in v2)
             Verify: git log --oneline → 2 commits

Phase 4  → EPIC 4   : .claude/settings.json deny rules + chmod protocol
             Verify: validate_raw_immutability.py → PASS

Phase 5  → EPIC 5   : 7 templates in templates/

Phase 6  → EPIC 6   : Ontology documented (no new files)

Phase 7  → EPIC 7   : Manifest protocols (headers already created in EPIC 2)

Phase 8  → EPIC 8   : Complete CLAUDE.md
             Verify: wc -l CLAUDE.md → 250+ lines

Phase 9  → EPIC 9   : Source registry, Web Clipper config, promotion workflow
             Verify: After first promotion, validate_source_metadata.py → PASS
             Verify: validate_raw_immutability.py → PASS

Phase 10 → EPIC 10  : First ingest (preview then apply via trip_ingest.py)
             Verify: run_all_validations.py → PASS
             Verify: git log → [ingest] commit present

Phase 11 → EPIC 11  : 9 command files in .claude/commands/
             Verify: validate_command_names.py → PASS

Phase 12 → EPIC 12  : Obsidian vault opened, graph filters configured
             Verify: validate_links.py → PASS

Phase 13 → EPIC 13  : exchange-rate.md, first itinerary, first decision
             Verify: validate_travel_schema.py → PASS

Phase 14 → EPIC 14  : Session continuity verified via /trip-context

Phase 15 → EPIC 15  : Deferred — implement after core system is working
```

---

# CRITIQUE-TO-FIX TRACEABILITY

Every item in the v1 critique has been addressed. The table below maps critique numbers to v2 changes.

| Critique # | Topic | v2 location |
|------------|-------|-------------|
| HP-1 | Frontmatter parser broken | EPIC 0 Task 0.2 (`_yaml_util.py`); used by Tasks 0.4, 0.9, 0.10 |
| HP-2 | Template values contradict enums | EPIC 5 (templates unchanged); EPIC 0 Task 0.4 (enums now include `n-a`) |
| HP-3 | `itinerary` in DECISION_TYPES | EPIC 0 Task 0.10 (removed from `DECISION_TYPES`) |
| HP-4 | "Stub scripts" mislabeled | TDD PHILOSOPHY section; EPIC 0 renamed "Initial Validation Layer" |
| HP-5 | `_source-list.md` in `raw/` | EPIC 9 (moved to `sources/`); EPIC 2 (new `sources/` directory) |
| MP-6 | Permission rule path format | EPIC 4 Task 4.1 (both relative and absolute patterns) |
| MP-7 | Bash deny rules weak | EPIC 4 Task 4.1 (advisory framing); CLAUDE.md "Permission model" section |
| MP-8 | chmod incomplete | EPIC 4 Task 4.2 (file + directory chmod); EPIC 9 introduces `incoming/` staging |
| MP-9 | Slash commands not enforcement | EPIC 0 Task 0.14 (`trip_ingest.py`); EPIC 11 (commands invoke it) |
| VS-frontmatter | Parser, YAML lists, dates, sources | EPIC 0 Task 0.4 (all addressed via shared parser + new checks) |
| VS-index | Substring search | EPIC 0 Task 0.7 (wikilink/markdown-link regex only) |
| VS-links | planned_pages.txt comments, duplicates | EPIC 0 Task 0.8 (comments skipped, duplicate-stem warnings) |
| VS-raw-immut | Directory bit ignored | EPIC 0 Task 0.5 (directory + file checks) |
| VS-run-all | Timestamp collisions | EPIC 0 Task 0.13 (microsecond IDs + group ID) |
| S-10 | Phase numbering | PHASE EXECUTION ORDER + EXECUTION ORDER SUMMARY reconciled |
| S-11 | Git too late | EPIC 3 (git moved to Phase 3) |
| Add'l VALID_TIME unused | Enum not enforced | EPIC 0 Task 0.4 (now enforced) |
| Add'l planned_pages.txt missing | Not in REQUIRED_FILES | EPIC 0 Task 0.3 (added) |
| Add'l staleness | No enforcement | EPIC 0 Task 0.12 (new `validate_staleness.py`) |
| Add'l multi-value season | Rejected | EPIC 0 Task 0.4 (`normalize_list` + per-element check) |

---

*End of MASTER PLAN v2 — Travel Guide LLM Wiki — Trip_to_Japan*

---

## Assistant

*Progress update*

The master plan will be checked for architecture, phase order, validator logic, command workflows, permissions, Obsidian integration, and internal contradictions. Only readiness status and any material inspection limits will be reported.

---

## Assistant

The complete **Travel Guide LLM Wiki Master Plan v2** has been inspected.

The review covered:

- all 16 phases and EPICs;
- directory structure and global/project governance;
- validation scripts and TDD workflow;
- YAML schema and page templates;
- manifest lifecycles;
- source capture, promotion, and immutability controls;
- ingest preview/apply state machine;
- Claude Code permissions and slash commands;
- Obsidian configuration;
- itinerary, budget, and decision outputs;
- session recovery and continuity;
- acceptance criteria and execution order;
- v1-to-v2 correction traceability.

Several implementation risks and internal consistency points have been retained for later discussion.

**Ready to continue.**

---

## User

Here is master plan of the 2nd wiki project. Inspect it.

"""
<see appended text>

"""

Let me know when you're ready to continue.

### Attached file: `Pasted markdown(21).md`

`C:\Users\user\AppData\Roaming\Claude\local-agent-mode-sessions\4fbed4c3-0d44-4d6a-b5ca-cd139a39f2b4\2c4b7ef8-704b-4a96-97af-2495de1a203c\local_4099c433-2502-4726-9c87-95a01b31b46a\outputs\MASTER_PLAN_v3.md`

-----

# MASTER PLAN v3 — Procedural Knowledge Extraction (PKE) LLM Wiki
## Project02_Internal_procedure — Schema, CLAUDE.md, Skills, and TDD Integration Plan (v3)
*Built on the same design principles as the Travel Guide LLM Wiki. This plan is written to be executed by Claude Code. The status is POC / Beta.*

> v3 is a complete, standalone replacement for v2. It folds in the accepted design corrections (Tier 1 defects and Tier 2 high-value, low-cost additions), records the deferred items (Tier 3) in Part L, and embeds a machine-readable schema and validation specification (Part F). The lean per-procedure philosophy is retained.

---

## Change log (v2 → v3)

| # | Area | v2 state | v3 state | Tier |
|---|------|----------|----------|------|
| 1 | ID policy | Examples only (`F1`, `REQ-3.4c`, `REF-adp`); no rule | A deterministic ID grammar is defined per page type and enforced (Part B.9, Part F `id_patterns.yml`). | 1 |
| 2 | `classification` vocabulary | Listed in vocab, used by no page type (internal contradiction) | Attached to `requirement`, `finding`, `change`, `revision-draft`; `unknown` added and phase-gated (Part B.3, B.4). | 1 |
| 3 | Behavioural validators | Five described at a high level only | Exact required-field tables per type, driven by `required_fields.yml` (Part F); rules on empty strings, placeholders, and dates fixed (Part E). | 1 |
| 4 | Empty-pass behaviour | "Content validators PASS on empty input" (always) | Phase-aware. Empty pass is allowed only in `bootstrap`/`skeleton`; later phases enforce minimum content (Part B.10, Part E.1). | 1 |
| 5 | Repository model | "Each procedure its own repo, shared tracked once" (ambiguous) | A single monorepo for the whole POC; atomic commits across shared and per-procedure files (Part B.1, EPIC 5). | 1 |
| 6 | Citation checking | Body citation syntax defined, never validated | `validate_citations.py` parses and resolves every `(source: …)` and `(basis: …)` (Part E.6). | 1 |
| 7 | Manifest spec | Three CSVs named without headers/rules | Headers, required rows, and sync rules defined; `validate_manifests.py` added (Part E.8, Part F). | 1 |
| 8 | Traceability scope | Invariant began at `finding` | Extended to the extraction side: source→section, section→requirement, decision→finding, form→basis, draft-section→change (Part B.5, Part E.5). | 1 |
| 9 | Reference verification | `cited_revision`, `current_revision`, `validity` only | Adds `reference_role`, `current_revision_source`, `..._verified_by/_on`, `controlled_index_checked`, `issue_blocker` (Part B.3, B.7). | 2 |
| 10 | Raw-source immutability | Read-only bit only | SHA-256 manifest plus `validate_raw_sources.py` (Part B.1, Part E.7). | 2 |
| 11 | Extraction audit | Raw PDF → wiki directly | A read-only-derived `derived/` layer (text, clause map, extraction notes) sits between raw and wiki (Part B.1, EPIC 7b). | 2 |
| 12 | Source vs synthesis | Implicit | `content_origin` field on every page (Part B.3). | 2 |
| 13 | `confidence` | Vocabulary without meaning | A definition rubric is fixed and phase-gated (Part B.11). | 2 |
| 14 | `actor` resolution | Free text role id | Must resolve to a `role` page for `shall`/`should` requirements (Part E.4). | 2 |
| 15 | Requirement granularity | One requirement per page, no split rule | A splitting rule (one atomic obligation per page) and core action fields are defined (Part B.3, Part D.1). | 2 |
| 16 | Golden-example calibration | EPIC 14 (late) | Moved early: the example defines draft-quality rules before Procedure_B runs (Part D.4, EPIC order in Part G). | 2 |
| 17 | Example overfitting | Example = quality bar | Normative qualities separated from example-specific qualities (Part H). | 2 |
| 18 | Scope control | None | `change_type` taxonomy with `requires_human_approval` (Part B.3). | 2 |
| 19 | Human gates | Approval mentioned, not mapped | Explicit gate map and gate `decision` pages (Part I). | 2 |
| 20 | Semantic lint | Vague (EPIC 15) | A defined semantic-lint checklist (Part E.9). | 2 |
| 21 | Risk register | Absent | Added (Part J). | 2 |
| 22 | Deferred items | Scattered | Consolidated Tier 3 list (Part L). | — |

Deferred (Tier 3) corrections are listed in Part L with the reason each waits.

---

## INPUTS AVAILABLE TO THIS PLAN

The plan is grounded in four inputs.

1. **The reference corpus:** ADP-1.1.080 Rev 8, the General Conditions Rev 24, QAP-9.7.002 Rev 1, and the RE25 (Remont 2025) outage manual. The RE25 manual has been read (text version). Chapter 10 defines the entry meeting (§10.1) and the exit meeting (§10.2); Chapter 6 defines the QA/QC role, reporting, and meeting cadence (§6.1–§6.3). No RE25-dependent item remains provisional.
2. **The original procedures:** SKV.QA-002/2012 Rev 0 (entry meetings) and SKV.QA-003/2012 Rev 0 (exit meetings), both supplied and read.
3. **The approved update example:** SKV.QA-003 Rev 1 draft (exit meetings). This sets the minimum quality bar and is the golden fixture for the drafting skill.
4. **The review observations** recorded earlier for SKV.QA-002/2012.

The purpose of the wiki is to turn a thin, dated procedure into structured, fully traceable knowledge, to check it against the current corpus, and to draft a modern revision that matches the approved example.

---

# PART A — DESIGN RATIONALE

The generic scaffold of the Travel Guide wiki is reused without change: immutable raw sources, a model-owned wiki, a control file, citations, confidence, internal links, an append-only log, git versioning, a test-first validation layer, and an approval-gated workflow.

The travel domain layer is discarded and replaced by a procedure-review domain layer. The shift in emphasis is the key design idea.

- The Travel wiki valued **breadth**: many web sources fused into many interlinked pages.
- The PKE wiki values **depth and traceability**: a small fixed corpus, where every requirement is traced to a source clause, every finding is traced to evidence and to an authoritative basis, and every proposed change is traced to a finding and to the reference that mandates it.

This traceability chain is the unique core of the PKE schema. It is what allows a drafted revision to be defended clause by clause.

## A.1 The lean-versus-rigour balance (new in v3)

Two pressures act on this plan. One pressure favours a lean POC. The other pressure favours strict, machine-checked rigour. v3 resolves the two as follows. Corrections that stop a silent failure, or that repair an internal contradiction, or that protect the id-based traceability chain are adopted now, because the cost is low and the risk of skipping them is high. Corrections that mainly add production weight are deferred to Part L. The aim is a focused POC whose guarantees cannot quietly break — not a half-built production system.

---

# PART B — THE PKE WIKI SCHEMA

## B.1 Architecture and directory layout

The machinery (skills, scripts, templates, the reference corpus, and the machine-readable schema) is shared. Per-procedure folders stay lean. A single git repository tracks the whole project, so a commit can change a shared validator and a procedure output atomically.

```
/home/nekiee/LLL_Wiki/Project02_Internal_procedure/
    .git/                          ← ONE repository for the whole POC (v3)
    _shared/
        CLAUDE.md                  ← shared PKE domain rules (inherited by both procedures)
        reference-index.md         ← controlled list of reference docs and revisions
        schema/                    ← machine-readable schema (v3; see Part F)
            page_types.yml
            vocabularies.yml
            required_fields.yml
            id_patterns.yml
            terminology_map.yml
        references/                ← immutable reference PDFs (single copy, read-only)
            adp-1-1-080-rev8.pdf
            splosni-pogoji-rev24.pdf
            qap-9-7-002-rev1.pdf
            re25-prirocnik.pdf
        skills/
            procedure-extraction/SKILL.md
            reference-crosscheck/SKILL.md
            finding-authoring/SKILL.md
            revision-drafting/SKILL.md
            nek-procedure-template/SKILL.md
        scripts/
            _fm_util.py
            _schema_util.py        ← loads _shared/schema/*.yml (v3)
            validate_structure.py
            validate_frontmatter.py
            validate_raw_sources.py    ← v3
            validate_citations.py      ← v3
            validate_references.py
            validate_traceability.py
            validate_findings.py
            validate_manifests.py      ← v3
            validate_draft.py
            run_all_validations.py
        templates/
            procedure-overview.md  section.md  requirement.md  role.md
            definition.md  abbreviation.md  reference.md  form.md
            finding.md  change.md  decision.md  revision-draft.md
    Procedure_A/                   ← SKV.QA-003 (exit meetings) — has an approved example
        raw/                       ← the source procedure PDF (immutable)
        derived/                   ← extraction audit layer (v3; read-only after lock)
            text/                  ← extracted text per source
            page-images/           ← optional page renders
            clause-map.csv         ← source clause -> derived location
            extraction-notes.md    ← unreadable tables/images, confidence notes
        wiki/                      ← extracted, structured pages
            draft/                 ← draft section pages + DRAFT-ASSEMBLED.md (optional split)
        manifests/                 ← pages.csv, findings.csv, runs.csv, raw_sources.csv
        project-state.yml          ← lifecycle phase + gate status (v3)
        CLAUDE.md  index.md  log.md  current-status.md
    Procedure_B/                   ← SKV.QA-002 (entry meetings)
        raw/  derived/  wiki/  manifests/  project-state.yml
        CLAUDE.md  index.md  log.md  current-status.md
```

Rationale for the shared layer: both procedures depend on the same reference corpus, the same review skills, and the same schema. A single shared copy prevents drift. Rationale for the single repository: separate repositories with a "shared layer tracked once" make cross-cutting commits awkward; one repository keeps history atomic for a POC. Separate repositories are deferred (Part L).

Rationale for the `derived/` layer: the sources are PDFs, and the RE25 text was supplied with infographics removed. PDF extraction errors are common. A read-only-after-lock derived layer lets a reviewer tell a source error apart from an extraction error. Wiki pages cite a source clause that must also appear in `clause-map.csv`.

## B.2 Wiki page types

| Type | Purpose |
|------|---------|
| `procedure-overview` | One per procedure. Identity, purpose, scope, status, update decision link. |
| `section` | One per numbered section of the source procedure. Paraphrased content, source clause, links. |
| `requirement` | A single atomic normative requirement extracted from a section (modality, actor, action). |
| `role` | A responsibility holder, with duties and source clauses. |
| `definition` | A defined term. |
| `abbreviation` | An acronym, its expansion, and a current/obsolete flag. |
| `reference` | A referenced external document, with cited and current revision and a validity flag. |
| `form` | An appendix, template, or minute form. |
| `finding` | A gap, obsolescence, or conflict, with severity, evidence, and authoritative basis. |
| `change` | A proposed edit: links a finding to a target section, a basis, and a draft section. |
| `decision` | A recorded review or gate decision (for example, "update required", "findings approved"). |
| `revision-draft` | The assembled drafted revision (the example-equivalent output). |

## B.3 Frontmatter schema

Common fields on every page:

```yaml
id:            # unique page id following the Part B.9 grammar, e.g. SEC-3, REQ-3-04, REF-QAP, F-001, CHG-001
title:
type:          # one of the page types in B.2
procedure_id:  # e.g. SKV.QA-002/2012
content_origin: # extracted | paraphrased | inferred | synthesized | drafted  (v3)
status:        # draft | active | superseded | under-review | obsolete
confidence:    # high | medium | low | unknown   (meaning fixed in B.11)
created:       # YYYY-MM-DD
updated:       # YYYY-MM-DD
last_verified: # YYYY-MM-DD
related_pages: []
```

Source fields are no longer common to every page. They are required only for extraction-origin page types and are replaced by `derived_from` on synthesis pages (v3):

```yaml
# required on: section, requirement, role, definition, abbreviation, reference, form
source:        # raw/<file>.pdf
source_clause: # e.g. 3.4.a

# required on synthesis pages: finding, change, decision, revision-draft
derived_from: []   # ids of the pages this page is built from, e.g. [F-001, CHG-001]
```

Type-specific fields:

```yaml
# reference
cited_revision:            # revision named in the source procedure (or "none")
current_revision:          # current revision from reference-index.md (or "unknown")
validity:                  # valid | superseded | unknown | not-applicable
reference_role:            # normative | informative | template | historical   (v3)
current_revision_source:   # e.g. reference-index.md; supplied-copy; controlled-index  (v3)
current_revision_verified_by:  # name/role or "" until verified  (v3)
current_revision_verified_on:  # YYYY-MM-DD or ""  (v3)
controlled_index_checked:  # true | false   (v3)
issue_blocker:             # true | false  — true until controlled-index confirmation (v3)

# requirement
modality:          # shall | should | may | informative
actor:             # role id; must resolve to a role page for shall/should (v3)
action:            # the obligated action (verb phrase)  (v3)
object:            # what the action acts on  (v3, optional)
condition:         # trigger/precondition or "" (v3, optional)
timing:            # cadence/deadline or "" (v3, optional)
record:            # record generated or "" (v3, optional)
validity:          # valid | drifted | obsolete | unknown
classification:    # SR | AQ | NSR | n-a | unknown   (v3)

# finding
severity:          # high | medium | low
provisional:       # true | false
provisional_reason: # required when provisional is true
evidence_refs: []  # ids of section/requirement pages (>=1)
basis_refs: []     # ids of reference pages (>=1)
change_refs: []    # ids of change pages (>=1 when severity high/medium and not provisional)
classification:    # SR | AQ | NSR | n-a | unknown   (v3)

# change
finding_refs: []   # ids of finding pages (>=1)
target_section:    # id of the section page the change edits
basis_refs: []     # ids of reference pages (>=1)
draft_ref:         # id of a revision-draft or a draft section
change_type:       # compliance_update | terminology_update | clarification |
                   # template_completion | scope_expansion | editorial   (v3)
requires_human_approval: # true | false  — always true for scope_expansion (v3)
classification:    # SR | AQ | NSR | n-a | unknown   (v3)

# decision
decision_status:   # approved | rejected | deferred | update-required | no-update (v3)
decider:           # name/role or "" until decided
decision_date:     # YYYY-MM-DD or ""
affected_pages: [] # ids the decision governs

# abbreviation
expansion:
obsolete:          # true | false
replacement:       # current term if obsolete

# revision-draft
classification:    # SR | AQ | NSR | n-a | unknown   (v3)
```

## B.4 Controlled vocabularies

```
type           : the twelve page types in B.2
status         : draft | active | superseded | under-review | obsolete
confidence     : high | medium | low | unknown        (meaning in B.11)
content_origin : extracted | paraphrased | inferred | synthesized | drafted
severity       : high | medium | low
validity (ref) : valid | superseded | unknown | not-applicable
validity (req) : valid | drifted | obsolete | unknown
modality       : shall | should | may | informative
classification : SR | AQ | NSR | n-a | unknown        (used by requirement, finding, change, revision-draft)
reference_role : normative | informative | template | historical
change_type    : compliance_update | terminology_update | clarification | template_completion | scope_expansion | editorial
decision_status: approved | rejected | deferred | update-required | no-update
phase          : bootstrap | skeleton | extracted | crosschecked | findings_authored | changes_authored | draft_ready
```

The v2 contradiction is resolved: `classification` now has a home (four page types) and an `unknown` placeholder whose use is phase-gated (B.10).

## B.5 The traceability invariant (the unique core)

The schema enforces one chain end to end. v3 extends the chain to the extraction side, so extraction quality is checked, not only the finding-onward half.

```
raw clause ──> section ──> requirement ──┐
                  │                       │
                  └────────────> finding ─┼─> change ──> revision-draft (section)
                                  │       │      │
                  decision ───────┘       │      │
                  basis (reference) ──────┴──────┘
                  form ──> requirement | basis
```

Rules (extraction side, new in v3):
- Every `section` cites at least one raw clause `(source: raw/<file>.pdf#<clause>)`, and that clause appears in `clause-map.csv`.
- Every `requirement` names a `parent_section` that resolves to a `section`.
- Every `decision` links to at least one `finding` (via `derived_from` or `affected_pages`).
- Every `form` maps to at least one `requirement` or one `reference` basis.

Rules (finding-onward, from v2, retained):
- Every `finding` cites at least one evidence page (`section` or `requirement`) and at least one basis page (`reference`).
- Every `finding` of severity `high` or `medium` that is not provisional cites at least one `change`.
- Every provisional `finding` carries a `provisional_reason` and is excluded from the change-required gate until resolved.
- Every `change` cites at least one `finding`, names an existing `target_section`, cites at least one `reference` as basis, and names an existing draft target.
- No `change` is an orphan (a change with no finding).

The validator in Part E enforces this chain by id. This invariant is what lets every word of the drafted revision be defended against an authoritative source.

## B.6 Citation and linking syntax

- Source citation in body text: `(source: raw/<file>.pdf#<clause>)`.
- Authoritative basis citation: `(basis: REF-<id> §<clause>)`.
- Internal links by id: `[[REQ-3-04c]]`, `[[F-002]]`, `[[CHG-001]]`.
- Unsupported statement: `(not stated)` — never fabricated.
- Conflict: `(conflict: REF-a §x vs REF-b §y)`.

These are now machine-checked by `validate_citations.py` (Part E.6): every `source:` must resolve to a file in `raw/`; every `basis: REF-x` must resolve to a `reference` page; every clause part must be non-empty.

## B.7 Reference-validity and terminology-mapping model

Reference validity is the PKE form of "staleness". Each `reference` page records the revision cited by the old procedure and the current revision from `reference-index.md`. A mismatch is flagged. v3 adds verification provenance, so the Part H admission ("revisions must be confirmed against the controlled index before issuance") is encoded in the schema, not left in prose. A reference stays `issue_blocker: true` until `controlled_index_checked: true`. A reference may still be used for POC drafting while blocked, but the draft cannot pass the issuance gate (Part I) with any blocker open.

Terminology mapping becomes a first-class controlled object, `_shared/schema/terminology_map.yml` (Part F), instead of a prose table. This lets cross-check be validated: every obsolete term found in a section must produce a `finding`, a justified no-change `decision`, or a documented exception.

## B.8 RE25 evidence and its effect on the findings

The RE25 manual is the strongest authoritative basis for both procedures. Three clauses are directly on point.

- **RE25 §10.1 (entry meeting).** Procurement convenes the entry meeting. The attendee list includes an SKV representative. The agenda covers pre-outage activities, the schedule, SKV requirements, commercial requirements, access, internal rules, and NEK expectations. The minutes go to a defined distribution list, including SKV.
- **RE25 §10.2 (exit meeting).** Procurement convenes the exit meeting with the same attendees. The agenda covers the preliminary report, scope/schedule/quality check, deviations, equipment removal, and lessons learned, which must be recorded. The clause ties the exit meeting to QAP-9.7.002: a written supplier evaluation is performed where needed, and a corrective-program request (ZKP) may be raised.
- **RE25 §6.3 (QA/QC role).** External QA/QC staff report to SKV; deviation reports (NCR) are copied to SKV.QC; a weekly Monday 12:00 SKV meeting is held in the TO meeting room (§6.3.b and §12.5).

Effect on the earlier findings for the entry procedure (SKV.QA-002/2012):
- **F3 (obsolete archival path):** strengthened. RE25 confirms routing of minutes through procurement to a defined list, making the 2012 "SKV Filer 2" path obsolete. The replacement is anchored to RE25 §10.1.
- **F6 (hard-coded meeting logistics):** refined. RE25 §6.3.b and §12.5 confirm a weekly Monday 12:00 SKV meeting, so the cadence can be kept while the wording references the current outage manual rather than freezing detail.
- **F9 (generic outage-manual reference):** closed. The reference resolves to the RE25 / Remont 2025 manual (§10.1, §10.2, §6.3). The provisional flag is removed.
- **QAP-9.7.002 linkage (F2):** strengthened. RE25 §10.2 itself ties the exit meeting to QAP-9.7.002.

The `provisional` mechanism stays in the schema. It is no longer needed for RE25 but remains useful for any future source that cannot be read at review time.

## B.9 ID grammar (new in v3)

IDs are central to every validator, so a deterministic grammar is fixed. The grammar lives in `_shared/schema/id_patterns.yml` (Part F) and is enforced by `validate_frontmatter.py`.

| Type | Pattern | Example |
|------|---------|---------|
| procedure-overview | `OVR-<proc-shortcode>` | `OVR-QA002` |
| section | `SEC-<source-section>` | `SEC-6`, `SEC-6-3` |
| requirement | `REQ-<section>-<seq>` (seq two digits) | `REQ-6-03` |
| role | `ROLE-<shortname>` (UPPER) | `ROLE-SKVQC` |
| definition | `DEF-<shortname>` (UPPER) | `DEF-NCR` |
| abbreviation | `ABBR-<token>` (UPPER) | `ABBR-NAB` |
| reference | `REF-<shortcode>` (UPPER) | `REF-QAP`, `REF-RE25` |
| form | `FORM-<shortname>` | `FORM-ENTRY-MIN` |
| finding | `F-<NNN>` (three digits) | `F-001` |
| change | `CHG-<NNN>` | `CHG-001` |
| decision | `DEC-<NNN>` | `DEC-001` |
| revision-draft | `DRAFT-<proc-shortcode>-<rev>` | `DRAFT-QA002-R1` |
| draft section | `DSEC-<proc-shortcode>-<NN>` | `DSEC-QA002-03` |

Rule: an id must match exactly one pattern, must be unique across the procedure wiki, and every internal link `[[id]]` must resolve.

## B.10 Project lifecycle phases (new in v3)

Each procedure carries a `project-state.yml` whose `phase` controls validator strictness. The empty-pass behaviour from v2 is kept only for the first two phases.

```yaml
# Procedure_X/project-state.yml
procedure_id: SKV.QA-002/2012
phase: skeleton            # one value from the phase vocabulary (B.4)
raw_sources_locked: false
reference_registry_verified: false
golden_example_calibrated: false
last_validation_run: ""
overall_status: under-review
gates:
  reference_registry: pending   # pending | approved | rejected | deferred
  extraction: pending
  findings: pending
  change_set: pending
  draft_ready: pending
  issuance: pending
```

Phase gates (what content may be empty):

| Phase | Empty requirements? | Empty findings? | Empty draft? | Placeholders/`unknown` allowed? |
|-------|:---:|:---:|:---:|:---:|
| `bootstrap` | yes | yes | yes | yes |
| `skeleton` | yes | yes | yes | yes |
| `extracted` | no | yes | yes | yes |
| `crosschecked` | no | yes | yes | limited (references resolved) |
| `findings_authored` | no | no, unless a `no-update` decision says so | yes | no for findings |
| `changes_authored` | no | no | yes | no for changes |
| `draft_ready` | no | no (no open high/medium non-provisional) | no | none |

## B.11 Confidence rubric (new in v3)

The `confidence` value now has a fixed meaning. `unknown` is a placeholder only and is rejected from the `extracted` phase onward.

| Confidence | Meaning |
|------------|---------|
| high | Source clause and basis clause are both readable and directly applicable. |
| medium | Source is readable, but the basis needs interpretation or cross-document mapping. |
| low | Source or basis is incomplete, ambiguous, or only indirectly applicable. |
| unknown | Initial placeholder only; not allowed after the `extracted` phase. |

---

# PART C — CLAUDE.md CONTENT

## C.1 Shared control file — `_shared/CLAUDE.md`

```markdown
# LLM Wiki — PKE Domain Control Schema (Shared)

## Scope
Shared rules for all procedure-review projects under Project02_Internal_procedure.
Each procedure project extends this file. On conflict, the procedure file wins.

## Mission
Extract procedural knowledge from a controlled source procedure into structured,
fully traceable wiki pages. Cross-check the procedure against the current
reference corpus. Record findings. Draft a modern revision that meets the NEK
procedure template and the approved quality bar (the SKV.QA-003 Rev 1 example).

## Roles
- Raw sources are immutable. The source procedure and the reference corpus are never edited.
- The derived/ layer is written once at extraction, then locked read-only.
- The wiki is written and owned by the model.
- The human curates inputs, confirms revisions and storage locations, approves
  each gate (Part I of the master plan), and approves the draft.

## Session start protocol
1. Read this shared file, then the procedure CLAUDE.md.
2. Read the procedure project-state.yml (phase + gate status).
3. Read the procedure current-status.md and index.md.
4. Read _shared/reference-index.md and _shared/schema/*.yml.
5. Output a short state summary: phase, pages by type, open findings, open gates,
   draft status, next action.

## Directory layout
- _shared/: references, reference-index.md, schema/, skills, scripts, templates, this file.
- Per procedure: raw/, derived/, wiki/, manifests/, project-state.yml, CLAUDE.md,
  index.md, log.md, current-status.md.
- One git repository for the whole project. Commits may span shared and per-procedure files.

## Core rules (non-negotiable)
1. Never edit raw/ or _shared/references/. Never edit derived/ after it is locked.
2. Wiki-first: read the wiki, schema, and reference-index before reading raw PDFs.
3. Citation: every extracted claim cites its source clause: (source: raw/<file>.pdf#<clause>).
   Every cited clause must also appear in derived/clause-map.csv.
4. Traceability invariant (master plan Part B.5), extraction side included: every section
   cites a raw clause; every requirement names a parent section; every finding links to
   evidence and to an authoritative basis; every high/medium non-provisional finding links
   to a change; every change links to a finding, a target section, a basis, and a draft
   target; every decision links to a finding; every form maps to a requirement or basis.
   No orphan changes.
5. No invented content. If the source is silent, mark (not stated) — never fabricate.
   content_origin must label every page as extracted, paraphrased, inferred, synthesized,
   or drafted.
6. Reference validity: every reference page records cited_revision, current_revision,
   validity, reference_role, and verification provenance. A mismatch is flagged. A reference
   stays issue_blocker: true until controlled_index_checked: true.
7. Provisional findings: any finding that depends on a not-yet-readable source is marked
   provisional with a reason, and is excluded from the change-required gate until resolved.
8. ID grammar (master plan Part B.9) is mandatory; every internal link must resolve.
9. Phase discipline (master plan Part B.10): the phase in project-state.yml controls
   validator strictness. Do not advance the phase until that phase's gate is approved.
10. Skills are mandatory reading. Before extraction, cross-check, finding authoring, or
    drafting, the matching SKILL.md is read first.
11. Run validations after any significant write.
12. No claim about live plant systems (storage paths, current revision numbers) is asserted
    as fact. Such items are marked for human verification and keep issue_blocker: true.

## PKE workflow
ingest -> derive(extract text) -> extract(pages) -> cross-check -> findings ->
decision -> change-set -> draft -> validate -> record. Human gates sit between
phases (master plan Part I).

## Schema
Page types, frontmatter, controlled vocabularies, ID grammar, and lifecycle phases are
defined in the master plan, Part B, and in machine-readable form in _shared/schema/*.yml.
Templates for every page type live in _shared/templates/.

## Terminology mapping
The controlled map is _shared/schema/terminology_map.yml. Cross-check applies it to every
section and records each application as a finding, a justified no-change decision, or a
documented exception.

## Drafting rules
- Read revision-drafting and nek-procedure-template SKILL.md first.
- The draft must contain, in order: cover (with "Nadomesca"), Namen, Obseg,
  Reference (versioned), Definicije in okrajsave, Odgovornosti, the work sections,
  a link to QAP-9.7.002, Zapisi in arhiviranje (with the transitional-location pattern),
  the Dodatek checklist, and a change log ("Spremembe v postopku").
- Every change page must appear in the draft.
- A scope_expansion change is included only after explicit human approval.

## Commands
/pke-context  /pke-ingest  /pke-derive  /pke-extract  /pke-crosscheck  /pke-findings
/pke-decide   /pke-draft   /pke-lint    /pke-gate     /pke-closeday

## Git commit convention
[init] [ingest] [derive] [extract] [crosscheck] [finding] [decision] [change]
[draft] [lint] [gate] [fix] [session]

## Session end protocol
Update project-state.yml and current-status.md, append log.md, run all validations,
commit on PASS.
```

## C.2 Per-procedure control file — `Procedure_X/CLAUDE.md`

The per-procedure file is short. It extends the shared file and pins specifics.

```markdown
# PKE Project — Procedure_B (SKV.QA-002/2012)
This file extends _shared/CLAUDE.md. On conflict, this file wins.

## Procedure identity
- id: SKV.QA-002/2012
- shortcode: QA002
- title: QA Highlights at Entry Outage Meetings
- source: raw/skv-qa-002-2012.pdf
- pair: SKV.QA-003 (exit meetings) — keep consistent
- target template: nek-procedure-template (modern NEK shape)

## Applicable references
- REF-ADP (ADP-1.1.080 Rev 8), REF-SP (General Conditions Rev 24),
  REF-QAP (QAP-9.7.002 Rev 1),
  REF-RE25 (RE25 / Remont 2025 manual — read; entry §10.1, exit §10.2, QA/QC §6.3).

## Procedure-specific notes
- This is the ENTRY procedure. Its package checklist must align with
  ADP-1.1.080 Appendix 6.4 and with the General Conditions entry-meeting minute template.
- Open deviations must be closed before the EXIT meeting (link to SKV.QA-003).
- This procedure is an entry procedure; example-specific exit clauses from the
  golden fixture are NOT forced in (master plan Part H, normative vs example-specific).
```

---

# PART D — SKILLS REQUIRED

Five skills are required to reach the approved example's quality. Each is a folder with a `SKILL.md` of best practices. A sixth skill is deferred.

## D.1 `procedure-extraction`
- **When to use:** any time a source procedure must be turned into structured wiki pages.
- **What it encodes:** how to segment a procedure into sections; how to detect normative requirements and their modality (shall/should/may); the **requirement-splitting rule** (one page per atomic obligation — a clause such as "Procurement shall convene the meeting, record minutes, and distribute them" becomes three requirements); how to fill the requirement action fields (actor, action, object, condition, timing, record); how to lift roles, definitions, abbreviations, references, and forms; how to write one page per element with frontmatter, a valid id (Part B.9), a `content_origin` label, and a source-clause citation; the rule never to invent content.
- **Why needed:** the example separates content into clean sections, definitions, abbreviations, and roles. Extraction produces the building blocks that later assemble into that shape, and the splitting rule keeps requirement pages stable.

## D.2 `reference-crosscheck`
- **When to use:** after extraction, to test the procedure against the current corpus.
- **What it encodes:** how to compare each cited revision to the current revision in `reference-index.md`; how to fill the verification-provenance fields and set `issue_blocker`; how to apply `terminology_map.yml` to every section; how to detect process drift, such as a missing link to QAP-9.7.002; how to record each gap as an evidence-and-basis pair.
- **Why needed:** the example versions every reference, adds QAP-9.7.002, and modernises terms. Cross-check is what surfaces those needs with an authoritative basis.

## D.3 `finding-authoring`
- **When to use:** to write findings from cross-check output.
- **What it encodes:** the finding shape (statement, source clause, severity, evidence, basis, recommendation, classification); a severity rubric (High = must fix; Medium = should fix; Low = improvement); the provisional rule.
- **Why needed:** findings are the justified bridge between the old text and the proposed edits. They make the draft defensible.

## D.4 `revision-drafting`
- **When to use:** to assemble the drafted revision from changes.
- **What it encodes:** how to map findings and changes into the modern section structure; how to write the change log; how to produce the checklist appendix; the quality bar set by the approved SKV.QA-003 Rev 1 example, which is named as the calibration fixture. **Calibration is performed early** (see Part G order): the example is read and its normative qualities (Part H) are turned into draft-quality rules before Procedure_B is drafted, so the skill is tuned before errors can propagate.
- **Why needed:** this skill produces the actual deliverable and must reach the example's depth without copying its exit-specific wording into an entry procedure.

## D.5 `nek-procedure-template`
- **When to use:** whenever a draft revision is written.
- **What it encodes:** the canonical NEK procedure structure (cover with "Nadomesca"; Namen; Obseg; Reference; Definicije in okrajsave; Odgovornosti; work sections; Dodatki; "Spremembe v postopku"; periodic-review block); classification (SR/AQ/NSR); citation style; the transitional-location pattern for obsolete paths.
- **Why needed:** the example follows exactly this shape. The template guarantees the draft is structurally complete.

## D.6 `docx-export` (deferred)
- **When to use:** later, if the final deliverable must be a controlled Word document.
- **Why deferred:** the POC deliverable is markdown, matching the example. The built-in docx skill can be added when a Word output is required.

---

# PART E — TDD VALIDATION LAYER

## E.1 Philosophy (phase-aware in v3)

The validators are written first, in EPIC 0. They contain real logic from the start. The v2 rule "content validators PASS on empty input" is kept only for the `bootstrap` and `skeleton` phases. From the `extracted` phase onward, each validator reads `project-state.yml` and enforces the minimum content for that phase (Part B.10). Structural validators FAIL until the structure exists. No later epic begins until a baseline run produces the expected PASS/FAIL mix.

The schema is data, not code. The behavioural validators load `_shared/schema/*.yml` (Part F) through `_schema_util.py`, so the required-field tables, vocabularies, and id patterns live in one place and cannot drift between scripts.

## E.2 Validators and behaviour

| Validator | Behaviour |
|-----------|-----------|
| `validate_structure.py` | Required project dirs and files exist for the current phase. |
| `validate_frontmatter.py` | Every page has valid frontmatter; id matches its pattern; controlled vocab respected; required fields per type present (driven by `required_fields.yml`); placeholders/`unknown` rejected by phase; `actor` resolves to a `role` for shall/should. |
| `validate_raw_sources.py` | Every `raw/` file is listed in `raw_sources.csv`; checksums match; files are read-only; sources named in frontmatter exist. |
| `validate_citations.py` | Every `(source: …)` resolves to a `raw/` file and a `clause-map.csv` row; every `(basis: REF-x …)` resolves to a `reference` page; clause parts are non-empty; each `section` has ≥1 source citation; each `finding` has ≥1 evidence and ≥1 basis citation. |
| `validate_references.py` | Every reference page records cited/current revision, validity, role, and verification fields; mismatches flagged; any reference cited in a section has a reference page; `issue_blocker` true until controlled-index check. |
| `validate_traceability.py` | Enforces the full Part B.5 invariant, extraction side included (code below). |
| `validate_findings.py` | Severity in vocab; each high/medium finding has a change unless provisional; provisional findings carry a reason; terminology hits resolved to finding/decision/exception. |
| `validate_manifests.py` | `pages.csv`, `findings.csv`, `runs.csv`, `raw_sources.csv` have correct headers; every wiki page appears in `pages.csv`; every finding appears in `findings.csv`. |
| `validate_draft.py` | The revision-draft contains all required NEK sections in order; every change appears; change log and checklist present; archival uses the transitional pattern; plus the semantic-lint checklist (E.9). |
| `run_all_validations.py` | Runs all validators for a project, logs to `manifests/runs.csv`, returns aggregate PASS/FAIL, honours phase. |

## E.3 Code anchor 1 — `_shared/scripts/_fm_util.py` (complete)

```python
#!/usr/bin/env python3
"""Shared frontmatter parser and helpers for the PKE validation layer.
PyYAML is required: pip install pyyaml
All validators import from this module so a fix here propagates everywhere.
"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(filepath):
    """Parse YAML frontmatter. Returns (fields_dict_or_None, body_str)."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    content = content.replace("\r\n", "\n")
    if not content.startswith("---\n"):
        return None, content
    rest = content[4:]
    end_idx = rest.find("\n---\n")
    if end_idx == -1:
        if rest.endswith("\n---"):
            fm_text = rest[: len(rest) - 4]
            body = ""
        else:
            return None, content
    else:
        fm_text = rest[:end_idx]
        body = rest[end_idx + 5:]
    try:
        fields = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        print(f"YAML parse error in {filepath}: {exc}", file=sys.stderr)
        return None, body
    if fields is None:
        fields = {}
    if not isinstance(fields, dict):
        return None, body
    return fields, body


def is_valid_date(value):
    """Return True for YYYY-MM-DD or the literal placeholder."""
    if value is None:
        return False
    s = str(value).strip()
    if s == "YYYY-MM-DD":
        return True
    return bool(DATE_RE.match(s))


def is_placeholder_date(value):
    """Return True only for the literal placeholder YYYY-MM-DD."""
    return value is not None and str(value).strip() == "YYYY-MM-DD"


def normalize_value(value):
    """Convert a scalar to a clean comparable string."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def normalize_list(value):
    """Return a list view of a value. Scalars become single-element lists."""
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v is not None]
    if isinstance(value, str):
        if "," in value:
            return [v.strip() for v in value.split(",") if v.strip()]
        if value.strip() == "":
            return []
        return [value.strip()]
    return [value]


if __name__ == "__main__":
    print("PASS: _fm_util.py loaded; PyYAML available.")
```

## E.4 Code anchor 2 — `_shared/scripts/_schema_util.py` (complete)

This loader makes the schema data-driven. Every behavioural validator imports it, so the field tables, vocabularies, id patterns, and phase order are defined once in `_shared/schema/` (Part F).

```python
#!/usr/bin/env python3
"""Load the machine-readable PKE schema from _shared/schema/*.yml.

Resolution order for the schema directory:
  1) PKE_SCHEMA_DIR environment variable, if set;
  2) ../schema relative to this script (the standard _shared/schema layout).

All behavioural validators call get_schema() so the rules live in one place.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _fm_util import yaml  # reuse the same PyYAML import

PHASE_ORDER = [
    "bootstrap", "skeleton", "extracted", "crosschecked",
    "findings_authored", "changes_authored", "draft_ready",
]


def schema_dir():
    env = os.environ.get("PKE_SCHEMA_DIR")
    if env:
        return os.path.abspath(env)
    return os.path.abspath(os.path.join(SCRIPT_DIR, "..", "schema"))


def _load_yaml(name):
    path = os.path.join(schema_dir(), name)
    if not os.path.isfile(path):
        print(f"FAIL: schema file missing: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data is not None else {}


_CACHE = {}


def get_schema():
    """Return a dict with keys: page_types, vocabularies, required_fields, id_patterns."""
    if _CACHE:
        return _CACHE
    _CACHE.update({
        "page_types": _load_yaml("page_types.yml"),
        "vocabularies": _load_yaml("vocabularies.yml"),
        "required_fields": _load_yaml("required_fields.yml"),
        "id_patterns": _load_yaml("id_patterns.yml"),
    })
    return _CACHE


def compiled_id_patterns():
    """Return {page_type: compiled_regex} from id_patterns.yml."""
    patterns = get_schema()["id_patterns"]
    out = {}
    for ptype, pat in patterns.items():
        out[ptype] = re.compile(pat)
    return out


def phase_at_least(current, target):
    """True if current phase is at or beyond target in PHASE_ORDER."""
    try:
        return PHASE_ORDER.index(current) >= PHASE_ORDER.index(target)
    except ValueError:
        return False


def read_phase(project_root):
    """Read phase from project-state.yml; default to 'bootstrap' if absent."""
    path = os.path.join(project_root, "project-state.yml")
    if not os.path.isfile(path):
        return "bootstrap"
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return str(data.get("phase", "bootstrap")).strip() or "bootstrap"


if __name__ == "__main__":
    s = get_schema()
    print("PASS: _schema_util.py loaded schema:",
          ", ".join(f"{k}={len(s[k])}" for k in s))
```

## E.5 Code anchor 3 — `_shared/scripts/validate_traceability.py` (complete, extended)

This is the v2 traceability validator extended with the extraction-side rules from Part B.5. It still imports only from `_fm_util.py` plus the phase helper, and returns the v2 empty-pass behaviour while phase is `bootstrap`/`skeleton`.

```python
#!/usr/bin/env python3
"""Validate the PKE traceability invariant for one procedure project (v3).

Usage:
    python3 validate_traceability.py /path/to/Procedure_X
    # or set the PKE_PROJECT environment variable

The invariant (master plan Part B.5), extraction side included:
  Extraction side
    - Every section cites at least one raw clause (source: raw/<file>.pdf#<clause>).
    - Every requirement names a parent_section that resolves to a section.
    - Every decision links to at least one finding.
    - Every form maps to at least one requirement or one reference (basis).
  Finding-onward
    - Every finding cites >=1 evidence (section/requirement) and >=1 basis (reference).
    - Every high/medium non-provisional finding cites >=1 change.
    - Every provisional finding carries a provisional_reason.
    - Every change cites >=1 finding, a resolving target_section, >=1 basis (reference),
      and a resolving draft_ref.
    - No change is an orphan.
"""
import glob
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _fm_util import parse_frontmatter, normalize_value, normalize_list
from _schema_util import read_phase, phase_at_least

SOURCE_CITATION_RE = re.compile(r"\(source:\s*raw/[^#]+#[^)\s]+\)")


def resolve_project_root():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    env = os.environ.get("PKE_PROJECT")
    if env:
        return os.path.abspath(env)
    print("FAIL: no project path given (argv[1] or PKE_PROJECT).", file=sys.stderr)
    sys.exit(2)


def load_pages(wiki_dir):
    """Return (by_id, pages). by_id maps id -> (type, relpath). pages: list of tuples."""
    by_id = {}
    pages = []
    for fp in glob.glob(os.path.join(wiki_dir, "**", "*.md"), recursive=True):
        fm, body = parse_frontmatter(fp)
        if fm is None:
            continue
        pid = normalize_value(fm.get("id", ""))
        ptype = normalize_value(fm.get("type", ""))
        if not pid:
            continue
        rel = os.path.relpath(fp, wiki_dir)
        by_id[pid] = (ptype, rel)
        pages.append((pid, ptype, fm, body, rel))
    return by_id, pages


def main():
    project_root = resolve_project_root()
    wiki_dir = os.path.join(project_root, "wiki")
    if not os.path.isdir(wiki_dir):
        print(f"FAIL: wiki dir not found: {wiki_dir}")
        sys.exit(1)

    phase = read_phase(project_root)
    by_id, pages = load_pages(wiki_dir)
    failures = []

    def exists_of_type(ref_id, allowed_types):
        info = by_id.get(ref_id)
        if info is None:
            return False
        return info[0] in allowed_types

    sections = [(p, fm, b, rel) for p, t, fm, b, rel in pages if t == "section"]
    requirements = [(p, fm, rel) for p, t, fm, b, rel in pages if t == "requirement"]
    decisions = [(p, fm, rel) for p, t, fm, b, rel in pages if t == "decision"]
    forms = [(p, fm, rel) for p, t, fm, b, rel in pages if t == "form"]
    findings = [(p, fm, rel) for p, t, fm, b, rel in pages if t == "finding"]
    changes = [(p, fm, rel) for p, t, fm, b, rel in pages if t == "change"]

    # Empty pass only in the earliest phases (v3 phase-aware behaviour).
    if not phase_at_least(phase, "extracted") and not findings and not changes:
        print(f"PASS: validate_traceability.py — phase '{phase}', empty pass")
        sys.exit(0)

    # Extraction side (enforced from 'extracted' onward).
    if phase_at_least(phase, "extracted"):
        for pid, fm, body, rel in sections:
            if not SOURCE_CITATION_RE.search(body or ""):
                failures.append(f"{rel}: section {pid} has no (source: raw/...#clause) citation")
        for pid, fm, rel in requirements:
            parent = normalize_value(fm.get("parent_section", ""))
            if not exists_of_type(parent, {"section"}):
                failures.append(f"{rel}: requirement {pid} parent_section '{parent}' does not resolve")

    if phase_at_least(phase, "findings_authored"):
        for pid, fm, rel in decisions:
            linked = normalize_list(fm.get("derived_from")) + normalize_list(fm.get("affected_pages"))
            if not any(exists_of_type(normalize_value(r), {"finding"}) for r in linked):
                failures.append(f"{rel}: decision {pid} links to no finding")

    if phase_at_least(phase, "draft_ready"):
        for pid, fm, rel in forms:
            linked = normalize_list(fm.get("related_pages")) + normalize_list(fm.get("basis_refs"))
            ok = any(exists_of_type(normalize_value(r), {"requirement"}) for r in linked) or \
                 any(exists_of_type(normalize_value(r), {"reference"}) for r in linked)
            if not ok:
                failures.append(f"{rel}: form {pid} maps to no requirement or reference basis")

    # Finding-onward side (v2 invariant, retained).
    for pid, fm, rel in findings:
        severity = normalize_value(fm.get("severity", "")).lower()
        provisional = normalize_value(fm.get("provisional", "")).lower() in ("true", "yes", "1")
        evidence = normalize_list(fm.get("evidence_refs"))
        basis = normalize_list(fm.get("basis_refs"))
        change_refs = normalize_list(fm.get("change_refs"))
        if not any(exists_of_type(normalize_value(r), {"section", "requirement"}) for r in evidence):
            failures.append(f"{rel}: finding {pid} has no valid evidence_refs (section/requirement)")
        if not any(exists_of_type(normalize_value(r), {"reference"}) for r in basis):
            failures.append(f"{rel}: finding {pid} has no valid basis_refs (reference)")
        if provisional:
            if not normalize_value(fm.get("provisional_reason", "")):
                failures.append(f"{rel}: provisional finding {pid} has no provisional_reason")
        else:
            if severity in ("high", "medium"):
                if not any(exists_of_type(normalize_value(r), {"change"}) for r in change_refs):
                    failures.append(f"{rel}: finding {pid} (severity {severity}) has no valid change_refs")

    for pid, fm, rel in changes:
        finding_refs = normalize_list(fm.get("finding_refs"))
        target_section = normalize_value(fm.get("target_section", ""))
        basis = normalize_list(fm.get("basis_refs"))
        draft_ref = normalize_value(fm.get("draft_ref", ""))
        if not any(exists_of_type(normalize_value(r), {"finding"}) for r in finding_refs):
            failures.append(f"{rel}: change {pid} is an orphan (no valid finding_refs)")
        if not exists_of_type(target_section, {"section"}):
            failures.append(f"{rel}: change {pid} target_section '{target_section}' does not resolve to a section")
        if not any(exists_of_type(normalize_value(r), {"reference"}) for r in basis):
            failures.append(f"{rel}: change {pid} has no valid basis_refs (reference)")
        if not exists_of_type(draft_ref, {"revision-draft", "section"}):
            failures.append(f"{rel}: change {pid} draft_ref '{draft_ref}' does not resolve")

    if failures:
        print("FAIL: validate_traceability.py")
        for m in failures:
            print(f"  {m}")
        sys.exit(1)
    print(f"PASS: validate_traceability.py — phase '{phase}', "
          f"{len(findings)} findings, {len(changes)} changes traced")


if __name__ == "__main__":
    main()
```

---

## E.6 Code anchor 4 — `_shared/scripts/validate_citations.py` (complete, new in v3)

```python
#!/usr/bin/env python3
"""Validate body citations for one procedure project (v3).

Rules:
  - Every (source: raw/<file>.pdf#<clause>) resolves to a file in raw/ AND the
    <clause> appears in derived/clause-map.csv.
  - Every (basis: REF-<id> §<clause>) resolves to a reference page; clause non-empty.
  - Every section page has at least one (source: ...) citation (from 'extracted' phase).
  - Every finding page has at least one evidence citation and at least one basis citation.
  - Clause parts are never empty.
"""
import csv
import glob
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _fm_util import parse_frontmatter, normalize_value
from _schema_util import read_phase, phase_at_least

SOURCE_RE = re.compile(r"\(source:\s*(raw/[^#\s]+)#([^)\s]+)\)")
BASIS_RE = re.compile(r"\(basis:\s*(REF-[A-Za-z0-9]+)\s*§?\s*([^)\s]+)?\)")


def resolve_project_root():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    env = os.environ.get("PKE_PROJECT")
    if env:
        return os.path.abspath(env)
    print("FAIL: no project path given (argv[1] or PKE_PROJECT).", file=sys.stderr)
    sys.exit(2)


def load_clause_map(project_root):
    """Return a set of clause strings recorded in derived/clause-map.csv."""
    path = os.path.join(project_root, "derived", "clause-map.csv")
    clauses = set()
    if not os.path.isfile(path):
        return clauses, False
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c = (row.get("source_clause") or "").strip()
            if c:
                clauses.add(c)
    return clauses, True


def main():
    project_root = resolve_project_root()
    wiki_dir = os.path.join(project_root, "wiki")
    raw_dir = os.path.join(project_root, "raw")
    if not os.path.isdir(wiki_dir):
        print(f"FAIL: wiki dir not found: {wiki_dir}")
        sys.exit(1)

    phase = read_phase(project_root)
    clause_set, clause_map_present = load_clause_map(project_root)
    reference_ids = set()
    pages = []
    for fp in glob.glob(os.path.join(wiki_dir, "**", "*.md"), recursive=True):
        fm, body = parse_frontmatter(fp)
        if fm is None:
            continue
        pid = normalize_value(fm.get("id", ""))
        ptype = normalize_value(fm.get("type", ""))
        rel = os.path.relpath(fp, wiki_dir)
        pages.append((pid, ptype, body or "", rel))
        if ptype == "reference":
            reference_ids.add(pid)

    if not phase_at_least(phase, "extracted"):
        print(f"PASS: validate_citations.py — phase '{phase}', empty pass")
        sys.exit(0)

    failures = []
    for pid, ptype, body, rel in pages:
        sources = SOURCE_RE.findall(body)
        bases = BASIS_RE.findall(body)

        for rawpath, clause in sources:
            disk = os.path.join(project_root, rawpath)
            if not os.path.isfile(disk):
                failures.append(f"{rel}: source citation file not found: {rawpath}")
            if not clause.strip():
                failures.append(f"{rel}: source citation has empty clause for {rawpath}")
            elif clause_map_present and clause.strip() not in clause_set:
                failures.append(f"{rel}: source clause '{clause}' not in derived/clause-map.csv")

        for ref_id, clause in bases:
            if ref_id not in reference_ids:
                failures.append(f"{rel}: basis citation {ref_id} has no reference page")
            if clause is None or not str(clause).strip():
                failures.append(f"{rel}: basis citation {ref_id} has empty clause")

        if ptype == "section" and not sources:
            failures.append(f"{rel}: section {pid} has no (source: ...) citation")
        if ptype == "finding":
            if not sources and not bases:
                failures.append(f"{rel}: finding {pid} has no source/basis citation in body")

    if not clause_map_present and phase_at_least(phase, "extracted"):
        failures.append("derived/clause-map.csv is missing (required from 'extracted' phase)")

    if failures:
        print("FAIL: validate_citations.py")
        for m in failures:
            print(f"  {m}")
        sys.exit(1)
    print(f"PASS: validate_citations.py — phase '{phase}', {len(pages)} pages scanned")


if __name__ == "__main__":
    main()
```

## E.7 Code anchor 5 — `_shared/scripts/validate_raw_sources.py` (complete, new in v3)

```python
#!/usr/bin/env python3
"""Validate raw-source immutability for one procedure project (v3).

manifests/raw_sources.csv header:
  file_id,filename,sha256,size_bytes,source_type,added_on,added_by,locked

Rules:
  - Every file in raw/ is listed in raw_sources.csv.
  - Every listed file exists in raw/.
  - Recorded sha256 matches the file on disk.
  - locked == true for every source from the 'skeleton' phase onward.
"""
import csv
import glob
import hashlib
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from _schema_util import read_phase, phase_at_least

HEADER = ["file_id", "filename", "sha256", "size_bytes",
          "source_type", "added_on", "added_by", "locked"]


def resolve_project_root():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    env = os.environ.get("PKE_PROJECT")
    if env:
        return os.path.abspath(env)
    print("FAIL: no project path given (argv[1] or PKE_PROJECT).", file=sys.stderr)
    sys.exit(2)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    project_root = resolve_project_root()
    raw_dir = os.path.join(project_root, "raw")
    manifest = os.path.join(project_root, "manifests", "raw_sources.csv")
    phase = read_phase(project_root)

    if not os.path.isdir(raw_dir):
        print(f"FAIL: raw dir not found: {raw_dir}")
        sys.exit(1)

    raw_files = sorted(
        os.path.basename(p) for p in glob.glob(os.path.join(raw_dir, "*"))
        if os.path.isfile(p)
    )

    # Bootstrap allows an empty raw/ and absent manifest.
    if not phase_at_least(phase, "skeleton") and not raw_files and not os.path.isfile(manifest):
        print(f"PASS: validate_raw_sources.py — phase '{phase}', empty pass")
        sys.exit(0)

    if not os.path.isfile(manifest):
        print(f"FAIL: raw_sources.csv missing: {manifest}")
        sys.exit(1)

    failures = []
    listed = {}
    with open(manifest, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != HEADER:
            failures.append(f"raw_sources.csv header mismatch. Expected: {HEADER}")
        for row in reader:
            listed[(row.get("filename") or "").strip()] = row

    for fn in raw_files:
        if fn not in listed:
            failures.append(f"raw/{fn} is not listed in raw_sources.csv")

    for fn, row in listed.items():
        disk = os.path.join(raw_dir, fn)
        if not os.path.isfile(disk):
            failures.append(f"raw_sources.csv lists {fn}, but raw/{fn} does not exist")
            continue
        recorded = (row.get("sha256") or "").strip().lower()
        actual = sha256_of(disk)
        if recorded and recorded != actual:
            failures.append(f"raw/{fn} sha256 mismatch (recorded {recorded[:12]}…, actual {actual[:12]}…)")
        if phase_at_least(phase, "skeleton"):
            if (row.get("locked") or "").strip().lower() not in ("true", "yes", "1"):
                failures.append(f"raw/{fn} is not marked locked in raw_sources.csv")

    if failures:
        print("FAIL: validate_raw_sources.py")
        for m in failures:
            print(f"  {m}")
        sys.exit(1)
    print(f"PASS: validate_raw_sources.py — phase '{phase}', {len(raw_files)} raw files verified")


if __name__ == "__main__":
    main()
```

## E.8 Remaining validators — exact rule tables

The remaining validators are thin once the schema files (Part F) exist. Each imports `_fm_util.py` and `_schema_util.py`, accepts a project path, and honours the phase. Their full code is produced during EPIC 0 execution; the rule tables below are the acceptance contract.

**`validate_structure.py`** — required paths by phase:

| Path | Required from phase |
|------|---------------------|
| `CLAUDE.md`, `index.md`, `log.md`, `current-status.md`, `project-state.yml` | skeleton |
| `raw/`, `derived/`, `wiki/`, `manifests/` | skeleton |
| `manifests/{pages,findings,runs,raw_sources}.csv` | skeleton |
| `derived/text/`, `derived/clause-map.csv` | extracted |
| at least one `wiki/**/*.md` of type `section` | extracted |
| at least one `revision-draft` (or `wiki/draft/` set) | draft_ready |

**`validate_frontmatter.py`** — per page: `id` matches its `id_patterns.yml` regex and is unique; `type` in vocab; every field in `required_fields.yml[type].common` and `[type].specific` present and non-empty; every controlled value in its vocab; dates valid (placeholder `YYYY-MM-DD` rejected from `extracted`); `confidence: unknown` rejected from `extracted`; `classification: unknown` rejected from `changes_authored`; for `requirement` with modality `shall`/`should`, `actor` resolves to a `role` page unless `actor` is `not stated`; synthesis pages carry `derived_from`, extraction pages carry `source`+`source_clause`.

**`validate_references.py`** — every `reference` records `cited_revision`, `current_revision`, `validity`, `reference_role`, and verification fields; flag where `cited_revision != current_revision` and `validity != superseded`; every `REF-x` cited in any section body has a `reference` page; `issue_blocker` must be `true` while `controlled_index_checked` is `false`.

**`validate_findings.py`** — `severity` in vocab; each high/medium finding has ≥1 `change` unless `provisional`; each `provisional` finding has a `provisional_reason`; for every terminology id in `terminology_map.yml` whose `old_terms` appear in a section body, there is a finding, a `no-update` decision, or a recorded exception referencing that section.

**`validate_manifests.py`** — headers exactly as in Part F; every `wiki/**/*.md` page id appears in `pages.csv`; every `finding` id appears in `findings.csv`; `runs.csv` rows append-only.

## E.9 `validate_draft.py` and the semantic-lint checklist

Structural checks (from v2): the `revision-draft` contains every required NEK section in order; every `change` page id appears in the draft; the change log ("Spremembe v postopku") and the Dodatek checklist are present; the archival section uses the transitional-location pattern, not a fixed file-server path.

Semantic-lint checklist (new in v3 — sharpens EPIC 15). Each item is a defined check; items not yet automated are run as a recorded manual review and logged in `runs.csv` with the reviewer:

| Check | Purpose |
|-------|---------|
| Each `shall` statement names a resolvable actor | Prevents passive, unenforceable requirements. |
| Each listed reference is used in at least one operative clause | Prevents decorative reference lists. |
| Each high finding changes draft text (the change is implemented, not just cited) | Prevents superficial closure. |
| Each obsolete term from `terminology_map.yml` is removed or justified | Ensures terminology modernization. |
| Each record entry has owner, storage location, retention, and transition note | Strengthens archival control. |
| Each checklist/form item maps to a requirement or a reference basis | Prevents arbitrary checklist content. |
| No `scope_expansion` change appears without an approved gate decision | Protects original intent. |

## E.10 `run_all_validations.py`

The aggregator accepts a project path, reads `project-state.yml`, runs every validator in dependency order (`_fm_util` self-test, `_schema_util` self-test, then structure, frontmatter, raw_sources, citations, references, traceability, findings, manifests, draft), prints a per-validator and aggregate PASS/FAIL, and appends one row per validator to `manifests/runs.csv`.

Recorded EPIC 0 baseline against an empty `Procedure_X` in phase `skeleton`: `validate_structure.py` FAIL (content not built); frontmatter, citations, traceability, findings, draft PASS (empty pass); references PASS; raw_sources PASS or FAIL depending on whether the source is placed; overall FAIL. This baseline is recorded before any later epic begins.

---

# PART F — MACHINE-READABLE SCHEMA SPECIFICATION (new in v3)

These files live in `_shared/schema/`. They are the single source of truth that the behavioural validators load through `_schema_util.py` (Part E.4). The prose in Part B and the data here must agree; on any conflict, these files win, because code reads them, not the prose.

## F.1 `_shared/schema/page_types.yml`

```yaml
# The twelve page types and which side of the workflow each belongs to.
section:             {origin: extraction, summary: "one per numbered source section"}
requirement:         {origin: extraction, summary: "one atomic normative obligation"}
role:                {origin: extraction, summary: "a responsibility holder"}
definition:          {origin: extraction, summary: "a defined term"}
abbreviation:        {origin: extraction, summary: "an acronym + expansion"}
reference:           {origin: extraction, summary: "a referenced external document"}
form:                {origin: extraction, summary: "an appendix/template/minute form"}
procedure-overview:  {origin: synthesis,  summary: "one per procedure, identity + status"}
finding:             {origin: synthesis,  summary: "a gap/obsolescence/conflict"}
change:              {origin: synthesis,  summary: "a proposed edit"}
decision:            {origin: synthesis,  summary: "a recorded review or gate decision"}
revision-draft:      {origin: synthesis,  summary: "the assembled drafted revision"}
```

## F.2 `_shared/schema/vocabularies.yml`

```yaml
status:          [draft, active, superseded, under-review, obsolete]
confidence:      [high, medium, low, unknown]
content_origin:  [extracted, paraphrased, inferred, synthesized, drafted]
severity:        [high, medium, low]
validity_ref:    [valid, superseded, unknown, not-applicable]
validity_req:    [valid, drifted, obsolete, unknown]
modality:        [shall, should, may, informative]
classification:  [SR, AQ, NSR, n-a, unknown]
reference_role:  [normative, informative, template, historical]
change_type:     [compliance_update, terminology_update, clarification,
                  template_completion, scope_expansion, editorial]
decision_status: [approved, rejected, deferred, update-required, no-update]
phase:           [bootstrap, skeleton, extracted, crosschecked,
                  findings_authored, changes_authored, draft_ready]
# Phase from which a placeholder/unknown value is rejected:
unknown_rejected_from:
  confidence: extracted
  classification: changes_authored
  placeholder_date: extracted
```

## F.3 `_shared/schema/required_fields.yml`

```yaml
# Fields common to every page (all required, non-empty unless noted).
common:
  - id
  - title
  - type
  - procedure_id
  - content_origin
  - status
  - confidence
  - created
  - updated
  - last_verified
  - related_pages   # may be an empty list

# Source fields required on extraction-origin pages.
source_required_types: [section, requirement, role, definition, abbreviation, reference, form]
source_fields: [source, source_clause]

# derived_from required on synthesis-origin pages.
derived_required_types: [finding, change, decision, revision-draft]
derived_field: derived_from

# Type-specific required fields.
specific:
  reference:
    - cited_revision
    - current_revision
    - validity            # in vocabularies.validity_ref
    - reference_role
    - current_revision_source
    - controlled_index_checked
    - issue_blocker
  requirement:
    - modality
    - actor
    - action
    - validity            # in vocabularies.validity_req
    - classification
    - parent_section
  finding:
    - severity
    - provisional
    - evidence_refs       # >=1
    - basis_refs          # >=1
    - classification
    # change_refs required when severity in [high, medium] and not provisional
    # provisional_reason required when provisional == true
  change:
    - finding_refs         # >=1
    - target_section
    - basis_refs           # >=1
    - draft_ref
    - change_type
    - requires_human_approval
    - classification
  decision:
    - decision_status
    - affected_pages
  abbreviation:
    - expansion
    - obsolete
    # replacement required when obsolete == true
  revision-draft:
    - classification

# Optional requirement action fields (validated for vocab only if present).
requirement_optional: [object, condition, timing, record]
```

## F.4 `_shared/schema/id_patterns.yml`

```yaml
# One regex per page type (anchored). Matches the grammar in master plan Part B.9.
procedure-overview: "^OVR-[A-Z0-9]+$"
section:            "^SEC-[0-9]+(-[0-9]+)*$"
requirement:        "^REQ-[0-9]+(-[0-9]+)*-[0-9]{2}[a-z]?$"
role:               "^ROLE-[A-Z0-9]+$"
definition:         "^DEF-[A-Z0-9]+$"
abbreviation:       "^ABBR-[A-Z0-9]+$"
reference:          "^REF-[A-Z0-9]+$"
form:               "^FORM-[A-Z0-9-]+$"
finding:            "^F-[0-9]{3}$"
change:             "^CHG-[0-9]{3}$"
decision:           "^DEC-[0-9]{3}$"
revision-draft:     "^DRAFT-[A-Z0-9]+-R[0-9]+$"
# draft section pages (inside wiki/draft/) use the section page type rules
# unless a dedicated DSEC id is adopted:
draft-section:      "^DSEC-[A-Z0-9]+-[0-9]{2}$"
```

## F.5 `_shared/schema/terminology_map.yml`

```yaml
# Controlled, citable terminology map. Cross-check applies every entry to every section.
- id: TERM-001
  old_terms: [NCR]
  current_terms: [NCR, POR, FDCR, SPWAR, KP, ZKP]
  basis_refs: [REF-QAP]
  applies_to: ["SKV.QA-002/2012", "SKV.QA-003/2012"]
  default_severity: medium
  action: replace_narrow_deviation_language
  note: "NCR-only language must broaden to the full deviation and corrective-program set."

- id: TERM-002
  old_terms: ["inspection plan", "kontrolni plan"]
  current_terms: ["Plan kontrol", "WSIP", "PIK"]
  basis_refs: [REF-QAP, REF-ADP]
  applies_to: ["SKV.QA-002/2012", "SKV.QA-003/2012"]
  default_severity: medium
  action: replace_inspection_plan_terminology
  note: "ADP-1.1.080 App 6.4 governs the package/inspection terminology."

- id: TERM-003
  old_terms: [NAB]
  current_terms: ["NAB.LN"]
  basis_refs: [REF-SP]
  applies_to: ["SKV.QA-002/2012", "SKV.QA-003/2012"]
  default_severity: medium
  action: update_documentation_routing
  note: "Documentation routing now uses NAB.LN."

- id: TERM-004
  old_terms: ["SKV Filer 2", "file-server path", "fixed file path"]
  current_terms: ["current DMS location (transitional note allowed)"]
  basis_refs: [REF-SP, REF-RE25]
  applies_to: ["SKV.QA-002/2012", "SKV.QA-003/2012"]
  default_severity: high
  action: replace_with_transitional_location
  note: "RE25 §10.1 routes minutes via procurement to a defined list; the 2012 path is obsolete."

- id: TERM-005
  old_terms: ["remontni prirocnik", "generic outage manual"]
  current_terms: ["RE25 / Remont 2025 (entry §10.1, exit §10.2, QA/QC §6.3)"]
  basis_refs: [REF-RE25]
  applies_to: ["SKV.QA-002/2012", "SKV.QA-003/2012"]
  default_severity: high
  action: resolve_to_current_outage_manual
  note: "Resolves former finding F9; no longer provisional."

- id: TERM-006
  old_terms: ["meeting cadence", "NCR reporting"]
  current_terms: ["weekly Monday 12:00 SKV QA/QC meeting; daily NCR report to SKV.QC"]
  basis_refs: [REF-RE25]
  applies_to: ["SKV.QA-002/2012", "SKV.QA-003/2012"]
  default_severity: low
  action: anchor_cadence_to_outage_manual
  note: "RE25 §6.3.b and §12.5 confirm the cadence; reference the manual, do not freeze detail."
```

---

# PART G — INTEGRATION PLAN (GITHUB-ISSUES STYLE, TDD ORDER)

Execution order is test-first. The v3 order keeps the eighteen-epic structure but makes two corrections: the machine-readable schema is built before the validators that read it, and golden-example calibration moves ahead of the second procedure so the drafting skill is tuned before errors can propagate.

## EPIC 0 — Schema and validation layer

**What & Why:** The schema data and the test layer are the foundation. Validators read the schema; the schema must exist first.

### Task 0.1 — Install PyYAML and create `_shared/scripts/` and `_shared/schema/`
- [ ] `python3 -c "import yaml"` succeeds inside the VM environment.
- [ ] `_shared/scripts/` and `_shared/schema/` exist.

### Task 0.2 — Create the schema files (Part F)
- [ ] `page_types.yml`, `vocabularies.yml`, `required_fields.yml`, `id_patterns.yml`, `terminology_map.yml` match Part F.

### Task 0.3 — Create `_fm_util.py` and `_schema_util.py`
- [ ] `_fm_util.py` matches Part E.3 and self-tests PASS.
- [ ] `_schema_util.py` matches Part E.4, loads all five schema files, and self-tests PASS.

### Task 0.4 — Create `validate_traceability.py` and `validate_citations.py`
- [ ] `validate_traceability.py` matches Part E.5; empty pass in `bootstrap`/`skeleton`.
- [ ] `validate_citations.py` matches Part E.6; empty pass before `extracted`.

### Task 0.5 — Create the remaining validators
- [ ] `validate_raw_sources.py` matches Part E.7.
- [ ] `validate_structure.py`, `validate_frontmatter.py`, `validate_references.py`, `validate_findings.py`, `validate_manifests.py`, `validate_draft.py` satisfy the Part E.8/E.9 rule tables and import both utils.
- [ ] Each validator accepts a project path and reads `project-state.yml`.

### Task 0.6 — Create `run_all_validations.py` and record the baseline
- [ ] The aggregator runs every validator, prints per-validator and aggregate PASS/FAIL, appends to `manifests/runs.csv`.
- [ ] The Part E.10 baseline is reproduced and recorded.

## EPIC 1 — Shared layer and reference registry

### Task 1.1 — Place the corpus in `_shared/references/`
- [ ] The four reference PDFs are present and read-only.

### Task 1.2 — Create `_shared/reference-index.md`
- [ ] Each reference has an id (Part B.9), title, current revision, validity, role, and a note.
- [ ] Revisions match the supplied copies (ADP-1.1.080 Rev 8, General Conditions Rev 24, QAP-9.7.002 Rev 1).
- [ ] The RE25 entry records the read manual with the governing clauses (entry §10.1, exit §10.2, QA/QC §6.3); validity `valid`; `controlled_index_checked: false` and `issue_blocker: true` until human confirmation.

## EPIC 2 — PKE skills authoring

### Task 2.1 — Author the five SKILL.md files (Part D)
- [ ] Each skill has a name, a when-to-use trigger, and the Part D contents.
- [ ] `procedure-extraction` states the requirement-splitting rule.
- [ ] `revision-drafting` names the SKV.QA-003 Rev 1 example as its quality bar and calibration fixture.

## EPIC 3 — Page-type templates

### Task 3.1 — Create one template per page type
- [ ] `_shared/templates/` holds a template for each type in Part B.2.
- [ ] Each template's frontmatter matches Part B.3 and `required_fields.yml`.

## EPIC 4 — Per-procedure skeletons

### Task 4.1 — Build Procedure_A and Procedure_B folders
- [ ] Each has raw/, derived/, wiki/, manifests/, project-state.yml, CLAUDE.md, index.md, log.md, current-status.md.
- [ ] `manifests/` holds pages.csv, findings.csv, runs.csv, raw_sources.csv with the Part F headers.
- [ ] `project-state.yml` starts at phase `skeleton`.
- [ ] `validate_structure.py` returns PASS for phase `skeleton`.

## EPIC 5 — Git initialization

### Task 5.1 — Initialize ONE repository and commit the skeleton
- [ ] A single git repository covers the whole project (shared + both procedures).
- [ ] The commit convention from CLAUDE.md is used.
- [ ] The skeleton, schema, scripts, templates, and skills are committed.

## EPIC 6 — CLAUDE.md authoring

### Task 6.1 — Write `_shared/CLAUDE.md` — matches Part C.1.
### Task 6.2 — Write each `Procedure_X/CLAUDE.md` — matches Part C.2, with correct id, shortcode, source, and references.

## EPIC 7 — Source ingest and derived extraction

### Task 7.1 — Place the source procedures in raw/ and lock them
- [ ] `Procedure_B/raw/skv-qa-002-2012.pdf` and `Procedure_A/raw/skv-qa-003-2012.pdf` are present and read-only.
- [ ] Each is recorded in `manifests/raw_sources.csv` with a SHA-256; `validate_raw_sources.py` PASS.

### Task 7.2 — Build the derived layer
- [ ] `derived/text/` holds extracted text per source; `derived/clause-map.csv` maps each source clause used by wiki pages to a derived location; `derived/extraction-notes.md` records unreadable tables/images and confidence.
- [ ] After build, `derived/` is locked read-only.

## EPIC 8 — Procedure extraction (Procedure_A first, for calibration)

### Task 8.1 — Extract Procedure_A into wiki pages
- [ ] `procedure-extraction` SKILL.md is read first.
- [ ] One `section` page per numbered source section; one `requirement` page per atomic obligation (splitting rule); each reference/definition/abbreviation/role/form has its page.
- [ ] Every page cites a source clause; ids follow Part B.9; `content_origin` set; no invented content.
- [ ] Phase advances to `extracted`; `validate_frontmatter.py` and `validate_citations.py` PASS.

## EPIC 9 — Reference cross-check and terminology mapping

### Task 9.1 — Run the cross-check on Procedure_A
- [ ] `reference-crosscheck` SKILL.md is read first.
- [ ] Each reference page's cited/current revision, role, and verification fields are filled; mismatches flagged.
- [ ] `terminology_map.yml` applied to every section; each warranted change noted; process drift (e.g. missing QAP-9.7.002 link) recorded.
- [ ] Phase advances to `crosschecked`; `validate_references.py` PASS.

## EPIC 10 — Findings authoring
### Task 10.1 — Author findings from cross-check output
- [ ] `finding-authoring` SKILL.md is read first.
- [ ] Each finding has severity, evidence_refs, basis_refs, classification; provisional findings carry a reason (RE25-dependent findings are not provisional).
- [ ] Phase advances to `findings_authored`; `validate_findings.py` PASS.

## EPIC 11 — Update decision
### Task 11.1 — Record the update determination as a `decision` page linked to its findings.

## EPIC 12 — Change-set authoring
### Task 12.1 — Author one change per intended edit
- [ ] Each high/medium non-provisional finding has ≥1 change with finding, target_section, basis, draft target, `change_type`, and `requires_human_approval`.
- [ ] Phase advances to `changes_authored`; `validate_traceability.py` PASS.

## EPIC 13 — Calibration against the golden example (moved early)

**What & Why:** The approved SKV.QA-003 Rev 1 draft is the quality benchmark. Procedure_A reproduces it, and the comparison turns the example into a TDD acceptance fixture **before** Procedure_B runs, so the skills are tuned first.

### Task 13.1 — Assemble the Procedure_A draft and compare to the example
- [ ] `revision-drafting` and `nek-procedure-template` SKILL.md are read first.
- [ ] The draft contains every required NEK section in order; every change appears; change log and checklist present; archival uses the transitional pattern.
- [ ] A gap report lists any section or change missing versus the example; the report is empty or each gap is justified.
- [ ] Skills/validators are corrected if the comparison reveals gaps. Phase advances to `draft_ready`; `validate_draft.py` PASS.

## EPIC 14 — Procedure_B full run

### Task 14.1 — Run the calibrated pipeline on Procedure_B (entry meetings)
- [ ] Extraction, cross-check, findings, decision, change-set, draft, validate — using the same skills.
- [ ] Example-specific exit clauses are NOT forced into the entry draft (Part H).
- [ ] `run_all_validations.py` PASS at phase `draft_ready`.

## EPIC 15 — Validation gate, lint, and traceability

### Task 15.1 — Run the full suite and the semantic lint
- [ ] `run_all_validations.py` returns overall PASS.
- [ ] The Part E.9 semantic-lint checklist passes; any manual items are logged with a reviewer in `runs.csv`.

## EPIC 16 — Output and deliverable packaging

### Task 16.1 — Export the review record and the draft
- [ ] A single markdown deliverable per procedure: overview, findings, decision, change set, drafted revision.
- [ ] A Word export is offered later (docx-export skill), not built now.

## EPIC 17 — Cross-procedure consistency

### Task 17.1 — Compare the entry/exit pair
- [ ] Terminology, deviation handling, and archival rules match between SKV.QA-002 and SKV.QA-003.
- [ ] The "close open deviations before the exit meeting" rule is consistent in both drafts.

## EPIC 18 — Session continuity and deferred expansion

### Task 18.1 — Verify session continuity
- [ ] A new session run of `/pke-context` reproduces phase, pages by type, open findings, open gates, draft status, and next action.

### Task 18.2 — Record deferred features — the Part L list is current.

---

# PART H — HOW THE SCHEMA REPRODUCES THE APPROVED EXAMPLE

Each example section is reached from page types and a finding-driven change.

| Approved example section | Schema pages that produce it | Driven by |
|--------------------------|------------------------------|-----------|
| Cover with "Nadomesca" | `revision-draft` + nek-procedure-template skill | template rule |
| 1.0 Namen, 2.0 Obseg | `section` pages + revision-drafting | finding: thin purpose/scope |
| 3.0 Reference (versioned) | `reference` pages with current_revision + verification fields | finding F1 (stale references) |
| 4.0 Definicije in okrajsave | `definition` + `abbreviation` pages | finding: no definitions |
| 5.0 Odgovornosti | `role` pages | finding: no responsibilities |
| 6.0 Vhodni podatki, 7.0 Priprava, 8.0 QA poudarki | `section` + `requirement` pages | extraction + alignment to App 6.4 |
| 9.0 Link to QAP-9.7.002 | `change` page | finding F2 (missing QAP linkage) |
| 11.0 Zapisi (transitional location) | `change` page | finding F3 (obsolete path) |
| Dodatek 1 checklist | `form` page + revision-drafting | template rule |
| Change log | `revision-draft` change-log section | template rule |

## H.1 Normative vs example-specific qualities (new in v3)

The example is the minimum quality bar and the calibration fixture, not the only acceptable wording. To stop an entry procedure being forced into an exit shape, the qualities are split.

**Normative (must hold for every drafted procedure):** a versioned Reference section; a Responsibilities section with resolvable actors; a QAP-9.7.002 linkage; an archival section using the transitional-location pattern; a change log; a checklist appendix; the NEK section order; every change implemented.

**Example-specific (may differ for Procedure_B):** the exact wording; the exact section numbering; procedure-specific checklist items; exit-meeting-only clauses such as the preliminary report, equipment removal, supplier evaluation, and lessons-learned recording. Procedure_B (entry) substitutes its own agenda items from RE25 §10.1 (pre-outage activities, schedule, SKV/commercial requirements, access, internal rules, NEK expectations).

---

# PART I — HUMAN APPROVAL GATES (new in v3)

The acceptance criteria are mostly files and validator PASS/FAIL. A controlled procedure review also needs points where a human decides. Each gate is recorded as a `decision` page and reflected in `project-state.yml -> gates`. A phase does not advance until its gate is `approved`. The final issuance gate cannot pass while any reference carries `issue_blocker: true`.

| Gate | Sits after | Human decision | Records |
|------|-----------|----------------|---------|
| Reference registry | EPIC 1 | Confirm current revisions against the controlled index | sets `controlled_index_checked`, clears `issue_blocker` where confirmed |
| Extraction | EPIC 8 | Confirm source-clause mapping is faithful | `DEC-` page, phase → `extracted` accepted |
| Findings | EPIC 10 | Accept or reject findings | `DEC-` page linked to findings |
| Change-set | EPIC 12 | Accept or reject proposed changes; approve any `scope_expansion` | `DEC-` page; `requires_human_approval` cleared per change |
| Draft ready | EPIC 13/14 | Approve the draft for formal review | `DEC-` page, phase → `draft_ready` accepted |
| Issuance | after EPIC 16 | Confirm controlled-document requirements; no open blockers | `DEC-` page; all references `issue_blocker: false` |

A gate `decision` page records:

```yaml
decision_status: approved | rejected | deferred
decider:
decision_date:
basis_refs: []
affected_pages: []
```

---

# PART J — RISK REGISTER (new in v3)

## J.1 High-risk items

| Risk | Impact | Control (where addressed) |
|------|--------|---------------------------|
| Validators under-specified | False PASS or inconsistent implementation | Machine-readable schema + rule tables (Parts E, F) |
| No phase-aware validation | Empty/incomplete projects pass | Lifecycle phases (B.10), phase gates in every validator (E.1) |
| No source checksum | Raw files change unnoticed | `raw_sources.csv` + `validate_raw_sources.py` (E.7) |
| Reference validity not independently verified | Draft cites stale revisions | Verification fields + `issue_blocker` + issuance gate (B.7, I) |
| Golden example used too late | Skills calibrated after errors propagate | Calibration moved to EPIC 13, before Procedure_B (G) |
| Terminology map not machine-readable | Cross-check inconsistent | `terminology_map.yml` + `validate_findings.py` rule (F.5, E.8) |
| No extracted-text layer | PDF extraction errors hard to audit | `derived/` layer + clause map (B.1, EPIC 7.2) |
| Human gates unclear | Automated output mistaken for approved | Gate map + gate decisions (Part I) |

## J.2 Medium-risk items

| Risk | Impact | Control |
|------|--------|---------|
| ID naming not standardized | Broken links, validator complexity | ID grammar (B.9, F.4) |
| `confidence` undefined | Subjective metadata | Confidence rubric, phase-gated (B.11) |
| `classification` unused | Schema inconsistency | Attached to four page types (B.3, B.4) |
| Draft structural checks too shallow | Weak draft passes | Semantic-lint checklist (E.9) |
| Repository model ambiguous | Version-control confusion | Single monorepo for the POC (B.1, EPIC 5) |
| Scope creep in drafts | Unintended expansion | `change_type` + approval flag + gate (B.3, I) |
| Example overfitting | Entry forced into exit shape | Normative vs example-specific split (H.1) |

---

# PART K — ASSUMPTIONS, LIMITS, AND VERIFICATION ITEMS

- Revision numbers used here come from the supplied copies. They must be confirmed against the controlled document index at issuance, because newer revisions may exist. v3 encodes this in the schema (`controlled_index_checked`, `issue_blocker`) and in the issuance gate, so the admission is enforced, not merely noted.
- The RE25 manual has been read (text version), so its reference page and the RE25-dependent findings are no longer provisional. The text was supplied with infographics removed; if any clause numbering must be quoted exactly in an issued revision, the clause references should be confirmed against the controlled PDF. The `derived/` layer records any clause whose extraction is uncertain.
- Both source procedures (SKV.QA-002/2012 and SKV.QA-003/2012) are in hand, so the input blockers from the prior readiness check are closed.
- Live plant systems cannot be browsed from here. Storage locations and current revisions are marked for human verification and keep `issue_blocker: true` until confirmed.
- The plan is a POC. The lean per-procedure layout is kept, with the validation layer, schema, and templates centralized in `_shared/` so quality is still protected.
- The approved example is the minimum quality bar and the calibration fixture, not the only acceptable wording (Part H.1).
- The precision gaps noted in v2 are now closed in v3: consolidated required-field tables (Part F.3), manifest CSV headers (Part F / E.8), a single final success gate (Part L.1 below references the issuance gate and `run_all_validations.py`), and an explicit step to confirm that placed filenames match the names assumed in the plan (EPIC 7.1, `validate_raw_sources.py`).

## K.1 Final success gate

A procedure draft is ready only when all of the following hold:
1. all required structure exists for `draft_ready`;
2. all raw sources are locked and checksum-verified;
3. all frontmatter passes (ids, vocab, required fields, no placeholders/`unknown`);
4. all citations resolve (source and basis);
5. all references are valid or explicitly marked `issue_blocker: true`;
6. all high/medium non-provisional findings have changes;
7. all changes appear in the draft;
8. all NEK template sections required by the template exist, in order;
9. the semantic-lint checklist passes;
10. a human `decision` page marks the draft ready for review, and — for issuance — no reference carries `issue_blocker: true`.

`run_all_validations.py` checks 1–9 automatically; item 10 is the human gate (Part I).

---

# PART L — DEFERRED ITEMS (TIER 3)

These corrections are sound for a durable production system but add weight beyond the POC. Each waits with a stated reason. None of them protect the id-based traceability chain now, so deferral is safe.

| Deferred item | Reason for deferral |
|---------------|---------------------|
| Six-way document split (ARCHITECTURE / SCHEMA / WORKFLOW / VALIDATION_SPEC / BACKLOG / CLAUDE) | The single consolidated plan is workable for a POC; the highest-value split (machine-readable schema + validation spec) is already taken into `_shared/schema/` and Part E/F. Full split adds maintenance overhead. |
| Full seven-state lifecycle as a separate engine | A single `phase` flag in `project-state.yml` (B.10) delivers the needed strictness without a separate state machine. |
| Section-level drafting as the default | A `wiki/draft/` split is allowed (B.1) but not required; a single `revision-draft` is adequate for procedures of this size. Adopt per-section drafts if a procedure grows large. |
| Full requirement field set as mandatory (object/condition/timing/record/verification on every requirement) | The splitting rule plus `actor`/`action` are mandatory now; the remaining fields stay optional to keep extraction lean. |
| Agent-neutral rewrite of the plan | The POC is explicitly executed by Claude Code. Agent-neutral phrasing is a durability concern for later, not a POC blocker. |
| Compressing the eighteen epics into phases | The epic structure aids issue tracking; compression is cosmetic and does not change control. |
| docx export | The POC deliverable is markdown; the built-in docx skill is added when a Word output is required. |
| Controlled-document-index connector for live revision checks | Live plant systems cannot be browsed from here; the issuance gate covers the manual check meanwhile. |
| Automated requirement-extraction tuning and a cross-procedure consistency report generator | Premature; revisit after the core pipeline is proven on both procedures. |

---

*End of Master Plan v3 — PKE LLM Wiki — Project02_Internal_procedure*

---

## Assistant

*Progress update*

The second master plan will be reviewed for architecture, schema consistency, phase gates, validator logic, traceability, human approvals, and alignment with the first project. Only readiness status and material inspection limits will be reported.

---

## Assistant

The complete **Procedural Knowledge Extraction LLM Wiki Master Plan v3** has been inspected.

The review covered:

- shared and per-procedure architecture;
- monorepo design;
- machine-readable schema;
- page types, identifiers, and controlled vocabularies;
- lifecycle phases and human approval gates;
- source, derived, and wiki-layer separation;
- citation and end-to-end traceability rules;
- validation scripts and TDD sequence;
- raw-source checksum and immutability controls;
- extraction, cross-check, finding, change, and drafting skills;
- Procedure_A calibration and Procedure_B execution;
- reference verification and issuance blockers;
- risk register, assumptions, final success gate, and deferred items;
- alignment with the first Travel Guide Wiki project.

Several internal consistency issues and implementation risks have been recorded for later analysis.

**Ready to continue.**

---

## User

Aslo, we aquired some lessons learned on file transfer between local repo and Github repo.

"""
<see appended text>

"""
Let me know when you're ready to continue.

### Attached file: `Pasted markdown(22).md`

# Github file transfer - Summary and Lessons Learned

## 1. Initial objective

The task had two possible transfer paths:

1. Transfer project files from a Hyper-V virtual machine to a USB drive.
2. Push the project from the virtual machine to GitHub through an interactive authentication process.

The GitHub route was selected and completed successfully.

The project was located inside the Linux virtual machine at:

```text
/home/nekiee/CC_FIN
```

The intended GitHub repository was:

```text
https://github.com/nekiee13/CC_FIN
```

---

# 2. Environment discovered during troubleshooting

## Windows host

The Windows host already had Git installed:

```text
git version 2.51.0.windows.1
```

An incorrect `gh.exe` executable was initially found at:

```text
G:\pinokio\bin\miniconda\Scripts\gh.exe
```

That executable belonged to the Pinokio Miniconda environment and returned:

```text
gh version DEV
```

This was not the official GitHub CLI installation and was unsuitable for reliable GitHub authentication.

The official GitHub CLI was then installed through Winget.

The first installation command failed because Winget attempted to query the Microsoft Store source and encountered a certificate error:

```text
0x8a15005e
The server certificate did not match any of the expected values.
```

The issue was bypassed by forcing the `winget` source:

```powershell
winget install --id GitHub.cli -e --source winget
```

The official executable was then verified directly:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" --version
```

Installed version:

```text
gh version 2.94.0
```

The Windows host was successfully authenticated to GitHub as:

```text
nekiee13
```

However, that authentication applied only to the Windows host. It did not automatically apply inside the Linux virtual machine.

---

## Linux virtual machine

The Linux virtual machine initially had Git but did not have GitHub CLI.

The project repository already existed locally and had the following state:

```text
On branch main
Your branch is ahead of 'origin/main' by 10 commits.
```

Several directories were untracked:

```text
CSV_OUTPUT/lstm_baseline_smoke/
CSV_OUTPUT/spike_level/
CSV_OUTPUT/spike_returns/
CSV_OUTPUT/spike_returns_full/
CSV_OUTPUT/spike_returns_v2/
```

The original Git remote was:

```text
https://github.com/nekiee13/opencode-FIN.git
```

This was the wrong destination repository for the current task.

---

# 3. Main sequence of actions

## Step 1: Verify the local repository

The project directory was entered:

```bash
cd /home/nekiee/CC_FIN
```

Repository status was checked:

```bash
git status
```

This confirmed:

* The active branch was `main`.
* Ten commits were waiting to be pushed.
* Several output directories were untracked.
* The untracked directories were not part of the ten commits.

---

## Step 2: Inspect the configured remote

The configured remote was checked:

```bash
git remote -v
```

The result showed:

```text
origin  https://github.com/nekiee13/opencode-FIN.git
```

This detail should have been treated as a blocking validation point before any push was attempted.

Instead, an initial push was attempted against that remote.

---

## Step 3: First authentication failure

The initial `git push` requested a username and password:

```text
Username for 'https://github.com': nekiee13
Password for 'https://nekiee13@github.com':
```

GitHub rejected the push with:

```text
remote: Permission to nekiee13/opencode-FIN.git denied to nekiee13.
fatal: unable to access ...
The requested URL returned error: 403
```

This demonstrated that normal Git credential handling inside the virtual machine had not yet been configured correctly.

---

## Step 4: Install GitHub CLI inside the VM

GitHub CLI was installed inside Ubuntu:

```bash
sudo apt install gh
```

Installed version:

```text
2.46.0-4
```

This version was older than the Windows host version, but it was sufficient for authentication and Git credential integration.

---

## Step 5: Authenticate using a pasted token

The first GitHub CLI login inside the VM used:

```bash
gh auth login
```

The selected method was:

```text
Paste an authentication token
```

The login completed successfully, and `gh auth status` showed an active authenticated account.

However, `git push` still failed with HTTP 403.

Repository inspection showed that the authenticated account had full permissions:

```json
{
  "admin": true,
  "maintain": true,
  "pull": true,
  "push": true,
  "triage": true
}
```

This indicated that the account itself was not the problem.

The likely cause was the pasted token. The token either lacked suitable repository-content write permission or was incompatible with the intended Git operation.

---

## Step 6: Replace token login with browser device authentication

The GitHub CLI session was removed:

```bash
gh auth logout --hostname github.com
```

A browser-based login was then attempted:

```bash
gh auth login --hostname github.com --git-protocol https --web
```

That failed because the Linux VM session had no graphical display:

```text
Error: no DISPLAY environment variable specified
```

A headless device-flow workaround was then used:

```bash
BROWSER=echo gh auth login --hostname github.com --git-protocol https --web
```

This command caused GitHub CLI to print:

* A one-time device code.
* The GitHub device login URL.

The authentication was completed through a separate browser.

The result was successful:

```text
✓ Authentication complete.
✓ Configured git protocol
✓ Logged in as nekiee13
```

Git credential integration was then configured:

```bash
gh auth setup-git
```

After that, `git push` worked correctly.

---

## Step 7: First successful push went to the wrong repository

The ten commits were successfully pushed to:

```text
https://github.com/nekiee13/opencode-FIN.git
```

The push result showed:

```text
main -> main
```

Technically, the push succeeded. Operationally, it was incorrect because the required target repository was `CC_FIN`.

This was the main process error in the conversation.

---

## Step 8: Validate the intended repository

The intended repository was checked:

```bash
gh repo view nekiee13/CC_FIN --json nameWithOwner,viewerPermission
```

The result confirmed:

```json
{
  "nameWithOwner": "nekiee13/CC_FIN",
  "viewerPermission": "ADMIN"
}
```

This verified that:

* The repository existed.
* The authenticated account had administrative access.
* The repository was a valid push destination.

---

## Step 9: Correct the remote URL

The local repository remote was changed:

```bash
git remote set-url origin https://github.com/nekiee13/CC_FIN.git
```

The corrected remote was verified:

```bash
git remote -v
```

Result:

```text
origin  https://github.com/nekiee13/CC_FIN.git (fetch)
origin  https://github.com/nekiee13/CC_FIN.git (push)
```

---

## Step 10: Push to the correct repository

The correct push command was executed:

```bash
git push -u origin main
```

Result:

```text
[new branch] main -> main
branch 'main' set up to track 'origin/main'
```

The project history was successfully pushed to:

```text
https://github.com/nekiee13/CC_FIN
```

The local `main` branch now tracks:

```text
origin/main
```

---

# 4. Important lessons learned

## Lesson 1: Authentication is machine-specific

Authentication completed on the Windows host does not automatically authenticate Git operations inside a Linux virtual machine.

Each operating system environment maintains its own:

* Git configuration.
* Credential store.
* GitHub CLI configuration.
* Personal access tokens or OAuth tokens.

Therefore, GitHub CLI had to be installed and authenticated separately inside the VM.

---

## Lesson 2: Always verify the remote before pushing

The most important operational lesson is that the remote destination must be checked before any push.

The required pre-push command is:

```bash
git remote -v
```

The destination should be compared carefully against the intended repository.

For this project, the correct output should have been:

```text
origin  https://github.com/nekiee13/CC_FIN.git
```

The previous output pointed to:

```text
opencode-FIN.git
```

Because that mismatch was not corrected before the first successful push, ten commits were uploaded to the wrong repository.

A safer pre-push sequence is:

```bash
pwd
git status
git remote -v
git branch --show-current
```

Only after those checks should this command be executed:

```bash
git push
```

---

## Lesson 3: A successful push is not proof that the correct task was completed

Git can report a completely successful transfer while still sending data to the wrong destination.

Technical success and task success are different.

Technical success means:

* Authentication worked.
* Objects were transferred.
* The remote accepted the branch.

Task success means:

* The correct project was selected.
* The correct branch was selected.
* The correct repository was selected.
* The intended files were included.
* Unwanted files were excluded.

All five conditions must be checked.

---

## Lesson 4: GitHub account passwords should not be used for Git pushes

GitHub no longer accepts ordinary account passwords for HTTPS Git operations.

Suitable methods include:

* GitHub CLI browser authentication.
* GitHub CLI device flow.
* A properly scoped personal access token.
* SSH keys.
* Git Credential Manager.

For a headless Linux VM, the device flow proved reliable:

```bash
BROWSER=echo gh auth login --hostname github.com --git-protocol https --web
```

This method avoids the need for a graphical browser inside the VM.

---

## Lesson 5: A valid token can still fail Git push

The account had full repository permissions, yet the pasted token still produced HTTP 403.

This means that repository ownership and account authorization are not sufficient by themselves.

The token must also permit the specific operation.

For fine-grained personal access tokens, relevant access normally includes:

* Access to the target repository.
* Repository contents write permission.

For classic personal access tokens, the `repo` scope is normally required for private repositories.

The device-flow login avoided the token-scope ambiguity.

---

## Lesson 6: `gh auth status` does not prove that `git push` will work

The following command:

```bash
gh auth status
```

can confirm that GitHub CLI is logged in.

It does not always prove that Git is using the same credentials or that the token can write repository content.

The following command is also required:

```bash
gh auth setup-git
```

This configures Git to use GitHub CLI as the credential helper.

Credential configuration can be inspected with:

```bash
git config --global --list --show-origin
```

The relevant lines were:

```text
credential.https://github.com.helper=
credential.https://github.com.helper=!/usr/bin/gh auth git-credential
```

---

## Lesson 7: No output can indicate success

Several commands produced no terminal output:

```bash
gh auth setup-git
```

and:

```bash
git remote set-url origin ...
```

For these commands, no output normally means successful completion.

Verification should still follow.

For example:

```bash
git remote -v
```

should be run after changing a remote.

---

## Lesson 8: Untracked files are not included automatically

The untracked `CSV_OUTPUT` directories were not included in the push.

Git only pushes committed content.

The sequence:

```bash
git push
```

does not automatically include new untracked files.

To include them, the files must first be added and committed:

```bash
git add CSV_OUTPUT/
git commit -m "Add CSV output results"
git push
```

However, output directories should be reviewed before inclusion. Generated data may be:

* Large.
* Reproducible.
* Temporary.
* Unsuitable for source control.
* Better stored outside Git.

A `.gitignore` rule may be more appropriate:

```gitignore
CSV_OUTPUT/
```

The decision should be based on whether those outputs are required as part of the repository.

---

## Lesson 9: Repository naming and folder naming are independent

The local folder was named:

```text
CC_FIN
```

but its remote repository was configured as:

```text
opencode-FIN
```

Git does not assume that a folder named `CC_FIN` should connect to a repository named `CC_FIN`.

The association is controlled only by the remote URL in:

```text
.git/config
```

Therefore, folder names should never be used as proof of the remote destination.

---

## Lesson 10: Mixed environments can create executable conflicts

On the Windows host, PowerShell found GitHub CLI in:

```text
G:\pinokio\bin\miniconda\Scripts\gh.exe
```

rather than the official installation.

This happened because the Pinokio Miniconda directory appeared earlier in the Windows `PATH`.

The command:

```powershell
Get-Command gh
```

was useful because it showed exactly which executable PowerShell was using.

The command:

```powershell
(Get-Command gh).Source
```

showed the full file path.

When multiple versions exist, the official executable can be called explicitly:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe"
```

A later cleanup of the Windows `PATH` may be appropriate so that the official GitHub CLI is found before the Pinokio version.

---

# 5. Security lessons

## Token handling

A token was pasted into the VM during authentication.

Although the terminal output shown later masked most of the token, authentication tokens should always be treated as secrets.

Recommended precautions:

* Tokens should not be pasted into chat messages.
* Tokens should not be stored in shell history.
* Tokens should not be committed to Git.
* Tokens should be revoked if accidental exposure is suspected.
* Device-flow authentication should be preferred where practical.

The final browser/device-flow authentication was safer and easier to maintain than manual token entry.

---

## Credential storage

GitHub CLI reported storage in the system keyring.

This is preferable to embedding credentials in:

* Remote URLs.
* Shell scripts.
* Git configuration files.
* Environment files.
* Plain-text credential files.

The remote should remain:

```text
https://github.com/nekiee13/CC_FIN.git
```

It should not contain a username, password, or token.

---

# 6. Final working configuration

## Project location

```text
/home/nekiee/CC_FIN
```

## Active branch

```text
main
```

## Correct remote

```text
https://github.com/nekiee13/CC_FIN.git
```

## Tracking relationship

```text
main -> origin/main
```

## GitHub account

```text
nekiee13
```

## Authentication method

GitHub CLI browser device flow with HTTPS Git protocol.

## Successful final push command

```bash
git push -u origin main
```

---

# 7. Recommended routine for future pushes

The following sequence should be used from inside the project directory.

## Check location

```bash
pwd
```

Expected result:

```text
/home/nekiee/CC_FIN
```

## Check repository state

```bash
git status
```

## Check destination

```bash
git remote -v
```

Expected destination:

```text
https://github.com/nekiee13/CC_FIN.git
```

## Review changes

```bash
git diff
```

## Review untracked and modified files

```bash
git status --short
```

## Add intended changes

```bash
git add .
```

## Review staged changes

```bash
git status
```

## Commit

```bash
git commit -m "Describe the changes"
```

## Push

```bash
git push
```

Because the upstream relationship is now configured, `git push` should be sufficient for later updates.

---

# 8. Recovery required for the accidental repository push

The ten commits were also pushed to:

```text
https://github.com/nekiee13/opencode-FIN
```

Whether cleanup is required depends on whether those commits belong there.

Possible responses include:

1. Leave the commits in place when they are harmless or relevant.
2. Revert the commits through normal Git history.
3. Reset the remote branch to an earlier commit and force-push, but only after confirming that no other users depend on the branch.
4. Archive or delete the wrong repository if it is obsolete.

The safest approach is usually a normal revert rather than rewriting shared history.

---

# 9. Core lesson

The central lesson is:

```text
Authentication must be configured inside the environment performing the push, and the remote URL must be verified before every important push.
```

The authentication problem was solved correctly through GitHub CLI device flow. The main process mistake was allowing a successful push before confirming that `origin` pointed to the intended `CC_FIN` repository.

---

## Assistant

The GitHub file-transfer lessons have been inspected and incorporated into the project context.

The retained controls include:

- environment-specific GitHub authentication;
- headless GitHub CLI device-flow login;
- mandatory remote verification before each push;
- branch, repository, and staged-file checks;
- separation of technical push success from task success;
- handling of untracked and generated files;
- credential-helper verification;
- token and secret protection;
- recovery options after an accidental push;
- recommended pre-push and post-change verification sequences.

These controls are relevant to the planned LLM Wiki monorepos and project repositories.

**Ready to continue.**

---

## User

A now we need to start developing 3rd project - Nuclear Quality Assurance Supplier Audit Wiki (NQA-1 Wiki)

GOAL:
Create LLM-Wiki that will enable evaluation of a company quality assurance sytsem evaluation, againsts 10 CFR 50 Appendix B requirements.

Ultimate question:
Does QA system comply to 10 CFR 50 Appendix B requirements, as described in ASME NQA-1.


# LLM-Wiki NQA Supplier Audit - General information

1. Multiple companies will be processed (Enconet, TEKOL, Ekonerg and more) - ref Obsidian Wiki folders
2. All source documentation (raw) will be prepared by user. All documentation will be in either in pdf, md or in HTML format (mostly md format will be used).
3. Some documents are large (100 or more pages - ref. OpenKB project implementation features)
4. Possible languages are Croatian, Slovenian and English.
5. NQA Supplier Audit projects will share top-level Claude.md (schema applicable to all companies) but each company should or may have it's own sub-level Claude.md (specifics related to individual company) - ref. HackerNoon article
6. Because of complexity of Wiki tasks related to NQA Supplier Audit process, extensive interconnections are expected (ref. BrainDB project implementation features)

-----

Let me know when you're ready to continue.

---

## Assistant

The third-project context has been analyzed and incorporated.

The working scope now includes:

- a shared NQA Supplier Audit framework for multiple companies;
- company-specific audit workspaces;
- assessment against **10 CFR Part 50, Appendix B**;
- interpretation and evidence mapping through **ASME NQA-1**;
- PDF, Markdown, and HTML source ingestion;
- large-document processing;
- Croatian, Slovenian, and English content;
- shared top-level `CLAUDE.md` governance;
- optional company-level `CLAUDE.md` extensions;
- dense traceability among criteria, procedures, evidence, findings, and conclusions;
- a final defensible compliance determination for each company.

The central evaluation question has been retained:

> Does the supplier’s quality assurance system comply with 10 CFR Part 50, Appendix B, as interpreted and described through ASME NQA-1?

**Ready to continue.**

---

## User

Export this conversation as markdown file.

---
