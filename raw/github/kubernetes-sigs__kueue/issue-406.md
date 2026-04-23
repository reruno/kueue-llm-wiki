# Issue #406: Kueue workloads admitted but jobs remain suspended

**Summary**: Kueue workloads admitted but jobs remain suspended

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/406

**Last updated**: 2022-10-04T14:32:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@eskaug](https://github.com/eskaug)
- **Created**: 2022-09-30T16:00:33Z
- **Updated**: 2022-10-04T14:32:14Z
- **Closed**: 2022-10-03T18:42:16Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What happened**:
Kueue workloads correctly show admission, but jobs remain suspended and no pods are created.

**What you expected to happen**:
Job should be unsuspended, and pod created to begin work.

**How to reproduce it (as minimally and precisely as possible)**:
My nodes are labeled individually to match my ResourceFlavor labels:
```
kubectl label nodes node1 flavor-label=flavor-label-1
kubectl label nodes node2 flavor-label=flavor-label-2
kubectl label nodes node3 flavor-label=flavor-label-3
kubectl label nodes node4 flavor-label=flavor-label-4
```

resourcelabels.yaml
```
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ResourceFlavor
metadata:
  name: flavor-1
  labels:
    flavor-label: flavor-label-1
---
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ResourceFlavor
metadata:
  name: flavor-2
  labels:
    flavor-label: flavor-label-2
---
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ResourceFlavor
metadata:
  name: flavor-3
  labels:
    flavor-label: flavor-label-3
---
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ResourceFlavor
metadata:
  name: flavor-4
  labels:
    flavor-label: flavor-label-4
```

ClusterQueue references the same resource flavors, and includes resource limits.
clusterqueues.yaml
```
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ClusterQueue
metadata:
  name: shared-clusterqueue
spec:
  cohort: my-cohort
  namespaceSelector: {}
  queueingStrategy: BestEffortFIFO
  resources:
  - name: "cpu"
    flavors:
    - name: flavor-1
      quota:
        min: "1.15"
    - name: flavor-2
      quota:
        min: "2"
    - name: flavor-3
      quota:
        min: "2"
    - name: flavor-4
      quota:
        min: "2"
---
apiVersion: kueue.x-k8s.io/v1alpha2
kind: LocalQueue
metadata:
  namespace: default
  name: shared-queue
spec:
  clusterQueue: shared-clusterqueue
```

1.1-job.yaml
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: job-1.1-
  annotations:
    kueue.x-k8s.io/queue-name: shared-queue
spec:
  backoffLimit: 0
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        args: ["3600s"]
        resources:
          requests:
            cpu: 1.1
      restartPolicy: Never
```

**Anything else we need to know?**:
Notes: I have attempted to simplify my setup a little bit by only including one resource type, though we are hoping to use both CPU and memory constraints.

**Environment**:
- Kubernetes version (use `kubectl version`):
```
Client Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.2", GitCommit:"8b5a19147530eaac9476b0ab82980b4088bbc1b2", GitTreeState:"clean", BuildDate:"2021-09-15T21:38:50Z", GoVersion:"go1.16.8", Compiler:"gc", Platform:"linux/amd64"}

Server Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.6", GitCommit:"f59f5c2fda36e4036b49ec027e556a15456108f0", GitTreeState:"clean", BuildDate:"2022-01-19T17:26:47Z", GoVersion:"go1.16.12", Compiler:"gc", Platform:"linux/amd64"}
```
- Kueue version (use `git describe --tags --dirty --always`):
`kubectl describe -n kueue-system deployment.apps/kueue-controller-manager`:
```
  Containers:
   manager:
    Image:      gcr.io/k8s-staging-kueue/kueue:v0.2.1
```
- Cloud provider or hardware configuration:
On-prem cluster including 4 identical VMs.  Each has 2 CPUs and 15.5G RAM
- OS (e.g: `cat /etc/os-release`):
CentOS 7.9.2009 Core
- Kernel (e.g. `uname -a`):
I don't have direct access to the host machines, but if more details are relevant here I will work to get them.
- Install tools:
- Others:

## Discussion

### Comment by [@eskaug](https://github.com/eskaug) — 2022-09-30T16:07:56Z

Apologies, I forgot to include my log findings in the original report!  I'm a little new at this, obviously.

The first sign of trouble in the kueue controller logs comes after the "CreatedWorkload" event is logged:
```
"caller":"scheduler/scheduler.go:353",
"msg":"Could not admit workload and assigning flavors in apiserver",
"workload":{"name":"job-1.1-5v4q7","namespace":"default"},
"clusterQueue":{"name":"shared-clusterqueue"},
"error":"Incorrect version specified in apply patch. Specified patch version: , expected: kueue.x-k8s.io/v1alpha2"
```

Next the workload is re-queued, followed by "Workload successfully admitted and assigned flavors".
Trouble begins again when the controller attempts to reconcile the workload after admission:
```
"caller":"job/job_controller.go:191",
"msg":"Unsuspending job",
"controller":"job",
"controllerGroup":"batch",
"controllerKind":"Job",
"job":{"name":"job-1.1-5v4q7","namespace":"default"},
"namespace":"default",
"name":"job-1.1-5v4q7",
"reconcileID":"a67d8f03-46c5-422c-90e7-f579101af06e",
"job":{"name":"job-1.1-5v4q7","namespace":"default"},
"error":"Job.batch \"job-1.1-5v4q7\" is invalid: spec.template: Invalid value: 
core.PodTemplateSpec{<<full spec definition removed for brevity>>}: field is immutable",
"stacktrace":"sigs.k8s.io/kueue/pkg/controller/workload/job.(*JobReconciler).Reconcile\n\t/workspace/pkg/controller/workload/job/job_controller.go:191\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:121\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:320\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:273\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:234"}
```

### Comment by [@kirk-glenn](https://github.com/kirk-glenn) — 2022-09-30T16:54:02Z

- Kernel (e.g. uname -a):

> [kglenn@apcvlp02399 ~]$ uname -a
> Linux apcvlp02399 3.10.0-1160.31.1.el7.x86_64 1 SMP Thu Jun 10 13:32:12 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
> [kglenn@apcvlp02399 ~]$

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-03T09:27:01Z

> Next the workload is re-queued, followed by "Workload successfully admitted and assigned flavors".

It looks like the first problem is transitory. Still, I think it shouldn't happen. I'll try to debug further.

The second problem seems to be because the feature `JobMutableNodeSchedulingDirectives` is disabled. This is expected in a 1.22 cluster, where the feature is alpha. Either upgrade to 1.23 or enable `JobMutableNodeSchedulingDirectives`.

### Comment by [@eskaug](https://github.com/eskaug) — 2022-10-04T14:32:13Z

Thank you for your attention on this.  An update to k8s 1.23 appears to have resolved the issue in our testing.
