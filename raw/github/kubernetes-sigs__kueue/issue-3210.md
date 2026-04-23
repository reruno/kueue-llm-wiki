# Issue #3210: Unexpected preemption between ClusterQueues within a Cohort

**Summary**: Unexpected preemption between ClusterQueues within a Cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3210

**Last updated**: 2024-10-14T11:09:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@octotocat](https://github.com/octotocat)
- **Created**: 2024-10-09T22:31:40Z
- **Updated**: 2024-10-14T11:09:26Z
- **Closed**: 2024-10-14T07:38:32Z
- **Labels**: `kind/support`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In a setup where three ClusterQueues (Q1, Q2, and Q3) are part of the same cohort, we observed that a high-priority workload (WL3) from Q3 preempted a low-priority workload (WL1) from Q1, despite preemption policies being configured to prevent this. Specifically:
- `reclaimWithinCohort: Never`
- `borrowWithinCohort.policy: Never`
- `withinClusterQueue: LowerPriority`

**What you expected to happen**:
WL3 should have remained pending because:
- The preemption policies (`reclaimWithinCohort: Never` and `borrowWithinCohort.policy: Never`) should have prevented resource reclamation across ClusterQueues within the same cohort.
- There was no candidate for preemption within Q1 based on the preemption policy (`withinClusterQueue: LowerPriority`).

**How to reproduce it (as minimally and precisely as possible)**:
1. Set up three ClusterQueues (Q1, Q2, Q3) in the same cohort with the following preemption policies:
   - `reclaimWithinCohort: Never`
   - `borrowWithinCohort.policy: Never`
   - `withinClusterQueue: LowerPriority`
2. Assign 8 GPUs in total to the cluster.
3. Submit 4-GPU low-priority workloads (WL1 and WL2) to Q1 and Q2, respectively.
4. Submit a 4-GPU high-priority workload (WL3) to Q3 and admit it.
5. Observe that WL3 preempts WL1, despite the preemption policy setup.

**Anything else we need to know?**:
It appears the preemption policy does not fully respect the cohort-level restrictions, allowing WL3 to preempt WL1, which contradicts the configured settings.
WL1 Status/Events did not log the preemption. Kueue immediately started a new WL1-1 for the deployment and WL1 was evicted. It occurred to WL1 or WL2 randomly. Attached Kueue controller logs during the event happened. In this log [kueue_logs.txt](https://github.com/user-attachments/files/17319516/kueue_logs.txt), WL2 was evicted. 
This unexpected preemption behavior also occurs between cohorts. According to the documentation, preemption should never happen between cohorts.

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.2
- Kueue version (use `git describe --tags --dirty --always`): v0.8.1
- Cloud provider or hardware configuration: 
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools: helm
- Others:

test.yaml: 
```
apiVersion: v1
kind: Namespace
metadata:
  name: dac-resv-1
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "dac-resv-1"
spec:
  namespaceSelector: {} # match all.
  cohort: cohort-dedicated
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: LowerPriority
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
        - name: "default-flavor"
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 4
              borrowingLimit: 0
              lendingLimit: 0
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: dac-resv-1
  name: dac-resv-1
spec:
  clusterQueue: dac-resv-1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dac-resv1-deployment
  namespace: dac-resv-1
spec:
  replicas: 1
  selector:
    matchLabels:
      kueue-job: "true"
  template:
    metadata:
      labels:
        kueue-job: "true"
        kueue.x-k8s.io/queue-name: dac-resv-1
    spec:
      priorityClassName: low-priority-class
      containers:
        - name: pod-dac-resv-1
          image: busybox
          command: ["sh", "-c", "sleep infinity"]
          ports:
            - containerPort: 80
          resources:
            requests:
              nvidia.com/gpu: "4"
            limits:
              nvidia.com/gpu: "4"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                      - 10.0.101.70
---
apiVersion: v1
kind: Namespace
metadata:
  name: dac-resv-2
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "dac-resv-2"
spec:
  namespaceSelector: {} # match all.
  cohort: cohort-dedicated
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: LowerPriority
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
        - name: "default-flavor"
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 4
              borrowingLimit: 0
              lendingLimit: 0
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: dac-resv-2
  name: dac-resv-2
spec:
  clusterQueue: dac-resv-2
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dac-resv2-deployment
  namespace: dac-resv-2
spec:
  replicas: 1
  selector:
    matchLabels:
      kueue-job: "true"
  template:
    metadata:
      labels:
        kueue-job: "true"
        kueue.x-k8s.io/queue-name: dac-resv-2
    spec:
      priorityClassName: low-priority-class
      containers:
        - name: pod-dac-resv-2
          image: busybox
          command: ["sh", "-c", "sleep infinity"]
          ports:
            - containerPort: 80
          resources:
            requests:
              nvidia.com/gpu: "4"
            limits:
              nvidia.com/gpu: "4"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                      - 10.0.101.70
---
apiVersion: v1
kind: Namespace
metadata:
  name: dac-resv-3
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "dac-resv-3"
spec:
  namespaceSelector: {} # match all.
  cohort: cohort-dedicated
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: LowerPriority
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
        - name: "default-flavor"
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 4
              borrowingLimit: 0
              lendingLimit: 0
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: dac-resv-3
  name: dac-resv-3
spec:
  clusterQueue: dac-resv-3
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dac-resv3-deployment
  namespace: dac-resv-3
spec:
  replicas: 1
  selector:
    matchLabels:
      kueue-job: "true"
  template:
    metadata:
      labels:
        kueue-job: "true"
        kueue.x-k8s.io/queue-name: dac-resv-3
    spec:
      priorityClassName: high-priority-class
      containers:
        - name: pod-dac-resv-3
          image: busybox
          command: ["sh", "-c", "sleep infinity"]
          ports:
            - containerPort: 80
          resources:
            requests:
              nvidia.com/gpu: "4"
            limits:
              nvidia.com/gpu: "4"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                      - 10.0.101.70
```
WL1:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:...
status:...
spec:
  active: true
  podSets:...
  priority: 10
  priorityClassName: low-priority-class
  priorityClassSource: scheduling.k8s.io/priorityclass
  queueName: dac-resv-1
```
Other setups:
Installed Kueue from helm chart. 
Integrated with "pod" in Values.integrations.frameworks. 
Enabled "waitForPodsReady" with "blockAdmission". 
Did not enable fairSharing.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-10T05:17:00Z

/cc @mbobrovskyi @trasc 
PTAL

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-10T07:20:47Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-10T08:23:59Z

In your example `test.yaml` you have three different ClusterQueues with `nvidia.com/gpu=4` on each of them and all of Workloads running on separate ClusterQueues which is correct because each Pod have requests `nvidia.com/gpu=4`. 

```
kubectl get wl -A
NAMESPACE    NAME                                              QUEUE           RESERVED IN   ADMITTED   FINISHED   AGE
dac-resv-1   pod-dac-resv1-deployment-7bd484bfdb-x5f4s-857c8   dac-resv-lq-1   dac-resv-1    True                  3s
dac-resv-2   pod-dac-resv2-deployment-9d4dff9dd-cr9lf-f5046    dac-resv-lq-2   dac-resv-2    True                  3s
dac-resv-3   pod-dac-resv3-deployment-54b4f969cb-rhgm7-83a91   dac-resv-lq-3   dac-resv-3    True                  3s
```

So it doesn't preempt from another ClusterQueue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-10T14:14:33Z

> Assign 8 GPUs in total to the cluster.

I think that the confusion is here. Kueue is not aware of the cluster's actual resources. Instead, it uses `nominalQuota` from the `ClusterQueue` to understand how many resources it has.

### Comment by [@octotocat](https://github.com/octotocat) — 2024-10-10T19:16:40Z

Thank you for investigating this issue.
This situation arises when the cluster has insufficient resources. Are you suggesting that this behavior is expected as long as Kueue allows the workload to be admitted? 
I have some concerns about scenarios where GPU utilization in the cluster is high. There may be potential race conditions that could allow a workload to be admitted despite insufficient resources, which could pose a significant risk.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-11T07:35:31Z

> Are you suggesting that this behavior is expected as long as Kueue allows the workload to be admitted?

Yes, Kueue is not checking if the resources described in the ClusterQueue's definition are meet by the cluster's overall resources or if such resources are currently in use by  workloads that are not managed by Kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-11T09:01:34Z

I see, if you specify more quota than the actual resources, then you may be observing preemptions at the level of Pods by kube-scheduler, rather than Kueue.

To mitigate that I saw some users assign a bit more cluster capacity than actual quota for some buffer (say 10%) for the high priority Jobs. This buffer can be used for low-priority Jobs and may mitigate for nodes going down.

Alternatively use ProvisioningRequest with check-capacity from ClusterAutoscaler. In this setup the CA simulates if the Job could run, and gives green light to Kueue via the AdmissionCheck mechanism (see [here](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#provisioningrequest-configuration)).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-11T13:03:04Z

> I see, if you specify more quota than the actual resources, then you may be observing preemptions at the level of Pods by kube-scheduler, rather than Kueue.

In that case, I would recommend using the WorkloadPriorityClass instead of core kube PriorityClass: https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/

This can mitigate the race condition between Kueue and kube-scheduler. This WorkloadPriorityClass is used for preempting and ordering only inside Kueue, never used by kube-scheduler.

### Comment by [@octotocat](https://github.com/octotocat) — 2024-10-12T00:05:50Z

> In that case, I would recommend using the WorkloadPriorityClass instead of core kube PriorityClass: https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/

Thanks, this works.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-14T07:38:29Z

Excellent! Closing as the behavior is WAI from Kueue PoV, and we have a workaround for the kube-scheduler initiated preemptions.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-14T07:38:33Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3210#issuecomment-2410296747):

>Excellent! Closing as the behavior is WAI from Kueue PoV, and we have a workaround for the kube-scheduler initiated preemptions.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-14T11:09:23Z

/remove-kind bug
/kind support
