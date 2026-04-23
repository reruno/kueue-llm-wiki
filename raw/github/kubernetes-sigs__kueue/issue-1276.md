# Issue #1276: [Job] Job could not borrow quota from the next Flavor

**Summary**: [Job] Job could not borrow quota from the next Flavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1276

**Last updated**: 2023-10-30T02:47:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@B1F030](https://github.com/B1F030)
- **Created**: 2023-10-27T10:24:36Z
- **Updated**: 2023-10-30T02:47:33Z
- **Closed**: 2023-10-30T02:47:33Z
- **Labels**: `kind/bug`, `triage/needs-information`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
![image](https://github.com/kubernetes-sigs/kueue/assets/77265354/ffa6aa27-7337-44d0-8271-718cfa957499)
When there is not enough nominal quota of resources in a ResourceFlavor, the incoming Workload could not borrow quota in the ClusterQueue or Cohort.

**What you expected to happen**:
The incoming Workload should borrow quota and turn to Running.

**How to reproduce it (as minimally and precisely as possible)**:
Here is my clusterQueue yaml:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "flavor-fungibility-cq"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "x86"
      resources:
      - name: "cpu"
        nominalQuota: 500m
      - name: "memory"
        nominalQuota: 2Gi
    - name: "arm"
      resources:
      - name: "cpu"
        nominalQuota: 500m
      - name: "memory"
        nominalQuota: 2Gi
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: Preempt
```
and my job yaml:
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: flavor-fungibility-queue
spec:
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        imagePullPolicy: IfNotPresent
        args: ["60s"]
        resources:
          requests:
            cpu: 500m
            memory: "500Mi"
      restartPolicy: Never
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
Client Version: v1.26.0
Kustomize Version: v4.5.7
Server Version: v1.26.0
- Kueue version (use `git describe --tags --dirty --always`):
v0.5.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
manifests.yaml
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T13:39:54Z

I don't see a cohort defined for this ClusterQueue. And do you have a 2nd ClusterQueue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T13:40:05Z

/triage needs-information

### Comment by [@B1F030](https://github.com/B1F030) — 2023-10-28T05:55:31Z

Thanks! I thought this "borrowing" can happen in one ClusterQueue without cohort...
Now I tried this on two ClusterQueue within one cohort, and it works!
By the way i can paste my yaml on, in case somebody else meet this situation as i do.

### Comment by [@B1F030](https://github.com/B1F030) — 2023-10-28T05:58:55Z

`# cat arch-arm-cq.yaml`
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "arch-arm-cq"
spec:
  namespaceSelector: {} # match all.
  cohort: "arch"
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "arm"
      resources:
      - name: "cpu"
        nominalQuota: 500m
        borrowingLimit: 500m
      - name: "memory"
        nominalQuota: 2Gi
        borrowingLimit: 2Gi
    - name: "x86"
      resources:
      - name: "cpu"
        nominalQuota: 500m
        borrowingLimit: 500m
      - name: "memory"
        nominalQuota: 2Gi
        borrowingLimit: 2Gi
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: Preempt
```
`# cat arch-x86-cq.yaml`
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "arch-x86-cq"
spec:
  namespaceSelector: {} # match all.
  cohort: "arch"
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "x86"
      resources:
      - name: "cpu"
        nominalQuota: 500m
        borrowingLimit: 500m
      - name: "memory"
        nominalQuota: 2Gi
        borrowingLimit: 2Gi
    - name: "arm"
      resources:
      - name: "cpu"
        nominalQuota: 500m
        borrowingLimit: 500m
      - name: "memory"
        nominalQuota: 2Gi
        borrowingLimit: 2Gi
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: Preempt
```
`# cat sample-job.yaml `
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: arch-arm-queue
spec:
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        imagePullPolicy: IfNotPresent
        args: ["60s"]
        resources:
          requests:
            cpu: 500m
            memory: "100Mi"
      restartPolicy: Never
```

### Comment by [@B1F030](https://github.com/B1F030) — 2023-10-28T06:03:14Z

![16984723334843](https://github.com/kubernetes-sigs/kueue/assets/77265354/2431c4c2-3e3f-4757-ae5f-7cdb251585d4)
It works now, with correct yaml, Job can borrow quota from the next Flavor.
Thanks again for inspiring me! I think this issue has been resolved, can be closed anytime.
