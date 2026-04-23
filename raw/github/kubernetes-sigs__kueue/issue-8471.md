# Issue #8471: TAS: TopologyUngater can not recognize rank-based ordering for MPIJob with runLauncherAsWorker

**Summary**: TAS: TopologyUngater can not recognize rank-based ordering for MPIJob with runLauncherAsWorker

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8471

**Last updated**: 2026-01-19T13:03:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-08T15:27:56Z
- **Updated**: 2026-01-19T13:03:15Z
- **Closed**: 2026-01-19T13:03:15Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 30

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When I created a MPIJob with runLaucherAsWorker mode, Kueue failed to assign topology to Pods based on the rank ordering (`training.kubeflow.org/replica-index`) as you can see kueue-controller-manager logs in the following:

```shell
"level":"error","ts":"2026-01-08T14:45:32.36847947Z","caller":"tas/topology_ungater.go:415","msg":"failed to read rank information from Pods","controller":"tas_topology_ungater","namespace":"default","name":"mpijob-pi-8e2f6","reconcileID":"8d2976c6-f349-4783-a4ec-780f6435cca7","error":"incorrect label value \"2\" for Pod \"default/pi-worker-1\": validation error: value should be less than 2","stacktrace":"sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable\n\t/workspace/pkg/controller/tas/topology_ungater.go:415\nsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains\n\t/workspace/pkg/controller/tas/topology_ungater.go:330\nsigs.k8s.io/kueue/pkg/controller/tas.(*topologyUngater).Reconcile\n\t/workspace/pkg/controller/tas/topology_ungater.go:222\nsigs.k8s.io/kueue/pkg/controller/core.(*leaderAwareReconciler).Reconcile\n\t/workspace/pkg/controller/core/leader_aware_reconciler.go:77\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
```

The root cause is that TopologyUngater expects the max rank index is less than the number of ranks in https://github.com/kubernetes-sigs/kueue/blob/e355ea8d26bb8e597e7304b626df96e147760a64/pkg/util/pod/pod.go#L106-L115.

However, runLaucherAsWorker MPIJob worker replica starts from 1 (`training.kubeflow.org/replica-index: 1`) instead of 0 because index 0 (`training.kubeflow.org/replica-index: 0`) is the launcher replica.

**What you expected to happen**:
TAS succeded to assign topologies to Pods based on rank ordering (`training.kubeflow.org/replica-index`).

**How to reproduce it (as minimally and precisely as possible)**:

The following is a step-by-step reproducible flow:

1. Setup cluster, Kueue, and MPIOperator

```shell
$ kind create cluster

$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.15.2/manifests.yaml

$ cat <<EOF | kubectl apply -f -
apiVersion: kueue.x-k8s.io/v1beta2
kind: Topology
metadata:
  name: "default"
spec:
  levels:
  - nodeLabel: "kubernetes.io/hostname"
---
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta2
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    kubernetes.io/os: linux
  topologyName: "default"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "tas-cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 100
      - name: "memory"
        nominalQuota: 100Gi
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "default"
  name: "tas-user-queue"
spec:
  clusterQueue: "tas-cluster-queue"
EOF

$ kubectl apply --server-side -f https://raw.githubusercontent.com/kubeflow/mpi-operator/v0.7.0/deploy/v2beta1/mpi-operator.yaml
```

2. Create MPIJob with runLauncherAsWorker

```shell
$ cat <<EOF | k apply -f -
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: pi
  labels:
    kueue.x-k8s.io/queue-name: "tas-user-queue"
spec:
  slotsPerWorker: 1
  runLauncherAsWorker: true  
  runPolicy:
    cleanPodPolicy: Running
    ttlSecondsAfterFinished: 60
  sshAuthMountPath: /home/mpiuser/.ssh
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
          - image: mpioperator/mpi-pi:openmpi
            name: mpi-launcher
            securityContext:
              runAsUser: 1000
            command:
            - mpirun
            args:
            - -n
            - "2"
            - /home/mpiuser/pi
            resources:
              limits:
                cpu: 1
                memory: 1Gi
    Worker:
      replicas: 2
      template:
        spec:
          containers:
          - image: mpioperator/mpi-pi:openmpi
            name: mpi-worker
            securityContext:
              runAsUser: 1000
            command:
            - /usr/sbin/sshd
            args:
            - -De
            - -f
            - /home/mpiuser/.sshd_config
            resources:
              limits:
                cpu: 1
                memory: 1Gi
EOF
```

