# kueuectl

**Summary**: `kueuectl` (installable as the `kubectl-kueue` plugin) is Kueue's CLI for day-to-day operator and user tasks: creating ClusterQueues and LocalQueues, listing/stopping/resuming workloads, draining queues, and passing through to underlying jobs.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-29

---

## Installation

Ships as a standalone binary and a `kubectl` plugin (`kubectl kueue ...`). The plugin pattern is conventional in the Kubernetes ecosystem and doesn't require anything special beyond the binary being on `$PATH`.

## Command surface

The CLI grew incrementally during v0.6–v0.7. Representative tracking issues:

- **Create**: `kueuectl create clusterqueue`, `kueuectl create localqueue` ([[issue-2113]] — Allow create ClusterQueue).
- **List**: `kueuectl list workloads`, `kueuectl list clusterqueue` ([[issue-2135]], [[issue-2114]]).
- **Stop / Resume**: `kueuectl stop workload`, `kueuectl stop clusterqueue`, `kueuectl stop localqueue`, and matching `resume` ([[issue-2132]], [[issue-2133]], [[issue-2137]], [[issue-2138]], [[issue-2139]]). Stop on a CQ can either drain (evict admitted) or just hold (let admitted finish); there's separate flaky-test coverage for both ([[issue-2247]], [[issue-2245]]).
- **Pass-through**: "Add Pass-through commands" ([[issue-2180]]) — `kueuectl` can proxy operations on the underlying job.
- **List pods for a job**: a convenience over `kubectl get pods -l` ([[issue-2204]]).

## Validation

`kueuectl create localqueue` validates that the target ClusterQueue exists ([[issue-2112]]). ResourceFlavor names with hyphens were rejected by an earlier validation bug ([[issue-2701]]).

## Test infrastructure

`kueuectl` tests use a fake clock to avoid real-time flakiness ([[issue-2287]]).

## Deleting a Workload uses a UID precondition

`kueuectl delete workload` deletes the Workload's owner as well. It used to delete **by name**, so a stale Workload whose owner had already been deleted and recreated with the same name destroyed the *replacement* object. [[pr-14831]] (fixes [[issue-14830]]; cherry-picks [[pr-14882]], [[pr-14883]]) preserves the UID from each Workload owner reference and passes it as a **delete precondition**, so the delete is refused when the UID no longer matches.

## `list clusterqueue` honours the chunk size

`list clusterqueue` never set `Options.Limit` in `Complete()`, unlike `list localqueue`, `list workload` and `list resourceflavor`, which all call `listRequestLimit()`. `KUEUECTL_LIST_REQUEST_LIMIT` therefore had no effect and every invocation issued a single unbounded LIST. [[pr-14864]] (cherry-picks [[pr-14880]], [[pr-14881]]) adds the missing call; an invalid limit is now rejected up front instead of silently producing an unusable setting.

Open inconsistency: `kueuectl create clusterqueue` validates resource-group overlap differently from the webhook ([[issue-14926]]).

## `list pods --for` fixes

`--for pod/NAME` derives its selector from the Pod integration's `PodLabelSelector()`, which formats `kueue.x-k8s.io/pod-group-name=<value>` without checking the label exists.

- **Standalone Pod.** The selector became `pod-group-name=` (empty value) and matched nothing (`No resources found`). The CLI now detects a Pod without the group label and selects it by namespace and name through a field selector, merged with any user `--field-selector` and `--selector`; `PodLabelSelector()` is unchanged (source: pr-15435.md).
- **Annotation-based groups.** When the group name is stored in the `kueue.x-k8s.io/pod-group-name` **annotation** rather than the label (annotation form, see [[integration-leaderworkerset]]), label selectors cannot match. kueuectl now reads the annotation, lists the namespace's Pods without a group selector and filters client-side (source: pr-15739.md, fixes issue-15709.md).

## `list workload --for`

The command lists again without the job-uid label when the first query is empty, then keeps Workloads owned by the target object. The retry test was a substring check, so a `-l` selector already containing the job-uid requirement retried forever. The fallback now runs only while the list uses the selector the command built, and only once (source: pr-16040.md, fixes issue-16038.md). With `DeploymentJobUIDLabel` on, `--for deployment/foo` returns that Deployment's Workloads (previously nothing; source: pr-15641.md).

## `list localqueue`: Active column and filter

`list localqueue` gained an `ACTIVE` column (from the LocalQueue `Active` condition) and `--active=true|false`, mirroring `list clusterqueue`; combinable with `--clusterqueue`; repeated `--active` values are rejected (source: pr-15866.md).

## `version` honours `--namespace`

`kueuectl version` looked up the `kueue-controller-manager` Deployment only in `kueue-system`. An explicit `-n/--namespace` is now honoured; unset keeps `kueue-system` (source: pr-15963.md, fixes issue-15958.md; backports pr-15976.md, pr-15977.md).

Open: `kueuectl delete workload --all` handles only the first list page and ignores the continue token ([[issue-16185]]).

## Related pages

- [[kueue-overview]] — what Kueue is and where the CLI fits.
- [[cluster-queue]] — the CLI's main creation target.
- [[local-queue]] — tenant-side CLI target.
- [[workload]] — what `stop` / `resume` / `list` act on.
- [[visibility-api]] — what some list commands query under the hood.
- [[debugging-guide]] — when `kueuectl` helps diagnose stuck workloads.
