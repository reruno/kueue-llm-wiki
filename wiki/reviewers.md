
# Reviewers and the Kueue Review Process

**Summary**: Overview of Kueue's reviewer roster, OWNERS structure, Prow approval workflow, and how individual reviewers divide responsibility. Use this page as the entry point when navigating to a specific reviewer profile or to [[code-quality|the project's shared code quality bar]].

**Sources**: `raw/kueue/OWNERS`, `raw/kueue/OWNERS_ALIASES`, `raw/kueue/CONTRIBUTING.md`, `raw/kueue/AGENTS.md`, and analysis of PR review comments across `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-12

---

## OWNERS structure

Kueue uses Kubernetes-style OWNERS files. The root `OWNERS` references aliases in `OWNERS_ALIASES`, with **path-filter overrides** for sensitive areas.

### Top-level approvers and reviewers

```
kueue-approvers:        gabesaba, mimowo, tenzen-y
kueue-reviewers:        gabesaba, mbobrovskyi, mimowo, pbundyra, tenzen-y,
                        kannon92, pajakd, olekzabl, kshalot, sohankunkerkar
```

Approval requires one approver from `kueue-approvers`. `/lgtm` can come from any reviewer.

### Path-filter overrides

| Path pattern | Approver alias | Notes |
|---|---|---|
| `go.(mod\|sum)`, `package(-lock)?.json`, `vendor/...`, `Makefile-deps.mk` | `dependency-approvers` (mbobrovskyi, pbundyra) | Dependency bumps |
| `*_test.go`, `Makefile-(verify\|test).mk`, `.golangci*.yaml` | `test-approvers` (mbobrovskyi, pbundyra) | Test infrastructure and lint config |
| `AGENTS.md` | `agent-approvers` (amy) | Experimental agent instructions |

This is why dependency-bump and test-infrastructure PRs route to mbobrovskyi or PBundyra first, even when the rest of the diff is in core scheduler code.

### Emeritus approvers

Listed in the root OWNERS as `emeritus_approvers` and no longer active: `ahg-g`, `alculquicondor`, `denkensk`, `kerthcet`. Their CHANGELOG history is still useful context for design decisions made before 0.10.

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
| @gabesaba | Scheduler internals, preemption correctness, performance, MultiKueue edge cases | [[reviewer-gabesaba]] |
| @mbobrovskyi | Test infrastructure, dependency bumps, SSA migration, code consolidation | [[reviewer-mbobrovskyi]] |
| @PBundyra | API design, Kubernetes versioning rules, Concurrent Admission KEP, fair sharing | [[reviewer-pbundyra]] |

Other active reviewers without dedicated profile pages:

- **@kannon92** — Integrations (especially Kubeflow, RayJob), surface-level API review
- **@pajakd** — TAS, scheduler details
- **@olekzabl** — Workload lifecycle
- **@kshalot** — Performance and test reliability
- **@sohankunkerkar** — Integrations and documentation

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
