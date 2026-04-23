# Issue #2096: when a jobset type workload created using Kueue is suspended

**Summary**: when a jobset type workload created using Kueue is suspended

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2096

**Last updated**: 2024-04-29T15:54:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@googs1025](https://github.com/googs1025)
- **Created**: 2024-04-29T12:39:13Z
- **Updated**: 2024-04-29T15:54:12Z
- **Closed**: 2024-04-29T15:37:29Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 16

## Description

When I create a jobset type workload using the following configuration, I notice that it remains in a suspended state.
I'm unsure whether there are any errors in my configuration or if there are any operations that haven't been done.
The configuration for "cluster-queue", "local-queue", and "resource-flavor" is as follows:
```bash
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory", "pods"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 20
      - name: "memory"
        nominalQuota: 360Gi
      - name: "pods"
        nominalQuota: 500
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default-flavor
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: default
  name: user-queue
spec:
  clusterQueue: cluster-queue
```

```bash
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  generateName: sleep-job-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
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
                      cpu: 1
                      memory: "200Mi"
                  command:
                    - sleep
                  args:
                    - 100s
```

```bash
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get queue
NAME         CLUSTERQUEUE    PENDING WORKLOADS   ADMITTED WORKLOADS
user-queue   cluster-queue   0                   0
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get clusterqueue
NAME            COHORT   PENDING WORKLOADS
cluster-queue            0
root@VM-0-15-ubuntu:/home/ubuntu# kubectl create -f jobset-sample.yaml
jobset.jobset.x-k8s.io/sleep-job-vs6f5 created
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get jobset
NAME              RESTARTS   COMPLETED   SUSPENDED   AGE
sleep-job-vs6f5                          true        4s
```
describe `jobset` and `workload`
```bash
root@VM-0-15-ubuntu:/home/ubuntu# kubectl describe jobset
Name:         sleep-job-vs6f5
Namespace:    default
Labels:       kueue.x-k8s.io/queue-name=user-queue
Annotations:  <none>
API Version:  jobset.x-k8s.io/v1alpha2
Kind:         JobSet
Metadata:
  Creation Timestamp:  2024-04-29T12:33:55Z
  Generate Name:       sleep-job-
  Generation:          1
  Resource Version:    67994
  UID:                 1a52f8fa-fa81-4b3f-b826-592953d2b08d
Spec:
  Network:
    Enable DNS Hostnames:  false
    Subdomain:             some-subdomain
  Replicated Jobs:
    Name:      workers
    Replicas:  1
    Template:
      Metadata:
      Spec:
        Backoff Limit:    0
        Completion Mode:  Indexed
        Completions:      1
        Parallelism:      1
        Template:
          Metadata:
          Spec:
            Containers:
              Args:
                100s
              Command:
                sleep
              Image:  busybox
              Name:   sleep
              Resources:
                Requests:
                  Cpu:       1
                  Memory:    200Mi
            Restart Policy:  OnFailure
    Name:                    driver
    Replicas:                1
    Template:
      Metadata:
      Spec:
        Backoff Limit:    0
        Completion Mode:  Indexed
        Completions:      1
        Parallelism:      1
        Template:
          Metadata:
          Spec:
            Containers:
              Args:
                100s
              Command:
                sleep
              Image:  busybox
              Name:   sleep
              Resources:
                Requests:
                  Cpu:       1
                  Memory:    200Mi
            Restart Policy:  OnFailure
  Success Policy:
    Operator:  All
  Suspend:     true
Status:
  Conditions:
    Last Transition Time:  2024-04-29T12:33:55Z
    Message:               jobset is suspended
    Reason:                SuspendedJobs
    Status:                True
    Type:                  Suspended
  Replicated Jobs Status:
    Active:     0
    Failed:     0
    Name:       workers
    Ready:      0
    Succeeded:  0
    Suspended:  1
    Active:     0
    Failed:     0
    Name:       driver
    Ready:      0
    Succeeded:  0
    Suspended:  1
Events:
  Type    Reason           Age   From                                     Message
  ----    ------           ----  ----                                     -------
  Normal  CreatedWorkload  12s   jobset.x-k8s.io/jobset-kueue-controller  Created Workload: default/jobset-sleep-job-vs6f5-8e5eb
  Normal  SuspendedJobs    12s   jobset                                   jobset is suspended
root@VM-0-15-ubuntu:/home/ubuntu# kubectl describe  workload
Name:         jobset-sleep-job-vs6f5-8e5eb
Namespace:    default
Labels:       kueue.x-k8s.io/job-uid=1a52f8fa-fa81-4b3f-b826-592953d2b08d
Annotations:  <none>
API Version:  kueue.x-k8s.io/v1beta1
Kind:         Workload
Metadata:
  Creation Timestamp:  2024-04-29T12:33:55Z
  Finalizers:
    kueue.x-k8s.io/resource-in-use
  Generation:  1
  Owner References:
    API Version:           jobset.x-k8s.io/v1alpha2
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  JobSet
    Name:                  sleep-job-vs6f5
    UID:                   1a52f8fa-fa81-4b3f-b826-592953d2b08d
  Resource Version:        67984
  UID:                     bb328436-4241-4ce9-8417-d98694a0f6f9
Spec:
  Active:  true
  Pod Sets:
    Count:  1
    Name:   workers
    Template:
      Metadata:
      Spec:
        Containers:
          Args:
            100s
          Command:
            sleep
          Image:  busybox
          Name:   sleep
          Resources:
            Requests:
              Cpu:       1
              Memory:    200Mi
        Restart Policy:  OnFailure
    Count:               1
    Name:                driver
    Template:
      Metadata:
      Spec:
        Containers:
          Args:
            100s
          Command:
            sleep
          Image:  busybox
          Name:   sleep
          Resources:
            Requests:
              Cpu:        1
              Memory:     200Mi
        Restart Policy:   OnFailure
  Priority:               0
  Priority Class Source:
  Queue Name:             user-queue
Status:
  Admission:
    Cluster Queue:  cluster-queue
    Pod Set Assignments:
      Count:  1
      Flavors:
        Cpu:     default-flavor
        Memory:  default-flavor
        Pods:    default-flavor
      Name:      workers
      Resource Usage:
        Cpu:     1
        Memory:  200Mi
        Pods:    1
      Count:     1
      Flavors:
        Cpu:     default-flavor
        Memory:  default-flavor
        Pods:    default-flavor
      Name:      driver
      Resource Usage:
        Cpu:     1
        Memory:  200Mi
        Pods:    1
  Conditions:
    Last Transition Time:  2024-04-29T12:33:55Z
    Message:               Quota reserved in ClusterQueue cluster-queue
    Reason:                QuotaReserved
    Status:                True
    Type:                  QuotaReserved
    Last Transition Time:  2024-04-29T12:33:55Z
    Message:               The workload is admitted
    Reason:                Admitted
    Status:                True
    Type:                  Admitted
Events:
  Type    Reason         Age   From             Message
  ----    ------         ----  ----             -------
  Normal  QuotaReserved  65s   kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 1s
  Normal  Admitted       65s   kueue-admission  Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T14:44:32Z

@googs1025 I could not reproduce your issue. Could you share the reproducible steps?

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:00:00Z

The order in which I run
```bash
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get clusterqueue
No resources found

root@VM-0-15-ubuntu:/home/ubuntu# kubectl get localqueue
No resources found in default namespace.

root@VM-0-15-ubuntu:/home/ubuntu# kubectl apply -f cluster-queue.yaml
clusterqueue.kueue.x-k8s.io/cluster-queue created
resourceflavor.kueue.x-k8s.io/default-flavor created
root@VM-0-15-ubuntu:/home/ubuntu# kubectl apply -f local-queue.yaml
localqueue.kueue.x-k8s.io/user-queue created

root@VM-0-15-ubuntu:/home/ubuntu# kubectl create -f jobset-sample.yaml
jobset.jobset.x-k8s.io/sleep-job-rkd5w created

root@VM-0-15-ubuntu:/home/ubuntu# kubectl get jobset
NAME              RESTARTS   COMPLETED   SUSPENDED   AGE
sleep-job-rkd5w                          true        5s

```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T15:03:18Z

What version did you install kueue, JobSet, and Kubernetes?

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:14:22Z

The k8s I use is deployed with kind, and the version is v1.24. I don’t know if it is a version problem.
`kubectl apply --server-side -f https://github.com/kubernetes-sigs/jobset/releases/download/v0.5.0/manifests.yaml`
`kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/manifests.yaml`
```
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get node
NAME                     STATUS   ROLES           AGE   VERSION
cluster1-control-plane   Ready    control-plane   10h   v1.24.15
cluster1-worker          Ready    <none>          10h   v1.24.15
cluster1-worker2         Ready    <none>          10h   v1.24.15
```

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:20:12Z

I have the same problem using v1.28.0
```bash
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get node
NAME                     STATUS   ROLES           AGE     VERSION
cluster1-control-plane   Ready    control-plane   2m18s   v1.28.0
cluster1-worker          Ready    <none>          114s    v1.28.0
cluster1-worker2         Ready    <none>          115s    v1.28.0
root@VM-0-15-ubuntu:/home/ubuntu# kubectl get jobset
NAME              RESTARTS   COMPLETED   SUSPENDED   AGE
sleep-job-snpwg                          true        60s
```

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:22:09Z

Is it a problem with the flavors settings?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T15:24:20Z

I could reproduce this. It seems that the root cause is below:

```
"msg":"Reconciler error","controller":"jobset","controllerGroup":"jobset.x-k8s.io","controllerKind":"JobSet","JobSet":{"name":"sleep-job-lldhs","namespace":"default"},"namespace":"default","name":"sleep-job-lldhs","reconcileID":"9e764bc9-0c2b-466e-bc04-ec59ca4cc330","error":"admission webhook \"vjobset.kb.io\" denied the request: spec.labels[managedBy]: Invalid value: \"jobset.sigs.k8s.io/jobset-controller\": field is immutable","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:227"}
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T15:31:17Z

Once I installed the JobSet with main branch, the errors above are resolved.

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:31:33Z

This should be caused by a bug inside the jobset controller .
I checked the jobset controller log.
```bash
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:227
2024-04-29T15:53:29Z	LEVEL(-2)	Reconciling JobSet	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"sleep-job-xjzvf","namespace":"default"}, "namespace": "default", "name": "sleep-job-xjzvf", "reconcileID": "180d621e-8618-453e-9e39-036ef9a431d0", "jobset": {"name":"sleep-job-xjzvf","namespace":"default"}}
2024-04-29T15:53:29Z	LEVEL(-2)	Reconciling JobSet	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"sleep-job-xjzvf","namespace":"default"}, "namespace": "default", "name": "sleep-job-xjzvf", "reconcileID": "c3d22260-ee05-4e43-a57c-1a3387f07129", "jobset": {"name":"sleep-job-xjzvf","namespace":"default"}}
2024-04-29T15:53:29Z	ERROR	updating jobset status	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"sleep-job-xjzvf","namespace":"default"}, "namespace": "default", "name": "sleep-job-xjzvf", "reconcileID": "c3d22260-ee05-4e43-a57c-1a3387f07129", "error": "Operation cannot be fulfilled on jobsets.jobset.x-k8s.io \"sleep-job-xjzvf\": the object has been modified; please apply your changes to the latest version and try again"}
sigs.k8s.io/jobset/pkg/controllers.(*JobSetReconciler).updateJobSetStatus
	/workspace/pkg/controllers/jobset_controller.go:242
