# Issue #1555: A pending workload that's deleted is still listed in the visibility API `pendingworkloads` results

**Summary**: A pending workload that's deleted is still listed in the visibility API `pendingworkloads` results

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1555

**Last updated**: 2024-02-05T17:00:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-01-08T16:07:29Z
- **Updated**: 2024-02-05T17:00:21Z
- **Closed**: 2024-02-05T17:00:21Z
- **Labels**: `kind/bug`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 5

## Description

**What happened**:

If a pending workload is deleted, querying the visibility API stills reports the workload. 

**What you expected to happen**:

The workload should not be listed in the `pendingworkloads` sub-resource after it's deleted.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a workload such that it's going to be pending
2. Delete the job / workload
3. Query the visibility API

**Anything else we need to know?**:

Once the operator Pod is deleted / has restarted, the results are corrected.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.3
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-devel-146-ged81667f-dirty

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-26T13:06:33Z

Interesting, because the visibility API serves on-demand the data directly from the in-memory cache used by scheduler, which suggests the cache itself is not updated. Did you have a chance to check if the `PendingWorkloads` counter is correct: https://github.com/kubernetes-sigs/kueue/blob/1adca158dcb0aa77e00987a8cf37c35d17c64744/apis/kueue/v1beta1/clusterqueue_types.go#L230?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-26T13:47:01Z

> Interesting, because the visibility API serves on-demand the data directly from the in-memory cache used by scheduler, which suggests the cache itself is not updated.

Right, that'd be my understanding as well. I had traced it down to:

https://github.com/kubernetes-sigs/kueue/blob/1adca158dcb0aa77e00987a8cf37c35d17c64744/pkg/controller/core/workload_controller.go#L406-L408

For a pending workload, `workload.HasQuotaReservation(wl)` returns false, which skips the cache update.

Naively, I'd think that if statement could / should be removed. But I wanted to understand why it's been added in the first place, and if it's correct / safe to remove it.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-26T13:49:46Z

/cc @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T17:30:24Z

oh shoot, this is a bug introduced here: https://github.com/kubernetes-sigs/kueue/commit/57c714d2512519ecf27b4869d0dfb5b9c87be111#diff-60dd240c20adbd6a189d018d1c216c2d296730f446c341d8bf449fa6657964ffR242

it went from `admission==nil` to `IsWorkloadAdmitted`.

I think removing the `if` (always clear from queues) should be fine too.

And please add an integration test.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-29T17:16:59Z

/assign
