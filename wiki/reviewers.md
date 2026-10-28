# Reviewers and the Kueue Review Process

**Summary**: Overview of Kueue's reviewer roster, OWNERS structure, Prow approval workflow, and how individual reviewers divide responsibility. Use this page as the entry point when navigating to a specific reviewer profile or to [[code-quality|the project's shared code quality bar]].

**Sources**: `raw/kueue/OWNERS`, `raw/kueue/OWNERS_ALIASES`, `raw/kueue/CONTRIBUTING.md`, `raw/kueue/AGENTS.md`, and analysis of PR review comments across `raw/github/kubernetes-sigs__kueue/`; pr-16505.md, pr-16850.md, pr-16739.md, pr-17055.md, pr-14150.md; pr-17326.md, pr-17284.md, pr-17348.md, pr-17162.md, pr-17487.md, `raw/kueue/cmd/experimental/skills/OWNERS`, `raw/kueue/cmd/experimental/skills/reviewer/multikueue/SKILL.md` (OWNERS state re-read at kueue@3bbb8cce4).

**Last updated**: 2026-10-28

---

## OWNERS structure

Kueue uses Kubernetes-style OWNERS files. The root `OWNERS` references aliases in `OWNERS_ALIASES`, with **path-filter overrides** for sensitive areas.

### Top-level approvers and reviewers

```
kueue-approvers:        mimowo, sohankunkerkar, tenzen-y
kueue-reviewers:        mbobrovskyi, mimowo, pbundyra, tenzen-y, kannon92,
                        pajakd, olekzabl, kshalot, sohankunkerkar, amy, j-skiba
```

Approval requires one approver from `kueue-approvers`. `/lgtm` can come from any reviewer.

