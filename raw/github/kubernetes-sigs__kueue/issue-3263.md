# Issue #3263: Can the event type in insufficient resource wait situations be changed from `Normal` to `Warning`?

**Summary**: Can the event type in insufficient resource wait situations be changed from `Normal` to `Warning`?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3263

**Last updated**: 2024-10-18T14:35:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kebe7jun](https://github.com/kebe7jun)
- **Created**: 2024-10-18T10:30:08Z
- **Updated**: 2024-10-18T14:35:05Z
- **Closed**: 2024-10-18T14:35:05Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Now, when resources are insufficient and cannot be scheduled, an event will be recorded in the Workload, but the event type is Normal.

```
Events:
  Type    Reason   Age   From             Message
  ----    ------   ----  ----             -------
  Normal  Pending  11s   kueue-admission  couldn't assign flavors to pod set worker: insufficient quota for cpu in flavor default-flavor in ClusterQueue
```

In our system, we will focus on `Warning` type events, so `Normal` is likely to be filtered out, but obviously, this is likely to be the culprit of the application being unable to start.

So, I was wondering if I could change the type here to Warning?

https://github.com/kubernetes-sigs/kueue/blob/9332a5a3d911f191de262e41fe0508e9bccc2d77/pkg/scheduler/scheduler.go#L695

**Why is this needed**:

Changing its type to `Warning` will increase our attention and help users more quickly troubleshoot the reason why the workload cannot be started.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-18T10:42:03Z

Maybe, IIUC this [doc](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md#changing-the-api) doesn't specify expectations for events API. IIUC they are mostly for informative purposes, so backwards compatibility does not seem an issue.

I checked that `kube-scheduler` produces Warning `FailedScheduling` event in based on that: https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#example-debugging-pending-pods.

/cc @tenzen-y @alculquicondor @mwielgus   in case you have some opinions here.

### Comment by [@kebe7jun](https://github.com/kebe7jun) — 2024-10-18T13:08:01Z

I submitted a PR for this issue, feel free to discuss.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-18T13:29:32Z

Yeah, it sounds reasonable to match the same type as kube-scheduler.
