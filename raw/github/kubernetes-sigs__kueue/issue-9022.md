# Issue #9022: Eliminate the global state RayJob reconciler

**Summary**: Eliminate the global state RayJob reconciler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9022

**Last updated**: 2026-02-11T18:31:59Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-06T08:44:35Z
- **Updated**: 2026-02-11T18:31:59Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The current WIP PR https://github.com/kubernetes-sigs/kueue/pull/8341 is introducing the global state, following the pattern for TrainJob, but we should fix it going forward also for TrainJob: https://github.com/kubernetes-sigs/kueue/issues/9021

**Why is this needed**:

To avoid non-obvious failures in MultiKueue integration tests, motivation as for https://github.com/kubernetes-sigs/kueue/issues/9021

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T20:33:10Z

@hiboyang would you maybe find cycles to take the issue as you have already all the context? At the technical level I'm considering two options:
1. extend the PodSets interface
2. store the client inside the reconciler instance and allow to retrieve it via [JobReconcilerInterface](https://github.com/kubernetes-sigs/kueue/blob/c203cb5e688cfdd90a81ec660fc26bf170040391/pkg/controller/jobframework/integrationmanager.go#L50-L53). 

I think it makes sense to go for (2.) because it already has `SetupWithManager` and the lifetime of "client" is the same as "manager". Also, we will then have the client available in all functions, not just "PodSets" for free, wdyt?

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-08T07:03:55Z

Sounds good, I will work on this, will take a look at [JobReconcilerInterface](https://github.com/kubernetes-sigs/kueue/blob/c203cb5e688cfdd90a81ec660fc26bf170040391/pkg/controller/jobframework/integrationmanager.go#L50-L53). Thanks for the pointer!

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-09T06:27:08Z

@mimowo I am looking at [JobReconcilerInterface](https://github.com/kubernetes-sigs/kueue/blob/c203cb5e688cfdd90a81ec660fc26bf170040391/pkg/controller/jobframework/integrationmanager.go#L50-L53), it is possible to pass a "client" to the reconciler by extending `SetupWithManager` method, but we still need some way to pass the "client" to `GenericJob.PodSets(ctx context.Context)`, which does not have reference to the reconciler.

How do you like the idea to create another interface like `GenericJobV2` (could be other name), `GenericJobV2` extends `GenericJob` with an extra method `FetchPodSets(ctx context.Context, c client.Client)`. RayJob will implement `GenericJobV2`. This will not break backward compatibility.

Or add a new interface (similar like other single method interface like `JobWithPodLabelSelector`):
```
type JobWithFetchPodSets interface {
	FetchPodSets(ctx context.Context, c client.Client) ([]kueue.PodSet, error)
}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T11:21:20Z

I think `JobWithFetchPodSets` is an unnecessary complication. 

I'm ok with extending the PodSets interface for 0.17, unless maybe @tenzen-y has a better idea. Or maybe @kaisoz who work on TrainJob which also have the global state issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-09T19:19:55Z

Sorry I have no context for this issue. Could you point the root cause the reason why eliminating RayJob reconciller? Does that mean that you want to follow the similar pattern with LWS / StatefulSet?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T19:25:41Z

Not the reconciler as such, just the global state: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/trainjob/trainjob_controller.go#L87

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T09:25:01Z

Looked at this again, and I think extending the PodSet interface is actually also is consistent with what we already do here: https://github.com/kubernetes-sigs/kueue/blob/b228c433eb904202c28ad8dcab1509ad380e86a1/pkg/controller/jobframework/interface.go#L99

So, I'm ok with that. I don't see a need for `JobWithFetchPodSets`

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-11T17:31:33Z

Cool, you mean add `GenericJobV2` to extend `GenericJob`, like following?
```
type GenericJobV2 interface {
    GenericJob
    FetchPodSets(ctx context.Context, c client.Client) ([]kueue.PodSet, error)
}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T17:50:42Z

I meant to just change the existing interface, having two functions `PodSets` and `FetchPodSets` is not needed, I think

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-11T18:31:59Z

Sounds good, let me just change the existing interface.
