# Issue #9992: Allow TAS to ignore pods that have lower priority than workload trying to be scheduled

**Summary**: Allow TAS to ignore pods that have lower priority than workload trying to be scheduled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9992

**Last updated**: 2026-03-23T20:52:30Z

---

## Metadata

- **State**: open
- **Author**: [@SeungjinYang](https://github.com/SeungjinYang)
- **Created**: 2026-03-19T00:48:47Z
- **Updated**: 2026-03-23T20:52:30Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, when TAS [calculates capacity](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#capacity-calculation), the calculation "subtracts the usage coming from all other non-TAS Pods (owned mainly by DaemonSets, but also including static Pods, Deployments, etc.)"

It'd be nice if the usage of non-TAS pods were not considered if the k8s priority of these pods are lower than the k8s priority of the workload trying to be scheduled.

**Why is this needed**:

The specific motivation stems from Kueue's interaction with [Coreweave's HPC verification pods](https://docs.coreweave.com/platform/fleet-management/hpc-verification). From their documentation:

> You may briefly see a Job named hpc-verification-* in kubectl get pods -A while the test runs. The test uses a Kubernetes PriorityClass of cw-hpc-verification with a value of -1, meaning it always runs at a lower priority than customer workloads.

The idea here is that Coreweave may run static pods on the k8s cluster, but this pod is meant to be preempted when user pod needs the resource. However, I've observed this empirically does not work with TAS. What I believe is happening is some sort of a chicken and egg problem:
- For the HPC pod to be preempted, a pod requesting the resource being used by HPC pod needs to be scheduled.
- The pod (in this case a Kueue workload) is in SchedulingGated state. TAS blocks the pod's admission because does not see enough free resource on the node. TAS doesn't seem to be aware of the fact that the HPC pod would be preempted once the pod is scheduled, freeing up necessary resource for the pod to run.

Aside: I am using plain pods integration, if that matters.

Edit: I'm using [scenario 2 ](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/#the-relationship-between-pods-priority-and-workloads-priority) of the priority configuration:
> A job specifies only WorkloadPriorityClass
WorkloadPriorityClass is used for the workload’s priority.
WorkloadPriorityClass is not used for pod’s priority.

and therefore any workload pod's priority is 0.

**Completion requirements**:

TAS should check the workload pod's priority, and ignore usage of already scheduled pods that have lower priority than the pod trying to be scheduled.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-23T07:17:33Z

@SeungjinYang this sounds to me like a valid approach. I think this does not even require a new API, and we could introduce it as a bugfix for the integration with the core scheduler. We didn't do that in the original implementation as we were not aware of the usage pattern, most of the time TAS is responsible for accelerators while non-TAS pods are only DaemonSets / static Pods, but this looks like a legit use case for "fixing" the support.

On the technical level in nonTasUsageCache we already keep the information about the Pods' usage, so we could extend the information with their priority, and compare the priority with the priority in PodTemplate. I think the priority of the Workload is not relevant in this case. Certainly we will need a feature gate for safety.

As a workaround you may try to inject TAS annotation `kueue.x-k8s.io/podset-unconstrained-topology` to recognize the Coreweave's pods as TAS. 

cc @Huang-Wei @amy

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-03-23T20:49:06Z

> As a workaround you may try to inject TAS annotation kueue.x-k8s.io/podset-unconstrained-topology to recognize the Coreweave's pods as TAS.

I tried a similar approach to enroll those pods into Kueue TAS (I used `LocalQueueDefaulting` after talking to @tenzen-y offline), but it caused unknown ungating issue (maybe due to ungater's scalability) - we observed a lot of pods stay in SchedulingGated state.

For some context, CoreWeave's hcp-verfiication Job is cron-based (backed by argocd's [cron-workflow](https://argo-workflows.readthedocs.io/en/latest/cron-workflows/)) and hence will use plain Pod integration, and will spawn N `workload` simultaneously (`N` = number of nodes).

So to work around the issue, what I did internally is to build a custom Kueue image that ensure Kueue TAS simply bypass negative-priority Pods (configurable) - the code is at https://github.com/Huang-Wei/kueue/commit/bb27afed0383f3db21c406ff07fd0fe631e6eba6 (based off v0.16.2).

If needed, I can rework this commit as a PR onto `main`. Overall, I think Kueue TAS to have a knob to bypass certain pods is more efficient and sustainable.
