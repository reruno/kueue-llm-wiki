---
name: orchestrate
description: Hand a goal to the orchestrator agent, which plans the work and delegates to the analyzer, coder, and reviewer subagents. Use when the user invokes /orchestrate, or asks for a multi-step goal to be owned end to end — investigation, implementation, review, and verification — rather than answered directly.
argument-hint: <goal to deliver>
---

# Orchestrate

This skill delegates a goal to the `orchestrator` agent defined in `.claude/agents/orchestrator.md`. The orchestrator plans the work and delegates to `analyzer` (investigation), `coder` (edits), and `reviewer` (review), then reports back.

## Goal

The user invoked this with: $ARGUMENTS

## How to use this skill

### Step 1 — Check the goal is workable

If `$ARGUMENTS` is empty, ask the user what they want delivered and stop. Do not invent a goal.

If the goal is clear enough to start on, go to step 2. If a single answer would change the whole shape of the work (for example, which of two incompatible designs to build), ask that one question first — the orchestrator can ask too, but resolving it up front avoids a wasted round trip.

### Step 2 — Gather starting context

Do only cheap orientation here; the orchestrator does the real investigation.

- If the goal touches Kueue concepts, invoke the `kueue-wiki` skill first and pass its findings along.
- Note any files, errors, or constraints the user already mentioned in this conversation.

### Step 3 — Delegate to the orchestrator

Call the `Agent` tool with `subagent_type: "orchestrator"` and `run_in_background: false`, so you have the result before replying.

The prompt you pass must be self-contained — the orchestrator does not see this conversation. Include:

- **Goal**: the user's request, verbatim where possible.
- **Context**: relevant conversation history, files already identified, wiki findings, prior attempts and what failed.
- **Constraints**: anything the user ruled in or out, plus the repo rules — `raw/` is immutable, and `wiki/` may only be edited with the user's explicit approval.
- **Definition of done**: what the user will check, and which tests, lint, or build commands should pass.
- **Expected output**: changed files, verification performed, unverified areas, remaining risks.

### Step 4 — Report back

The orchestrator's report is not shown to the user, so relay it yourself:

- What was delivered, and which files changed.
- What verification ran and whether it passed. If something failed or was skipped, say so plainly with the output.
- Open questions the orchestrator raised, and remaining risks.

If the orchestrator stopped to ask a question, put that question to the user directly. When they answer, continue the same orchestrator thread with `SendMessage` rather than starting a fresh `Agent` call, so its context survives.

## Boundaries

- Do not commit, push, or deploy unless the user explicitly asked as part of the goal.
- Do not edit `wiki/`, `wiki/index.md`, or `wiki/log.md` without the user's explicit approval, and never touch `raw/`.
- Do not pass the orchestrator's report through verbatim — filter it for relevance and correctness.
