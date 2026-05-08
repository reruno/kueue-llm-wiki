---
name: kueue-wiki
description: Augment any question or task with context from the Kueue wiki knowledge base. Use this skill whenever the user asks anything about Kueue — scheduling, admission, preemption, quotas, integrations, architecture, APIs, or any related topic. Also trigger when the user is debugging a Kueue problem, designing a feature, or reviewing Kueue code and would benefit from wiki context. The skill reads the wiki index, identifies the most relevant pages, and synthesizes a grounded answer with citations. Always use this when the user prompt mentions Kueue, ClusterQueue, LocalQueue, Workload, cohort, preemption, admission checks, ResourceFlavor, or any Kueue concept.
argument-hint: <user prompt or question>
---

# Kueue Wiki Context Skill

This skill enriches any Kueue-related question or task by pulling in relevant wiki pages before answering. The wiki lives at `wiki/` under the project root (`/home/user1/Projects/kueue-llm-wiki/wiki/`).

## User prompt

The user invoked this with: $ARGUMENTS

## How to use this skill

### Step 1 — Read the index

Read `wiki/index.md` to get the full table of contents and one-line descriptions for every page.

### Step 2 — Identify relevant pages

Based on the user's prompt and the index descriptions, identify which pages are most relevant. Be generous — if a concept is related (even indirectly), include it. Typical queries touch 2-5 pages; complex ones may need more.

### Step 3 — Read the relevant pages

Read each identified page in full. Look for:
- Direct answers to the user's question
- Related concepts that add important context
- Links to other pages (`[[page-name]]`) that may be worth following if they add depth

### Step 4 — Synthesize and answer

Answer the user's prompt using what you found. Structure your response to address their specific question directly. Cite the wiki pages you used, e.g. `(wiki: admission.md)`.

If the wiki doesn't cover something the user needs, say so explicitly rather than guessing, and suggest what raw sources might have the answer.

### Step 5 — Offer to save new knowledge

If your answer contains a non-obvious insight that isn't already well-captured in the wiki, offer to create or update a wiki page for it. This keeps the knowledge base compounding.

## Principles

- Ground every factual claim in a wiki page. Don't add knowledge from general training that contradicts what the wiki says.
- If two wiki pages disagree, surface the contradiction rather than silently picking one.
- Keep the answer focused on the user's actual question — don't dump entire page contents.
- If the user's prompt is a task (not just a question), use the wiki context to inform your approach and mention which concepts are relevant to the implementation.