**Anything else we need to know?**:

The created Pods are following:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2026-01-08T14:46:41Z"
  finalizers:
  - batch.kubernetes.io/job-tracking
  generateName: pi-launcher-
  labels:
    batch.kubernetes.io/controller-uid: 23c06567-c814-4e70-8679-69353e459c23
    batch.kubernetes.io/job-name: pi-launcher
    controller-uid: 23c06567-c814-4e70-8679-69353e459c23
    job-name: pi-launcher
    training.kubeflow.org/job-name: pi
    training.kubeflow.org/job-role: launcher
    training.kubeflow.org/operator-name: mpi-operator
    training.kubeflow.org/replica-index: "0"
  name: pi-launcher-tntsp
  namespace: default
---
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kueue.x-k8s.io/podset-unconstrained-topology: "true"
    kueue.x-k8s.io/workload: mpijob-pi-1584c
  creationTimestamp: "2026-01-08T14:46:41Z"
  labels:
    kueue.x-k8s.io/podset: worker
    training.kubeflow.org/job-name: pi
    training.kubeflow.org/job-role: worker
    training.kubeflow.org/operator-name: mpi-operator
    training.kubeflow.org/replica-index: "1"
  name: pi-worker-0
  namespace: default
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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T15:34:35Z

We might need to allow them to specify `kueue.x-k8s.io/podset-group-name` for unconstrained and implicit TAS since runLauncherAsWorker is similar to PodSet group pattern. In this situation, Launcher and Worker are the same group over the replicaSpecs, similar to the LWS leader grouped worker.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T16:12:37Z

Thank you for reporting the issue.
 
So some approaches I can see:
1. introduce `PodIndexOffset: 1` in https://github.com/kubernetes-sigs/kueue/blob/e355ea8d26bb8e597e7304b626df96e147760a64/apis/kueue/v1beta2/workload_types.go#L191C2-L191C15 which would be set by the MPIJob integration. Since this requires new API field we may as a quick fix introduce a hack in the TopologyUngater to use `PodIndexOffset: 1` for `training.kubeflow.org/replica-index`
2. in the MPIJob or, MPIJob integration in Kueue inject in webhook a label counting from 0: "kueue.x-k8s.io/pod-group-pod-index" (basically re-write counting from 1 to counting from 0).

I'm ok either way, (2.) does not require any API changes, just a change in the integration logic, so seems lighter and we could cherrypick.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T16:23:39Z

> Thank you for reporting the issue.
> 
> So some approaches I can see:
> 
> 1. introduce `PodIndexOffset: 1` in https://github.com/kubernetes-sigs/kueue/blob/e355ea8d26bb8e597e7304b626df96e147760a64/apis/kueue/v1beta2/workload_types.go#L191C2-L191C15 which would be set by the MPIJob integration. Since this requires new API field we may as a quick fix introduce a hack in the TopologyUngater to use `PodIndexOffset: 1` for `training.kubeflow.org/replica-index`
> 2. in the MPIJob or, MPIJob integration in Kueue inject in webhook a label counting from 0: "kueue.x-k8s.io/pod-group-pod-index" (basically re-write counting from 1 to counting from 0).
> 
> I'm ok either way, (2.) does not require any API changes, just a change in the integration logic, so seems lighter and we could cherrypick.

Thank you for proposing alternatives.
Either 1 or 2, we need to hack already assigned training.kubeflow.org/replica-index label (still keep using kf label vs put another lable). 

I think (1) is slightly dangerous for the maintenance since `offset` could curve the original label (training.kubeflow.org/replica-index) semantics. Instead of that, computing kueue.x-k8s.io/pod-group-pod-index based on training.kubeflow.org/replica-index, then keep original label semantics, sounds straightforward.

So, I think (2) is better.

WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T16:25:12Z

sgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T16:27:12Z

> sgtm

Awesome!

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-08T21:45:48Z

I'm fine to fix this but I'm curious how long we support Both Kubeflow Training Operator v1 and Trainer together.

Does this same problem happen for TrainJob MPI?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-08T21:46:08Z

cc @andreyvelich

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T02:45:11Z

> I'm fine to fix this but I'm curious how long we support Both Kubeflow Training Operator v1 and Trainer together.
> 

