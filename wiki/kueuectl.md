# kueuectl

**Summary**: `kueuectl` (installable as the `kubectl-kueue` plugin) is Kueue's CLI for day-to-day operator and user tasks: creating ClusterQueues and LocalQueues, listing/stopping/resuming workloads, draining queues, and passing `get`/`describe`/`edit`/`patch`/`delete` on Kueue resource types through to `kubectl`.

**Sources**: `raw/github/kubernetes-sigs__kueue/`; pr-15376.md, pr-16040.md, pr-16510.md, pr-16531.md, pr-16609.md, pr-16633.md, pr-16667.md, pr-16850.md, pr-16981.md, pr-17055.md, issue-17054.md; 2026-10-28 batch: pr-17708.md, issue-17707.md, pr-17818.md, pr-17829.md, pr-17830.md, `raw/kueue/cmd/kueuectl/app/passthrough/passthrough.go`, `raw/kueue/test/integration/singlecluster/kueuectl/passthrough_test.go`; `raw/kueue/CHANGELOG/CHANGELOG-0.20.md`, `CHANGELOG-0.19.md`, `CHANGELOG-0.18.md`.; 2026-11-24 batch: pr-18174.md, pr-18054.md, pr-18057.md, pr-18075.md, pr-18197.md, pr-18138.md, pr-18296.md, CHANGELOG-0.20.md, CHANGELOG-0.19.md

**Last updated**: 2026-11-24

---

## Installation

Ships as a standalone binary and a `kubectl` plugin (`kubectl kueue ...`). The plugin pattern is conventional in the Kubernetes ecosystem and doesn't require anything special beyond the binary being on `$PATH`.

## Command surface

The CLI grew incrementally during v0.6–v0.7. Representative tracking issues:

