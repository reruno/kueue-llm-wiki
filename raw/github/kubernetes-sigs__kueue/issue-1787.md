# Issue #1787: [multikueue] Jobs created on manager cluster remain "stuck" suspended

**Summary**: [multikueue] Jobs created on manager cluster remain "stuck" suspended

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1787

**Last updated**: 2024-03-06T15:56:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-04T10:22:53Z
- **Updated**: 2024-03-06T15:56:59Z
- **Closed**: 2024-03-06T15:56:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/king bug

**What happened**:

JobSets created on the manager cluster remain suspended for a long time (forever?).

**What you expected to happen**:

JobSets get admitted and running.

**How to reproduce it (as minimally and precisely as possible)**:

My setup has 3 clusters, one manager and two workers. On the manager cluster I only have the JobSet CRD installed, and on other clusters I have JobSet CRD with controller. I use Kueue 0.6 with feature-gate=MultiKueue enabled.

This is my manager:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
  admissionChecks:
  - sample-multikueue
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: AdmissionCheck
metadata:
  name: sample-multikueue
spec:
  controllerName: kueue.x-k8s.io/multikueue
  parameters:
    apiGroup: kueue.x-k8s.io
    kind: MultiKueueConfig
    name: multikueue-test
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: MultiKueueConfig
metadata:
  name: multikueue-test
spec:
  clusters:
  - multikueue-test-worker1
  - multikueue-test-worker2
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: MultiKueueCluster
metadata:
  name: multikueue-test-worker1
spec:
  kubeConfig:
    locationType: Secret
    location: worker1-secret
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: MultiKueueCluster
metadata:
  name: multikueue-test-worker2
spec:
  kubeConfig:
    locationType: Secret
    location: worker2-secret
```
my workers:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
```

My Jobset:
```yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  generateName: sleep-job-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  suspend: true
  network:
    enableDNSHostnames: false
    subdomain: some-subdomain
  replicatedJobs:
    - name: workers
      replicas: 1
      template:
        spec:
          parallelism: 1
          completions: 1
          backoffLimit: 0
          template:
            spec:
              containers:
                - name: sleep
                  image: busybox
                  resources:
                    requests:
                      cpu: 1
                      memory: "200Mi"
                  command:
                    - sleep
                  args:
                    - 100s
    - name: driver
      template:
        spec:
          parallelism: 1
          completions: 1
          backoffLimit: 0
          template:
            spec:
              containers:
                - name: sleep
                  image: busybox
                  resources:
                    requests:
                      cpu: 2
                      memory: "200Mi"
                  command:
                    - sleep
                  args:
                    - 100s
```

Once created I see that the workload on the management cluster looks like this:
```yaml
> kubectl get workloads -oyaml
apiVersion: v1
items:
- apiVersion: kueue.x-k8s.io/v1beta1
  kind: Workload
  metadata:
    creationTimestamp: "2024-03-04T10:05:23Z"
    finalizers:
    - kueue.x-k8s.io/resource-in-use
    generation: 1
    labels:
      kueue.x-k8s.io/job-uid: db10c1a0-0781-4693-9676-c67247fdbda5
    name: jobset-sleep-job-hjksj-83145
    namespace: default
    ownerReferences:
    - apiVersion: jobset.x-k8s.io/v1alpha2
      blockOwnerDeletion: true
      controller: true
      kind: JobSet
      name: sleep-job-hjksj
      uid: db10c1a0-0781-4693-9676-c67247fdbda5
    resourceVersion: "9382420"
    uid: 3dbfcda7-65ac-428f-abc1-f781d7297836
  spec:
    active: true
    podSets:
    - count: 1
      name: workers
      template:
        metadata: {}
        spec:
          containers:
          - args:
            - 100s
            command:
            - sleep
            image: busybox
            name: sleep
            resources:
              requests:
                cpu: "1"
                memory: 200Mi
    - count: 1
      name: driver
      template:
        metadata: {}
        spec:
          containers:
          - args:
            - 100s
            command:
            - sleep
            image: busybox
            name: sleep
            resources:
              requests:
                cpu: "2"
                memory: 200Mi
    priority: 0
    priorityClassSource: ""
    queueName: user-queue
  status:
    admission:
      clusterQueue: cluster-queue
      podSetAssignments:
      - count: 1
        flavors:
          cpu: default-flavor
          memory: default-flavor
        name: workers
        resourceUsage:
          cpu: "1"
          memory: 200Mi
      - count: 1
        flavors:
          cpu: default-flavor
          memory: default-flavor
        name: driver
        resourceUsage:
          cpu: "2"
          memory: 200Mi
    admissionChecks:
    - lastTransitionTime: "2024-03-04T10:05:23Z"
      message: ""
      name: sample-multikueue
      state: Pending
    conditions:
    - lastTransitionTime: "2024-03-04T10:05:23Z"
      message: Quota reserved in ClusterQueue cluster-queue
      reason: QuotaReserved
      status: "True"
      type: QuotaReserved
kind: List
metadata:
  resourceVersion: ""
```
Also, there are workloads created on the worker clusters, but not JobSets.

When I edit the workload on manager cluster then it works, the JobSets starts working.

**Anything else we need to know?**:

This clusters were created a couple of days ago, and it used to work. Then I tested today and it no longer works, without any changes.

**Environment**:
- Kubernetes version (use `kubectl version`): 1.28.3-gke.1286000
- Kueue version (use `git describe --tags --dirty --always`): 0.6
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-04T10:23:44Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-03-05T15:19:07Z

#1806 add the connection monitoring and reconnect part of MultiKueue