sigs.k8s.io/jobset/pkg/controllers.(*JobSetReconciler).Reconcile
	/workspace/pkg/controllers/jobset_controller.go:116
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:119
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:316
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:266
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:227
2024-04-29T15:53:29Z	ERROR	Reconciler error	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"sleep-job-xjzvf","namespace":"default"}, "namespace": "default", "name": "sleep-job-xjzvf", "reconcileID": "c3d22260-ee05-4e43-a57c-1a3387f07129", "error": "Operation cannot be fulfilled on jobsets.jobset.x-k8s.io \"sleep-job-xjzvf\": the object has been modified; please apply your changes to the latest version and try again"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:329
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:266
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:227
2024-04-29T15:53:29Z	LEVEL(-2)	Reconciling JobSet	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"sleep-job-xjzvf","namespace":"default"}, "namespace": "default", "name": "sleep-job-xjzvf", "reconcileID": "21ef2335-2e25-46eb-a73a-2425ea55c9ea", "jobset": {"name":"sleep-job-xjzvf","namespace":"default"}}
2024-04-29T15:53:29Z	LEVEL(-2)	Reconciling JobSet	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"sleep-job-xjzvf","namespace":"default"}, "namespace": "default", "name": "sleep-job-xjzvf", "reconcileID": "43327a94-d2b7-41ae-bd2f-6e215d2354f0", "jobset": {"name":"sleep-job-xjzvf","namespace":"default"}}

```

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:32:48Z

> Once I installed the JobSet with main branch, the errors above are resolved.

This is a bit strange

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T15:34:11Z

I guess that the bug above was resolved by https://github.com/kubernetes-sigs/jobset/pull/528 or https://github.com/kubernetes-sigs/jobset/pull/527.

Those commits is not released, yet.

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:35:20Z

Maybe I should let @kannon92  @danielvegamyhre know about this too
/PTAL I found that there seems to be a bug in jobset version v0.5.0

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:36:28Z

> I guess that the bug above was resolved by [kubernetes-sigs/jobset#528](https://github.com/kubernetes-sigs/jobset/pull/528) or [kubernetes-sigs/jobset#527](https://github.com/kubernetes-sigs/jobset/pull/527).
> 
> Those commits is not released, yet.

I see thanks. @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T15:37:30Z

Anyway, this is not kueue related bug. Please open an issue on the JobSet side.
I believe that JobSet can release a patch version v0.5.1.

/close

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-29T15:40:15Z

Thank you for solving the problem for me, thank you very much. @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T15:45:59Z

/kind support