Kufeflow has 3 types of Training components: Trainer v1 (TFJob, PyTorchJob, XGBoostJob, ...), Trainer v2 (TrainJob), and MPIOperator (MPIJob).
Trainer v1 will be shutting down in 2026 mid, but MPIOperator will be supported after Trainer v1 deletion.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T02:47:49Z

> > Does this same problem happen for TrainJob MPI?

I didn't check that.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T03:11:18Z

@kannon92 As I check TrainJob MPI in my local, TrainJob doesn't have this problem, but it has another problem, where each replica is handled as another role, even though launcher and worker should be the same replica in case of runLauncherAsNode.

I will create another issue in this repository.

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-01-09T13:43:08Z

@tenzen-y I would love us at some point to talk about MPIJob future given the recent support of MPI in TrainJob.

Given that @vsoch is working on integrating Flux within Trainer: https://github.com/kubeflow/trainer/pull/2909, it will allow us to support other flavors of MPI like PMIx which is not possible today in MPI Operator: https://github.com/kubeflow/mpi-operator/issues/12

I think, users will get additional benefits if they migrate their MPI workloads to TrainJob.

cc @astefanutti

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T14:26:39Z

> [@tenzen-y](https://github.com/tenzen-y) I would love us at some point to talk about MPIJob future given the recent support of MPI in TrainJob.
> 
> Given that [@vsoch](https://github.com/vsoch) is working on integrating Flux within Trainer: [kubeflow/trainer#2909](https://github.com/kubeflow/trainer/pull/2909), it will allow us to support other flavors of MPI like PMIx which is not possible today in MPI Operator: [kubeflow/mpi-operator#12](https://github.com/kubeflow/mpi-operator/issues/12)
> 
> I think, users will get additional benefits if they migrate their MPI workloads to TrainJob.
> 
> cc [@astefanutti](https://github.com/astefanutti)

Yes, we can discuss it. I'm not familiar with the Flux framework. So, if it can natively (no code changes) support deepspeed, PyTorch, other ML frameworks, we can migrate that. Otherwise, it might be hard migration for end users.

But, in this issue, it is out of scope.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T10:56:31Z

> Thank you for reporting the issue.
> 
> So some approaches I can see:
> 
> 1. introduce `PodIndexOffset: 1` in https://github.com/kubernetes-sigs/kueue/blob/e355ea8d26bb8e597e7304b626df96e147760a64/apis/kueue/v1beta2/workload_types.go#L191C2-L191C15 which would be set by the MPIJob integration. Since this requires new API field we may as a quick fix introduce a hack in the TopologyUngater to use `PodIndexOffset: 1` for `training.kubeflow.org/replica-index`
> 2. in the MPIJob or, MPIJob integration in Kueue inject in webhook a label counting from 0: "kueue.x-k8s.io/pod-group-pod-index" (basically re-write counting from 1 to counting from 0).
> 
> I'm ok either way, (2.) does not require any API changes, just a change in the integration logic, so seems lighter and we could cherrypick.

@mimowo After some additional investigations, I found that (2) is not possible on the Kueue side because the Kueue PodIntegration webhook doesn't have a way to determine if an incoming Pod should consider an offset and add `kueue.x-k8s.io/pod-group-pod-index` to Pod annotations.

As a mitigation, we can consider implementing a Pod defaulting webhook for MPIJob integration, but this is much more complicated because webhook endpoints are called randomly, which means we need to handle race conditions between PodIntegration webhook defaultings and MPIJobIntegration webhook defaultings.

So, we might need to select (1).... Any thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T10:59:18Z

> @mimowo After some additional investigations, I found that (2) is not possible on the Kueue side because the Kueue PodIntegration webhook doesn't have a way to determine if an incoming Pod should consider an offset and add kueue.x-k8s.io/pod-group-pod-index to Pod annotations.

I think (2.) is possible but you also need to set the `kueue.x-k8s.io/pod-group-pod-index-label: kueue.x-k8s.io/pod-group-pod-index` annotation. In fact for the label you can then use any name, does not need to be `kueue.x-k8s.io/pod-group-pod-index`. Could you verify that?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:06:43Z

> > [@mimowo](https://github.com/mimowo) After some additional investigations, I found that (2) is not possible on the Kueue side because the Kueue PodIntegration webhook doesn't have a way to determine if an incoming Pod should consider an offset and add kueue.x-k8s.io/pod-group-pod-index to Pod annotations.
> 
> I think (2.) is possible but you also need to set the `kueue.x-k8s.io/pod-group-pod-index-label: kueue.x-k8s.io/pod-group-pod-index` annotation. In fact for the label you can then use any name, does not need to be `kueue.x-k8s.io/pod-group-pod-index`. Could you verify that?

Yes, that's right. we should specify the label. However, Pod integration webhook just copy index from `kueue.x-k8s.io/pod-group-pod-index`:

https://github.com/kubernetes-sigs/kueue/blob/b29a3a03798877b8304d9a1aa714a34127a42805/pkg/controller/jobs/pod/pod_webhook.go#L177-L182

What is the component name you assume adding kueue.x-k8s.io/pod-group-pod-index to Pod?
Currently, MPIJob Pods will be created in the following step:

1. User: Create MPIJob
2. MPIOperator: Create batch/v1 Job for launcher
3. Kueue: Admit MPIJob
4. KCM: Create Pods for batch/v1 Job
5. MPIOperator: Create Pods for workers

So, someone needs to be in charge of adding the kueue.x-k8s.io/pod-group-pod-index annotation to created Pods.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T11:34:05Z

> What is the component name you assume adding kueue.x-k8s.io/pod-group-pod-index to Pod?

I'm thinking to do this inside Kueue code in the mpijob_webhook to set `kueue.x-k8s.io/pod-group-pod-index` by decrementing by 1 `training.kubeflow.org/replica-index`.

I might be missing something, but IIUC MPI project sets the replica label already during creation (and not in webhook): https://github.com/kubeflow/mpi-operator/blob/master/pkg/controller/mpi_job_controller.go#L1464

So, are you sure there is an issue with random order of calling the webhooks?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:51:22Z

> I might be missing something, but IIUC MPI project sets the replica label already during creation (and not in webhook): https://github.com/kubeflow/mpi-operator/blob/master/pkg/controller/mpi_job_controller.go#L1464

yes, your understanding is correct.

> I'm thinking to do this inside Kueue code in the mpijob_webhook to set kueue.x-k8s.io/pod-group-pod-index by decrementing by 1 training.kubeflow.org/replica-index.

So, do you assume adding another endpoint for MPIJob Pods to https://github.com/kubernetes-sigs/kueue/tree/main/pkg/controller/jobs/mpijob (e.g., mpijob_pod_webhook.go)? 

```go
type MPIJobPodWebhook struct {
	client                       client.Client
	manageJobsWithoutQueueName   bool
	managedJobsNamespaceSelector labels.Selector
	kubeServerVersion            *kubeversion.ServerVersionFetcher
}
```

Currently, MPIJob integration have endpoint only for MPIJob: https://github.com/kubernetes-sigs/kueue/blob/18aa9e9a2c8dad20445e4cbf147bd05f30a5ee2d/config/components/webhook/manifests.yaml#L142-L160

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:58:37Z

> So, are you sure there is an issue with random order of calling the webhooks?

If we add MPIJobPodWebhook and mutate Pod labels, both Pod integration defaulter and MPIJob integration defaulter mutate Pods randomly. So, I was concerned that any rollback might happen randamly in some times.

But, I might be too worried. Do you think that such an edge case is possible to avoid on the kube-apiserver side?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T12:00:15Z

> So, do you assume adding another endpoint for MPIJob Pods to https://github.com/kubernetes-sigs/kueue/tree/main/pkg/controller/jobs/mpijob (e.g., mpijob_pod_webhook.go)?
> Currently, MPIJob integration have endpoint only for MPIJob:

I see, yeah this is what I was thinking about, but this seems quite involving, and the performance will worsen. It will also be very specific for MPIJob. Smilar naming pattern 0 for leader and 1... for workers seems like also possible for other projects.

So on the second thought I'm leaning to introduce (2.). Maybe we can make it more lightweight by a dedicated annotation rather than workload-level field, say `kueue.x-k8s.io/pod-index-offset: 1` would be set in the MPIJob template, and subtracted in computations. WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T12:15:57Z

> I see, yeah this is what I was thinking about, but this seems quite involving, and the performance will worsen. It will also be very specific for MPIJob. Smilar naming pattern 0 for leader and 1... for workers seems like also possible for other projects.

Yeah exactly. The performance is another negative point for option (1).

> So on the second thought I'm leaning to introduce (2.). Maybe we can make it more lightweight by a dedicated annotation rather than workload-level field, say kueue.x-k8s.io/pod-index-offset: 1 would be set in the MPIJob template, and subtracted in computations. WDYT?

Do you assume a offset annotation is added by Kueue MPIJob integration webhook? or users? 
TBH, I'd handle offset annotation by Kueue side rather than users for better UX.

But, in your solution, we have another problem. Who can recompute index based on offset annotation? If the answer is Pod integration webhook, it means that (1) Pod webhook needs to recognize MPIJob specific index label (training.kubeflow.org/replica-index) to obtain original index or (2) Pod webhook needs to find root resource to find Workload resource for .spec.topologyRequest.podIndexLabel. 

I am missing anything what you represent. Please let me know whether this aligns with your idea.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T12:38:24Z

> Do you assume a offset annotation is added by Kueue MPIJob integration webhook? or users?

I think by "Kueue MPIJob integration webhook" we could inject it into the PodTemplate.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T12:39:37Z

> But, in your solution, we have another problem. Who can recompute index based on offset annotation?

I think the effective index would be computed in TopologyUngater. It will just additionally subtract the value of `kueue.x-k8s.io/pod-index-offset` from what it reads from `training.kubeflow.org/replica-index`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T12:48:18Z

> > But, in your solution, we have another problem. Who can recompute index based on offset annotation?
> 
> I think the effective index would be computed in TopologyUngater. It will just additionally subtract the value of `kueue.x-k8s.io/pod-index-offset` from what it reads from `training.kubeflow.org/replica-index`

Oh, I see. I can catch up what you mean. In that case, the offset annotation could work well, thank you!

As another point, I'm wondering if we should use `kueue.x-k8s.io/pod-group-pod-index-offset` rather than `kueue.x-k8s.io/pod-index-offset` to align with `kueue.x-k8s.io/pod-group-pod-index` pattern. Any thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T12:54:49Z

> I'm wondering if we should use kueue.x-k8s.io/pod-group-pod-index-offset rather than kueue.x-k8s.io/pod-index-offset to align with kueue.x-k8s.io/pod-group-pod-index pattern. Any thoughts?

I'm ok with `kueue.x-k8s.io/pod-group-pod-index-offset`. Yes, it will not be used on PodGroup as integration, but it will be used for the "conceptual" pod proup, so I'm ok with either that or `kueue.x-k8s.io/pod-index-offset`. No preference really.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T13:50:31Z

> > I'm wondering if we should use kueue.x-k8s.io/pod-group-pod-index-offset rather than kueue.x-k8s.io/pod-index-offset to align with kueue.x-k8s.io/pod-group-pod-index pattern. Any thoughts?
> 
> I'm ok with `kueue.x-k8s.io/pod-group-pod-index-offset`. Yes, it will not be used on PodGroup as integration, but it will be used for the "conceptual" pod proup, so I'm ok with either that or `kueue.x-k8s.io/pod-index-offset`. No preference really.

Uhm, that sounds reasonable. OTOH, we call it PodIndexLabel as we can see in https://github.com/kubernetes-sigs/kueue/blob/1d44089f5250e741e4ffbcd91cb576bdc600f8e6/pkg/controller/jobframework/tas.go#L35-L38, which is accommodated by the Pod index label represented by each framework-specific index label.

So, I think your first proposal, `kueue.x-k8s.io/pod-index-offset` sounds better.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T13:59:11Z

Yes, maybe we should have named the previous annotation/labels as `kueue.x-k8s.io/pod-index`, and `kueue.x-k8s.io/pod-index-label`, but it does not feel like we need renaming now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T15:06:07Z

> Yes, maybe we should have named the previous annotation/labels as `kueue.x-k8s.io/pod-index`, and `kueue.x-k8s.io/pod-index-label`, but it does not feel like we need renaming now.

Yes, I think so too. We can just introduce a new `kueue.x-k8s.io/pod-index-offset` annotation.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T19:04:21Z

I fixed this in https://github.com/kubernetes-sigs/kueue/pull/8618

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T12:37:06Z

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/8618#discussion_r2704597604, I confirmed that our LWS integration has the same problem. Let me open another issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T12:44:57Z

> As we discussed in [#8618 (comment)](https://github.com/kubernetes-sigs/kueue/pull/8618#discussion_r2704597604), I confirmed that our LWS integration has the same problem. Let me open another issue.

Created: https://github.com/kubernetes-sigs/kueue/issues/8661
