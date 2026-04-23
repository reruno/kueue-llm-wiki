# Issue #2681: Job preemption across cluster queue doesn't work for apiVersion v1beta1

**Summary**: Job preemption across cluster queue doesn't work for apiVersion v1beta1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2681

**Last updated**: 2024-08-01T20:04:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Zhenshan-Jin](https://github.com/Zhenshan-Jin)
- **Created**: 2024-07-23T15:20:51Z
- **Updated**: 2024-08-01T20:04:36Z
- **Closed**: 2024-08-01T20:04:36Z
- **Labels**: `needs-kind`, `kind/documentation`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 6

## Description

**What happened**:
Following the tutorial, I have set up the `WorkloadPriorityClass` with high and low priority ([tutorial](https://kueue.sigs.k8s.io/docs/tasks/manage/run_job_with_workload_priority/)) and set up two `ClusterQueue`s with preemption enabled ([tutorial](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption)) within the same cohort but I can't make the high priority job in cluster queue a to preempt the low priority job in cluster queue b. 

**What you expected to happen**:
I am expecting the high priority job in cluster queue a will preempt the low priority job in cluster queue b. 

**How to reproduce it (as minimally and precisely as possible)**:
Command to run
```
# define queues
kubectl apply -f cluster-queue-cohort-a.yaml -f cluster-queue-cohort-b.yaml
kubectl apply -f default-flavor.yaml
kubectl create namespace cohort-3
kubectl apply -f default-user-queue-cohort-a.yaml -f default-user-queue-cohort-b.yaml
# define priority class
kubectl apply -f high-priority.yaml -f low-priority.yaml

# run low priority job which requires 4 cpu in cluster queue b with cpu quota of 4
kubectl create -f sample-job-low-priority-cohort-b.yaml

# run high priority job which requires 6 cpu in cluster queue a with cpu quota of 4
kubectl create -f sample-job-high-priority-cohort-a.yaml
```
yaml file definition    
*high-priority.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: high-priority
value: 10000
```
*low-priority.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: low-priority
value: 100
```
*cluster-queue-cohort-a.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-cohort-a-3"
spec:
  namespaceSelector: {} # match all.
  cohort: "team-ab-3"
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 5000
    withinClusterQueue: LowerPriority
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 4
      - name: "memory"
        nominalQuota: 36Gi
```
*cluster-queue-cohort-b.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-cohort-b-3"
spec:
  namespaceSelector: {} # match all.
  cohort: "team-ab-3"
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 5000
    withinClusterQueue: LowerPriority
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 4
      - name: "memory"
        nominalQuota: 36Gi
```
*default-flavor.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
```
*default-user-queue-cohort-a.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "cohort-3"
  name: "user-queue-cohort-a-3"
spec:
  clusterQueue: "cluster-queue-cohort-a-3"
```
*default-user-queue-cohort-b.yaml*
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "cohort-3"
  name: "user-queue-cohort-b-3"
spec:
  clusterQueue: "cluster-queue-cohort-b-3"
```
*sample-job-high-priority-cohort-a.yaml*
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  namespace: cohort-3
  labels:
    kueue.x-k8s.io/queue-name: user-queue-cohort-a-3
    kueue.x-k8s.io/priority-class: high-priority
spec:
  parallelism: 6
  completions: 6
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["15s"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
```
*sample-job-low-priority-cohort-b.yaml*
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  namespace: cohort-3
  labels:
    kueue.x-k8s.io/queue-name: user-queue-cohort-b-3
    kueue.x-k8s.io/priority-class: low-priority
spec:
  parallelism: 4
  completions: 4
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["15s"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
```

**Anything else we need to know?**:

**Environment**: 
- Kubernetes version (use `kubectl version`):
```
Client Version: v1.29.1
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.30.2-eks-db838b0
```
- Kueue version (use `git describe --tags --dirty --always`): 0.8.0
- Cloud provider or hardware configuration: Amazon EKS
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools: see https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version
- Others:

## Discussion

### Comment by [@Zhenshan-Jin](https://github.com/Zhenshan-Jin) — 2024-07-24T17:07:00Z

@trasc could you help to check if this is indeed a bug ? Thank you!

### Comment by [@trasc](https://github.com/trasc) — 2024-07-25T05:33:37Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-07-25T16:55:36Z

In short, the low priority job is consider for eviction because the cluster queue in which it runs is not borrowing. 

Some additional detail on preempt-within-cohort-while-borrowing can be found in the [features KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1337-preempt-within-cohort-while-borrowing).

To get to the scenario I think you are targeting, you can add a third cluster-queue that adds 1 cpu  to the cohort

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-cohort-c-3"
spec:
  namespaceSelector: {} # match all.
  cohort: "team-ab-3"
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 5000
    withinClusterQueue: LowerPriority
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 1
      - name: "memory"
        nominalQuota: 36Gi
```

and increase the resource requirements of the low priority job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  namespace: cohort-3
  labels:
    kueue.x-k8s.io/queue-name: user-queue-cohort-b-3
    kueue.x-k8s.io/priority-class: low-priority
spec:
  parallelism: 5
  completions: 5
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["15s"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
```


Please let me know which section of the documentation we can improve to make this behavior a bit more clear.

### Comment by [@trasc](https://github.com/trasc) — 2024-07-25T17:11:45Z

/remove-kind bug

### Comment by [@trasc](https://github.com/trasc) — 2024-07-25T17:12:09Z

/kind documentation

### Comment by [@Zhenshan-Jin](https://github.com/Zhenshan-Jin) — 2024-08-01T20:04:08Z

@trasc Thank you for your instruction. I tried your example and it works. 

I think it would be good to mention clearly about the preemption in Kueue is guaranteed quota vs over-quota. Only the job that is served with over-quota will be preempted by other jobs in the same cohort. The only place mentioned about the rule is https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption
> only preempt Workloads in the cohort that have lower priority than the pending Workload.

which doesn't clearly express the actual behavior. 

I will close the issue
