# Issue #9466: [Fair Sharing] Extend nominal-first priority to cohort-level nominal quotas in hierarchical setups

**Summary**: [Fair Sharing] Extend nominal-first priority to cohort-level nominal quotas in hierarchical setups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9466

**Last updated**: 2026-02-28T08:44:21Z

---

## Metadata

- **State**: open
- **Author**: [@mukund-wayve](https://github.com/mukund-wayve)
- **Created**: 2026-02-25T08:26:43Z
- **Updated**: 2026-02-28T08:44:21Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: [@mukund-wayve](https://github.com/mukund-wayve)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

PR #9407 (fixing #9406) ensures that workloads fitting within their ClusterQueue's nominal quota are prioritized in fair sharing admission ordering and preemption, regardless of the CQ's DRS from borrowing on other flavors. 

However, this fix only operates at the CQ level.
In hierarchical cohort setups, the same class of bug exists at the cohort level. A cohort has its own nominal quota in addition to it's ClusterQueues' quota, and descendants of that cohort should have preferential access to resources within that cohort's nominal allocation. Today, even with #9407, the DRS comparison at an ancestor cohort can deprioritize a workload whose entire subtree is within nominal — solely because of borrowing on a different flavor.

**What you expected to happen**:

The nominal-first principle should apply at every level of the cohort hierarchy: if a workload's usage (including the incoming workload) stays within the nominal quota of its ancestor cohort for the contested flavor-resources, that workload should be preferred at that level of comparison — regardless of the ancestor's aggregate DRS from borrowing on other flavors.

**How to reproduce it (as minimally and precisely as possible)**:

Setup — two flavors (h100-reserved, a10-spot), hierarchical cohort tree:

```
Root
├── Cohort1 (own nominalQuota: 40 h100-reserved GPUs — shared pool for its members)
│   ├── CQ-A  (nominal: 10 h100-reserved, using 8; borrowing 200 a10-spot from Root)
│   └── CQ-B  (nominal: 20 h100-reserved, using all 20 — fully utilized, nothing to lend)
│
└── Cohort2 (no own quota)
    └── CQ-C  (nominal: 30 h100-reserved, using 28)
```

CQ-A submits a workload needing 5 h100-reserved GPUs:
- CQ-A usage becomes 13, exceeding CQ-A's nominal of 10 — #9407 does not apply.
- CQ-B is fully utilizing its 20 GPUs — there is nothing to borrow from CQ-B.
- The extra 3 GPUs come from Cohort1's own shared pool of 40.
- Cohort1 SubtreeQuota = 40 (own) + 10 (CQ-A) + 20 (CQ-B) = 70. Cohort1 usage = 13 + 20 = 33, within 70. Cohort1 is not borrowing from Root.

CQ-C submits a workload needing 5 h100-reserved GPUs:
- CQ-C usage becomes 33, exceeding CQ-C's nominal of 30.
- Cohort2 SubtreeQuota = 30 (CQ-C only, no own quota). Usage = 33 > 30. Cohort2 must borrow from Root.

Observed: At the Root-level comparison, Cohort1 has higher DRS (inflated by 200 a10-spot borrowing), so CQ-C's workload is ordered first — even though CQ-C's cohort needs to borrow from Root while CQ-A's cohort is using its own shared pool.

Expected: CQ-A's workload should be preferred. CQ-A is using resources from Cohort1's own shared pool — not borrowing from CQ-B (which has nothing to spare), and not borrowing from Root. Cohort1's a10-spot borrowing should not block its members from accessing Cohort1's own h100-reserved quota.

The same issue applies to fair sharing preemption: if CQ-A needs to preempt a workload from CQ-C to fit, the DRS strategy gate may block the preemption because Cohort1's DRS exceeds Cohort2's DRS — even though Cohort1 is within its own nominal quota for the contested resource.

**Anything else we need to know?**:

This was identified by @pajakd [during review of PR #9407](https://github.com/kubernetes-sigs/kueue/pull/9407#issuecomment-3943059429):
> This PR looks good but will work for using nominal quota of CQ. But in more complex hierarchies, there could be a nominal quota of a cohort for which the descendants of that cohort should have a preferential access, right?
>
> CQ1 -> Cohort1 -> Root
> CQ2 -> Cohort2 -> Root
>
> In the above example if CQ1 and CQ2 were competing for nominal quota in Cohort1, then CQ1 should be preferred, regardless if it is borrowing more in some other flavor.

**Environment**: 

Kubernetes version (use kubectl version): v1.33.5
Kueue version (use git describe --tags --dirty --always): v0.15.2
Cloud provider or hardware configuration: Azure Kubernetes Service
OS (e.g: cat /etc/os-release): Linux

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-28T08:44:19Z

/assign @mukund-wayve
