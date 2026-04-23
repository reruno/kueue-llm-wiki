# Issue #3693: TAS: Kueue crashes with panic when the node running a workload is deleted

**Summary**: TAS: Kueue crashes with panic when the node running a workload is deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3693

**Last updated**: 2024-12-03T10:57:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-29T18:39:48Z
- **Updated**: 2024-12-03T10:57:01Z
- **Closed**: 2024-12-03T10:57:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

**What happened**:

Kueue crashes with panic when a new workload is scheduled after a node is deleted, which was hosting another workload.

**What you expected to happen**:

No panic, admission of new workloads continues.

**How to reproduce it (as minimally and precisely as possible)**:

1. create a TAS workload
2. delete one of the nodes hosting one of the pods of the workload
3. schedule another workload
*Issue*:  kueue panics with the following stacktrace:

```
E1129 18:33:53.869062       1 panic.go:262] "Observed a panic" panic="runtime error: invalid memory address or nil pointer dereference" panicGoValue="\"invalid memory address or nil pointer dereference\"" stacktrace=<
	goroutine 478 [running]:
	k8s.io/apimachinery/pkg/util/runtime.logPanic({0x302f5d0, 0x49be620}, {0x27352c0, 0x49259f0})
		/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:107 +0xbc
	k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x302f5d0, 0x49be620}, {0x27352c0, 0x49259f0}, {0x49be620, 0x0, 0x10000000043b665?})
		/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:82 +0x5e
	k8s.io/apimachinery/pkg/util/runtime.HandleCrash({0x0, 0x0, 0xc000baf500?})
		/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:59 +0x108
	panic({0x27352c0?, 0x49259f0?})
		/usr/local/go/src/runtime/panic.go:785 +0x132
	sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).initializeFreeCapacityPerDomain(...)
		/workspace/pkg/cache/tas_flavor_snapshot.go:198
	sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).addUsage(...)
		/workspace/pkg/cache/tas_flavor_snapshot.go:193
	sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshotForNodes(0xc001702ba0, {{0x3038760?, 0xc001897800?}, 0x0?}, {0xc0018ac408, 0x3, 0x3?}, {0xc0012c5008, 0x10, 0x10})
		/workspace/pkg/cache/tas_flavor.go:121 +0x730
	sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshot(0xc001702ba0, {0x302f4f0, 0xc0016c9140})
		/workspace/pkg/cache/tas_flavor.go:105 +0x64e
	sigs.k8s.io/kueue/pkg/cache.(*Cache).Snapshot(0xc000828d20, {0x302f4f0, 0xc0016c9140})
		/workspace/pkg/cache/snapshot.go:103 +0x4c5
	sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc000a48820, {0x302f4f0, 0xc0015d6120})
		/workspace/pkg/scheduler/scheduler.go:192 +0x225
	sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
		/workspace/pkg/util/wait/backoff.go:43 +0x2b
	k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0xc000c8c078?)
		/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226 +0x33
	k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc001ec5f30, {0x30018c0, 0xc000c8c078}, 0x0, 0xc001b161c0)
		/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227 +0xaf
	sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x302f4f0, 0xc0015d6120}, 0xc000f8c050, {0x3028410, 0xc000ff2000})
		/workspace/pkg/util/wait/backoff.go:42 +0xd3
	sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x302f4f0, 0xc0015d6120}, 0xc000f8c050)
		/workspace/pkg/util/wait/backoff.go:34 +0x8f
	created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 1123
		/workspace/pkg/scheduler/scheduler.go:147 +0x131
```

**Anything else we need to know?**:

The reason is [here](https://github.com/kubernetes-sigs/kueue/blob/cac26f0b8fba6fae0da089ca3f8d04106bbe16de/pkg/cache/tas_flavor_snapshot.go#L192-L194). If the node is deleted, then we didn't initialize the domainID, then we try to addUsage coming from workload in cache. I believe the simplest fix is to just skip adding usage for such domains. This will prevent panic and allow the workloads to schedule on existing nodes.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-29T18:40:14Z

cc @PBundyra @mwysokin @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T07:14:09Z

/assign swastik959
/assign mimowo

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-02T07:14:12Z

@mimowo: GitHub didn't allow me to assign the following users: swastik959.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3693#issuecomment-2510744079):

>/assign swastik959
>/assign mimowo


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