**Correction (2026-10-21):** this block was stale. gabesaba stepped down as approver on 2026-06-01 (#11834) and is listed under `emeritus_approvers`; sohankunkerkar became a full approver on 2026-08-07 (#13927); amy joined `kueue-reviewers` on 2026-06-23 (#12423); j-skiba joined on 2026-10-16 (pr-17326) (source: `raw/kueue/OWNERS`, `raw/kueue/OWNERS_ALIASES`, `git log` of both files).

**Becoming a reviewer.** Self-nomination is a PR that adds you to `kueue-reviewers`, with evidence for the checklist used in pr-17326: org member for at least 3 months, primary reviewer for at least 5 PRs, and at least 20 substantial PRs reviewed or merged, plus a summary of the areas you cover. It is assigned to the approvers for `/lgtm` and `/approve` (source: pr-17326.md). j-skiba covers TAS node-failure handling, inadmissible-workload observability (KEP-10852), scheduler/quota internals including Dynamic Quota Orchestration, and kueue-populator.

### Path-filter overrides

| Path pattern | Approver alias | Notes |
|---|---|---|
| `go.(mod\|sum)`, `vendor/...`, `hack/make/deps.mk` | `dependency-approvers` (mbobrovskyi, pbundyra) | Dependency bumps |
| `package(-lock)?.json` | `dependency-approvers` or `release-team` | npm dependencies (KueueViz, site) |
| `*_test.go`, `hack/make/(verify\|test).mk`, `.golangci*.yaml` | `test-approvers` (mbobrovskyi, olekzabl, pbundyra) | Test infrastructure and lint config |
| `AGENTS.md`, `cmd/experimental/skills/` (own OWNERS file) | `agent-approvers` / `agent-reviewers` (amy, kannon92, pbundyra) | Agent instructions, skills and the skillsaw config (`cmd/experimental/skills/.skillsaw.yaml`, moved there by pr-17487) |
| `Makefile`, `README.md`, `INSTALL.md`, `Chart.yaml`, `SECURITY-INSIGHTS.yaml` | `release-team` (mbobrovskyi, Singularity23x0) | Release-managed files |
| `Dockerfile`, `.dockerignore` / `netlify.toml` | `infra-approvers` / `hugo-approvers` (mbobrovskyi) | Images / website build |

This is why dependency-bump and test-infrastructure PRs route to mbobrovskyi or PBundyra first, even when the rest of the diff is in core scheduler code.

### Emeritus approvers

Listed in the root OWNERS as `emeritus_approvers` and no longer active: `ahg-g`, `alculquicondor`, `denkensk`, `gabesaba`, `kerthcet`. Their CHANGELOG history is still useful context for design decisions made before 0.10.

### Security and release

- `SECURITY_CONTACTS`: `mimowo`, `tenzen-y`
- Release issue assignees (per `.github/ISSUE_TEMPLATE/NEW_RELEASE.md`): `mimowo`, `tenzen-y`

---

## Reviewer profiles

Detailed profiles for the most active approvers/reviewers:

| Reviewer | Focus area | Profile |
|---|---|---|
| @mimowo | TAS, MultiKueue, workload eviction, cache/scheduler internals, RayJob, ProvisioningRequest; the hard blocker on naming, tests, upgrade safety | [[reviewer-mimowo]] |
| @tenzen-y | Release management & cherry-picks, TAS annotation semantics, client-go plumbing | [[reviewer-tenzen-y]] |
| @gabesaba (emeritus approver since 2026-06) | Scheduler internals, preemption correctness, performance, MultiKueue edge cases | [[reviewer-gabesaba]] |
| @mbobrovskyi | Test infrastructure, dependency bumps, SSA migration, code consolidation | [[reviewer-mbobrovskyi]] |
| @PBundyra | API design, Kubernetes versioning rules, Concurrent Admission KEP, fair sharing | [[reviewer-pbundyra]] |

Other active reviewers without dedicated profile pages:

- **@kannon92** — Integrations (especially Kubeflow, RayJob), surface-level API review
- **@pajakd** — TAS, scheduler details
- **@olekzabl** — Workload lifecycle
- **@kshalot** — Performance and test reliability
- **@sohankunkerkar** — approver since 2026-08; integrations, documentation, and the per-LocalQueue pending-metric and preemption performance work in this window (pr-17414, pr-17448)
- **@j-skiba** — reviewer since 2026-10 (pr-17326); TAS node failure, unadmitted-workload observability, DQO, kueue-populator
- **@danylott** — primary `/lgtm` on KueueViz PRs in this window; verifies UI changes locally and asks for release notes that warn about behaviour changes, e.g. that an invalid `KUEUEVIZ_AUTH_MODE` now fails startup (source: pr-17143.md, pr-17235.md, pr-17088.md)
- **@henry3260** — frequent `/lgtm` on kueuectl and KueueViz fixes. Asks for tests that would fail on the old code, for example asserting a slice is non-nil, or putting a Workload on page 2 when testing pagination (source: pr-16739.md, pr-16850.md, pr-17055.md)

**CI gotcha.** If Prow shows obsolete required jobs as blockers (for example after a test-infra job change that was reverted), maintainers ask the author to push a no-op commit to retrigger the current job set (source: pr-16850.md, pr-16739.md).

---

## Agent instructions and review skills

- `AGENTS.md` is the single agent-instruction file; `CLAUDE.md`, which only referenced it, was removed (pr-17284). The PR text and AI summary describe a contribution workflow added to `AGENTS.md`, but the merged commit only deletes `CLAUDE.md`; the workflow is in the `kueue-pr-issue-workflow` skill that `AGENTS.md` links, and a separate PR to add it to `AGENTS.md` is still open (pr-17361) (source: `git show` of the merge commit in raw/kueue).
- Agents must start each reply with `_Kueue Development (context canary, see AGENTS.md)_`; if it disappears, the agent has probably lost `AGENTS.md` from its context (pr-17348).
- Reviewer skills live in `cmd/experimental/skills/reviewer/`. New in this window: `multikueue` — minimise reads from remote worker clusters, e.g. requeue from manager-cluster Workloads instead of listing on workers, keeping only reads needed for correctness (pr-17162). See [[code-quality]].

---

## Approval workflow (Prow commands)

Kueue uses [Prow](https://prow.k8s.io/) for PR automation. The standard sequence:

1. **`/ok-to-test`** — required for external contributors before CI runs. Usually issued by [[reviewer-mbobrovskyi|@mbobrovskyi]] or another reviewer who recognizes the author.
2. **`/lgtm`** — any reviewer signals the diff looks correct. Adds the `lgtm` label.
3. **`/approve`** — an approver in `kueue-approvers` (or relevant path-filter alias) approves the merge.
4. **`/cherrypick release-0.X`** — schedules a cherry-pick once the PR merges.

### Other commands seen frequently

| Command | Used by | Meaning |
|---|---|---|
| `/hold` | Any reviewer | Blocks merge regardless of approvals; used when investigation is pending |
| `/unhold` | The person who placed the hold | Releases the hold |
| `/assign @user` | Any reviewer | Routes design decisions to a specific approver |
| `/release-note-edit` | Approver | Tightens user-facing release-note text inline |
| `/retest` | Author or reviewer | Re-runs failing CI jobs |
| `/lifecycle frozen` | Approver | Prevents the bot from staling out a long-running PR |
| `/set-release-note` | `release-team` or `kueue-approvers` (since pr-16505.md) | Replaces the release note. It takes **everything after the command** in that comment as the note, so put `/kind`, `/cherrypick` and other commands in a separate comment (source: pr-16850.md) |
| `/hold cancel` or `/unhold` | Hold owner | Both release a hold; `/remove hold` does nothing (source: pr-14150.md) |

### Conditional approvals

A common pattern: an approver gives `/lgtm` without `/approve` when they're satisfied with the code but want a domain expert (or top approver) to do the final approve. From [[reviewer-tenzen-y|tenzen-y]] on pr-10677:

```
Looks awesome!
/approve
Leaving lgtm @mimowo @mwysokin
```

This splits the approval into two halves: the architectural sign-off (from a top approver) and the line-by-line correctness check (from a domain reviewer).

---

## Division of responsibility

The five most active reviewers have observable, non-overlapping focus areas. This shapes who you should expect to comment on which kinds of PRs:

| Concern | Primary reviewer |
|---|---|
| Naming, log levels, test coverage details, comment accuracy, upgrade-safety code retention | [[reviewer-mimowo|@mimowo]] |
| Release-branch hygiene, cherry-pick decisions, release notes that match user-visible behavior, annotation semantics in TAS | [[reviewer-tenzen-y|@tenzen-y]] |
| Scheduler invariants, preemption loops, cache coherency, performance regressions in event handlers | [[reviewer-gabesaba|@gabesaba]] |
| Duplication across code paths, multi-concern PRs, integration-test gaps in metrics/observability, Go idiom suggestions, dependency bumps | [[reviewer-mbobrovskyi|@mbobrovskyi]] |
| API field markers and JSON tags, deprecation timing relative to API version promotion, KEP-driven design discussion | [[reviewer-pbundyra|@PBundyra]] |

When a PR lands in someone else's primary area, they typically defer rather than re-litigate. For example, gabesaba rarely flags naming nits — those belong to mimowo. mimowo rarely re-derives a scheduler invariant from scratch — that's gabesaba's lane.

---

## How to get a PR reviewed quickly

Patterns observed across approved PRs:

1. **One concern per PR**: cleanup + bugfix gets sent back; split first
2. **Squash before final approval**: a single clean commit is required (mimowo will ask for `git push --force` after each iteration)
3. **Integration test included from the first push**: missing tests are the single most common cause of multi-round review
4. **Feature gate off-state tested**: if your PR adds a feature gate, also test with it disabled
5. **Release note in PR template**: tenzen-y rewrites missing/vague ones, but a good first draft saves a round
6. **TODO + GitHub issue for any code kept for backwards compatibility**: if you must keep a code path for two releases, add the TODO with the exact target version and link the cleanup issue
7. **For API changes, align the KEP first**: PBundyra will `/hold` for design discussion otherwise

For the shared technical quality bar these reviewers enforce, see [[code-quality]].

---

## Related pages

- [[code-quality]]
- [[reviewer-mimowo]]
- [[reviewer-tenzen-y]]
- [[reviewer-gabesaba]]
- [[reviewer-mbobrovskyi]]
- [[reviewer-pbundyra]]
- [[release-process]]
- [[testing]]
- [[testing-integration]]
- [[feature-gates]]
