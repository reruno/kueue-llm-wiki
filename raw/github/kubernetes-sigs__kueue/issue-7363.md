# Issue #7363: jobframework JobReconciler don't update PodsReady condition timely when updata status failed

**Summary**: jobframework JobReconciler don't update PodsReady condition timely when updata status failed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7363

**Last updated**: 2025-11-07T11:18:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olderTaoist](https://github.com/olderTaoist)
- **Created**: 2025-10-23T11:34:21Z
- **Updated**: 2025-11-07T11:18:58Z
- **Closed**: 2025-11-07T11:18:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@olderTaoist](https://github.com/olderTaoist)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
when enable `waitForPodsReady` feature,  submit  [batch job](https://kubernetes.io/docs/concepts/workloads/controllers/job/),  the jobframework [JobReconciler](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L514) don't update PodsReady condition timely when update status failed, the error message is as follows
```
{"level":"error","ts":"2025-10-23T09:54:18.123509681Z","caller":"jobframework/reconciler.go:523","msg":"Updating workload status","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"k8s-job-20m-mxy","namespa
ce":"default"},"namespace":"default","name":"k8s-job-20m-mxy","reconcileID":"23c12b4b-786f-42f5-bd58-a10213f56e19","job":"default/k8s-job-20m-mxy","gvk":"batch/v1, Kind=Job","error":"Internal error occurred: failed calling webhook \"vwork
load.kb.io\": Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 169.169.109.130:443: connect: connection refused","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobf
ramework.(*JobReconciler).ReconcileGenericJob\n\t/Users/didi/ml/kueue/pkg/controller/jobframework/reconciler.go:523\nsigs.k8s.io/kueue/pkg/controller/jobframework.(*genericReconciler).Reconcile\n\t/Users/didi/ml/kueue/pkg/controller/jobfr
amework/reconciler.go:1522\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/Users/didi/ml/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controlle
r-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/Users/didi/ml/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:340\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Contro
ller[...]).processNextWorkItem\n\t/Users/didi/ml/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:300\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.1\n\t/Users/didi
/ml/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:202"}
```
**What you expected to happen**:
set PodsReady condition to True timely when updata status failed

**How to reproduce it (as minimally and precisely as possible)**:

for example, in the above situation, access to the webhook sometimes works and sometimes doesn't.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version: master
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@olderTaoist](https://github.com/olderTaoist) — 2025-10-23T11:36:40Z

/assign olderTaoist

### Comment by [@olderTaoist](https://github.com/olderTaoist) — 2025-11-03T11:49:04Z

in my situation, i notice that when a [batch job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) pod changes from pending to ready, but the batch job's status.ready doesn't change, the job's [PodReady](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_controller.go#L318) remains false. Therefore, the batch job framework should also listen for pod event information. as fellow:
```
{"level":"Level(-3)","ts":"2025-10-28T01:04:50.13980978Z","caller":"jobframework/reconciler.go:1447","msg":"Generating PodsReady condition","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"k8s-job-20m-mxy","namespace":"default"},"namespace":"default","name":"k8s-job-20m-mxy","reconcileID":"6a0451e6-f0ce-49e2-a4d4-b96bdbab9e05","job":"default/k8s-job-20m-mxy","gvk":"batch/v1, Kind=Job","Current PodsReady condition":"&Condition{Type:PodsReady,Status:False,ObservedGeneration:1,LastTransitionTime:2025-10-27 08:24:40 +0000 UTC,Reason:WaitForStart,Message:Not all pods are ready or succeeded,}","Pods are ready":false}

{"level":"Level(-3)","ts":"2025-10-28T02:10:16.313011389Z","caller":"jobframework/reconciler.go:1447","msg":"Generating PodsReady condition","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"k8s-job-20m-mxy","namespace":"default"},"namespace":"default","name":"k8s-job-20m-mxy","reconcileID":"64a3cdc0-5236-4382-a4a3-fd07067ba895","job":"default/k8s-job-20m-mxy","gvk":"batch/v1, Kind=Job","Current PodsReady condition":"&Condition{Type:PodsReady,Status:False,ObservedGeneration:1,LastTransitionTime:2025-10-27 08:24:40 +0000 UTC,Reason:WaitForStart,Message:Not all pods are ready or succeeded,}","Pods are ready":true}
```

I'm not sure if this is a bug in batch jobs.

@mimowo @PBundyra PTAL
