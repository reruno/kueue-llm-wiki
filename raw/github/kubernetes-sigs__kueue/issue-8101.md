# Issue #8101: TAS only removing single SchedulingGate for Kubeflow TrainJob test case

**Summary**: TAS only removing single SchedulingGate for Kubeflow TrainJob test case

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8101

**Last updated**: 2025-12-09T14:29:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bd-hhause](https://github.com/bd-hhause)
- **Created**: 2025-12-05T17:18:42Z
- **Updated**: 2025-12-09T14:29:27Z
- **Closed**: 2025-12-09T13:15:45Z
- **Labels**: `kind/bug`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 23

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Hi @kaisoz I am trying out TAS support with a simplified TrainJob and I could use some help understanding the behavior I'm experiencing. I'm running the test on a KinD cluster to mock our production GPU environment.

The TrainJob is succesfully submitted. I see two pods created, but one of them has the schedulingGates removed and the other does not:
```
k get po -n nexus
NAME                      READY   STATUS            RESTARTS   AGE
test-tas-node-0-0-dbhcx   1/1     Running           0          30m
test-tas-node-0-1-9rrgf   0/1     SchedulingGated   0          30m
```

I see some errors in the kueue controller for the pod with the SchedulingGates: 
```
{
  "level": "error",
  "ts": "2025-12-05T19:11:31.708024711Z",
  "caller": "tas/topology_ungater.go:413",
  "msg": "failed to read rank information from Pods",
  "controller": "tas_topology_ungater",
  "namespace": "nexus",
  "name": "trainjob-test-tas-2b8b5",
  "reconcileID": "1d0a556e-8445-4129-9ab3-855fbf825600",
  "error": "incorrect label value \"1\" for Pod \"nexus/test-tas-node-0-1-djtwk\": validation error: value should be less than 1",
  "stacktrace": "sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable\n\t/workspace/pkg/controller/tas/topology_ungater.go:413\nsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains\n\t/workspace/pkg/controller/tas/topology_ungater.go:328\nsigs.k8s.io/kueue/pkg/controller/tas.(*topologyUngater).Reconcile\n\t/workspace/pkg/controller/tas/topology_ungater.go:222\nsigs.k8s.io/kueue/pkg/controller/core.(*leaderAwareReconciler).Reconcile\n\t/workspace/pkg/controller/core/leader_aware_reconciler.go:77\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"
}
```

**What you expected to happen**:
Both pods in the TrainJob start when the TAS condition is met.

**How to reproduce it (as minimally and precisely as possible)**:
KinD config:
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: kindest/node:v1.30.6
  - role: worker
    image: kindest/node:v1.30.6
    kubeadmConfigPatches:
    - |
      kind: JoinConfiguration
      nodeRegistration:
        name: worker-01
  - role: worker
    image: kindest/node:v1.30.6
    kubeadmConfigPatches:
    - |
      kind: JoinConfiguration
      nodeRegistration:
        name: worker-02
  - role: worker
    image: kindest/node:v1.30.6
    kubeadmConfigPatches:
    - |
      kind: JoinConfiguration
      nodeRegistration:
        name: worker-03
```
With the following patches made:
```
function create_kind_cluster() {
  ensure_host_sysctls
  generate_kind_config "${WORKER_COUNT}"
  kind create cluster --name "${CLUSTER_NAME}" --config "${CONFIG_FILE}"

  worker_nodes=$(kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' | grep -v control-plane)
  for node in $worker_nodes; do
    # These are added for parity with our prod cluster, but aren't required for a repro
    kubectl label node "$node" hardware-type=gpu --overwrite
    kubectl label node "$node" node-role.kubernetes.io/worker="" --overwrite
    kubectl taint node "$node" nvidia.com/gpu=true:NoSchedule --overwrite
    kubectl label node "$node" nvidia.com/gpu.present=true --overwrite
    # Mock the GPU resource
    kubectl patch node "$node" --type=json -p='[{"op": "add", "path": "/status/capacity/nvidia.com~1gpu", "value":"2"}]' --subresource=status
  done
}
```

These are the minimal examples that I used for my test. Our main use case is to avoid admission of multi node workloads when the topology condition of N GPUs over M nodes is not met.

My topology and resource flavor are defined as:
```
Name:         default
API Version:  kueue.x-k8s.io/v1beta2
Kind:         Topology
Spec:
  Levels:
    Node Label:  kubernetes.io/hostname
---
Name:         default
API Version:  kueue.x-k8s.io/v1beta2
Kind:         ResourceFlavor
Spec:
  Node Labels:
    nvidia.com/gpu.present:  true
  Tolerations:
    Effect:       NoSchedule
    Key:          nvidia.com/gpu
    Operator:     Exists
  Topology Name:  default
```

My test TrainingRuntime and TrainJob are defined as:
```
apiVersion: trainer.kubeflow.org/v1alpha1
kind: TrainingRuntime
metadata:
  name: test-tas
spec:
  template:
    spec:
      replicatedJobs:
      - name: node
        template:
          metadata:
            labels:
              trainer.kubeflow.org/trainjob-ancestor-step: trainer
          spec:
            template:
              metadata:
                labels:
                  trainer.kubeflow.org/trainjob-ancestor-step: trainer
              spec:
                containers:
                - name: node
                restartPolicy: Never
                tolerations:
                - effect: NoSchedule
                  key: nvidia.com/gpu
                  operator: Equal
                  value: "true"
---
apiVersion: trainer.kubeflow.org/v1alpha1
kind: TrainJob
metadata:
  name: test-tas
spec:
  managedBy: trainer.kubeflow.org/trainjob-controller
  runtimeRef:
    apiGroup: trainer.kubeflow.org
    kind: TrainingRuntime
    name: test-tas
  trainer:
    image: busybox
    command: ["sleep", "infinity"]

    numNodes: 2

    resourcesPerNode:
      limits:
        cpu: "2"
        memory: 8Gi
        nvidia.com/gpu: "2"
      requests:
        cpu: "2"
        memory: 8Gi
        nvidia.com/gpu: "2"
```

**Anything else we need to know?**:
The clusterqueue and localqueue are minimal for this example and the LocalQueue is named `default`. I can provide those manifests too if necessary.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.30.6
- Kueue version (use `git describe --tags --dirty --always`): v1.15.0
- Kubeflow Trainer version: v2.1.0
- Jobset version: v0.10.0
- Cloud provider or hardware configuration: local KinD cluster
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.5 LTS
- Kernel (e.g. `uname -a`): Linux 6.8.0-52-generic # 53~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Jan 15 19:18:46 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T18:48:58Z

cc @kaisoz @mszadkow @IrvingMg @mbobrovskyi in case some of you have cycles to check what might be going on

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T18:50:55Z

> UPDATE: It looks like the controller is looking up the index by label but the value for the completion index is an annotation. I will look into this more.

Ah, maybe you have an old version of k8s? I remember the index was initially added just as an annotation, and later as a label. I don't exactly remember which version introduced it as a label

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T18:55:03Z

Ok found it, this is the enhancement: https://github.com/kubernetes/enhancements/issues/4017

So it should be by default from 1.28+. Make sure your control-plane (server) is running that version or higher.

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T18:55:15Z

> > UPDATE: It looks like the controller is looking up the index by label but the value for the completion index is an annotation. I will look into this more.
> 
> Ah, maybe you have an old version of k8s? I remember the index was initially added just as an annotation, and later as a label. I don't exactly remember which version introduced it as a label

Sorry, I just updated the issue. Both pods do in fact have the `batch.kubernetes.io/job-completion-index` labels: 

```
Name:             test-tas-node-0-0-784pj
Namespace:        nexus
Priority:         0
Service Account:  default
Node:             worker-01/172.18.0.2
Start Time:       Fri, 05 Dec 2025 12:17:05 -0500
Labels:           batch.kubernetes.io/controller-uid=1c356e2b-f791-426a-9cc6-d24a2429bb30
                  batch.kubernetes.io/job-completion-index=0
                  batch.kubernetes.io/job-name=test-tas-node-0
                  controller-uid=1c356e2b-f791-426a-9cc6-d24a2429bb30
```
```
k describe po -n nexus test-tas-node-0-1-z7f7g | grep completion-index
'                  batch.kubernetes.io/job-completion-index=1
Annotations:      batch.kubernetes.io/job-completion-index: 1
      JOB_COMPLETION_INDEX:   (v1:metadata.labels['batch.kubernetes.io/job-completion-index'])
```

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T18:58:13Z

Also confirming my K8s version:

```
NAME                         STATUS   ROLES           AGE    VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION     CONTAINER-RUNTIME
kind-gpu-sim-control-plane   Ready    control-plane   103m   v1.30.6   172.18.0.7    <none>        Debian GNU/Linux 12 (bookworm)   6.8.0-52-generic   containerd://1.7.18
worker-01                    Ready    worker          103m   v1.30.6   172.18.0.2    <none>        Debian GNU/Linux 12 (bookworm)   6.8.0-52-generic   containerd://1.7.18
worker-02                    Ready    worker          103m   v1.30.6   172.18.0.8    <none>        Debian GNU/Linux 12 (bookworm)   6.8.0-52-generic   containerd://1.7.18
worker-03                    Ready    worker          103m   v1.30.6   172.18.0.3    <none>        Debian GNU/Linux 12 (bookworm)   6.8.0-52-generic   containerd://1.7.18

```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T18:58:48Z

interesting, can you check the workload that you have? `kubectl get workload -oyaml`

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T19:01:09Z

@mimowo Here's the workload:

```
apiVersion: v1
items:
- apiVersion: kueue.x-k8s.io/v1beta2
  kind: Workload
  metadata:
    creationTimestamp: "2025-12-05T18:57:23Z"
    finalizers:
    - kueue.x-k8s.io/resource-in-use
    generation: 1
    labels:
      kueue.x-k8s.io/job-uid: a6f76c94-06d6-42b2-ae50-6cf0a5f80fb1
    name: trainjob-test-tas-95b32
    ownerReferences:
    - apiVersion: trainer.kubeflow.org/v1alpha1
      blockOwnerDeletion: true
      controller: true
      kind: TrainJob
      name: test-tas
      uid: a6f76c94-06d6-42b2-ae50-6cf0a5f80fb1
    resourceVersion: "23691"
    uid: 13333701-b477-4a5c-84d8-84884078e1f3
  spec:
    active: true
    podSets:
    - count: 1
      name: node
      template:
        metadata:
          labels:
            trainer.kubeflow.org/trainjob-ancestor-step: trainer
        spec:
          containers:
          - command:
            - sleep
            - infinity
            image: busybox
            name: node
            resources:
              limits:
                cpu: "2"
                memory: 8Gi
                nvidia.com/gpu: "2"
              requests:
                cpu: "2"
                memory: 8Gi
                nvidia.com/gpu: "2"
          restartPolicy: Never
          tolerations:
          - effect: NoSchedule
            key: nvidia.com/gpu
            operator: Equal
            value: "true"
      topologyRequest:
        podIndexLabel: batch.kubernetes.io/job-completion-index
        subGroupCount: 1
        subGroupIndexLabel: jobset.sigs.k8s.io/job-index
    priority: 0
    queueName: default
  status:
    admission:
      clusterQueue: general
      podSetAssignments:
      - count: 1
        flavors:
          cpu: default
          memory: default
          nvidia.com/gpu: default
        name: node
        resourceUsage:
          cpu: "2"
          memory: 8Gi
          nvidia.com/gpu: "2"
        topologyAssignment:
          levels:
          - kubernetes.io/hostname
          slices:
          - domainCount: 1
            podCounts:
              universal: 1
            valuesPerLevel:
            - universal: worker-01
    conditions:
    - lastTransitionTime: "2025-12-05T18:57:23Z"
      message: Quota reserved in ClusterQueue general
      observedGeneration: 1
      reason: QuotaReserved
      status: "True"
      type: QuotaReserved
    - lastTransitionTime: "2025-12-05T18:57:23Z"
      message: The workload is admitted
      observedGeneration: 1
      reason: Admitted
      status: "True"
      type: Admitted
kind: List
metadata:
  resourceVersion: ""
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:04:04Z

`subGroupIndexLabel: jobset.sigs.k8s.io/job-index`, do your Pods have that label: `jobset.sigs.k8s.io/job-index`?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:06:15Z

Looking at https://github.com/kubernetes-sigs/kueue/issues/8101#issuecomment-3618144068 it does not seem they have it, wondering why this might be.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:07:07Z

can you show me the jobset created `kubectl get jobset -oyaml`? and `kubectl describe jobset`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:12:47Z

hmm, but the error  `label not found: no label \"batch.kubernetes.io/job-completion-index\" for Pod \"nexus/test-tas-node-0-0-dbhcx\"` is clearly thrown from https://github.com/kubernetes-sigs/kueue/blob/e83442679a42a890586398010db22c3bb1804a2b/pkg/util/pod/pod.go#L97

I don't have a clue for now. Maybe others can help to repro and investigate

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:14:10Z

One thing that catches my attention is `numNodes: 2` in the TrainJob spec as we don't seem to use it in our e2e tests, maybe there is a bug here.

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T19:14:36Z

Ah I see where the label confusion is coming from. I previously had the KinD version set to 1.26. Now that it is updated to 1.30.6, there is no longer an error in the kueue controller logs regarding the label. Please disregard the label issue. I've updated my original post to include the error below. 

What I do see now is the following error for the pod with the SchedulingGate:

```
{
  "level": "error",
  "ts": "2025-12-05T19:11:31.708024711Z",
  "caller": "tas/topology_ungater.go:413",
  "msg": "failed to read rank information from Pods",
  "controller": "tas_topology_ungater",
  "namespace": "nexus",
  "name": "trainjob-test-tas-2b8b5",
  "reconcileID": "1d0a556e-8445-4129-9ab3-855fbf825600",
  "error": "incorrect label value \"1\" for Pod \"nexus/test-tas-node-0-1-djtwk\": validation error: value should be less than 1",
  "stacktrace": "sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable\n\t/workspace/pkg/controller/tas/topology_ungater.go:413\nsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains\n\t/workspace/pkg/controller/tas/topology_ungater.go:328\nsigs.k8s.io/kueue/pkg/controller/tas.(*topologyUngater).Reconcile\n\t/workspace/pkg/controller/tas/topology_ungater.go:222\nsigs.k8s.io/kueue/pkg/controller/core.(*leaderAwareReconciler).Reconcile\n\t/workspace/pkg/controller/core/leader_aware_reconciler.go:77\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"
}
```

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T19:16:28Z

@mimowo Here's the jobset for the trainjob:

```
apiVersion: v1
items:
- apiVersion: jobset.x-k8s.io/v1alpha2
  kind: JobSet
  metadata:
    creationTimestamp: "2025-12-05T19:11:30Z"
    generation: 3
    labels:
      kueue.x-k8s.io/queue-name: default
    name: test-tas
    ownerReferences:
    - apiVersion: trainer.kubeflow.org/v1alpha1
      blockOwnerDeletion: true
      controller: true
      kind: TrainJob
      name: test-tas
      uid: 0de9019f-0de6-485f-9e03-5850a4d6fc2e
    resourceVersion: "26904"
    uid: 79e4c170-5016-43e0-8aec-f1a9bf638a37
  spec:
    network:
      enableDNSHostnames: true
      publishNotReadyAddresses: true
    replicatedJobs:
    - groupName: default
      name: node
      replicas: 1
      template:
        metadata:
          labels:
            trainer.kubeflow.org/trainjob-ancestor-step: trainer
        spec:
          completionMode: Indexed
          completions: 2
          parallelism: 2
          template:
            metadata:
              annotations:
                kueue.x-k8s.io/podset-unconstrained-topology: "true"
                kueue.x-k8s.io/workload: trainjob-test-tas-2b8b5
              labels:
                kueue.x-k8s.io/podset: node
                trainer.kubeflow.org/trainjob-ancestor-step: trainer
            spec:
              containers:
              - command:
                - sleep
                - infinity
                image: busybox
                name: node
                resources:
                  limits:
                    cpu: "2"
                    memory: 8Gi
                    nvidia.com/gpu: "2"
                  requests:
                    cpu: "2"
                    memory: 8Gi
                    nvidia.com/gpu: "2"
              nodeSelector:
                nvidia.com/gpu.present: "true"
              restartPolicy: Never
              schedulingGates:
              - name: kueue.x-k8s.io/topology
              tolerations:
              - effect: NoSchedule
                key: nvidia.com/gpu
                operator: Exists
    startupPolicy:
      startupPolicyOrder: AnyOrder
    successPolicy:
      operator: All
    suspend: false
  status:
    conditions:
    - lastTransitionTime: "2025-12-05T19:11:30Z"
      message: jobset is resumed
      reason: ResumeJobs
      status: "False"
      type: Suspended
    replicatedJobsStatus:
    - active: 1
      failed: 0
      name: node
      ready: 0
      succeeded: 0
      suspended: 0
    restarts: 0
kind: List
metadata:
  resourceVersion: ""

```

Thank you for taking a look at this. I'll keep investigating and provide any additional info that I find.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:21:31Z

I suspect there is indeed a bug wrt numNodes.

It looks like the JobSet has "parallelism: 2" , so it should create 2 pods. But our PodsSet in the workload has pods `count: 1`

So, I suspect the bug is in PodSet creation which does not take numNodes into account.

Now, because of the calculations we expect the maximal index for Pod to be 0, but we encounter a Pod which has index "1" - thus the parser is failing in topology_ungater.

If you need a workaround you can probably use `numNodes: 1` and move the numbers down to the TrainerRuntime JobSet template as we do in our e2e tests.

If you have fun fixing then you are more than welcome.

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T19:22:09Z

It does look like the `podSetAssignment` is inconsistent with the TrainJob: 

```
      podSetAssignments:
      - count: 1
        flavors:
          cpu: default
          memory: default
          nvidia.com/gpu: default
        name: node
        resourceUsage:
          cpu: "2"
          memory: 8Gi
          nvidia.com/gpu: "2"
        topologyAssignment:
          levels:
          - kubernetes.io/hostname
          slices:
          - domainCount: 1
            podCounts:
              universal: 1
            valuesPerLevel:
            - universal: worker-01
```

I'd expect the count to be 2 in this case.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:22:27Z

exactly

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-05T19:23:27Z

That makes sense. I will try the workaround you suggested.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T19:30:13Z

I'm also curious because we mostly delegate PodSets creation to the helpers in Kubeflow: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/trainjob/trainjob_controller.go#L219-L286

So maybe there is an issue / inconsistency in the helpers speculation for now, but we really don't see to have custom code computing the PodSet count explicitly in Kueue.

cc @astefanutti @andreyvelich @tenzen-y maybe have some suggestion where the bug might be lurking

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-07T09:31:37Z

@bd-hhause @mimowo I'll try to have a look today 🙂

/assign

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-08T16:54:53Z

I had a look at this and, indeed, this is a bug related to the `numNodes` field, as @mimowo pointed out. The `trainer.numNodes` field defines the number of training nodes that will be created for a training job. The number of pods created is determined by the ML framework being used (Torch, MPI, etc.), although in most cases it ends up matching `numNodes`.

Kueue uses some Kubeflow helpers to reconstruct the TrainJob’s jobset in memory at runtime, avoiding the need for a lookup. However, the assignment of the jobset’s parallelism and completions happens outside these helpers. In my opinion, this should be done inside the helpers, so I’ll open an issue in the Trainer to start a discussion.

In the meantime, I’ve opened [this PR](https://github.com/kubernetes-sigs/kueue/pull/8135), which fixes this problem by performing the assignment in the controller. If the Kubeflow maintainers agree to move this logic into a helper, we can remove this code later, and the tests are already in place.
WDYT @mimowo?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T17:08:25Z

@bd-hhause would you like to test the fix?

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-12-09T14:29:27Z

Hi @kaisoz @mimowo , thanks for the quick fix! I can pull down master and test it out at some point this week.
