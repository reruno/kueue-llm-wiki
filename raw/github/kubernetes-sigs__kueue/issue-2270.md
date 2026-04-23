# Issue #2270: BestEffortFIFO ClusterQueue not functioning as expected

**Summary**: BestEffortFIFO ClusterQueue not functioning as expected

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2270

**Last updated**: 2024-11-23T10:08:14Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@agngrant](https://github.com/agngrant)
- **Created**: 2024-05-23T15:46:35Z
- **Updated**: 2024-11-23T10:08:14Z
- **Closed**: 2024-11-23T10:08:12Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 8

## Description

**What happened**:
Submitting after conversation on Slack Channel.

A K8s Cluster with multiple clusterqueues in the same cohort has each queue using BestEffortFIFO scheduling strategy. 

One queue (queue-i) has both nominal quota and can borrow from another queue (queue-m). Submissions to queue-i after a time have started to stop being processed - a group of pending workloads appear to be blocking subsequent workloads from being considered. 

Jobs A, B and C seem to get examined continuously by the reconciler with job E, F and G which could fit into the queue resources are not being scheduled. 

Jobs E, F, G either are not given statuses or are not moved forward to use available resource.

**What you expected to happen**:

When Job A, B and C are waiting on 4 GPUs and Job E, F are only requiring CPU and G only require 1 GPU which is available for E,F and G to be added to run before A, B and C. This seems to be what the BestEffortFIFO description indicates.

This appears to work on other queues on the same cluster - though those queues are less populated.


**How to reproduce it (as minimally and precisely as possible)**:

Five replicas of the queue controller.

With different variants of  following  (with values for each ranging up to 1000 in different tests):
```yaml
    controller:
      groupKindConcurrency:
        Job.batch: 10
        Pod: 10
        Workload.kueue.x-k8s.io: 10
        LocalQueue.kueue.x-k8s.io: 10
        ClusterQueue.kueue.x-k8s.io: 10
        ResourceFlavor.kueue.x-k8s.io: 11
    clientConnection:
      qps: 50
      burst: 100
```

ResourceFlavours: 11
All defined with yaml such as:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "gpu-a100-owned"
spec:
  nodeLabels:
    nvidia.com/gpu.present: "true"
    nvidia.com/gpu.product: NVIDIA-A100-SXM4-40GB
    owned_node: "true"
```
Main Cluster Queue - this has no user-queue and can only be borrowed from.

Standard Queues - can borrow from main cluster queue upto limited but no nominal quota.

Owned Queue - can borrow from main cluster queue but also has nominal quota on specific resource flavours.

submit N jobs to Owned queue + M jobs to other queues. There is still a large amount of resource available in the main queue, but the Owned queue has hit limits on several GPU types. 

Submit a Job with no GPUs - this should be run quickly but it waits for days in the queue until GPUs are released and the queue moves forward.

cluster 
**Anything else we need to know?**:

The kueue-controller-manager is looping over the same set of jobs on the queue seemingly according to the logs:

This is an example of the log (jobs and identifiers altered):

```bash
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.338457517Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.356051564Z","logger":"localqueue-reconciler","caller":"core/localqueue_controller.go:151","msg":"Queue update event","localQueue":{"name":"queue-i-user-queue","namespace":"queue-i"}}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.408043612Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.408174335Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.440990822Z","logger":"localqueue-reconciler","caller":"core/localqueue_controller.go:151","msg":"Queue update event","localQueue":{"name":"queue-i-user-queue","namespace":"queue-i"}}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.462278246Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.462386688Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.517825875Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.517928096Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.57499746Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.575161236Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.629990998Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.630123565Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.688532654Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.688774344Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.752545498Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.752763284Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.815911609Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-5-e565e","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.81605738Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-5-e565e","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.87201318Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.872240924Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.927585155Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.927744171Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.991140568Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:52.991269608Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:53.051492274Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:53.051702716Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:53.106039761Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
{"level":"Level(-2)","ts":"2024-05-23T15:30:53.106222702Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:321","msg":"Got generic event","obj":{"name":"job-user-3-a4d95","namespace":"queue-i"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-05-23T15:30:53.163957936Z","logger":"workload-reconciler","caller":"core/workload_controller.go:507","msg":"Workload update event","workload":{"name":"job-user-3-a4d95","namespace":"queue-i"},"queue":"queue-i-user-queue","status":"pending"}
```

**Environment**:
- Kubernetes version (use `kubectl version`): v1.24.10 RKE2
- Kueue version (use `git describe --tags --dirty --always`): v0.6.2
- Cloud provider or hardware configuration: KVM with Nvidia GPUs
- OS (e.g: `cat /etc/os-release`): Ubuntu 20.04
- Kernel (e.g. `uname -a`):
- Install tools: Rancher/RKE2
- Others:  5.4.0-163-generic

## Discussion

### Comment by [@agngrant](https://github.com/agngrant) — 2024-05-23T16:04:29Z

Additional Note: Pausing the queue and making the workloads which appear to be blocking the queue inactive, seems to temporarily unblock the queue but reinserting them ends with a similar issue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:22:44Z

Since you are using node labels in your Resource Flavor, this is likely a duplicate of https://github.com/kubernetes-sigs/kueue/issues/2391

Could you try using image `gcr.io/k8s-staging-kueue/kueue:v20240619-v0.7.0-8-gaa682c90` to see if the issue persist?

Sorry we missed your issue earlier. Feel free to ping one of the OWNERS if you don't receive a response within a week.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-23T22:15:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-24T08:10:13Z

@agngrant would you like to test a newer version as suggested in https://github.com/kubernetes-sigs/kueue/issues/2270#issuecomment-2189992924?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-24T09:03:48Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T09:09:10Z

@agngrant do you have any update for this issue when trying to repro on latest Kueue? As indicated by the previous comments the issue likely already solved.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-23T10:08:08Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-23T10:08:13Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2270#issuecomment-2495425806):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
