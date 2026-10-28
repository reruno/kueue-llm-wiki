# Release process

**Summary**: Kueue cuts a minor release roughly every eight weeks (recent minors: v0.18, v0.19, v0.20) and keeps patching the two previous minors. Patch releases pick fixes into release branches. Release artifacts include container images, a manifest bundle, Helm charts, an SBOM and OpenVEX data; SLSA attestations and artifact signing are still open requests ([[issue-1466]], [[issue-1477]]).

**Sources**: `raw/github/kubernetes-sigs__kueue/`; pr-14150.md, pr-16442.md, pr-16917.md, pr-16916.md, pr-16440.md, pr-16439.md, pr-16456.md, pr-16476.md, pr-16502.md, pr-16505.md, pr-16690.md, pr-16711.md, pr-16714.md, pr-16850.md; `raw/kueue/RELEASE.md`, `raw/kueue/release-timelines/`, `raw/kueue/.github/ISSUE_TEMPLATE/NEW_RELEASE.md`, `raw/kueue/CHANGELOG/CHANGELOG-0.20.md`, `CHANGELOG-0.19.md`, `CHANGELOG-0.18.md`; 2026-10-21 batch: pr-17258.md, pr-17259.md, pr-17261.md, pr-17262.md, issue-16938.md, issue-17026.md, pr-17264.md, pr-17265.md, issue-17256.md, pr-17266.md, pr-17298.md, pr-17299.md, pr-17116.md, pr-17129.md, pr-17130.md, pr-17137.md, issue-17113.md, pr-17126.md, pr-17227.md, pr-16340.md, pr-17295.md, pr-17296.md, pr-17148.md; 2026-10-28 batch: pr-17613.md, pr-17614.md, pr-17615.md, pr-17616.md, pr-17200.md, issue-17193.md, pr-17566.md, pr-17567.md, pr-17577.md, pr-17592.md, pr-17593.md, pr-17607.md, issue-17597.md, pr-17625.md, pr-17626.md, pr-17101.md, issue-17085.md, pr-17606.md, pr-17117.md, pr-17807.md, pr-17842.md, issue-17813.md, pr-17849.md, pr-17850.md, pr-17729.md, pr-17736.md, issue-17728.md, pr-17632.md, pr-17591.md, pr-17603.md, pr-17604.md, pr-13307.md; `raw/kueue/hack/cherry_pick_pull.sh`, `raw/kueue/hack/releasing/set_release_note.py`, `raw/kueue/.github/workflows/sync-dependabot.yaml`, `raw/kueue/.github/dependabot.yml`, `raw/kueue/Makefile` (`prepare-release-branch`), `raw/kueue/hack/make/test.mk` (CHANGELOGs re-read at kueue@966f00d21).

**Last updated**: 2026-10-28

---

## Release cycle and milestones

