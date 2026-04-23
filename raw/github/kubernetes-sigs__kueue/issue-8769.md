# Issue #8769: LeaderWorkerSet pods get stuck during rolling updates

**Summary**: LeaderWorkerSet pods get stuck during rolling updates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8769

**Last updated**: 2026-02-10T20:01:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PannagaRao](https://github.com/PannagaRao)
- **Created**: 2026-01-23T17:35:07Z
- **Updated**: 2026-02-10T20:01:40Z
- **Closed**: 2026-02-10T20:01:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: 

During the rolling update, the surge/extra replica pods get stuck in Pending (SchedulingGated) and never transition to Running. As a result, the rolling update cannot make progress and does not complete.

**What you expected to happen**:

I expected the rolling update to complete successfully. Surge replica pods should be created as part of the update to allow progress, and once the update finishes, the extra replicas should be terminated so the system converges back to the desired replica count.

**How to reproduce it (as minimally and precisely as possible)**:

- Apply a LeaderWorkerSet manifest with a rolling update strategy, for example:

```
metadata:
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  rolloutStrategy:
    type: RollingUpdate
    rollingUpdateConfiguration:
      maxUnavailable: 2
      maxSurge: 2
```

- Wait for the initial pods to be created successfully.

- Modify the LeaderWorkerSet template (for example, change a container command or sleep duration).

- Reapply the manifest and observe the rolling update getting stuck.


Kueue Version : v0.16.0-rc.0
LeaderWorkerSet (LWS): v0.7.0

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-23T17:39:02Z

Could you provide more information on your Kueue setup and the LWS manifest?

Is the workload being gated because there isn't enough quota for the extra pods?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-23T17:42:10Z

One thing that could be useful is to see if you can reproduce this as a e2e test. That could make it easier to propose a fix.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-23T17:47:07Z

Could you also share LWS and Kueue versions?
Kueue LWS is moving very fast, so this might be a previous Kueue-specific one.

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-01-23T19:42:16Z

> Could you provide more information on your Kueue setup and the LWS manifest?
> 
> Is the workload being gated because there isn't enough quota for the extra pods?

I don't think the issue here is quota. In the exmaples I created, there was still plenty of quota available and Kueue logs show "error":"prebuilt workload not found"

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-01-23T19:43:06Z

> Could you also share LWS and Kueue versions? Kueue LWS is moving very fast, so this might be a previous Kueue-specific one.

I have added the versions. I was able to replicate the issue in the latest version of Kueue (even on main)

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-26T17:11:11Z

https://github.com/kubernetes-sigs/kueue/issues/8440

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-01-26T21:39:49Z

> One thing that could be useful is to see if you can reproduce this as a e2e test. That could make it easier to propose a fix.

I have added a PR with a possible fix and corresponding e2e in https://github.com/kubernetes-sigs/kueue/pull/8801. PTAL!

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-01-27T19:43:27Z

/assign @PannagaRao

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-10T19:38:40Z

@PannagaRao can we close this?

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-02-10T19:51:51Z

Yes, the PR with related fix is merged. https://github.com/kubernetes-sigs/kueue/pull/8801

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-10T20:01:33Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-10T20:01:39Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8769#issuecomment-3880400992):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
