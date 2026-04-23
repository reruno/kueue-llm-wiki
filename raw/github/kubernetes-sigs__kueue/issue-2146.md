# Issue #2146: The e2e test "Pod groups when Single CQ should admit group that fits" flakes

**Summary**: The e2e test "Pod groups when Single CQ should admit group that fits" flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2146

**Last updated**: 2024-05-08T19:13:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-07T07:57:18Z
- **Updated**: 2024-05-08T19:13:13Z
- **Closed**: 2024-05-08T19:13:13Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

/kind flake

**What happened**:

The test failed on the main branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-27/1787143043464302592

![image](https://github.com/kubernetes-sigs/kueue/assets/10359181/bda25d4b-73ff-4d4b-aaae-4b6c46c5f55d)


**What you expected to happen**:

No flake

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build?

**Anything else we need to know?**:

The build error message:
```
{Timed out after 5.003s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:129 with:
NotFoundError expects an error failed [FAILED] Timed out after 5.003s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:129 with:
NotFoundError expects an error
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:130 @ 05/05/24 15:36:38.784
}
```
The logs: https://storage.googleapis.com/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-27/1787143043464302592/artifacts/run-test-e2e-1.27.3/kind-worker2/containers/kueue-controller-manager-cff5b464d-hqcgs_kueue-system_manager-e8736f004e64986abcd2e09a3c53adc5638aff3eb17f822a4fe7a7e076f071c9.log

suggest there might also be an issue of clearing the cache (but it required more investigation):
```
2024-05-05T15:36:39.096811271Z stderr F 2024-05-05T15:36:39.096595158Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:494	Workload delete event	{"workload": {"name":"group","namespace":"pod-e2e-j77nb"}, "queue": "queue", "status": "finished"}
2024-05-05T15:36:39.096988914Z stderr F 2024-05-05T15:36:39.09674938Z	ERROR	workload-reconciler	core/workload_controller.go:508	Failed to delete workload from cache	{"workload": {"name":"group","namespace":"pod-e2e-j77nb"}, "queue": "queue", "status": "finished", "error": "cluster queue not found"}
2024-05-05T15:36:39.096999794Z stderr F sigs.k8s.io/kueue/pkg/controller/core.(*WorkloadReconciler).Delete.func1
2024-05-05T15:36:39.097003764Z stderr F 	/workspace/pkg/controller/core/workload_controller.go:508
2024-05-05T15:36:39.097006994Z stderr F sigs.k8s.io/kueue/pkg/queue.(*Manager).QueueAssociatedInadmissibleWorkloadsAfter
2024-05-05T15:36:39.097010184Z stderr F 	/workspace/pkg/queue/manager.go:380
2024-05-05T15:36:39.097013484Z stderr F sigs.k8s.io/kueue/pkg/controller/core.(*WorkloadReconciler).Delete
2024-05-05T15:36:39.097016534Z stderr F 	/workspace/pkg/controller/core/workload_controller.go:502
2024-05-05T15:36:39.097019544Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/source.(*EventHandler).OnDelete
2024-05-05T15:36:39.097022604Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/source/event_handler.go:161
2024-05-05T15:36:39.097025654Z stderr F k8s.io/client-go/tools/cache.ResourceEventHandlerFuncs.OnDelete
2024-05-05T15:36:39.097028795Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.29.4/tools/cache/controller.go:253
2024-05-05T15:36:39.097031765Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1
2024-05-05T15:36:39.097034575Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.29.4/tools/cache/shared_informer.go:977
2024-05-05T15:36:39.097037575Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1
2024-05-05T15:36:39.097040495Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.29.4/pkg/util/wait/backoff.go:226
2024-05-05T15:36:39.097043425Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil
2024-05-05T15:36:39.097046245Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.29.4/pkg/util/wait/backoff.go:227
2024-05-05T15:36:39.097049325Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil
2024-05-05T15:36:39.097052265Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.29.4/pkg/util/wait/backoff.go:204
2024-05-05T15:36:39.097055275Z stderr F k8s.io/apimachinery/pkg/util/wait.Until
2024-05-05T15:36:39.097058245Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.29.4/pkg/util/wait/backoff.go:161
2024-05-05T15:36:39.097061295Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run
2024-05-05T15:36:39.097064065Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.29.4/tools/cache/shared_informer.go:966
2024-05-05T15:36:39.097067055Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1
2024-05-05T15:36:39.097069975Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.29.4/pkg/util/wait/wait.go:72
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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-07T07:58:05Z

/cc @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-07T13:32:16Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-05-08T17:08:50Z

The clear cache error is logged both in ok and fail cases, and I did not found a direct connection to this test failing.

For now I propose to way for two distinct intervals: 
- 5s to observe the pods deleted.
- 5s to observe thw workload deleted.