From `RELEASE.md` as restructured by pr-14150.md (merged 2026-08-11, fixes #14147):

- One minor release about **every two months**, so every second Kueue minor lines up with a Kubernetes minor. The "aligned" Kueue minor ships about a month after the Kubernetes release, once its first patch release exists. A release may slip (the aim is no more than two weeks), and a slip does not move the next minor's target date.
- Each minor normally uses an **eight-week cycle**, with the public release planned for the middle of W8:

| Milestone | Timing | Meaning |
|---|---|---|
| D1 Planning opens | W1–W2 | Scope discussed at WG Batch, a planning meeting, or asynchronously in the issue |
| D2 Larger KEP review | W1–W4 | Larger KEPs should become visible early |
| D3 Scope cooldown | W5 | Maintainers fix the scope in terms of larger KEPs; small KEPs/KEP updates stay eligible until D4 |
| D4 KEP publication | W6 | Accepted KEPs published |
| C1 Code cooldown | W6 | All big feature PRs open, substantially complete and reviewable |
| C2 Code freeze | W7 | Feature PRs merged or deferred; only bug fixes or approved exceptions |
| R Public release | W8 | Release published |

- **Exceptions** are agreed between maintainers and the feature owner in a dedicated Slack group, and the decision is recorded in the feature tracking issue. Maintainers decide scope (based on their review capacity), approve feature PRs and exceptions, and may update the tentative schedule. The release team runs the publication.
- **Tentative timelines** live in `release-timelines/`: v0.20 had scope finalization on 4 Sep, code freeze on 17 Sep and release on 24 Sep (2026); v0.21 has scope on 5 Nov, freeze on 19 Nov and release on 25 Nov; v0.22 treats W3–W4 (late December) as a holiday window, with scope on 8 Jan, freeze on 21 Jan and release on 28 Jan. v0.20.0 was prepared on 2026-09-30, about a week after its tentative date (source: pr-16442.md).
- **Patch releases**: while working on minor N, the project keeps maintaining N-1 and N-2. Their release branches are tested by CI.

## Branching

Each minor version has a `release-0.X` branch. `main` is the trunk for the next minor. Patch releases go out from the release branch.

Representative release tracking issues:

- v0.4.1 ([[issue-1056]]), v0.4.2 ([[issue-1200]]).
- v0.5.0 ([[issue-1256]]), v0.5.1 ([[issue-1368]]), v0.5.2 ([[issue-1539]]).
- v0.15.8 ([[issue-10054]]), v0.16.5 ([[issue-10053]]), v0.16.6 ([[issue-10476]]), v0.17.1 ([[issue-10477]]).
- v0.16.7 ([[issue-10706]]), v0.17.2 ([[issue-10705]]) — paired patch releases on 2026-04-30 carrying CQ-finalizer fix ([[pr-10821]]), TAS stateWithLeader / NodeHotSwap fixes, FailureRecovery terminal-pod handling ([[pr-10853]]); the Helm/KueueViz fixes (#10977 / #10978 / #10979) and the `FinishOrphanedWorkloads` Alpha downgrade ([[pr-11010]]) followed in v0.16.8 / v0.17.3.
- v0.16.9 ([[issue-11360]]), v0.17.4 ([[issue-11359]]) — paired patch releases carrying the MultiKueue connection-health fixes (per-cluster reconcile lock [[pr-11332]]/[[pr-11333]]; exponential watch-establish timeout [[pr-11328]]/[[pr-11329]]), the MultiKueue AllAtOnce eviction-race fixes ([[pr-11472]]/[[pr-11473]] and [[pr-11507]]/[[pr-11508]]), the TAS multi-PodSet pod-count fix ([[pr-11326]]/[[pr-11331]]), the finished-Workload GC finalizer fix ([[pr-11307]]/[[pr-11308]]), and the scheduler `preemptionExpectations` race fix ([[pr-11648]]/[[pr-11647]]).
- v0.18 plan ([[issue-10261]] — "☂️ Release 0.18 plan" umbrella issue); v0.18.0 release tracking ([[issue-10861]]).

## v0.18.0 highlights (released 2026-05; RC1 on 2026-05-06)

From the changelog in [[issue-10861]]:

**Action required before upgrading**:

- Alpha `RejectUpdatesToCQWithInvalidOnFlavors` feature gate (off by default). When enabling it, fix any invalid `AdmissionCheckStrategy.OnFlavors` references first (#10384).
- The `evicted_workloads_once_total` metric's `detailed_reason` label was renamed to `underlying_cause` for consistency. Migrate dashboards and alerts.

**New features**:

- `quotaCheckStrategy` configuration for [[cluster-queue]] (#9808) — new `IgnoreUndeclared` mode admits Workloads that ask for resources the CQ does not list.
- Concurrent Admission introduced as an Alpha feature (#10610) — see [[concurrent-admission]].
- LWS `nodeSelector` mutability while running (#10275); `queue-name` mutable on idle LWS (#4932) — see [[integration-leaderworkerset]].
- `workload_eviction_latency_seconds` metric (#10323) — see [[metrics]].
- Improved Retry-state AdmissionCheck eviction message (#10623).
- Aggregate Kueue read-only ClusterRoles into the `view` ClusterRole (#10482).
- Stable graduations: `MultiKueueRedoAdmissionOnEvictionInWorker` (#10695), `MultiKueueWaitForWorkloadAdmitted` (#10656), `SkipFinalizersForPodsSuspendedByParent` (#10645).

**Notable bug fixes** (selected — see [[feature-gates]], [[topology-aware-scheduling]], [[fair-sharing]], [[multikueue]] for details):

- FailureRecovery: force-delete Failed/Succeeded pods on unreachable nodes ([[pr-10853]]).
- FairSharing nil-pointer panic on cohort-less CQs ([[pr-10891]]).
- CQ finalizer race after admission failure ([[pr-10821]]).
- TAS `stateWithLeader` over-estimation (#10783, cherry-pick [[pr-10841]]); empty `count=0` PodSets infinite loop (#10478); NodeHotSwap "late pods" pollution (#10760).
- Cohort subtree-quota refresh on cohort deletion ([[pr-10797]]).
- Cohort CPU metrics in CPU units (not milli) ([[pr-10747]]).
- MultiKueue: workload after eviction-on-worker incorrectly marked Admitted (#9670); deferred dispatch when other AdmissionChecks pending (#9866).
- TrainJob webhook no longer patches the TrainingRuntime ([[pr-10829]]).
- Multi-arch image builds for importer/populator/kueueviz-backend (#10775).
- Helm probe periodSeconds bug (#10978); FlowSchema fullname template (#10979); KueueViz plural workloadpriorityclasses (#10977).
- `FinishOrphanedWorkloads` downgraded to Alpha to fix the "Workloads marked Finished immediately after creation" regression ([[pr-11010]], [[issue-10901]]); requeue guard added ([[pr-11014]]).

## Release automation

### The release issue checklist (ChatOps)

A release is tracked by an issue opened from the **New Release** template (`.github/ISSUE_TEMPLATE/NEW_RELEASE.md`). The steps run as ChatOps commands on that issue: `/sync-release-notes`, optional `/create-release-candidate` (minor/major), `/create-release-branch`, `/tag-release`, `/create-draft-release` (changelog, artifacts, OpenVEX, SBOM), `/wait-for-images`, `/wait-for-prod-images`, `/publish-release`, `/update-krew-index`, `/merge-main-into-website`, `/create-devel-tag` and `/create-milestone`. Local scripts remain for PRs that need a personal fork: `prepare_pull.sh --target release|main`, `promote_pull.sh`, `milestone_pull.sh`, `ci_pull.sh`. OWNERS must LGTM the release proposal: at least two for a minor or major release, one for a patch.

Changes in this window:

- `/update-krew-index` submits the krew plugin release for the latest published release (source: pr-16476.md, fixes #16475).
- `/create-milestone` creates the next minor's milestone after a major or minor release. It skips milestones that already exist and rejects patch versions (source: pr-16502.md). `milestone_pull.sh` therefore no longer creates the milestone by default: release managers run it from forks without upstream write access, which returned 404. Set `CREATE_MILESTONE` to opt in; `SKIP_MILESTONE` was removed (source: pr-16714.md, fixes #16454).
- A successful ChatOps command ticks its own checklist item, matched by a `<!-- step:<command> -->` marker. Only the `Report Success` steps pass `mark-done`, so a failed command leaves its item unchecked (source: pr-16711.md, fixes #13359).
- The release-tag action distinguishes "no release" from a lookup error (one GraphQL query for published and draft releases) and stops on errors. It builds the replacement annotated tag locally and updates the remote with `--force-with-lease` instead of deleting the remote tag first. Before, a failure in between could leave a draft release without its tag (source: pr-16690.md, fixes #13501).
- **Release commands run only on release issues.** The `authorize` job of `.github/workflows/release-utils.yml` now requires the `area/release` label, so a release command quoted on another issue no longer posts `❌ Invalid issue title` or touches release logs; every downstream job depends on `authorize` (source: pr-17265.md, fixes issue-17256). The authorize step checks out only `.github` and `hack/releasing` at the triggering commit, cutting about 10 s per command (pr-17126).
- **ChatOps log ordering.** The latest run of each command is shown at the top of the chatops section, under the release notes; re-running a command archives its previous entry under History (source: pr-17266.md; backports pr-17298, pr-17299).
- **Checklist order.** `NEW_RELEASE.md` makes `/wait-for-images` a prerequisite of both `/create-draft-release` and image/Helm-chart promotion, which can then run in parallel (source: pr-17264.md).
- **Cancelling a manual submission stops the script.** `prepare_pull.sh`, `promote_pull.sh` and `ci_pull.sh` printed `Aborting.` but continued to look up PRs and edit the release issue; they now `exit 1` (source: pr-17116.md; backports pr-17129, pr-17130). Unit tests under `hack/releasing/*_test.py` run in `make verify`.
- **release-notes tool v0.22.0.** `sync-notes.sh` no longer passes `--required-author=""`, which newer `kubernetes/release` versions reject with `unknown flag` (source: pr-17137.md, fixes issue-17113).
- Members of `kueue-approvers` (not only `release-team`) may use `/set-release-note` (source: pr-16505.md, fixes #16131).
- **`/set-release-note` parsing (2026-10-22).** The old gotcha (everything after the command, including `/kind bug`, became the note; pr-16850) is fixed. `hack/releasing/set_release_note.py` now takes the text after the **last** line that is exactly `/set-release-note` (case-insensitive, alone on its line), up to the next line that is a known Prow command or any `/remove-*`. Other lines starting with `/` stay in the note. The command may now follow other commands or text in the same comment; the workflow triggers when a line starts with `/set-release-note`. It is rejected when combined with `/release-note-edit` or `/release-note-none`, when the note is empty, or when the note contains a fenced code block (source: pr-17101.md, fixes issue-17085). The success comment now echoes the note that was set in a `release-note` block, written via `--success-comment-file` and posted with `--body-file`, so the author sees what was kept (source: pr-17606.md).
- **Manual dry runs leave the release issue alone.** With `DRY_RUN`, `prepare_pull.sh` and `promote_pull.sh` used to skip pushes and PR creation but still look up matching PRs and edit the release issue body. Submission, existing-PR lookup and issue updates now sit together inside the non-dry-run block. `prepare_pull.sh --target all` still continues to the main target after a dry-run release target. `ci_pull.sh` already exited early. Covered by the table in `hack/releasing/manual_release_submission_test.py` (45 subcases), which `make verify` runs (source: pr-17117.md, split from #16935).
- **Release-branch README links point at versioned docs.** `make prepare-release-branch` now rewrites `https://kueue.sigs.k8s.io/docs/...` (and any older `/v0.X/docs/...`) links in `README.md` to `/$(DOCS_VERSION)/docs/...`. `DOCS_VERSION` is derived from `RELEASE_BRANCH` (`release-0.20` → `v0.20`), and the rewrite is skipped when `RELEASE_BRANCH=main`. Anchors and subpaths are kept; non-doc links such as `/community/` are untouched (source: pr-17842.md, fixes issue-17813; picked to release-0.20/0.19 as pr-17849/pr-17850). Follow-up to the README rewrite (pr-17718, see [[kueue-overview]]).

### Versioned docs

The site at kueue.sigs.k8s.io publishes from the `website` branch, which tracks `main`. Docs are versioned **by path in one deploy**: development docs are under `site/content/<locale>/docs` (`/docs/`), and each release is a frozen copy under `site/content/<locale>/v0.X/docs` (`/v0.X/docs/`), chosen from a header dropdown. The dropdown keeps `main` plus the current and previous release. The `main`-update PR from `prepare_pull.sh` runs `hack/releasing/snapshot-docs.py`. It copies each locale's docs from the release branch, rewrites `/docs/` links, prunes old snapshots and prepends a `[[params.versions]]` entry in `site/hugo.toml`. Patch releases re-freeze the existing snapshot (source: `raw/kueue/RELEASE.md`, `NEW_RELEASE.md`; updated by pr-16456.md).

### The cherry-pick script (`hack/cherry_pick_pull.sh`)

Manual cherry-picks (when the bot's `/cherry-pick` fails) use `hack/cherry_pick_pull.sh`. Since pr-17200 (merged 2026-10-21, fixes issue-17193) it applies each PR as **one squashed commit**. It used to replay every commit with `git am -3`, so a large PR rewritten across many review rounds hit the same conflict once per commit (source: pr-17200.md; raw/kueue/hack/cherry_pick_pull.sh):

1. `gh pr view <pr> --repo=<org>/<name> --json title,baseRefOid,author,commits,body,labels`. The script then fetches `pull/<pr>/head` and unshallows the clone if needed, because a shallow clone truncates `git log` and breaks `merge-base`.
2. `PR_BASE = merge-base(PR_HEAD, baseRefOid)` uses the PR's **own** base commit, not `main`. A PR based on a release branch would otherwise pull in that branch's whole history.
3. `git commit-tree PR_HEAD^{tree} -p PR_BASE` builds the squashed commit, which is applied with `git cherry-pick --no-rerere-autoupdate --no-commit`. Because this uses the merge machinery, delete/modify conflicts become resolvable unmerged paths and binary files work.
4. Conflicts (`git diff --diff-filter=U`) prompt `Proceed? [y/n]`. A pick that fails **without** conflicts aborts instead of committing an incomplete tree.
5. The commit is authored as the PR author (the commit whose GitHub login matches, else the oldest commit's author). Other commit authors and existing trailers become `Co-authored-by:`. It uses `git commit -s` because the original per-commit sign-offs are lost in the squash and DCO needs one. Per-commit author attribution is lost.

`hack/legacy_cherry_pick_pull.sh` keeps the old per-commit `git am` flow as a fallback. Hardening that followed (source: pr-17577.md, pr-17607.md):

- `gh pr view` and `gh pr create` pass `--repo`, so `gh repo set-default`, `GH_REPO` pointing at a fork, or a fork named `origin` no longer yields `Could not resolve to a PullRequest`. The org/name now come from the last two URL path parts, so `ssh://`, `user@host:` and SSH-alias remotes work.
- gh runs with `CLICOLOR_FORCE=0 GH_FORCE_TTY=''`, so colour or a pager cannot corrupt the JSON that `jq` reads.
- `git log --no-show-signature`, so `log.showSignature=true` does not leak signature lines into the message or the author.
- `git rerere` runs before `cherry-pick --quit`, so resolutions are recorded. `--no-rerere-autoupdate` makes a reused resolution still stop at the prompt instead of aborting with `no conflicts to resolve`.
- The message goes through stdin (`--file=-`), because `-m` fails at 128 KiB and that would lose the resolution at the last step.
- **Committing the resolution yourself before typing `y` works again** (issue-17597: the script printed `Nothing staged ... Aborting` and, without `DRY_RUN`, its cleanup deleted the branch holding the commit). The script records HEAD before the pick. If HEAD is still on the pick branch and descends from it, `git reset --soft` re-stages the resolution and the script commits as usual.

The script is identical on main, release-0.20 and release-0.19 (backports pr-17566/pr-17567, pr-17592/pr-17593, pr-17625/pr-17626). Set `DRY_RUN=1` to stop before pushing and creating the PR.

### Dependabot

- `.github/dependabot.yml` gives every weekly ecosystem its own `schedule.day`: Docker on Monday, Go modules (the largest, up to 9 PRs) on Tuesday, npm and pip on Wednesday. github-actions stays daily. Thursday is kept free for patch releases and their cherry-pick waves, and Friday so a failed PR does not wait over the weekend. Before this, all ecosystems opened 9–14 PRs together on Friday around 09:33 UTC, each starting about 54 presubmits. 7 of 9 Pod-scheduling-timeout incidents in three months fell in that window (source: pr-17632.md).
- **Dependabot Version Sync** (`.github/workflows/sync-dependabot.yaml`) commits `make sync-hugo-version` for hugo bumps, and `make manifests update-helm` for controller-tools bumps, back to the Dependabot PR. Two fixes: it now also triggers on `labeled`, because Dependabot adds `ok-to-test` after `opened`, so the first run was always skipped (other label events are ignored, and a per-PR `concurrency` group stops overlapping pushes) (source: pr-17729.md). It also triggers on **`pull_request` instead of `pull_request_target`**, ahead of GitHub's default block on `pull_request_target` in public repositories from 2026-12-02. Dependabot branches live in the repository, so `pull_request` runs for them, and `permissions: contents: write` raises the otherwise read-only Dependabot token for the push (source: pr-17736.md, issue-17728.md). The job only runs when both the PR author and the actor are `dependabot[bot]`. See [[security-supply-chain]].

### Older automation notes

- **Cherry-pick automation** lifts fixes from main to release branches; "Cherry-picker should copy release notes" ([[issue-1715]]) addressed the release-note-propagation gap.
- **Promotion PR automation** was hardened to always rebase onto latest main ([[issue-10535]] — ensure the promotion PR is created on top of the latest main branch).
- **SLSA attestations** — requested, not implemented ([[issue-1466]], open).
- **Signing** — GitHub release artifacts are not signed ([[issue-1477]], open).
- **OLM listing** — images are packaged for OperatorHub ([[issue-1101]]).
- **Helm chart sync** — webhook configs auto-sync to helm ([[issue-1461]]).

## Kubernetes version support

Kueue supports a rolling window of Kubernetes minor versions (typically the current and previous two). `manager` tests run against multiple kind versions. Kubernetes 1.30 changed scheduling-gate behavior and Kueue had to track ([[issue-2029]]).

**A Kubernetes minor is dropped when it reaches end of life.** Kubernetes 1.34 reached EOL on 2026-10-27, and pr-17807 removed it the same day. `E2E_K8S_VERSIONS` in `hack/make/test.mk` is now `1.35.8 1.36.4 1.37.0` (default `E2E_K8S_VERSION=1.36`), and the README and installation guide say **1.35 or newer is recommended; only such versions are officially supported and tested**. The Prow job changes live in a companion `kubernetes/test-infra` PR (#38170), so a drop needs both repositories (source: pr-17807.md; raw/kueue/README.md, site/content/en/docs/getting-started/installation.md). Removing the version also let pr-17686 drop Kueue's custom-built secretreader image, which existed only for the older version (see [[testing-e2e]]). This applies to main; release branches keep their own lists.

## Dependency management

Kueue depends on `cluster-autoscaler/apis` for the ProvisioningRequest types; historically these were sometimes pinned to unreleased commits ([[issue-1194]], [[issue-1896]] — use a released cluster-autoscaler/apis module). Similar for KubeRay ([[issue-1634]]).

## v0.18.6 and v0.19.2 (paired patch releases, 2026-08)

Prepared by [[pr-14685]] ([[issue-14322]]) and [[pr-14686]] ([[issue-14323]]); `main` and the website were re-synced by [[pr-14690]], [[pr-14691]], [[pr-14692]], [[pr-14696]]. Headline content landing on these two branches around this window (not all of it is in v0.18.6 / v0.19.2: the reserved-`pods` refusal and its gate, the AdmissionCheck `observedGeneration` refresh, pr-14731, the LWS revision-guard fix and the two `kueuectl` fixes first shipped in v0.18.7 / v0.19.3; pr-14064, pr-14076 and pr-14050 were already in v0.18.5):

- the pod-group foreign-Workload adoption fix ([[pr-14617]], [[pr-14630]]) — see [[integration-plain-pod]];
- the reserved `pods` resource-name refusal plus its `ReservedResourceNameValidation` escape-hatch gate ([[pr-14756]], [[pr-14758]], [[pr-14773]], [[pr-14774]]) — see [[dra]];
- TAS elastic leader-assignment preservation ([[pr-14064]], [[pr-14076]]) and the `TASCacheTopologyTree` gate at Alpha/off ([[pr-14639]], [[pr-14644]]);
- MultiKueue `nominatedClusterNames` MAP clearing ([[pr-14643]], [[pr-14659]]) and AdmissionCheck `observedGeneration` refresh ([[pr-14914]], [[pr-14915]], [[pr-14933]], [[pr-14934]]);
- observability fixes on `kueue_pod_scheduling_gate_removal_seconds` ([[pr-14731]], [[pr-14530]]) and the metrics overflow / `+Inf` fix ([[pr-14050]]);
- LeaderWorkerSet queue-name backfill ([[pr-14602]], [[pr-14603]]) and the revision-guard precedence fix ([[pr-14892]], [[pr-14893]]);
- `kueuectl` UID-precondition delete ([[pr-14882]], [[pr-14883]]) and clusterqueue list chunking ([[pr-14880]], [[pr-14881]]).

Follow-on patch releases v0.18.7 ([[issue-14694]]) and v0.19.3 ([[issue-14693]]) followed. The most recent patch releases at this snapshot are listed below.

## Releases in this window

Dates are when the release-prep PR merged into the release branch.

| Release | Prepared | Prep PR | Headline changes |
|---|---|---|---|
| **v0.20.0** | 2026-09-30 | pr-16442.md | New minor; `v1beta1` no longer served; see the action-required list below |
| **v0.19.7** | 2026-09-30 | pr-16440.md | `HighMaxParallelismWithinReconcile` (8 → 32 concurrent API updates per reconcile); AFS fair-sharing vs priority order fix; Cohort-cycle hang fix (`CohortCycleDetected`); LWS/StatefulSet rolling-update ungating without quota fixed; `kueue_cohort_subtree_admitted_active_workloads` after hierarchy changes; Admitted events reporting 0s; TAS requeue only for CQs using the changed flavor; KueueViz empty Workloads page crash; `kueuectl list pods --for pod/NAME` fixes; fair-sharing preemption up to 20% faster |
| **v0.18.11** | 2026-09-30 | pr-16439.md | Same set as v0.19.7 backported to 0.18, plus the ConcurrentAdmission panic on Workload names without `-` |
| **v0.20.1** | 2026-10-08 | pr-16917.md | FairSharing weighted-share overflow / zero-weight / huge-weight fixes and `kueue_cohort_weighted_share` NaN; int64-overflow admission fixes; pending-workload metric refresh on LocalQueue/ClusterQueue lifecycle; `kueue_replaced_workload_slices_total` exposed; TAS second-pass and elastic PodSet-group fixes; Workloads no longer inherit Kueue-internal labels via `labelKeysToCopy`; new Alpha `KubeRayServiceUsingTopLevelSuspend`; `MultiKueueRayInTreeAutoscaling` now requires `SkipChildJobSuspension`; kueuectl `create clusterqueue` ordering and `delete workload` propagation fixes; KueueViz detail-page fixes |
| **v0.19.8** | 2026-10-08 | pr-16916.md | Mostly the same fixes as v0.20.1; also adds the Alpha `SkipChildJobSuspension` gate (off by default) to 0.19 |
| **v0.20.2** | 2026-10-15 | pr-17259.md (issue-17026) | No action required beyond the standard notes. KueueViz shows Pods of pod-group Workloads (feature); kueuectl fixes (hyphenated resource names, empty `queueName`, `version` with Helm release names, `--for` duplicates, `create localqueue --dry-run=client`); DRA requeue with stale charges; zero-count PodSet flavor on retry; FairSharing preemption within nominal quota; JobSet restart keeping evicted quota; pod-group role-hash quota bypass closed behind Alpha/off `PodIntegrationVerifyRoleRequests`; `SkipReassignmentForPodOwnedWorkloads` gated-Pod requeue; cohort-cycle requeue and borrowing-preemption-within-CQ fixes; TAS non-adjacent PodSet groups, overlapping-flavor preemption, `FlavorFungibilityPreserveScanProgress` fixes and clearer required-topology messages; metrics stale-series fixes; negative Pod overhead rejected; KueueViz Status column, empty-list loading, 30 s shutdown timeout, `/ws/namespaces` watch gating |
| **v0.19.9** | 2026-10-15 | pr-17258.md (issue-16938) | **ACTION REQUIRED:** invalid `metrics.localQueueMetrics.localQueueSelector` now fails startup when `metrics.localQueueMetrics.enable` is true (#16977). Otherwise mostly the v0.20.2 set (no `/ws/namespaces` change: release-0.19 KueueViz has no per-user authorization), plus `kueuectl list workload --for` hanging with a `job-uid` selector (#16963) and SparkApplication `SUBMISSION_FAILED` running outside quota with `OnFailure`/`Always` (#16976) |
| **v0.20.3** | 2026-10-22 | pr-17614.md (#17279) | No action beyond the standard notes. **Features:** RayService in-tree autoscaling under MultiKueue (`MultiKueueRayInTreeAutoscaling`, #17466); `ClassicalPreemptionCandidateOrderCache` as Alpha/off (#17296). **Fixes:** the KueueViz authorization and UI set (unknown `KUEUEVIZ_AUTH_MODE` fails startup, SAR cache-key collision, `/ws/cohorts` ClusterQueue names, graceful shutdown, missing-LocalQueue details page, broken links, flavor labels/taints, preemptor tooltip); TAS cold-start cache wait (#17455), node-slot over-admission (#17327), rank ordering for 0-indexed PodSet groups via `pod-index-offset: "0"` (#17512), failed-node replacement with succeeded Pods (#17502); committed-admission cache rollback (#17474); Cohorts kept in the scheduler cache on every replica (#17404); fair-sharing evict/re-admit loop (#17349); `HoldAndDrain` with held/deleted LocalQueues (#17480); a Job adopting a finished prebuilt Workload (#16994); StatefulSet scale-to-zero releasing quota early (#17540); TrainJob blocked by a same-named Workload (#17571); MultiKueue `Closed` preemption-gate writes (#17468) and batch/Job re-dispatch loop on k8s 1.35+ (#17569); LocalQueue metric performance (#17416, #17452). **Other:** Alpha `LogLevelForSchedulerMainLoop` (#17370); workload-controller logging cleanup with renamed `localQueue`/`prevLocalQueue` keys (#17332) |
| **v0.19.10** | 2026-10-22 | pr-17613.md (#17280) | Mostly the v0.20.3 set (`ClassicalPreemptionCandidateOrderCache` #17295, `LogLevelForSchedulerMainLoop` #17371). Not included, because release-0.19 KueueViz has no per-user authorization: the `/ws/cohorts` and SAR cache-key fixes. Also not included: the RayService autoscaling feature and the custom-label LocalQueue metric change. The Deployment/StatefulSet/LWS default-WorkloadPriorityClass fix applies with `WorkloadPriorityClassDefaulting` enabled (#17313) |

(source: CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md at kueue@8922c563e; v0.20.2 / v0.19.9 rows at kueue@3bbb8cce4; v0.20.3 / v0.19.10 rows at kueue@966f00d21). **Changelog oddity:** some v0.19.10 entries cite the main PR rather than the release-0.19 backport, for example #16630 (cold-start cache wait) and #17346 (Cohorts in the cache on every replica). Look up the backport when you need the release-0.19 commit. `main` and `website` were re-synced by pr-17261 / pr-17262 (and website pr-17263 / pr-17267). For v0.20.3 / v0.19.10, pr-17616 / pr-17615 updated `main`: the CHANGELOG, version parameters in the English and Chinese docs, and, for the latest minor, the Helm chart and installation examples.

**What the 2026-10-22 patches picked up.** The fixes that this page earlier listed as merged after v0.20.2 / v0.19.9 shipped in v0.20.3 / v0.19.10: the KueueViz authorization and UI fixes ([[dashboard]]), the LocalQueue metric fixes ([[metrics]]), the workload-controller logging cleanup (#17332 / #17410), the cold-start cache sync (#17455) and the committed-admission cache rollback (#17474 / #17578). **Merged to the release branches after the 2026-10-22 cut**, so pending the next patch: the KueueViz secondary-informer `watch` gating (pr-17755, release-0.20 only), the owner-reference fix (pr-17667 / pr-17669), and the `RayClusterHeadPodReady` Alpha/off backports (pr-17603 / pr-17604, see [[feature-gates]]). Each patch changelog starts with an "Actions Required Before Upgrading" section telling users to read the `.0` notes of every minor they cross and the earlier patch notes of their own minor line.

## v0.20: action required

- **`v1beta1` is no longer served.** Run `hack/migrate-to-v1beta2.sh` before upgrading. See [[api-versions]] ([[pr-14558]]).
- **`TASRecomputeAssignmentWithinSchedulingCycle` now requires `TopologyAwareScheduling`.** If TAS is disabled, set the gate to `false` before upgrading ([[pr-14256]]).
- **A Configuration that names `pods`** as a DRA `deviceClassMappings[].name` or in a resource transformation will now stop the manager at startup (`os.Exit`). Rename it, or set `ReservedResourceNameValidation=false` for one release ([[pr-13989]], [[pr-14778]]). Renaming an `outputs` key also requires updating the matching ClusterQueue resource name.
- **`kueue_pod_scheduling_gate_removal_seconds` gained a `replica_role` label**, changing that metric's series identity ([[pr-14488]]).
- **`RejectUpdatesToCQWithInvalidOnFlavors` is Beta/on** — fix invalid `AdmissionCheckStrategy.OnFlavors` references first ([[pr-14776]]).

Further action-required items from the v0.20.0 changelog (source: CHANGELOG-0.20.md):

- **AFS:** `AdmissionFairSharingAnchorAtQuotaReservation` is Beta/on (LocalQueue usage counts from quota reservation). If you explicitly disable `AdmissionFairSharing`, disable this gate too, or startup validation rejects the configuration. Remove it from the configuration before rolling back to a release that does not know it (#15000).
- **KueueViz:** with authentication enabled, every request is checked with a SubjectAccessReview. Users need get/list/watch; custom RBAC must let the backend SA create `subjectaccessreviews` (#13810; see [[dashboard]]).
- **LeaderWorkerSet:** `spec.leaderWorkerTemplate.size` is immutable while Kueue manages the LWS (gate `LWSImmutableGroupSize`), which closes a quota bypass. Recreate the LWS to resize (#13279).
- **Observability:** an invalid `metrics.localQueueMetrics.localQueueSelector` is rejected at startup; before, it silently exposed all LocalQueues (#16379).
- **RayService:** `RayServiceValidateUpgradeStrategy` is Beta/on. Zero-downtime upgrades need `ElasticJobsViaWorkloadSlices` plus the `kueue.x-k8s.io/elastic-job: "true"` annotation, or `spec.upgradeStrategy.type: None` (#16094).
- **SparkApplication:** Workloads now reserve `cores` as CPU and Spark's memory overhead (at least 384Mi per Pod). Raise quotas if needed (#15833).
- **TAS:** slice sizes must be positive, and `podSetSliceRequiredTopology` and `podSetSliceSize` must be set together (#12728).
- **TrainJob:** Trainer v2.3 is required; v2.2 is API-incompatible (#14504).
- **Custom integrations:** `ComposableJob.Load` now returns `(*jobframework.LoadResult, error)`; use `jobframework.NewLoadResult(shouldFinalize, found)` (#12849).

## On main (v0.21 dev): action-required changes so far

- **Logging:** eight scheduler progress messages moved from V(2) to **V(3)**: `Scheduling cycle starts`, `Obtained heads`, `Snapshot taken`, `Nomination done`, `Attempting to schedule workload`, `Workload re-queued`, `Workload processing done`, `Scheduling cycle complete`. Dashboards or log alerts built on them need `-v=3`. Motivation: a Workload waiting for preemption is retried about every 10 ms, and one Workload produced 26,184 of these lines in 35 s (source: pr-17227.md, raw/kueue/pkg/scheduler/scheduler.go). Unconditional on main. The release branches shipped the same move as opt-in behind the Alpha `LogLevelForSchedulerMainLoop` gate in v0.20.3 / v0.19.10 (#17370 / #17371). Main has no such gate.
- **RayCluster:** the Beta `RayClusterHeadPodReady` gate (on by default) bases `PodsReady` on the head Pod's `HeadPodReady` condition. It **requires KubeRay v1.3.0+**; with an older KubeRay set `RayClusterHeadPodReady=false` (pr-17591; release-note-action-required). See [[feature-gates]].
- **FairSharing (behaviour change):** the `FairSharingPreemptWithinNominal` claim is evaluated at the preemptor's almostLCA with each target. A ClusterQueue within its own nominal quota no longer preempts across a borrowing parent Cohort (pr-13307). See [[fair-sharing]].
- **Kubernetes 1.34 is no longer supported or tested** (pr-17807, above).
- **Helm:** `managerConfig` accepts only `mode`, `structuredOverrides` and `controllerManagerConfigYaml`; chart defaults moved from `values.yaml` to `templates/manager/_config.tpl` (pr-16312). See [[architecture#Configuring the manager through Helm]].

## Cherry-pick mechanics worth knowing

Feature-gate specs generally **cannot** be cherry-picked verbatim. Kueue never sets an emulation version, so the effective version is Kubernetes' `DefaultKubeBinaryVersion`; `featureSpecAtEmulationAndMinCompatVersion` therefore still selects a spec written as `{0.20, Default: true, Beta}` on a release-0.19 build, silently enabling the gate there. A backport that must stay opt-in has to rewrite the spec as `{0.19, Default: false, Alpha}`, and gate *dependencies* move from `main`'s `defaultFeatureGateDependencies` map to the branch's `validateFeatureGateDependency` in `pkg/config/validation.go`. ([[pr-14804]])

**Go language version on release branches.** `release-0.19` pins `-lang=go1.26` in `go.mod`. Test code on `main` that uses promoted fields in composite literals (for example `&kueue.WorkloadList{Continue: "page2"}` or `&batchv1.Job{Name: ..., UID: ...}`, described in review as a Go 1.27+ language feature) does not compile there. The manual cherry-pick must spell out the embedded struct: `ListMeta: metav1.ListMeta{Continue: ...}`, `ObjectMeta: metav1.ObjectMeta{...}` (source: pr-16850.md, which hit this on its release-0.19 pick).

Example from this batch: `ClassicalPreemptionCandidateOrderCache` (pr-16340, faster classical preemption by reusing candidate ordering) is `{0.21, Beta, on}` on main but was backported to release-0.20 and release-0.19 (pr-17296, pr-17295, merged after v0.20.2 / v0.19.9) as an Alpha gate, off by default (source: pr-17295.md, pr-17296.md, raw/kueue/pkg/features/kube_features.go).

**CI toolchain drift hits every branch at once.** When the kubekins image moved to Go 1.27.2 (export data v5), golangci-lint v2.13.2 failed every package with `typecheck`; the bump to v2.14.0 had to go to main and both release branches (pr-17148; backports pr-17151, pr-17152) (source: pr-17148.md). See [[code-quality]].

A manual cherry-pick is also required whenever the bot's automated pick fails on a diverged `go.mod` — see [[pr-14531]] for a worked example (dependency resolution to the branch's own versions, plus test-fixture adaptation to the branch's older internal API).

## Related pages

- [[feature-gates]] — graduation happens alongside releases.
- [[performance-and-scale]] — scale fixes land via patch releases.
