# Issue #9096: position within clusterqueues is sorted randomly

**Summary**: position within clusterqueues is sorted randomly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9096

**Last updated**: 2026-04-17T06:52:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mmolisch](https://github.com/mmolisch)
- **Created**: 2026-02-10T15:31:44Z
- **Updated**: 2026-04-17T06:52:00Z
- **Closed**: 2026-02-12T07:12:03Z
- **Labels**: `kind/bug`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Workloads within cluster-queue are sorted "randomly" each watch call -> nonstop changing `positionInClusterQueue`. No other workloads, in different queues, are waiting.
**What you expected to happen**:
workload in cluster-queue are not "randomly" sorted

**How to reproduce it (as minimally and precisely as possible)**:
`kubectl get --raw /apis/visibility.kueue.x-k8s.io/v1beta2/clusterqueues/cq-liveness/pendingworkloads \
| jq -r ".items
  | sort_by(.positionInClusterQueue)
  | (\"CLUSTER_POS\tLOCAL_POS\tNAMESPACE\tWORKLOAD\"),
    (.[] | \"\(.positionInClusterQueue)\t\(.positionInLocalQueue)\t\(.metadata.namespace)\t\(.metadata.name)\")"
'`
every second the workloads are changing positions

**Anything else we need to know?**:
We have 0 nominalQuota for each resource in team's clusterQueues and resources are defined in shared clusterQueue.

Helm values:
```enableKueueViz: false
controllerManager:
  nodeSelector:
    node-role.kubernetes.io/master: "true"
  replicas: 3
  featureGates:
    - name: VisibilityOnDemand
      enabled: true
enablePrometheus: true
enableCertManager: true
metrics:
  prometheusNamespace: observability
managerConfig:
  controllerManagerConfigYaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta2
    kind: Configuration

    admissionFairSharing:
      usageHalfLifeTime: "168h"
      usageSamplingInterval: "5m"
      resourceWeights:
        nvidia.com/gpu: 2.0
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8443
      enableClusterQueueResources: true
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: c1f6bfd2.kueue.x-k8s.io
    controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 100
      burst: 200
    #pprofBindAddress: :8082
    #waitForPodsReady:
    #  enable: true
    #manageJobsWithoutQueueName: true
    internalCertManagement:
      enable: false
    #  webhookServiceName: ""
    #  webhookSecretName: ""
    managedJobsNamespaceSelector:
      matchExpressions:
        - key: team
          operator: Exists
    integrations:
      frameworks:
      - "batch/job"
      - "pod"
```
cq-liveness
```apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: cq-liveness
spec:
  cohortName: rad
  admissionScope:
    admissionMode: UsageBasedAdmissionFairSharing
  flavorFungibility:
    whenCanBorrow: MayStopSearch
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  resourceGroups:
    - coveredResources: ["cpu", "memory", "ephemeral-storage", "github.com/fuse", "pods", "nvidia.com/gpu", "innovatrics.com/cpu-spread"]
      flavors:
      - name: "godel"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "bayes"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "fourier"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "maxwell"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "hawking"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "newton"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "euler"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "bob"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "mel"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "tim"
        resources:
        - name: "cpu"
          nominalQuota: '0'
        - name: "memory"
          nominalQuota: '0'
        - name: "ephemeral-storage"
          nominalQuota: '0'
        - name: "github.com/fuse"
          nominalQuota: '0'
        - name: "pods"
          nominalQuota: '0'
        - name: "nvidia.com/gpu"
          nominalQuota: '0'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
```
cq-shared
```apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: cq-shared
spec:
  cohortName: rad
  admissionScope:
    admissionMode: UsageBasedAdmissionFairSharing
  flavorFungibility:
    whenCanBorrow: MayStopSearch
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  resourceGroups:
    - coveredResources: ["cpu", "memory", "ephemeral-storage", "github.com/fuse", "pods", "nvidia.com/gpu", "innovatrics.com/cpu-spread"]
      flavors:
      - name: "godel"
        resources:
        - name: "cpu"
          nominalQuota: '253'
        - name: "memory"
          nominalQuota: '944Gi'
        - name: "ephemeral-storage"
          nominalQuota: '6454133255045120m' # 5.87Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '8'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '1'
      - name: "bayes"
        resources:
        - name: "cpu"
          nominalQuota: '125'
        - name: "memory"
          nominalQuota: '956Gi'
        - name: "ephemeral-storage"
          nominalQuota: '7663596045598720m' # 6.97Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '8'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '1'
      - name: "fourier"
        resources:
        - name: "cpu"
          nominalQuota: '125'
        - name: "memory"
          nominalQuota: '1026389809561600m' # 955.9Gi
        - name: "ephemeral-storage"
          nominalQuota: '3133608139161600m' # 2.85Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '8'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '1'
      - name: "maxwell"
        resources:
        - name: "cpu"
          nominalQuota: '125'
        - name: "memory"
          nominalQuota: '1026389809561600m' # 955.9Gi
        - name: "ephemeral-storage"
          nominalQuota: '3133608139161600m' # 2.85Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '8'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '1'
      - name: "hawking"
        resources:
        - name: "cpu"
          nominalQuota: '125'
        - name: "memory"
          nominalQuota: '944Gi'
        - name: "ephemeral-storage"
          nominalQuota: '3265549534494720m' # 2.97Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '8'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '1'
      - name: "newton"
        resources:
        - name: "cpu"
          nominalQuota: '125'
        - name: "memory"
          nominalQuota: '956Gi'
        - name: "ephemeral-storage"
          nominalQuota: '5464572790046720m' # 4.97Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '4'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '1'
      - name: "euler"
        resources:
        - name: "cpu"
          nominalQuota: '62'
        - name: "memory"
          nominalQuota: '452Gi'
        - name: "ephemeral-storage"
          nominalQuota: '5464572790046720m' # 4.97Ti
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '9'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "bob"
        resources:
        - name: "cpu"
          nominalQuota: '10'
        - name: "memory"
          nominalQuota: '27Gi'
        - name: "ephemeral-storage"
          nominalQuota: '474Gi'
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '1'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "mel"
        resources:
        - name: "cpu"
          nominalQuota: '10'
        - name: "memory"
          nominalQuota: '27Gi'
        - name: "ephemeral-storage"
          nominalQuota: '474Gi'
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '1'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
      - name: "tim"
        resources:
        - name: "cpu"
          nominalQuota: '10'
        - name: "memory"
          nominalQuota: '27Gi'
        - name: "ephemeral-storage"
          nominalQuota: '474Gi'
        - name: "github.com/fuse"
          nominalQuota: '5k'
        - name: "pods"
          nominalQuota: '110'
        - name: "nvidia.com/gpu"
          nominalQuota: '1'
        - name: "innovatrics.com/cpu-spread"
          nominalQuota: '0'
```
**Environment**:
- Kubernetes version (use `kubectl version`): v1.34.2+rke2r1
- Kueue version (use `git describe --tags --dirty --always`): v0.15.3
- Cloud provider or hardware configuration: RKE2 on-prem & VM
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04
- Kernel (e.g. `uname -a`): 5.15.0-143-generic
- Install tools:
- Others:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-10T16:22:03Z

Thanks for the report. This looks like a real bug. The ordering used for the visibility snapshot isn’t fully deterministic (map iteration and sort tie-breaking), so `positionInClusterQueue` can change between requests.

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T16:52:11Z

Hm, yes it needs to be deterministic.

Ideally we use the same ordering function as for scheduling with the same rules for tie breaking. Iirc we fallback eventually to ordering by creation timestamp, then by UUID which should make it deterministic.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-10T17:03:58Z

/assign

### Comment by [@mmolisch](https://github.com/mmolisch) — 2026-02-12T09:11:59Z

Thank you guys!

### Comment by [@mmolisch](https://github.com/mmolisch) — 2026-02-27T15:36:32Z

The issue still persists on 0.15.5, do I have to setup something differently? 

https://i.postimg.cc/KcKsYD6s/kueue-positions.gif ![]("https://i.postimg.cc/KcKsYD6s/kueue-positions.gif")

### Comment by [@mmolisch](https://github.com/mmolisch) — 2026-03-09T10:12:39Z

@mimowo @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-16T06:14:43Z

Hey @mmolisch, thanks for the follow-up and sorry this is still giving you trouble on v0.15.5. I think that fix only addressed the missing UID tie-breaker. Your config has `UsageBasedAdmissionFairSharing` enabled, which hits a different code path i.e. Snapshot() reads shared fair-sharing state (entry penalties, consumed resources) live during the sort. The scheduler updates that state concurrently, so the comparator sees inconsistent values mid-sort, breaking transitivity.

I reproduced this: ~600/1000 Snapshot() calls produce invalid orderings under concurrent penalty updates. Your setup is correct. It looks like a bug in the code. Working on a fix, will link the PR here.

### Comment by [@mmolisch](https://github.com/mmolisch) — 2026-04-16T13:54:37Z

Hello @sohankunkerkar the issue was resolved, but a new one was introduced. I upgraded to v0.17.0 and this is the behaviour of the same command as previously [![kueue-positions-v2.gif](https://i.postimg.cc/76BgCJXf/kueue-positions-v2.gif)](https://postimg.cc/5YCHT0hV)

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-04-16T14:47:33Z

Hey @mmolisch, thanks for sharing the new GIF. The original random shuffling issue fixed by #9899 seems resolved in v0.17.0. What this GIF shows looks different. The result set itself is changing in size between requests, not just the ordering. That points more toward an HA visibility inconsistency rather than another sorting issue. Could you file a separate bug with all the relevant details and tag me there? I have a suspicion about what might be going on, but I’d prefer to look at more details before jumping to any conclusions.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-17T06:52:00Z

> Hello [@sohankunkerkar](https://github.com/sohankunkerkar) the issue was resolved, but a new one was introduced. I upgraded to v0.17.0 and this is the behaviour of the same command as previously

HI @mmolisch , we released the HA-related internal cache inconsistency issues in v0.17.1. Could you try the latest version and share your results? Thank you.