- **Create**: `kueuectl create clusterqueue`, `kueuectl create localqueue` ([[issue-2113]] — Allow create ClusterQueue).
- **List**: `kueuectl list workload`, `kueuectl list clusterqueue` ([[issue-2135]], [[issue-2114]]).
- **Stop / Resume**: `kueuectl stop workload`, `kueuectl stop clusterqueue`, `kueuectl stop localqueue`, and matching `resume` ([[issue-2132]], [[issue-2133]], [[issue-2137]], [[issue-2138]], [[issue-2139]]). Stop on a CQ can either drain (evict admitted) or just hold (let admitted finish); there's separate flaky-test coverage for both ([[issue-2247]], [[issue-2245]]).
- **Pass-through**: "Add Pass-through commands" ([[issue-2180]]) — `get`, `describe`, `edit`, `patch` and `delete` on Kueue resource types are handed to `kubectl`. See [Pass-through commands](#pass-through-commands) below for the mechanism and the supported types.
- **List pods for a job**: a convenience over `kubectl get pods -l` ([[issue-2204]]).

## Pass-through commands

`cmd/kueuectl/app/passthrough/passthrough.go` registers one cobra subcommand per (verb, type) pair. The verbs are `get`, `delete`, `edit`, `describe` and `patch`. The `RunE` does not call the API itself. It looks up `kubectl` on `$PATH`, replaces `os.Args[0]` with that path and `syscall.Exec`s it, so `kueuectl get cq foo -o yaml` runs as `kubectl get cq foo -o yaml` with every flag unchanged. Unknown flags are whitelisted for that reason (`FParseErrWhitelist{UnknownFlags: true}`). Without `kubectl` on `$PATH`, the command fails with `pass-through command are not available: ..., PATH=...`. The one exception is `delete workload`, which is Kueue's own command (`delete.NewWorkloadCmd`, which also deletes the owner; see below).

| Type | Aliases |
|---|---|
| `workload` | `kwl`, `kueueworkload`, `kueueworkloads` |
| `clusterqueue` | `cq` |
| `localqueue` | `lq` |
| `resourceflavor` | `rf` |
| `cohort` | `co` (new) |
| `topology` | `topo` (new) |

**Cohort and Topology were added in this window** (source: pr-17708.md, fixes issue-17707.md). Before, `kueuectl get cohort` failed with `unknown command "cohort" for "kueuectl get"`. This is on main only: pr-17708 was not cherry-picked, so v0.20.x and v0.19.x still reject both types. Because the arguments go to `kubectl` unchanged, **an alias only works if the CRD declares it as a `shortName`**. The issue and PR first proposed `ch` for Cohort, and the reviewer had it changed to `co` to match `+kubebuilder:resource:scope=Cluster,shortName={co}` in `apis/kueue/v1beta2/cohort_types.go`. Topology declares `shortName={topo}` (source: pr-17708.md review; raw/kueue/config/components/crd/bases/). The generated CLI reference docs are rebuilt with `make generate-kueuectl-docs`.

**Test pattern** (`test/integration/singlecluster/kueuectl/passthrough_test.go`). The table runs every verb and alias against a real `kubectl` binary. ClusterQueue, ResourceFlavor, Cohort and Topology are cluster-scoped and reuse fixed names across entries and reruns. Cleanup used to rely on the CLI `delete` at the end of each entry, so a failed `get` or `patch` assertion left the object behind, and the next alias entry failed with `AlreadyExists`. Each entry now registers `ginkgo.DeferCleanup` right after `MustCreate`. The cleanup deletes with `client.IgnoreNotFound` and waits until the object is NotFound, so it is harmless once the CLI delete has already run (source: pr-17818.md; backported to release-0.19/0.20 as pr-17829/pr-17830). The PR text names `behavioral.ExpectObjectToBeDeleted`, but the merged code uses the inline `DeferCleanup` shown here (raw/kueue at kueue@966f00d21). General rule: register cleanup for cluster-scoped fixtures **immediately after creating them**, not at the end of the test body.

## Validation

`kueuectl create localqueue` validates that the target ClusterQueue exists ([[issue-2112]]). ResourceFlavor names with hyphens were rejected by an earlier validation bug ([[issue-2701]]).

### `create localqueue --dry-run=client` makes no API call

`Validate(ctx)` in `cmd/kueuectl/app/create/create_localqueue.go` called `ClusterQueues().Get()` unless `--ignore-unknown-cq` was set, even though `Run()` already skipped the create for client dry-run. Offline use (GitOps templating in CI with no cluster, or a ClusterQueue not yet applied) failed with `clusterqueues.kueue.x-k8s.io "<cq>" not found` or a dial error. The lookup is now guarded by `o.DryRunStrategy != dryrun.Client && !o.IgnoreUnknownCq`. `--dry-run=server` and a real create still fail on an unknown ClusterQueue unless `--ignore-unknown-cq` is passed (source: pr-17055.md, fixes issue-17054.md; backports pr-17109 to release-0.20, pr-17110 to release-0.19).

## `create clusterqueue` quota parsing

`--nominal-quota`, `--borrowing-limit` and `--lending-limit` take `flavor:res=qty;res=qty,flavor2:...`, parsed by `parseUserSpecifiedResourceQuotas` in `cmd/kueuectl/app/create/create_clusterqueue.go`. Fixes in this window:

- **Flavor resources are sorted into `coveredResources` order.** Flavors covering the same resource set are merged into one resource group, but each flavor kept the user's typing order. The webhook matches `flavors[i].resources[j]` to `coveredResources[j]` **by position**, so `--nominal-quota "alpha:cpu=1;memory=1,beta:memory=2;cpu=2"` was rejected with `must match the name in coveredResources` (and `--dry-run=client` printed an invalid object). Borrowing and lending limits move with their resource. Shipped in v0.20.1 / v0.19.8 (source: pr-16531.md; backports pr-16544, pr-16545; CHANGELOG-0.20.md).
- **Hyphenated resource names.** The resource-name segment regex was `\/?\w+`, and `\w` excludes `-`, so `example.com/v100-gpu`, `intel.com/sriov-net` or `habana.ai/gaudi-2` failed with `invalid resources specification`. It is now `\/?[\w\.-]+=` (source: pr-16981.md; backports pr-16987, pr-16988; issue-16980 tracked the same bug).
- **Shipped in v0.20.0** (source: CHANGELOG-0.20.md): decimal quantities such as `cpu=1.5` / `memory=1.5Gi` accepted (#15299); a trailing `;` accepted (#15491); a resource repeated in the same flag rejected with an error naming the resource and flag (#15514); `--borrowing-limit`/`--lending-limit` are optional per resource, and a limit for a resource with no nominal quota is reported instead of silently dropped; resource-group overlap detection made consistent (#14929).

Test convention reinforced by pr-16633.md: `cmp.Diff(want, got)` under a `(-want,+got)` label; `TestParseResourceQuotas` had the arguments reversed, so failures printed expected and actual swapped.

## Test infrastructure

`kueuectl` tests use a fake clock to avoid real-time flakiness ([[issue-2287]]).

## Deleting a Workload uses a UID precondition

`kueuectl delete workload` deletes the Workload's owner as well. It used to delete **by name**, so a stale Workload whose owner had already been deleted and recreated with the same name destroyed the *replacement* object. [[pr-14831]] (fixes [[issue-14830]]; cherry-picks [[pr-14882]], [[pr-14883]]) preserves the UID from each Workload owner reference and passes it as a **delete precondition**, so the delete is refused when the UID no longer matches.

### Owners are deleted with background propagation

The owner deletes go through the dynamic client. Without a `PropagationPolicy` the server default applies, which for batch/v1 Job is **Orphan**: the Job disappeared but its Pods kept running and the Workload was never garbage-collected, contrary to the command's help text. `delete_workload.go` now passes `PropagationPolicy: Background`, matching `kubectl delete`; UID preconditions and dry-run behaviour are unchanged. The integration test deletes a real Job owner; envtest has no garbage collector, so an orphaning delete would leave the Job stuck on the `orphan` finalizer, which is what the test detects. The kueuectl integration suite registers a no-op Job webhook so the test can create Jobs. Shipped in v0.20.1 / v0.19.8 (source: pr-16510.md; backports pr-16511, pr-16512).

## `list clusterqueue` honours the chunk size

`list clusterqueue` never set `Options.Limit` in `Complete()`, unlike `list localqueue`, `list workload` and `list resourceflavor`, which all call `listRequestLimit()`. `KUEUECTL_LIST_REQUEST_LIMIT` therefore had no effect and every invocation issued a single unbounded LIST. [[pr-14864]] (cherry-picks [[pr-14880]], [[pr-14881]]) adds the missing call; an invalid limit is now rejected up front instead of silently producing an unusable setting.

Open inconsistency: `kueuectl create clusterqueue` validates resource-group overlap differently from the webhook ([[issue-14926]]).

## `list pods --for` fixes

- **Structured output is one `PodList`.** `-o json` / `-o yaml` used to print each matching Pod as a separate document, which is not valid JSON for `jq`; non-empty results are now wrapped in one `v1/PodList`, consistent with `list workload -o json`. Other output formats still print per Pod. Shipped in v0.20.0, backported to release-0.18/0.19 (source: pr-15376.md; backports pr-15518, pr-15520). Related v0.20.0 fixes: `list` with `-o yaml|json` spanning more than one page (`KUEUECTL_LIST_REQUEST_LIMIT`, default 100) merges all pages into one document (#15348), and `list pods` no longer treats any output format containing `wide` (for example a JSONPath expression) as `-o wide` (#15156) (source: CHANGELOG-0.20.md).

`--for pod/NAME` derives its selector from the Pod integration's `PodLabelSelector()`, which formats `kueue.x-k8s.io/pod-group-name=<value>` without checking the label exists.

- **Standalone Pod.** The selector became `pod-group-name=` (empty value) and matched nothing (`No resources found`). The CLI now detects a Pod without the group label and selects it by namespace and name through a field selector, merged with any user `--field-selector` and `--selector`; `PodLabelSelector()` is unchanged (source: pr-15435.md).
- **Annotation-based groups.** When the group name is stored in the `kueue.x-k8s.io/pod-group-name` **annotation** rather than the label (annotation form, see [[integration-leaderworkerset]]), label selectors cannot match. kueuectl now reads the annotation, lists the namespace's Pods without a group selector and filters client-side (source: pr-15739.md, fixes issue-15709.md).

### Annotation-group scan warning (v0.21, pr-18174)

Kubernetes filters on label selectors server-side but not on annotations, so `kueuectl list pods --for pod/NAME` for a Pod group named by the `kueue.x-k8s.io/pod-group-name` **annotation** lists Pods in scope and filters client-side. The command now prints a warning to stderr first, stating the scan scope and the supplied label/field selectors and suggesting `--selector` when none was given. The scan stays in the anchor Pod's namespace, including with `--all-namespaces`. Label-based groups and standalone Pods stay silent, and the selected Pods are unchanged. (An earlier variant, pr-18173, described an all-namespaces scan and was not merged; pr-17909, the mixed label/annotation fix, was also still unmerged at this snapshot.) (source: pr-18174.md)

## `list` request limit

`KUEUECTL_LIST_REQUEST_LIMIT` controls pagination for `kueuectl list`; it is now documented in `kueuectl list --help` and the website reference (pr-18054). Negative values are rejected with an error; `0` is accepted and disables pagination (v0.20.5 via #18087; v0.19.13 via #18681). (source: pr-18054.md, CHANGELOG-0.20.md, CHANGELOG-0.19.md)

## `create clusterqueue` validation and error text

`create clusterqueue` validates quota specs with the API server's rules: valid values such as `cpu=1e-3` or a resource name like `foo--bar.example.com/gpu` are accepted, names the API server rejects are refused, and errors name the invalid spec and flag (v0.20.6 via #18540, v0.19.13 via #18542). The `invalid resource group` error names the conflicting flavors and the resources each covers (v0.20.5 / v0.19.12, #18097 / #18096). `kueuectl delete workload` usage now says it takes multiple names, that names and `--all` are mutually exclusive, and that `--all-namespaces` needs `--all` (v0.20.4 / v0.19.11). (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md)

## Ownership and test conventions

`cmd/kueuectl` has `kueuectl-approvers` (mbobrovskyi, since pr-17846) and `kueuectl-reviewers` (henry3260 self-nominated, pr-18057) aliases, also applied to the kueuectl docs and test OWNERS (pr-18075). Tests were reshaped: the pass-through table became independent scenarios, a shared in-process execution helper exists (pr-18197), the create-clusterqueue tests use a single `wantErr` string and inline error sentinels (pr-18138, pr-18296), and the CI builds `kueuectl` only for test targets that run it. (source: pr-18057.md, pr-18075.md, pr-18197.md, pr-18138.md, pr-18296.md)

## `list workload --for`

The command lists again without the job-uid label when the first query is empty, then keeps Workloads owned by the target object. The retry test was a substring check, so a `-l` selector already containing the job-uid requirement retried forever. The fallback now runs only while the list uses the selector the command built, and only once (source: pr-16040.md, fixes issue-16038.md; release-0.19 backport pr-16963). With `DeploymentJobUIDLabel` on, `--for deployment/foo` returns that Deployment's Workloads (previously nothing; source: pr-15641.md).

**Search structure after pr-16850.** `WorkloadOptions.Run()` (`cmd/kueuectl/app/list/list_workload.go`) now decides the search once:

1. Without `--for`, a single paginated `listAndPrint` with the user selector.
2. With `--for`, the selector is `<user -l>,kueue.x-k8s.io/job-uid=<uid>`. The owner-reference fallback (user selector only, filtered by `filterByOwnerReference(ownerUID)`) starts **only if the first page of the job-uid search is empty and has no continue token**. The first page is reused, not listed again, so the API server sees the same requests as before.

Previously a job-uid search that spanned pages and ended with an empty page could start the fallback and print Workloads twice. Pagination is in `forEachWorkloadPage`/`listWorkloadPage`, printing in `printWorkloadPage`/`listAndPrint`; `filterList` takes `ownerUID *types.UID` (`nil` = no owner filter) (source: pr-16850.md, fixes issue-16120).

**Workloads without `spec.queueName`.** `localQueues()` called `LocalQueues(ns).Get(ctx, "")` for any non-admitted Workload with an empty queue name. client-go rejects an empty name with `resource name may not be empty`, which `IgnoreNotFound` does not filter, so the **whole** `list workload` failed. Such Workloads are now listed with empty LOCALQUEUE and CLUSTERQUEUE columns (source: pr-16667.md; backports pr-16986, pr-16978).

Other `list workload` fixes shipped in v0.20.0 (source: CHANGELOG-0.20.md): `--clusterqueue` never matched pending Workloads, so `--clusterqueue X --status pending` always returned nothing (#15336); JOB TYPE / JOB NAME columns were printed in random order for multi-owner Workloads such as pod groups (#15357); `--for TYPE/NAME` for a non-existent object listed every Workload in the namespace and now prints `No resources found` (#15248); `--status` help now lists `quotareserved` (#15330).

## `list localqueue`: Active column and filter

`list localqueue` gained an `ACTIVE` column (from the LocalQueue `Active` condition) and `--active=true|false`, mirroring `list clusterqueue`; combinable with `--clusterqueue`; repeated `--active` values are rejected (source: pr-15866.md). Both shipped in v0.20.0, together with ACTIVE and REASON columns in `-o wide` for ClusterQueue and LocalQueue (#15633), and shell-completion fixes for `--clusterqueue`/`--localqueue` after a positional argument (#15375) and for `stop|resume workload` suggesting more than the one required name (#15449) (source: CHANGELOG-0.20.md).

## `version`: namespace and controller lookup

`kueuectl version` looked up the `kueue-controller-manager` Deployment only in `kueue-system`. An explicit `-n/--namespace` is now honoured; unset keeps `kueue-system` (source: pr-15963.md, fixes issue-15958.md; backports pr-15976.md, pr-15977.md).

The lookup was also **by name**, and NotFound meant "not installed". The Helm chart names the Deployment after the release, so after `helm install foo ...` only the client version was printed. `cmd/kueuectl/app/version/version.go` now does a single List with the selector `app.kubernetes.io/name=kueue,control-plane=controller-manager` (both kustomize and Helm have set these labels since v0.7; `kueuectl version` first shipped in v0.8). 0 matches = not installed (client version only), 1 = print its image, more than one = error listing the names. A KueueViz Deployment does not match. A Helm `nameOverride` changes `app.kubernetes.io/name` and stays unsupported; `control-plane` alone was rejected because it also matches other kubebuilder operators such as JobSet (source: pr-16609.md; backports pr-16953, pr-16966).

Open: `kueuectl delete workload --all` handles only the first list page and ignores the continue token ([[issue-16185]]).

## Which release carries the 2026-10 CLI fixes

From the v0.20.2 and v0.19.9 changelogs (both prepared 2026-10-15) (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md):

| Fix (section above) | main PR | v0.20.2 | v0.19.9 |
|---|---|---|---|
| hyphenated resource names in `create clusterqueue` | pr-16981 | #16987 | #16988 |
| `list workload` with an empty `spec.queueName` | pr-16667 | #16986 | #16978 |
| `version` on a Helm install with another release name | pr-16609 | #16953 | #16966 |
| `list workload --for` duplicates after an empty last page | pr-16850 | #17084 | #16850 |
| `list workload --for` never finishing when `-l` already has `job-uid` | pr-16040 | (in v0.20.0) | #16963 |
| `create localqueue --dry-run=client` makes no API call | pr-17055 | #17109 | #17110 |

The coveredResources ordering fix and `delete workload` background propagation shipped earlier, in v0.20.1 / v0.19.8.

**Release-note convention.** kueuectl fixes use the `CLI:` prefix in release notes (maintainers ask for it in review; source: pr-17055.md).

## Related pages

- [[kueue-overview]] — what Kueue is and where the CLI fits.
- [[cluster-queue]] — the CLI's main creation target.
- [[local-queue]] — tenant-side CLI target.
- [[workload]] — what `stop` / `resume` / `list` act on.
- [[visibility-api]] — what some list commands query under the hood.
- [[debugging-guide]] — when `kueuectl` helps diagnose stuck workloads.
