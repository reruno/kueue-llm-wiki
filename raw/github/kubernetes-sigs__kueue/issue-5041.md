# Issue #5041: Flaky E2E Test: StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0

**Summary**: Flaky E2E Test: StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5041

**Last updated**: 2025-07-25T05:06:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-18T07:42:11Z
- **Updated**: 2025-07-25T05:06:29Z
- **Closed**: 2025-07-25T05:06:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End Suite: kindest/node:v1.30.10: [It] StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:375 with:
Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:375 with:
Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:376 @ 04/18/25 07:24:31.271
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5030/pull-kueue-test-e2e-main-1-30/1913127191198044160

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-18T07:42:17Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T09:10:24Z

happend again recently https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-31/1925093654561558528

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-07-16T14:51:02Z

Have we considered using `util.VeryLongTimeout` in this case? AFAIK, changing the queue name triggers a rolling update in the StatefulSet, as the webhook updates pod labels to ensure correct scheduling. This causes each pod to terminate and restart sequentially, which can take significantly longer than the current (`util.Longtimeout`) timeout allows.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T14:58:05Z

@sohankunkerkar I'm sure open to extending the timeout. Do you have some evidence, looking into the logs which could support the hypothesis that extending timeout would help? If so, I'm happy to accept the PR.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-07-16T15:10:30Z

Yeah, this issue surfaced during [this change](https://github.com/openshift/kueue-operator/pull/441#discussion_r2207285597) to the Kueue Operator, where we run upstream Kueue e2e tests in CI. After modifying the leader election configuration to use longer lease durations, the test started [failing](https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/test-platform-results/pr-logs/pull/openshift_kueue-operator/441/pull-ci-openshift-kueue-operator-release-1.0-test-e2e-4-19/1945360009701363712/artifacts/test-e2e-4-19/e2e-kueue-upstream/build-log.txt) because it incorrectly assumed the controller would be immediately functional once the deployment was marked as available. However, in reality, the leader election was still in progress, and the controller hadn’t become active yet.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-17T20:00:58Z

TBH, it does not feel related, we already wait for Kueue manager to be Available before running e2e tests.

I looked at the logs of the build https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5030/pull-kueue-test-e2e-main-1-30/1913127191198044160

and the namespace for which the test failed was `sts-e2e-ljgzt` with the timeline of events:
```
  [1mSTEP:[0m Create StatefulSet [38;5;243m@ 04/18/25 07:23:45.216[0m
  [1mSTEP:[0m Checking that replicas is not ready [38;5;243m@ 04/18/25 07:23:45.251[0m
  [1mSTEP:[0m Update queue name [38;5;243m@ 04/18/25 07:23:46.252[0m
  [1mSTEP:[0m Waiting for replicas is ready [38;5;243m@ 04/18/25 07:23:46.27[0m
```
now, these are the logs of the Kueue manager in this time:

```
2025-04-18T07:23:45.212985235Z stderr F 2025-04-18T07:23:45.212782864Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:140	LocalQueue create event	{"localQueue": {"name":"sts-lq","namespace":"sts-e2e-ljgzt"}}
2025-04-18T07:23:45.215122602Z stderr F 2025-04-18T07:23:45.214952561Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:356	ClusterQueue update event	{"clusterQueue": {"name":"sts-cq"}}
2025-04-18T07:23:45.233477639Z stderr F 2025-04-18T07:23:45.233287367Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"sts-lq","namespace":"sts-e2e-ljgzt"}}
2025-04-18T07:23:45.311003525Z stderr F 2025-04-18T07:23:45.310514781Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:601	Workload create event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending"}
2025-04-18T07:23:45.311026755Z stderr F 2025-04-18T07:23:45.310628612Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:613	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:23:45.330689491Z stderr F 2025-04-18T07:23:45.330444059Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending"}
2025-04-18T07:23:45.330715562Z stderr F 2025-04-18T07:23:45.330594431Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:707	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:23:45.360205616Z stderr F 2025-04-18T07:23:45.359839074Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending"}
2025-04-18T07:23:45.360273227Z stderr F 2025-04-18T07:23:45.359962605Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:707	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:23:46.370037469Z stderr F 2025-04-18T07:23:46.368645918Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending"}
2025-04-18T07:23:46.370074289Z stderr F 2025-04-18T07:23:46.368744408Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:707	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq-invalid", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:23:46.404589184Z stderr F 2025-04-18T07:23:46.403579226Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending", "prevQueue": "sts-lq-invalid"}
2025-04-18T07:23:46.409785995Z stderr F 2025-04-18T07:23:46.409536383Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:631	Workload delete event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending"}
2025-04-18T07:24:31.289716957Z stderr F 2025-04-18T07:24:31.289509215Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:165	LocalQueue delete event	{"localQueue": {"name":"sts-lq","namespace":"sts-e2e-ljgzt"}}
2025-04-18T07:24:31.322200867Z stderr F 2025-04-18T07:24:31.321954415Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:601	Workload create event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending"}
2025-04-18T07:24:31.322229017Z stderr F 2025-04-18T07:24:31.322085786Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:613	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:24:31.322246277Z stderr F 2025-04-18T07:24:31.322122026Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:356	ClusterQueue update event	{"clusterQueue": {"name":"sts-cq"}}
2025-04-18T07:24:31.334769627Z stderr F 2025-04-18T07:24:31.334540635Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:343	ClusterQueue delete event	{"clusterQueue": {"name":"sts-cq"}}
2025-04-18T07:24:31.334791317Z stderr F 2025-04-18T07:24:31.334671426Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:349	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"sts-cq"}}
2025-04-18T07:24:31.33515214Z stderr F 2025-04-18T07:24:31.334946709Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending"}
2025-04-18T07:24:31.33518064Z stderr F 2025-04-18T07:24:31.335052899Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:707	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:24:31.349163132Z stderr F 2025-04-18T07:24:31.3489146Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending"}
2025-04-18T07:24:31.349195592Z stderr F 2025-04-18T07:24:31.349045911Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:707	ignored an error for now	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending", "error": "localQueue doesn't exist or inactive"}
2025-04-18T07:24:31.352994783Z stderr F 2025-04-18T07:24:31.352795811Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:631	Workload delete event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-ljgzt"}, "queue": "sts-lq", "status": "pending"}
```
So, one outstanding thing is many "ignored an error for now" errors. I'm not yet totally sure, but these are likely the reason why the workload was not picked up after queue-name change, just because the CQ was not active while the workload was updated. 

This is actually already ticketed here: https://github.com/kubernetes-sigs/kueue/issues/5310, but for now the easiest fix for the flakes is to just ensure the CQ is active by calling `ExpectClusterQueuesToBeActive`, and maybe also ExpectLocalQueuesToBeActive. We use this tactic in many other tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-17T20:01:45Z

Let me know if this makes sense and maybe you would also like to submit a PR fixing the flake along the lines.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-07-17T20:23:44Z

@mimowo Thanks for the apt reply. I think this is a much more targeted and accurate diagnosis than my initial leader election hypothesis.
