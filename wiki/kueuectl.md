# kueuectl

**Summary**: `kueuectl` (installable as the `kubectl-kueue` plugin) is Kueue's CLI for day-to-day operator and user tasks: creating ClusterQueues and LocalQueues, listing/stopping/resuming workloads, draining queues, and passing through to underlying jobs.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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

## Related pages

- [[cluster-queue]] — the CLI's main creation target.
- [[local-queue]] — tenant-side CLI target.
- [[workload]] — what `stop` / `resume` / `list` act on.
- [[visibility-api]] — what some list commands query under the hood.
