# Issue #6789: Race Condition Prevents Workload from Reflecting Inadmissible Status

**Summary**: Race Condition Prevents Workload from Reflecting Inadmissible Status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6789

**Last updated**: 2025-11-25T07:56:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-11T04:24:53Z
- **Updated**: 2025-11-25T07:56:37Z
- **Closed**: 2025-11-25T07:56:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**

The `Workload` status is not always updated to reflect the `Inadmissible` condition, even when the workload is clearly unschedulable under current cluster conditions. This leads to confusion for users and limits the usefulness of status-based observability for automation or debugging.

Note: A `Warning` event is correctly recorded, and the scheduler logs the following message:

```
"couldn't assign flavors to pod set main: insufficient unused quota for cpu in flavor default-flavor, 100m more needed"
```

**What you expected to happen**

When a workload cannot be admitted due to unmet scheduling constraints (e.g., resource quota, flavor mismatch, node selector, etc.), its `.status.conditions` should reflect the `Inadmissible` condition with an appropriate `reason` and `message`.

**Anything else we need to know?**

I believe this issue is caused by a race condition between the scheduler and the workload controller. The scheduler logs the following error:

```
{"level":"error","ts":"2025-09-10T20:56:50.879693-07:00","logger":"scheduler","caller":"scheduler/scheduler.go:776","msg":"Could not update Workload status","schedulingCycle":2,"error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"job-demo-2-56c73\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"..."}
```

When the scheduler fails to patch the admission status, it merely [logs the error](https://github.com/kubernetes-sigs/kueue/blob/a3887653ef8e71ef892afd327e9c0b35fc2471f9/pkg/scheduler/scheduler.go#L776) and relies on a future scheduling cycle to reattempt scheduling and update the workload status. However, unlike a controller-runtime reconciler, the scheduler does **not** immediately retry this workload scheduling, leading to status drift.

This results in workloads appearing pending without any `Inadmissible` condition, even though their scheduling failure is known and logged.

### **How to reproduce it (as minimally and precisely as possible)**

I encountered this issue in a MultiKueue setup, though I do not believe it is exclusive to MultiKueue.

**MultiKueue setup:**

* `worker1`: 2 CPUs
* `worker2`: 2 CPUs
* `manager`: 4 CPUs (aggregated)

**Steps:**

1. Submit a job requesting 3 CPUs — this will be placed and block quota in the manager cluster but won't fit in any worker cluster.
2. Submit a second job requesting `1100m` CPU.
3. Observe the second workload — in many cases, it will remain in `Pending` without an `Inadmissible` condition, even though it cannot be scheduled due to quota blockage.

In this setup, I can reproduce the issue with a frequency > 50%.

### **Environment**

* **Kubernetes version** (use `kubectl version`):
* **Kueue version** (use `git describe --tags --dirty --always`):
* **Cloud provider or hardware configuration**:
* **OS** (e.g., `cat /etc/os-release`):
* **Kernel** (e.g., `uname -a`):
* **Install tools**:
* **Others**:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-25T02:32:49Z

/cc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T02:52:35Z

Yes, this is a typical race condition. After we switch from SSA operation to PATCH operation, Kueue will face this race error more and more.
So, we are planning to implement retry mechanism for PATCH operation https://github.com/kubernetes-sigs/kueue/issues/6992

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T04:13:25Z

We should be mindful that not all failures are recoverable. In the case of a race condition, if we apply a patch with *strict* validation and the object is stale (has an older resource version), that patch will **never** succeed unless we either:

* relax the strict rule (i.e., ignore the resource version), or
* fetch a fresh version of the object and re-apply the patch.

Both approaches come with potential drawbacks.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T04:19:38Z

> We should be mindful that not all failures are recoverable. In the case of a race condition, if we apply a patch with _strict_ validation and the object is stale (has an older resource version), that patch will **never** succeed unless we either:
> 
> * relax the strict rule (i.e., ignore the resource version), or
> * fetch a fresh version of the object and re-apply the patch.
> 
> Both approaches come with potential drawbacks.

Yes, that's right. So, I proposed to retry PATCH only when Conflict errors happen.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T04:22:39Z

 I’m not sure a retry mechanism on its own would address **conflict** errors.

Conflicts usually look like this:

```
Operation cannot be fulfilled on jobs.batch "test": the object has been modified; please apply your changes to the latest version and try again
```

In those cases, retrying the same patch against the same resource version will still fail, typically the object needs to be fetched again and the patch reapplied.

Another option could be to use a non-strict patch (ignoring `resourceVersion`), but that might risk applying stale data over newer changes.

So while retries can definitely help with transient issues (timeouts, connection hiccups, etc.), conflicts may need a slightly different approach that involves refreshing the object first.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T04:37:10Z

@ichekrygin Sorry for your confusion. My `retry` semantic is 

1. Re-obtain a object
2. Re-patch to the object

https://github.com/kubernetes/client-go/blob/master/util/retry/util.go could hope to understand what we are planning.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T04:38:51Z

Yep, I missed the "re-obtain" part. Makes sense.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T11:50:11Z

/assign @mbobrovskyi 
Who is already working on the patch retry mechanism I can see under https://github.com/kubernetes-sigs/kueue/issues/6992

An additional comment is that in this case SSA and Patch does not matter, because the code here https://github.com/kubernetes-sigs/kueue/blob/0c661099c94fb3d44b3c586c914ea70460f29f96/pkg/scheduler/scheduler.go#L781-L786 is not using WithLooseOnApply, and thus resourceVersion is compared even for SSA.

I think to solve this issue we could use `WithLooseOnApply`. 

For Patch we can continue on the re-obtain and retry mechanism

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T11:54:52Z

Also note that there is no guarantee that the condition "`QuotaReserved: False" is set by kueue scheduler anyway. It is only set for the workload in the head of the queue. 

However, if you have a long queue of workloads then it is not going to be tagged with the condition for long. We could consider also setting `QueueReserved: False, Reason: Queued` set by workload_controller, but this means an extra request per workload, but IIUC this is not requested here.
