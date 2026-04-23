# Issue #6972: Single flavor HFS does work with feature flag  FlavorFungibilityImplicitPreferenceDefault  enabled in 0.13.4

**Summary**: Single flavor HFS does work with feature flag  FlavorFungibilityImplicitPreferenceDefault  enabled in 0.13.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6972

**Last updated**: 2025-09-30T20:51:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nuonuoli2009](https://github.com/nuonuoli2009)
- **Created**: 2025-09-23T22:12:21Z
- **Updated**: 2025-09-30T20:51:10Z
- **Closed**: 2025-09-30T20:50:55Z
- **Labels**: `kind/bug`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Single flavor HFS does work with feature flag  FlavorFungibilityImplicitPreferenceDefault  enabled in 0.13.4
We have a cluster deployed kueue 0.13.4 with HFS enabled. 
in total there are 8 nodes
project 1 has 2 nodes guaranteed and burst up to 8 nodes 
project 2 has 0 nodes guaranteed and burst up to 8 nodes 

1. submit 3*2tasks groups with priority 3 in project 1. All of them go running
2. submit 1*2tasks group with priority 2 in project 1. All of them go running 

Now we are using 8 in project 1, 2 is project guaranteed, 6 is in burst capacity

3. submit 1*2tasks group in project 2 with priority 2. They supposed to trigger one priority 3 task group preemption in project 1 and start running. But actually it does not. 

Events:
  Type     Reason         Age                 From             Message
  ----     ------         ----                ----             -------
  Warning  Pending        91s (x25 over 93s)  kueue-admission  Workload no longer fits after processing another workload
  Normal   QuotaReserved  82s                 kueue-admission  Quota reserved in ClusterQueue tuk5h6cvg73i-test-hfs-scenario-org-2-p4--cq, wait time since queued was 11s
  Normal   Admitted       82s                 kueue-admission  Admitted by ClusterQueue tuk5h6cvg73i-test-hfs-scenario-org-2-p4--cq, wait time since reservation was 0s

**What you expected to happen**:
both project could share half of the burst capacity 

**How to reproduce it (as minimally and precisely as possible)**:
see the description 
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):  
 Client Version: v1.32.2
Kustomize Version: v5.5.0
Server Version: v1.32.7-eks-b707fbb
- Kueue version (use `git describe --tags --dirty --always`): 0.13.4
- Cloud provider or hardware configuration: EKS
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-23T22:13:52Z

/cc

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T08:03:13Z

cc @pajakd @mwysokin

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-24T09:36:09Z

I think that this is WAI. 

First thing to note is that fair sharing does not look at priorities. It makes the decisions what to preempt primarily based on the usage. Secondly, the quota that is guaranteed does not count as shared quota so the fair sharing will only make sure that there is fair access to 6 nodes.

If I understand your setting correctly:
-  6 nodes in shared pool
-  2 are guaranteed to project 1

So, after the admission of the first tasks:
- project 1 is using 2 guaranteed + 4 shared
- project 2 is using 2 shared

So project 1 is using 66% of the shared resource and project 2 is using 33%. It is not very fair, but lets consider the scenario where the preemption does happen:
- project 1 would be using 2 guaranteed + 2 shared
- project 2 would be using 4 shared

Then, project 1 would be using 33% and project 2 would be using 66%. And we don't allow for such preemptions because that would end up in an infinite cycle. Our preemption strategies are best described in the docs (https://kueue.sigs.k8s.io/docs/concepts/preemption/#fair-sharing). 

Let me know if I'm wrong and/or this does not answer your question.

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-24T18:18:44Z

Sorry there was a typo in the description 
in total 8 nodes, project 1, 2 guaranteed 
project 1 has 6 running with priority 3 and 2 running with priority 2 (in total 8 running in project 1)
project submit 2 tasks, but it cannot start running.

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-24T18:23:41Z

after we disable the FlavorFungibilityImplicitPreferenceDefault feature flag

We run the same process:

in total 8 nodes, project 1, 2 guaranteed
project 1 has 6 running with priority 3 and 2 running with priority 2 (in total 8 running in project 1)
project submit 2 tasks, and it could trigger preemption in project 1 tasks and start running

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-25T05:50:53Z

/assign

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-25T08:22:44Z

This is interesting 🤔

I checked the code and tried to reproduce the scenario described. But I'm seeing the preemptions both with and without the FlavorFungibilityImplicitPreferenceDefault feature flag.

The `Workload no longer fits after processing another workload` log suggests that the preemption happened but the preempted workload (from project 1) got admitted again.

Could you please share:
1. clusterqueue configurations. In particular:
- what is the FlavorFungibility configuration
- are you using Admission Fair Sharing?
2. kueue logs of the successful (with FlavorFungibilityImplicitPreferenceDefault disabled) and unsuccessful runs

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T08:43:54Z

@pajakd I haven't tried myself, but maybe there is some interplay with other feature gates, see another issue: https://github.com/kubernetes-sigs/kueue/issues/6971#issuecomment-3329624054

Specifically I'm thinking about `PrioritySortingWithinCohort=false`, wdyt? Maybe worth testing if this is at play here.

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-25T16:54:36Z

Hi This is the feature gate 

--feature-gates=PrioritySortingWithinCohort=false,VisibilityOnDemand=false,MultiplePreemptions=true,FlavorFungibilityImplicitPreferenceDefault=true

and we are using hierarchy fair sharing right now. 

this the fair_share_preemption_strategies we are using now. 

fair_share_preemption_strategies: ["LessThanOrEqualToFinalShare", "LessThanInitialShare"]

Let me collect the cluster queue config

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-30T20:50:29Z

The issue has been fixed after version 0.13.5

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-30T20:51:10Z

/close
