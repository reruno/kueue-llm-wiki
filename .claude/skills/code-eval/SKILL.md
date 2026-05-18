---
name: code-eval
description: Evaluate the quality of a git diff between two commits. Scores the changes across four domains — Code Style, Buggy Behavior, Comments, and Small Architectural Decisions — then provides actionable recommendations for improvement. Use this skill when user wants to perform code quality evaluation.
argument-hint: <BaseCommit> <HeadCommit>
license: Apache-2.0
metadata:
  copyright: The Kubernetes Authors
---

# Code Evaluation Skill

Evaluate the quality of a git diff between two commits. Scores the changes across four domains — Code Style, Buggy Behavior, Comments, and Small Architectural Decisions — then provides actionable recommendations for improvement.

Use this when user wants to perform code quality evaluation. When user expresses a need for code quality review, but didn't provide the **BaseCommit** and **HeadCommit** arguments, remind user what arguments need to be provided for code evaluation

## Arguments

The user invoked this with: $ARGUMENTS

Parse two positional arguments from `$ARGUMENTS`:
- **BaseCommit** — the base (older) commit
- **HeadCommit** — the head (newer) commit

## Principles

- Ground every deduction in a specific line or pattern from the diff. No vague criticism.
- Do not penalize stylistic choices that are consistent with the surrounding code, even if you personally prefer something else.
- Do not invent bugs that aren't there. If the code looks correct, say so.
- Reward simplicity. If the diff is clean and well-structured, say so explicitly.
- Severity matters: backwards-compatibility violations and logic errors on the hot path are more serious than naming nits. Reflect this in point deductions.

## Step 1 — Retrieve the diff

Run:
```
git diff <BaseCommit> <HeadCommit>
```

Read the full output. This is the **Diff Code** you will evaluate.

Also run:
```
git diff <BaseCommit> <HeadCommit> --stat
```

to get a high-level overview of changed files.

## Step 2 — Understand context

For each changed file in the diff, read enough of the surrounding code (unchanged lines, nearby functions, imports) to understand:
- The existing code style and naming conventions
- Util/helper functions already available in the package or nearby packages
- The overall structure and architecture of the file
- What patterns exist for similar operations (e.g. how existing builder methods are named)

Use `git show <BaseCommit>:<filepath>` or read the file at HEAD if it gives better context.

Pay particular attention to:
- How existing functions/methods in the same package are named (builder pattern vs verb-noun, etc.)
- Whether shared helper logic already exists for the same operation across other types/adapters
- Log verbosity conventions (what V-level is used for recurring vs lifecycle events)
- Whether any deleted code might be needed during a rolling upgrade or version skew

## Step 3 — Evaluate across domains

Score the Diff Code on each domain below. Be strict but fair. Every point deduction must be noted so the user understands what happened.

Each domain file is independent and can be checked in parallel with the others. When reviewing a Diff Code, spawn all relevant domains as concurrent agents rather than running them sequentially. Domain contains defined rules, and each agent must check for violations of these rules. Also each finding must be clasified as high, medium, or low finding. 

Domains: 
| Skill | Max score |
|---|---|
| @architectural_decisions.md | 20 |
| @code_style.md | 40 |
| @buggy_behavior.md | 20 |
| @comments.md | 5 |



## Step 4 — Produce the report

Output the evaluation in this exact structure (Domains and score are example, there could be more domains added in the future):

```
## Code Evaluation Report

**Commits**: <BaseCommit>..<HeadCommit>
**Files changed**: (from --stat output)

---

### Domain: Code Style
**Score**: X/<num of points for this domain defined in Step 3>
**Findings**: (bullet list of specific observations, in accordance with the specified rules for findings)
  - <High/Medium/Low> | -x pt | <Finding Title>: <Explanation>

### Domain: Buggy Behavior
**Score**: X/<num of points for this domain defined in Step 3>
**Findings**: (bullet list of specific observations, in accordance with the specified rules for findings)
  - No findings

### Domain: Comments
**Score**: X/<num of points for this domain defined in Step 3>
**Findings**: (bullet list of specific observations, in accordance with the specified rules for findings)
  - No findings

### Domain: Architectural Decisions
**Score**: X/<num of points for this domain defined in Step 3>
**Findings**: (bullet list of specific observations, in accordance with the specified rules for findings)
  - <High/Medium/Low> | -x pt | <Finding Title>: <Explanation>

---

### Final Score: 
X% / 100%
<Points after deduction>pt / <Sum of all max points>pt

---

## Recommendations

(One recommendation per issue found. Only include recommendations where the score was reduced. Each recommendation must have all three sections below.)

### Recommendation N: <short title>

**Problem**: Describe the specific issue in the diff.
**Reason**: Explain why this is a problem — what goes wrong or degrades over time.
**Solution**: Give a concrete, actionable fix. Where possible, show a before/after code snippet.
```

Rules for findings: assume max score is already achieved, when you find violation of the rules, deduct points from the score and denote it. Points deduction depends on severity of a violation. Possible severities: high, medium, low. High=15pt, Medium=7pt, Low=3pt. Report format rules MUST NOT be broken, ensure that report abide by defined formating rules. Remember code evaluation MUST promote these principles: Maintainability, Simplicity, Backward Compatibility. 

