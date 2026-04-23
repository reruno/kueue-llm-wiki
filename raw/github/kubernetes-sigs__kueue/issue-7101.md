# Issue #7101: preemption bug with LessThanOrEqualToFinalShare and infinite preemption, v0.13.5

**Summary**: preemption bug with LessThanOrEqualToFinalShare and infinite preemption, v0.13.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7101

**Last updated**: 2025-10-07T15:05:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-30T22:19:28Z
- **Updated**: 2025-10-07T15:05:03Z
- **Closed**: 2025-10-07T15:05:03Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Note: There are 2 parts to this bug
1. preemption should happen in step 4 below
2. infinite preemption should not occur in step 5

<img width="1127" height="638" alt="Image" src="https://github.com/user-attachments/assets/8c2aef3e-783e-4217-ae1c-2de39ed5481e" />

1. proj-1: submit 4 podgroups. Each podgroup with 2 pods.
  ✅ Meets expectation: all 4 workloads get admitted
2. proj-2: submit 1 podgroup. podgroup has 6 pods.
  ✅ Meets expectation: 6 pod podgroup workload is not admitted
3. proj-2: submit 1 podgroup. podgroup has 5 pods.
  ✅ Meets expectation: 5 pod podgroup workload is not admitted
4. proj-2: submit 1 podgroup. podgroup has 4 pods.
  ❌ Does not meet expectation: 4 pod podgroup workload is not admitted.
  the ratio goes from 0:8 to 4:4. Which meets LessThanOrEqualToFinalShare requirement. 
5. proj-2: submit 1 podgroup. podgroup has 3 pods.
  ❌ ??? seems to trigger infinite preemption?
  I run `kubectl get workloads -w` -> see preemption flapping for a while
  `kubectl describe workload workload-123` -> see that it was preempted over 33 times (and counting)

Expanding 4, I also tried this:
1. proj-1: submit 4 podgroups. Each podgroup with 2 pods.
  ✅ Meets expectation: all 4 workloads get admitted
2. proj-2: submit 1 podgroup. podgroup has 4 pods.
  ❌ Does not meet expectation: 4 pod podgroup workload is still not admitted.

**Anything else we need to know?**:
CQ sample
```
  fairSharing:
    weight: 1.0
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      maxPriorityThreshold: 80000
      policy: LowerPriority
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
```

kueue controller v0.13.5, featureflags:
```
 --feature-gates=PrioritySortingWithinCohort=false,VisibilityOnDemand=false,FlavorFungibilityImplicitPreferenceDefault=true
```

kueue configmap fairshare settings:
```
    fairSharing:
      enable: true
      preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-10-01T00:32:58Z

I was able to reproduce the same, and observed that even at `step 4: proj-2: submit 1 podgroup. podgroup has 4 pods`, the last submitted workload in proj-1 goes into a preemption loop. Describing the workload, the events look like the following:
```
Events:
  Type     Reason                 Age                     From                  Message
  ----     ------                 ----                    ----                  -------
  Normal   QuotaReserved          4m36s (x2 over 9m23s)   kueue-admission       Quota reserved in ClusterQueue org-1-proj-1--cq, wait time since queued was 0s
  Normal   QuotaReserved          4m35s                   kueue-admission       Quota reserved in ClusterQueue org-1-proj-1--cq, wait time since queued was 2s
  Normal   EvictedDueToPreempted  2m49s                   kueue-admission       Preempted to accommodate a workload (UID: 527a9fa8-fb86-4116-b295-4f4dd72e478f, JobUID: UNKNOWN) due to Fair Sharing within the cohort
  Normal   Preempted              2m49s                   kueue-admission       Preempted to accommodate a workload (UID: 527a9fa8-fb86-4116-b295-4f4dd72e478f, JobUID: UNKNOWN) due to Fair Sharing within the cohort
  Normal   Admitted               2m47s (x7 over 9m23s)   kueue-admission       Admitted by ClusterQueue org-1-proj-1--cq, wait time since reservation was 0s
  Normal   EvictedDueToPreempted  2m47s (x5 over 4m36s)   kueue-admission       Preempted to accommodate a workload (UID: 3f209535-fea6-499c-bfac-c171f78cdd4d, JobUID: UNKNOWN) due to Fair Sharing within the cohort
  Normal   Preempted              2m47s (x5 over 4m36s)   kueue-admission       Preempted to accommodate a workload (UID: 3f209535-fea6-499c-bfac-c171f78cdd4d, JobUID: UNKNOWN) due to Fair Sharing within the cohort
  Normal   QuotaReserved          2m47s (x2 over 2m48s)   kueue-admission       Quota reserved in ClusterQueue org-1-proj-1--cq, wait time since queued was 109s
  Normal   QuotaReserved          2m47s (x2 over 2m47s)   kueue-admission       Quota reserved in ClusterQueue org-1-proj-1--cq, wait time since queued was 110s
  Warning  Pending                2m45s (x25 over 4m35s)  kueue-admission       Workload no longer fits after processing another workload
  Normal   OwnerReferencesAdded   7s (x19 over 2m40s)     pod-kueue-controller  Added 1 owner reference(s)
