# Issue #5555: [release-0-12] Flaky E2E TopologyAwareScheduling for Pod group when Creating a Pod group Should place pods based on the ranks-ordering

**Summary**: [release-0-12] Flaky E2E TopologyAwareScheduling for Pod group when Creating a Pod group Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5555

**Last updated**: 2025-06-10T07:46:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-06-07T07:23:20Z
- **Updated**: 2025-06-10T07:46:11Z
- **Closed**: 2025-06-10T07:46:10Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End TAS Suite: kindest/node:v1.32.3: [It] TopologyAwareScheduling for Pod group when Creating a Pod group Should place pods based on the ranks-ordering 

```
{Expected object to be comparable, diff:   map[string]string{
- 	"0": "kind-worker",
+ 	"0": "kind-worker5",
- 	"1": "kind-worker2",
+ 	"1": "kind-worker6",
- 	"2": "kind-worker3",
+ 	"2": "kind-worker7",
- 	"3": "kind-worker4",
+ 	"3": "kind-worker8",
  }
 failed [FAILED] Expected object to be comparable, diff:   map[string]string{
- 	"0": "kind-worker",
+ 	"0": "kind-worker5",
- 	"1": "kind-worker2",
+ 	"1": "kind-worker6",
- 	"2": "kind-worker3",
+ 	"2": "kind-worker7",
- 	"3": "kind-worker4",
+ 	"3": "kind-worker8",
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/pod_group_test.go:128 @ 06/07/25 07:18:42.892
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5553/pull-kueue-test-e2e-tas-release-0-12/1931245781155581952

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-07T07:23:26Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T06:27:14Z

I looked at this:
1. the failed test creates pods in `e2e-tas-pod-group-f2fgw` namespace

2. looking at the [kube-scheduler logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5553/pull-kueue-test-e2e-tas-release-0-12/1931245781155581952/artifacts/run-test-tas-e2e-1.32.3/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_d8014c4293c06421b769e1a2f382e2c2/kube-scheduler/0.log) related to the namespace we can see that just before scheduling of the pods, then "kind-worker" was taken out of the pool (first log line below):
```
2025-06-07T07:18:39.608246575Z stderr F I0607 07:18:39.608069       1 eventhandlers.go:120] "Delete event for node" node="kind-worker"
2025-06-07T07:18:39.608314076Z stderr F I0607 07:18:39.608208       1 node_tree.go:79] "Removed node from NodeTree" node="kind-worker" zone=""
2025-06-07T07:18:40.04160753Z stderr F I0607 07:18:40.041390       1 httplog.go:134] "HTTP" verb="GET" URI="/readyz" latency="110.202µs" userAgent="kube-probe/1.32" audit-ID="" srcIP="127.0.0.1:59372" resp=200
2025-06-07T07:18:40.153283693Z stderr F I0607 07:18:40.153086       1 eventhandlers.go:303] "Delete event for scheduled pod" pod="e2e-tas-job-nqpkv/ranks-job-2-ndn6s"
2025-06-07T07:18:40.272607758Z stderr F I0607 07:18:40.272401       1 eventhandlers.go:303] "Delete event for scheduled pod" pod="e2e-tas-job-nqpkv/ranks-job-1-xdm8w"
2025-06-07T07:18:40.275797746Z stderr F I0607 07:18:40.274939       1 eventhandlers.go:303] "Delete event for scheduled pod" pod="e2e-tas-job-nqpkv/ranks-job-0-lnvnv"
2025-06-07T07:18:40.276247132Z stderr F I0607 07:18:40.276065       1 eventhandlers.go:303] "Delete event for scheduled pod" pod="e2e-tas-job-nqpkv/ranks-job-3-6mvw7"
2025-06-07T07:18:41.018997921Z stderr F I0607 07:18:41.018813       1 eventhandlers.go:60] "Add event for node" node="kind-worker"
2025-06-07T07:18:41.019189414Z stderr F I0607 07:18:41.018967       1 node_tree.go:65] "Added node to NodeTree" node="kind-worker" zone=""
2025-06-07T07:18:41.041183276Z stderr F I0607 07:18:41.041003       1 httplog.go:134] "HTTP" verb="GET" URI="/readyz" latency="93.121µs" userAgent="kube-probe/1.32" audit-ID="" srcIP="127.0.0.1:59376" resp=200
2025-06-07T07:18:41.586320056Z stderr F I0607 07:18:41.585763       1 eventhandlers.go:132] "Add event for unscheduled pod" pod="e2e-tas-pod-group-f2fgw/test-pod-0"
2025-06-07T07:18:41.595986441Z stderr F I0607 07:18:41.595715       1 eventhandlers.go:132] "Add event for unscheduled pod" pod="e2e-tas-pod-group-f2fgw/test-pod-1"
2025-06-07T07:18:41.604197939Z stderr F I0607 07:18:41.604046       1 eventhandlers.go:132] "Add event for unscheduled pod" pod="e2e-tas-pod-group-f2fgw/test-pod-2"
2025-06-07T07:18:41.613904146Z stderr F I0607 07:18:41.613730       1 eventhandlers.go:132] "Add event for unscheduled pod" pod="e2e-tas-pod-group-f2fgw/test-pod-3"
2025-06-07T07:18:42.040059644Z stderr F I0607 07:18:42.039811       1 httplog.go:134] "HTTP" verb="GET" URI="/readyz" latency="94.361µs" userAgent="kube-probe/1.32" audit-ID="" srcIP="127.0.0.1:59392" resp=200
2025-06-07T07:18:42.666283012Z stderr F I0607 07:18:42.666114       1 schedule_one.go:99] "Attempting to schedule pod" pod="e2e-tas-pod-group-f2fgw/test-pod-1"
2025-06-07T07:18:42.666785518Z stderr F I0607 07:18:42.666629       1 schedule_one.go:99] "Attempting to schedule pod" pod="e2e-tas-pod-group-f2fgw/test-pod-0"
2025-06-07T07:18:42.666828028Z stderr F I0607 07:18:42.666729       1 default_binder.go:53] "Attempting to bind pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-1" node="kind-worker6"
2025-06-07T07:18:42.667034531Z stderr F I0607 07:18:42.666911       1 schedule_one.go:99] "Attempting to schedule pod" pod="e2e-tas-pod-group-f2fgw/test-pod-2"
2025-06-07T07:18:42.667205343Z stderr F I0607 07:18:42.667055       1 default_binder.go:53] "Attempting to bind pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-0" node="kind-worker5"
2025-06-07T07:18:42.667269514Z stderr F I0607 07:18:42.667183       1 schedule_one.go:99] "Attempting to schedule pod" pod="e2e-tas-pod-group-f2fgw/test-pod-3"
2025-06-07T07:18:42.667442536Z stderr F I0607 07:18:42.667310       1 default_binder.go:53] "Attempting to bind pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-2" node="kind-worker7"
2025-06-07T07:18:42.667473836Z stderr F I0607 07:18:42.667395       1 default_binder.go:53] "Attempting to bind pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-3" node="kind-worker8"
2025-06-07T07:18:42.673124863Z stderr F I0607 07:18:42.672911       1 schedule_one.go:325] "Successfully bound pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-1" node="kind-worker6" evaluatedNodes=9 feasibleNodes=1
2025-06-07T07:18:42.674339338Z stderr F I0607 07:18:42.674140       1 schedule_one.go:325] "Successfully bound pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-3" node="kind-worker8" evaluatedNodes=9 feasibleNodes=1
2025-06-07T07:18:42.674572851Z stderr F I0607 07:18:42.674387       1 schedule_one.go:325] "Successfully bound pod to node" pod="e2e-tas-pod-group-f2fgw/test-pod-0" node="kind-worker5" evaluatedNodes=9 feasibleNodes=1
```
3. This is in agreement with the build-log showing "Should update nodesToReplace at the workload when a node is deleted" was running before
4. in this test we do the following 
```
			ginkgo.DeferCleanup(func() {
				ginkgo.By(fmt.Sprintf("Re-creating node %s", nodeNameToDelete))
				originalNode.ResourceVersion = ""
				originalNode.UID = ""
				originalNode.ManagedFields = nil
				util.MustCreate(ctx, k8sClient, originalNode)

				util.SetNodeCondition(ctx, k8sClient, originalNode, &corev1.NodeCondition{
					Type:   corev1.NodeReady,
					Status: corev1.ConditionTrue,
				})
			})
```
which awaits for the Node to be ready. 

**Issue**: The code above does not indicate the Kueue already "sees" the new node. Kueue may have not yet received the event "ADDED" for the node, and thus avoided scheduling on it.

So, we need to make sure Kueue sees the node. To do so, I would recommend the test schedules (using TAS) a single Pod with specific nodeSelector, and awaits for quick completion of the node.

cc @PBundyra @pajakd @mbobrovskyi ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T07:46:05Z

/close
as https://github.com/kubernetes-sigs/kueue/pull/5593 is merging

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-10T07:46:11Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5555#issuecomment-2958020450):

>/close
>as https://github.com/kubernetes-sigs/kueue/pull/5593 is merging


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
