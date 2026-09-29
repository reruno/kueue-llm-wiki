# Issue #9345: [FairSharing] Scheduler chooses workload resulting in unbalanced DRS

**Summary**: [FairSharing] Scheduler chooses workload resulting in unbalanced DRS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9345

**Last updated**: 2026-09-21T18:30:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-02-18T15:50:07Z
- **Updated**: 2026-09-21T18:30:14Z
- **Closed**: 2026-09-21T18:30:14Z
- **Labels**: `kind/bug`, `priority/important-longterm`
- **Assignees**: [@apullo777](https://github.com/apullo777)
- **Comments**: 15

## Description

**What happened**:
During each scheduling cycle, we consider at most 1 workload from each CQ. In certain scenarios, this results in Kueue making scheduling decisions leading to an unfair DominantResourceShare (DRS).

Consider the following scenario:

```
- Root Cohort (4 GPU)
  - CQ-A (0 GPU)
  - CQ-B (0 GPU)
```

Suppose that each workload requests 1 GPU, and that this sequence of events occur:

```
t0: create a0, a1
t1: a0, a1 schedule; DRS(CQ-A): 500
t2: create a2, b0, b1
t3: a2, b0 schedule; DRS(CQ-A): 750, DRS(CQ-B): 250
```
**What you expected to happen**:

The "correct" scheduling decision would have been to schedule both workloads from CQ-B. Many other variations of this can occur (workloads in 1 queue request more resources; another queue has a lower FairSharing weight), but it boils down to the fact that the right scheduling order should be to go deeper into 1 CQ, before scheduling a workload from the other CQ.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
This problem is less pronounced as long as preemption is possible.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2026-02-19T21:25:33Z

@gabesaba What does this mean in practice? Like is it a brief period of preemptions while the tree is balancing correctly?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-20T09:52:11Z

> [@gabesaba](https://github.com/gabesaba) What does this mean in practice? Like is it a brief period of preemptions while the tree is balancing correctly?

Exactly. As long as preemptions are enabled and completed quickly, this is not a big issue. If preemptions are disabled, however, then this issue can result in longer lasting unfairness.

### Comment by [@amy](https://github.com/amy) — 2026-02-20T17:09:01Z

@gabesaba I see. To clarify... when would the DRS tree be used then? Is this for something like admission fairsharing + preemption off?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-21T17:29:41Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-21T18:10:33Z

/remove-lifecycle stale

### Comment by [@amy](https://github.com/amy) — 2026-05-21T18:14:44Z

/priority important-longterm

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-07-06T12:51:09Z

I'm stumbling into this now. I think this was always happening in our clusters. But I found the root issue only now. This causes significant workload churn. I see that we are going through cycles of wasteful admissions and in <~5-10 minutes, all of those workloads admitted in that duration are preempted. 

You can see this in action in these images:

<img width="1388" height="257" alt="Image" src="https://github.com/user-attachments/assets/b76396f7-df82-4011-b8cc-5ae6f8545f06" />


Yellow CQ borrows more and then is later preempted by the Green CQ because Yellow CQ ends up with a higher fair share value than Green CQ.


How the CQ Fair share looks:

<img width="418" height="214" alt="Image" src="https://github.com/user-attachments/assets/aa905e98-6612-4a1e-8dcc-2c537c171e61" />

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-07-06T12:53:55Z

@gabesaba is your suggestion then to try to admit multiple workloads per CQ per cycle so that this imbalance doesn't happen in the first place? I might give that a try

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-06T13:11:26Z

@mukund-wayve one approach we discussed internally in the past (also with @olekzabl) was to pick two items from each CQ (or any fixed number). 

Then, we nominate all the first CQ workloads, and process according to the iterator. Once we admit a workload from a CQ, we need to replace the previous one in the list, finding its new position (re-computing the DRS for the CQ). 

Then we continue processing the list but once we admit the second workload from the CQ we interrupt the scheduling cycle. 

This way we ensure two things:
1. if there is a CQ which has low DRS we will keep admitting its workloads first (fixing the bug)
2. in the typical balanced DRS situation we don't look beyong a fixed number of workloads (2) per CQ so it does not change the asymptotic complexity

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-07-14T17:00:18Z

This is up for grabs! I haven’t been able to find time to fix this yet. It would be great if someone could pick this up and help move it forward.

### Comment by [@amy](https://github.com/amy) — 2026-07-14T17:12:28Z

@mimowo let me know if you have someone in mind on your end. Otherwise was gonna ask wg-batch channel.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-14T17:17:52Z

This is a difficult task, discussing in wg batch is a good idea. I don't have anyone in mind, but better to choose someone with scheduler exp

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-14T17:27:56Z

maybe @apullo777 would like trying. That would be great fro. my PoV

### Comment by [@apullo777](https://github.com/apullo777) — 2026-07-14T20:08:23Z

Happy to take a look at this, thanks @mimowo

/assign

I reproduced the issue and reviewed #12834. The overall approach looks reasonable, and I would be happy to carry it forward in a fresh PR based on @mukund-wayve's work, with attribution :)

### Comment by [@amy](https://github.com/amy) — 2026-07-15T12:33:46Z

@apullo777 please tag me when the pr is ready. Thank you for picking it up!