```

### Comment by [@amy](https://github.com/amy) — 2025-10-01T02:10:12Z

To simplify this example, it also repros if you have this setup

<img width="576" height="462" alt="Image" src="https://github.com/user-attachments/assets/e849a98f-06c4-42b9-87b6-6e304d5396b7" />

---

Here is a dump of tournament logs:

- pod-groups 1 to 4 = each podgroup has 2 pods
- pod-group-5 = 1 podgroup with 6 pods
- pod-group-6 = 1 podgroup with 5 pods
- pod-group-7 = 1 podgroup with 4 pods
- pod-group-8 = 1 podgroup with 3 pods

```
Amys-MacBook-Pro:test-11-simplified amychen$ kubectl logs kueue-controller-manager-55c79f5fc5-289jx -n kueue-system | grep "DominantResourceShare values used during tournament"
{"level":"Level(-5)","ts":"2025-10-01T02:26:18.964917175Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2469,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:18.964949758Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2469,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-3","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.006531091Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2470,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.065160925Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2471,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}","{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.06518405Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2471,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.067763883Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2472,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.067906966Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2473,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.125860966Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2474,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.206560716Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2475,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.212825841Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2476,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.221362758Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2477,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.237616466Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2478,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.27077955Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2479,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-3","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 750.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.270843133Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2479,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.346808383Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2480,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}","{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.346842842Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2480,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.366065758Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2481,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.405907842Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2482,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.447941217Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2483,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.544970925Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2484,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}","{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.5451463Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2484,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.549441842Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2485,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}","{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.549477717Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2485,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-3","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.549693425Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2486,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.666971467Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2487,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.827729467Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2488,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.82778405Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2488,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-3","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.86515855Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2489,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.924961133Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2490,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 1000.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.926094717Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2490,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.926563092Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2491,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.92676905Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2492,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:19.989175467Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2493,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.06554005Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2494,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.070244259Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2495,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.080272134Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2496,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.097531675Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2497,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.129826342Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2498,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 750.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.129888717Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2498,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.19537605Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2499,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}","{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.195409842Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2499,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-3","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.200857134Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2500,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.223948634Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2501,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.266268967Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2502,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-8","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-8, drs: 375.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.34625205Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2503,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 750.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.346311592Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2503,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.350577467Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2504,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-6","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}","{parentCohort: org-1, workload test-namespace/pod-group-6, drs: 625.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.350610842Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2504,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-3","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-3, drs: 1000.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.350817342Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2505,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-7","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-7, drs: 500.000}"]}
```

Digging through one of the cycles, here's one of them (podgroup 2 and 5): 
```
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.34625205Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2503,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-1"},"winningWorkload":{"name":"pod-group-2","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-2, drs: 750.000}","{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
{"level":"Level(-5)","ts":"2025-10-01T02:26:20.346311592Z","logger":"scheduler","caller":"scheduler/fair_sharing_iterator.go:227","msg":"DominantResourceShare values used during tournament","schedulingCycle":2503,"rootCohort":{"name":"org-1"},"cohort":{"name":"org-1"},"clusterQueue":{"name":"project-2"},"winningWorkload":{"name":"pod-group-5","namespace":"test-namespace"},"drsValues":["{parentCohort: org-1, workload test-namespace/pod-group-5, drs: 750.000}"]}
```
Here, we can see that pod-group-2 then pod-group-5 won, because they have equivalent drs values. And then use timestamp to tiebreak and preempt each other. (will continue analyzing the cycles and add findings here)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T07:29:30Z

> Here, we can see that pod-group-2 then pod-group-5 won, because they have equivalent drs values. And then use timestamp to tiebreak and preempt each other. (will continue analyzing the cycles and add findings here)

Thank you @amy for the report. Indeed it seems this is hitting the issue of exactly equal DRS. For that case we may consider using additional tiebreaking like UID or creationTimestamp - both have the nice property that are stable over time so results would always be the same (for now this is brainstorming I'm not yet committed if this is the best approach, maybe the tournament logic could also be adjusted).

EDIT: note that we don't have a proof for no PreemptionCycles yet in the Hierarchical setup: https://kueue.sigs.k8s.io/docs/concepts/fair_sharing/#limitations. So, it might be a small fixeable bug, or also some more complex issue in case of deep hierarchies.

cc @gabesaba @PBundyra

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-01T13:41:04Z

I think that this is similar to https://github.com/kubernetes-sigs/kueue/issues/6929: Admissible (due to winning DRS) workload 7 or 8 triggered preemptions. Then, the preempted workloads sneak in during the next cycle when the inadmissible (in this case, due to too high DRS) workloads 5 & 6 are requeued.

> Expanding 4, I also tried this:
> proj-1: submit 4 podgroups. Each podgroup with 2 pods.
> ✅ Meets expectation: all 4 workloads get admitted
> proj-2: submit 1 podgroup. podgroup has 4 pods.
> ❌ Does not meet expectation: 4 pod podgroup workload is still not admitted.

I was unable to reproduce this scenario. I observed proj-2's workload preempting workloads from proj-1 and scheduling

### Comment by [@amy](https://github.com/amy) — 2025-10-01T14:01:59Z

1. @gabesaba Ah yeah, I agree with your assessment head of CQ blocking diagnosis for step 4. Let's chat about my proposal on the respective thread: https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3316170804
If the proposed solution looks good, I can pick up #6929

2. Re: expansion of 4, yeah you're right. I didn't wait long enough for `kubectl get workloads -n test-namespace -w`

3. Priority wise, preemption cycling takes precedence

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T07:56:36Z

@amy as a side note I noticed you are using still `PrioritySortingWithinCohort=false` with Fair sharing. This feature gate was intended only for a time being before introduction of FairSharing. I would like to consider dropping this feature gate now: https://github.com/kubernetes-sigs/kueue/issues/7133

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-02T12:28:26Z

I proposed a solution to solve both issues here: https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3360978483

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-02T12:39:52Z

Am I understanding correctly that proj2 is preempting workoads from proj1, but never the other way around? Proj1 is never preempting proj2, correct?

### Comment by [@amy](https://github.com/amy) — 2025-10-02T16:43:32Z

proj 1:
podgroup1 (2 pods) - never preempted
podgroup2 (2 pods) - preempted by workload in proj2 - podgroup7
podgroup3 (2 pods) - preempted by workload in proj2 - podgroup7
podgroup4 (2 pods) - never preempted

proj 2:
podgroup5 (6 pods) - never admitted (and never preempted)
podgroup6 (5 pods) - never admitted (and never preempted)
podgroup7 (4 pods) - never admitted (and never preempted)
podgroup8 (3 pods) - never admitted (and never preempted)

### Comment by [@amy](https://github.com/amy) — 2025-10-02T17:19:46Z

I'm not following: https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3360978483

> When BestEffortFIFO is enabled, we make the head of the queue sticky. That is, we keep trying to schedule it until the workload is admitted or the scheduling cycle returns a signal that it is inadmissible.

Could you walk through the scheduling iterations and how things change for head selection, putting things in the inadmissible map, and what remains in the scheduling heap?

proj-1: submit 4 podgroups. Each podgroup with 2 pods.
✅ Meets expectation: all 4 workloads get admitted
proj-2: submit 1 podgroup. podgroup has 6 pods.
✅ Meets expectation: 6 pod podgroup workload is not admitted
proj-2: submit 1 podgroup. podgroup has 5 pods.
✅ Meets expectation: 5 pod podgroup workload is not admitted

---
proj-2: submit 1 podgroup. podgroup has 4 pods.
❌ Does not meet expectation: 4 pod podgroup workload is not admitted.

If we pause here *before* submission of next podgroup, without your proposal, do the 6 pod and 5 pod workloads not get added to inadmissible map? It should because they fail flavor fitness. But also, this podgroup with 4 pods also seems to fail flavor fitness at this step. Like why does making the head sticky make this admissible 4 pod workload schedule. It currently won't ever schedule.

---
proj-2: submit 1 podgroup. podgroup has 3 pods.
❌ ??? seems to trigger infinite preemption?

I don't see in the logs that different preemptors are preempting the pods in proj-1. Its the same preemptor.

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-10-02T18:11:47Z

For the infinite preemption: we re-test in kueue version 0.13.4, run exactly steps in the original description and the feature gate setting is the same. Step 4 , tasks group of size 4 did not get in. But for step 5 with tasks group of size 3  submit, it did not trigger any infinite preemption. Tasks group of size 3 could get admitted and start running.
