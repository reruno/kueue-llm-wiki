# Issue #1974: Too many preemptions within ClusterQueue when already above nominal quota

**Summary**: Too many preemptions within ClusterQueue when already above nominal quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1974

**Last updated**: 2024-04-17T15:50:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-11T22:32:53Z
- **Updated**: 2024-04-17T15:50:45Z
- **Closed**: 2024-04-17T15:50:45Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 9

## Description

**What happened**:

In #614, we allowed preemption to happen when a CQ is above nominal, with an end state where the CQ continues to be above nominal quota. However, the circumstances in which that happens are hard to predict.
More commonly, we do preemptions until the incoming workload and the already running workloads fit within the nominal quota only (no borrowing).
This is encoded here:
 https://github.com/kubernetes-sigs/kueue/blob/3347afb5a8681f4fd2a5f3b1a5be8c5c0ebac488/pkg/scheduler/preemption/preemption.go#L119-L125

There are two problems with this approach:
1. It can lead to a lot of unnecessary preemptions. In one case that was diagnosed in a real cluster, a high priority job that uses all of the nominal quota caused the preemption of all running workloads.
2. It's extremely hard to explain to users what the behavior is.

**What you expected to happen**:

I propose the following rules for preemption:

1. A workload is only eligible to do preemptions if it fits fully within nominal quota (current behavior).  _Rationale: If the workload goes above nominal by itself, then it's an easy target for preemption, losing all the advantage of preemption_ https://github.com/kubernetes-sigs/kueue/blob/3347afb5a8681f4fd2a5f3b1a5be8c5c0ebac488/pkg/scheduler/flavorassigner/flavorassigner.go#L555-L560
2. If existing workloads are under nominal, the workload is eligible to preempt from other cluster queues and from its own workloads (fits within existing behavior), but, in the final result, the CQ is not above nominal. _Rationale: if it was only able to preempt from its own clusterqueue, and all the resources are being borrowed by someone else, then the workload wouldn't fit in the cluster, even if it's under nominal_  https://github.com/kubernetes-sigs/kueue/blob/3347afb5a8681f4fd2a5f3b1a5be8c5c0ebac488/pkg/scheduler/preemption/preemption.go#L119
3. If existing workloads are above nominal (in other words, currently borrowing) and the workload fits within nominal by itself (rule 1), **the workload is only eligible to preempt workloads from its own cluster queue, but the end result of running workloads is allowed to be above nominal**. Note that here there is no risk of affecting other CQs in the cohort (this would be new behavior).

Once implemented, we should add the rules above into the user documentation.

**How to reproduce it (as minimally and precisely as possible)**:

- 3 CQs, A, B, C of with nominal quota 2 each and no borrowing limit.
- A has 3 workloads of size 1 with priority `-1`
- C has 3 workloads of size 1 with priority `0`
- A new workload of size 2 for CQ A of priority `0` comes in

Current behavior: all running workloads in A are preempted.
Wanted behavior: only 2 workloads in A are preempted.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-11T22:33:06Z

/assign @mimowo 

FYI @tenzen-y

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-12T12:26:02Z

We can also consider dropping the limitation described in point 1: `A workload is only eligible to do preemptions if it fits fully within nominal quota`.

Just rules 2 and 3, in combination, seem easier to explain in user documentation.

UPDATE: discarded this approach, see https://github.com/kubernetes-sigs/kueue/issues/1974#issuecomment-2051866435

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-12T12:33:03Z

I'm wondering if we can just change the behavior, or should make it opt-it by config, or feature gate. 

I think it is unlikely someone would rely on previous behavior, but a feature gate (that enables the new behavior by defailt, but let's some users to revert) might be safer. WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-12T13:00:38Z

yes, a feature gate could help

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-12T14:26:24Z

@mimowo and I discussed offline and decided against https://github.com/kubernetes-sigs/kueue/issues/1974#issuecomment-2051664155 for two reasons:

- we cannot really guarantee that the freed quota is used by the workload causing the preemptions.
- it increases the size of the patch, so it's more risky to cherry-pick.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-15T19:20:43Z

> @mimowo and I discussed offline and decided against [#1974 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1974#issuecomment-2051664155) for two reasons:
> 
> * we cannot really guarantee that the freed quota is used by the workload causing the preemptions.
> * it increases the size of the patch, so it's more risky to cherry-pick.

SGTM. I think that dropping the limitation described in point 1 would bring us slightly aggressive behavior.
The batch admins should increase nominalQuota when the admins face the situation.

BTW, It seems that there are not any document updates.
@mimowo Could you work on it?

> Once implemented, we should add the rules above into the user documentation.

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-15T19:20:47Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1974#issuecomment-2057637296):

>> @mimowo and I discussed offline and decided against [#1974 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1974#issuecomment-2051664155) for two reasons:
>> 
>> * we cannot really guarantee that the freed quota is used by the workload causing the preemptions.
>> * it increases the size of the patch, so it's more risky to cherry-pick.
>
>SGTM. I think that dropping the limitation described in point 1 would bring us slightly aggressive behavior.
>The batch admins should increase nominalQuota when the admins face the situation.
>
>BTW, It seems that there are not any document updates.
>@mimowo Could you work on it?
>
>> Once implemented, we should add the rules above into the user documentation.
>
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-16T07:33:57Z

> BTW, It seems that there are not any document updates.
> @mimowo Could you work on it?

Sure, I will open a PR documenting the current set of rules. 

I guess I will put them [here](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption) for now, but it would be nice to have a docs page devoted to preemption at some point, as proposed [here](https://github.com/kubernetes-sigs/kueue/issues/1587).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-16T15:30:47Z

> > BTW, It seems that there are not any document updates.
> > @mimowo Could you work on it?
> 
> Sure, I will open a PR documenting the current set of rules.
> 
> I guess I will put them [here](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption) for now, but it would be nice to have a docs page devoted to preemption at some point, as proposed [here](https://github.com/kubernetes-sigs/kueue/issues/1587).

SGTM, thank you!
