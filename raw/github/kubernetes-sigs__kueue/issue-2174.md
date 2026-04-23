# Issue #2174: WaitForPodsReady: After a Workload is deactivated by exceeded the backoffLimit, the reactivated Workload could be immediately re-deactivated

**Summary**: WaitForPodsReady: After a Workload is deactivated by exceeded the backoffLimit, the reactivated Workload could be immediately re-deactivated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2174

**Last updated**: 2024-05-27T15:25:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-09T22:22:40Z
- **Updated**: 2024-05-27T15:25:12Z
- **Closed**: 2024-05-27T15:25:12Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 14

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

After the Workload is deactivated with `.spec.active=false` by exceeded re-queueing backoffLimit, if we manually reactivate it with `.spec.active=true`, it is immediately re-deactivated.

The root cause is the race condition between the workload-controller and kueue-scheduler by not resetting the `.status.requeueState.count` in the Workload while deactivating the Workload here: https://github.com/kubernetes-sigs/kueue/blob/0f0a315fe11704ee85bdc72fdc7f46d76d935a8e/pkg/controller/core/workload_controller.go#L196-L206.

So, the kueue-scheduler could pop the reactivated Workload from the queue before the `.status.requeueState.count` in the Workload here: https://github.com/kubernetes-sigs/kueue/blob/0f0a315fe11704ee85bdc72fdc7f46d76d935a8e/pkg/controller/core/workload_controller.go#L166-L170

Not resetting the `status.requeueState.count` is the intended behavior to notify users how many times the Job was requeued.
But, to avoid this race condition, we need to reset the `count` while deactivating the Workload.

**What you expected to happen**:
The reactivated Workload should be tried to re-queue until backoffLimit.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-09T22:38:26Z

cc: @alculquicondor @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-09T22:41:42Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-09T22:59:23Z

See also: #2175

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-09T23:16:53Z

[REJECTED]

--- 

Instead of resetting `requeueState` and adding a new API like #2175, we may be able to trigger the deactivation via the `Evicted` condition in the workload controller. Let's say the flow:

1. The workload exceeds the backoffLimit
2. The workload controller sets Evicted condition with `ExceedBackoffLimit` instead of setting `.spec.activate=false` here: https://github.com/kubernetes-sigs/kueue/blob/0f0a315fe11704ee85bdc72fdc7f46d76d935a8e/pkg/controller/core/workload_controller.go#L450-L453
3. The jobframework reconciler deactivates the Job instead of the `suspend` here: https://github.com/kubernetes-sigs/kueue/blob/0f0a315fe11704ee85bdc72fdc7f46d76d935a8e/pkg/controller/jobframework/reconciler.go#L413

Additionally, we could avoid requeuing (race condition) the Workload with Evicted by the `ExceedBackoffLimit` here: https://github.com/kubernetes-sigs/kueue/blob/0f0a315fe11704ee85bdc72fdc7f46d76d935a8e/pkg/queue/cluster_queue.go#L172

@alculquicondor @mimowo WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T15:24:10Z

> The jobframework reconciler deactivates the Job instead of the suspend here

It can be done in the workload controller as well.

However, how would a user "reactivate" the job (without having to clear the Evicted condition).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T15:31:37Z

> > The jobframework reconciler deactivates the Job instead of the suspend here
> 
> It can be done in the workload controller as well.

Yes, that's right. If we don't want to add deactivation in the jobframework reconciler, we can implement it in the workload-controller.

> However, how would a user "reactivate" the job (without having to clear the Evicted condition).

Once the Workload is re-activated (`.spec.active: false` ->  `.spec.active: true`), the workload-controller transits Eviction condition True to False during the workload-controller resets the requeueState (`.status.requeueState`).
@alculquicondor Does it sound good?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T15:39:43Z

The above proposal conflicts with step 3 (deactivating when the Evicted condition is set).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T15:47:18Z

> The above proposal conflicts with step 3 (deactivating when the Evicted condition is set).

Oh, you're right...
If we want to avoid resetting the requeueState, we need to update both the `.spec.active` and Evicted condition as a single API call... But, actually those are 2 API calls...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T15:58:28Z

Based on this discussion, I will create a PR to reset the requeueState.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T16:00:53Z

I think we can do the following:

1. Workload exceeds backoffLimit
2. Set active condition to false.
3. The workload controller sees the active field false, and see that there is a requeueState. In one API call: move the requeueState to lastRequeueState and set the Evicted condition to `ExceedBackoffLimit`.

If there is no `requeueState`, the controller assumes that the active field was set by the user instead.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T16:26:29Z

That makes sense. Thanks.
I'm assuming that we can expand the below to implement step 3.

https://github.com/kubernetes-sigs/kueue/blob/2ab58f69992db5689506cc2c6fe91fc338553878/pkg/controller/core/workload_controller.go#L196

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T16:27:52Z

Additionally, we need to add different implementation in the main branch and release-0.6 :(
Because the workload controller evolved much more in the main branch.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T16:39:52Z

Is this bug in 0.6?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T16:47:24Z

> Is this bug in 0.6?

Yes... I introduced this bug in https://github.com/kubernetes-sigs/kueue/pull/1838 :(
As an initial design, we assumed that the webhook resets the `requeueState.count` once the Workload is re-activated, so there is no race condition.
But, after that, we found that we could not perform webhook defaulting against both `spec` and `status.`

So, the root cause is not resetting the `.status.requeueState.count` when the Workload exceeds backoffLimit. That brought us the race condition between scheduler and workload-controller.
