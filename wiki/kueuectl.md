# kueuectl

**Summary**: `kueuectl` (installable as the `kubectl-kueue` plugin) is Kueue's CLI for day-to-day operator and user tasks: creating ClusterQueues and LocalQueues, listing/stopping/resuming workloads, draining queues, and passing through to underlying jobs.

**Sources**: `raw/github/kubernetes-sigs__kueue/`; pr-15376.md, pr-16040.md, pr-16510.md, pr-16531.md, pr-16609.md, pr-16633.md, pr-16667.md, pr-16850.md, pr-16981.md, pr-17055.md, issue-17054.md; `raw/kueue/CHANGELOG/CHANGELOG-0.20.md`, `CHANGELOG-0.19.md`, `CHANGELOG-0.18.md`.

**Last updated**: 2026-10-28

---

## Installation

Ships as a standalone binary and a `kubectl` plugin (`kubectl kueue ...`). The plugin pattern is conventional in the Kubernetes ecosystem and doesn't require anything special beyond the binary being on `$PATH`.

## Command surface

The CLI grew incrementally during v0.6–v0.7. Representative tracking issues:

- **Create**: `kueuectl create clusterqueue`, `kueuectl create localqueue` ([[issue-2113]] — Allow create ClusterQueue).
- **List**: `kueuectl list workload`, `kueuectl list clusterqueue` ([[issue-2135]], [[issue-2114]]).
- **Stop / Resume**: `kueuectl stop workload`, `kueuectl stop clusterqueue`, `kueuectl stop localqueue`, and matching `resume` ([[issue-2132]], [[issue-2133]], [[issue-2137]], [[issue-2138]], [[issue-2139]]). Stop on a CQ can either drain (evict admitted) or just hold (let admitted finish); there's separate flaky-test coverage for both ([[issue-2247]], [[issue-2245]]).
- **Pass-through**: "Add Pass-through commands" ([[issue-2180]]) — `kueuectl` can proxy operations on the underlying job.
- **List pods for a job**: a convenience over `kubectl get pods -l` ([[issue-2204]]).

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
