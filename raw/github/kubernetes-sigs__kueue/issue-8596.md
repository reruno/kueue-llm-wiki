# Issue #8596: Workload Admitted and PodsReady Timestamp regression

**Summary**: Workload Admitted and PodsReady Timestamp regression

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8596

**Last updated**: 2026-01-16T00:12:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2026-01-14T21:28:45Z
- **Updated**: 2026-01-16T00:12:54Z
- **Closed**: 2026-01-15T12:39:38Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
This is a change we observed moving from version 0.13.x to 0.15.2 - We extracted the workload admitted, QuotaReserved and podsReady information from the Workload Conditions. Earlier, these conditions did not flip to False when the workload got completed, so we had the correct timestamps on these conditions, however, after the Kueue upgrade, all these 3 conditions flip to False on workload completion (which seems fair enough). Due to this, the last transition time changes and we no longer have a way to get the exact time when these conditions were set.


**What you expected to happen**:
Apart from the Workload events which are not permanent, is there any reliable way to get this information for the workload as this breaks prior functionality.

**How to reproduce it (as minimally and precisely as possible)**:

1. Submit a workload
2. Wait for its completion
3. Describe the workload and check for the status:

```
Conditions:
    ...
    Status:                False
    Type:                  PodsReady
    ...
    Status:                True
    Type:                  QuotaReserved
    ...
    Status:                True
    Type:                  Admitted
    ...
    Status:                True
    Type:                  Finished
```

**Anything else we need to know?**:

There is also a section about `Status.Admission` which has useful information on workload resource usage, which disappears after the workload is completed - something which persisted in earlier versions. 

**Environment**:
- Kubernetes version (use `kubectl version`): v1.33.5
- Kueue version (use `git describe --tags --dirty --always`): v0.15.2
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`): 
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-14T22:32:20Z

cc @mbobrovskyi 

I seem to remember you working this area recently.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T07:54:43Z

Indeed, this has changed. The original motivation for the change was to flip `QuotaReserved=False` to clearly indicate the quota is released, and simplify working on https://github.com/kubernetes-sigs/kueue/pull/6477. 

In the process of doing the change we observed this also flips `Admitted` to False, but took decision to also flip `Admitted` and `PodsReady` (clearly underestimating the way people rely on the Workload object). I think clearing the `Admission` field is an unexpected consequence, and we should revert that.  

So the options I can see:
1. call it all a bad decision and don't flip `QuotaReserved` to `False` 
2. flip `QuotaReserved` to `False`, but revert flipping any other conditions, and clearing the `status.Admission` field
3. keep as is, but provide the information in other ways

As for (3.) you could probably get the information from a watch where you check all the transitions of the `Admitted` condition, but surely this is troublesome. Another alternative would be to check the `status.accumulatedPastExecutionTimeSeconds` - it does not give you timestamp, but actual accumulated running time, also including time before evictions (eg. preemptions).

I'm leaning towards (2.) to preserve the original intention, while minimizing the impact on other conditions and calling them a bug. Would (2.) be ok for you @varunsyal? In that case we could backport the fix.  I'm also ok with (1.). Let me check what @tenzen-y or @gabesaba think.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T08:41:44Z

FYI: I have also synced with @mbobrovskyi who suggests going with (1.) as the safest option as it basically means reverting the relatively small PR https://github.com/kubernetes-sigs/kueue/pull/7724, because for (2.) it is tricky to decouple setting `QuotaReserved=False` and `Admitted=False`. 

So maybe (1.), because it is the simplest. Also, we haven't yet achieved the goal of https://github.com/kubernetes-sigs/kueue/pull/6477 so we can re-consider how to do it best on another attempt.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-15T09:33:41Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T10:35:08Z

AFAIK, conditions are observed states, and they do not have a complete state transition or a historical state.
This is not Kueue specific concept, and it is a common Kubernetes concept: https://github.com/kubernetes/community/blob/92cda8d8ea6306599ebb4f813079fc5b1cf83220/contributors/devel/sig-architecture/api-conventions.md?plain=1#L484-L487

So, I think that observed conditions are Admitted=False, QuotaReserved=False, PodsReady=False sounds reasonable.
If we want to preserve the historical state data (e.g., admission), we should leverage https://github.com/kubernetes-sigs/kueue/blob/893ac75aebc20df200ebd8a59e3788a7909be166/apis/kueue/v1beta2/workload_types.go#L634-L637 field.

If we eventually expand the schedulingStats field and use Admitted=False, QuotaReserved=False, PodsReady=False after the workload finishes, I agree with (1) because our previous decision lacked consideration for existing users, which broke their production.

In other words, (1) is acceptable for a temporary solution to save their production for now, but eventually, we should use Admitted=False, QuotaReserved=False, PodsReady=False for finished workloads (and expanded schedulingStats).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T10:43:49Z

Thank you for the input! So, let's proceed with (1.) and re-consider setting the conditions to False only after some API (like `status.schedulingStats`) can preserve the historical information useful for the users.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T10:46:24Z

> Thank you for the input! So, let's proceed with (1.) and re-consider setting the conditions to False only after some API (like `status.schedulingStats`) can preserve the historical information useful for the users.

@mimowo  That sounds great to me 🥇 

@varunsyal Thank you for reporting this impact on your platform!

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-15T13:40:08Z

> Thank you for the input! So, let's proceed with (1.) and re-consider setting the conditions to False only after some API (like status.schedulingStats) can preserve the historical information useful for the users.

lgtm as well.

### Comment by [@varunsyal](https://github.com/varunsyal) — 2026-01-16T00:12:54Z

Thanks all for addressing this quickly!
