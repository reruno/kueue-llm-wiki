# Issue #4520: Flaky test: StatefulSet created should allow to scale up after scale down to zero

**Summary**: Flaky test: StatefulSet created should allow to scale up after scale down to zero

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4520

**Last updated**: 2025-10-24T16:29:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-07T17:26:53Z
- **Updated**: 2025-10-24T16:29:11Z
- **Closed**: 2025-10-24T16:26:57Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 29

## Description

/kind flake

**What happened**:

The test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4519/pull-kueue-test-e2e-main-1-31/1898055780486090752

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

run CI

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should allow to scale up after scale down to zero expand_less	54s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:317 with:
Expected
    <int32>: 3
to be <
    <int>: 3 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:317 with:
Expected
    <int32>: 3
to be <
    <int>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:319 @ 03/07/25 17:12:40.276
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Frun-test-e2e-singlecluster-1.31.0%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F4519%2Fpull-kueue-test-e2e-main-1-31%2F1898055780486090752%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4519/pull-kueue-test-e2e-main-1-31/1898055780486090752&lensIndex=2#)
End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0 expand_less	48s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:374 with:
Expected
    <int32>: 1
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:374 with:
Expected
    <int32>: 1
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:375 @ 03/07/25 17:13:27.9
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Frun-test-e2e-singlecluster-1.31.0%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F4519%2Fpull-kueue-test-e2e-main-1-31%2F1898055780486090752%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4519/pull-kueue-test-e2e-main-1-31/1898055780486090752&lensIndex=2#)
End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should delete all Pods if StatefulSet was deleted after being partially ready expand_less	53s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:424 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "sts-0",
                GenerateName: "sts-",
                Namespace: "sts-e2e-zprbh",
                SelfLink: "",
                UID: "3d3510b8-1da7-4a66-939b-e7c30f87fb43",
                ResourceVersion: "3694",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-07T17:13:30Z,
                },
                DeletionTimestamp: {
                    Time: 2025-03-07T17:14:06Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "apps.kubernetes.io/pod-index": "0",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/queue-name": "sts-lq",
                    "statefulset.kubernetes.io/pod-name": "sts-0",
                    "app": "sts-pod",
                    "controller-revision-hash": "sts-759ff9fbd8",
                    "kueue.x-k8s.io/pod-group-name": "statefulset-sts-18b6e",
                    "kueue.x-k8s.io/pod-group-pod-index": "0",
                    "kueue.x-k8s.io/podset": "5949e52e",
                },
                Annotations: {
                    "kueue.x-k8s.io/workload": "statefulset-sts-18b6e",
                    "kueue.x-k8s.io/pod-group-fast-admission": "true",
                    "kueue.x-k8s.io/pod-group-pod-index-label": "apps.kubernetes.io/pod-index",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "statefulset",
                    "kueue.x-k8s.io/role-hash": "5949e52e",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "sts",
                        UID: "146d532d-39ff-4e61-a377-a40cb4415419",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-07T17:13:30Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-fast-admission\":{},\"f:kueue.x-k8s.io/pod-group-pod-index-label\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/queue-name\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"146d532d-39ff-4e61-a377-a40cb4415419\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Ti...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:424 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "sts-0",
                GenerateName: "sts-",
                Namespace: "sts-e2e-zprbh",
                SelfLink: "",
                UID: "3d3510b8-1da7-4a66-939b-e7c30f87fb43",
                ResourceVersion: "3694",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-07T17:13:30Z,
                },
                DeletionTimestamp: {
                    Time: 2025-03-07T17:14:06Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "apps.kubernetes.io/pod-index": "0",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/queue-name": "sts-lq",
                    "statefulset.kubernetes.io/pod-name": "sts-0",
                    "app": "sts-pod",
                    "controller-revision-hash": "sts-759ff9fbd8",
                    "kueue.x-k8s.io/pod-group-name": "statefulset-sts-18b6e",
                    "kueue.x-k8s.io/pod-group-pod-index": "0",
                    "kueue.x-k8s.io/podset": "5949e52e",
                },
                Annotations: {
                    "kueue.x-k8s.io/workload": "statefulset-sts-18b6e",
                    "kueue.x-k8s.io/pod-group-fast-admission": "true",
                    "kueue.x-k8s.io/pod-group-pod-index-label": "apps.kubernetes.io/pod-index",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "statefulset",
                    "kueue.x-k8s.io/role-hash": "5949e52e",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "sts",
                        UID: "146d532d-39ff-4e61-a377-a40cb4415419",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-07T17:13:30Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-fast-admission\":{},\"f:kueue.x-k8s.io/pod-group-pod-index-label\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/queue-name\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"146d532d-39ff-4e61-a377-a40cb4415419\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Ti...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:425 @ 03/07/25 17:14:21.478
}
```

## Discussion

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-11T15:59:34Z

So far not managing to reproduce locally after 45 attempts with `stress --cpu 90`

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-11T18:55:01Z

End of logs for the 1st failed test (only selected namespace sts-e2e-xpspm), for [STEP: Wait for ReadyReplicas < 3](https://github.com/kubernetes-sigs/kueue/blob/65b4d527f868620a0d90a155a348dccb9b0e0296/test/e2e/singlecluster/statefulset_test.go#L313-L320):
```log
2025-03-07T17:11:55.453616203Z stderr F 2025-03-07T17:11:55.45340189Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "da57ed74-96b1-49f8-846f-4c8c8eb28617", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.453666604Z stderr F 2025-03-07T17:11:55.453553222Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "da57ed74-96b1-49f8-846f-4c8c8eb28617", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.453673454Z stderr F 2025-03-07T17:11:55.453599983Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "da57ed74-96b1-49f8-846f-4c8c8eb28617", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.593965567Z stderr F 2025-03-07T17:11:55.593703633Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "c95717ec-8eff-441f-95cb-4786e6cc4bad"}
2025-03-07T17:11:55.594265181Z stderr F 2025-03-07T17:11:55.593994767Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "c95717ec-8eff-441f-95cb-4786e6cc4bad", "pod": {"name":"sts-0","namespace":"sts-e2e-xpspm"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:11:55.594296681Z stderr F 2025-03-07T17:11:55.594082478Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "c95717ec-8eff-441f-95cb-4786e6cc4bad", "pod": {"name":"sts-1","namespace":"sts-e2e-xpspm"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:11:55.594302171Z stderr F 2025-03-07T17:11:55.594174539Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "c95717ec-8eff-441f-95cb-4786e6cc4bad", "pod": {"name":"sts-2","namespace":"sts-e2e-xpspm"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:11:55.680823865Z stderr F 2025-03-07T17:11:55.680208867Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "dd40499e-dc43-4a9f-a5c5-8d60af4d7998"}
2025-03-07T17:11:55.680855125Z stderr F 2025-03-07T17:11:55.68047504Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "dd40499e-dc43-4a9f-a5c5-8d60af4d7998", "pod": {"name":"sts-1","namespace":"sts-e2e-xpspm"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:11:55.681413492Z stderr F 2025-03-07T17:11:55.681106538Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-1","namespace":"sts-e2e-xpspm"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-xpspm"}, "uid": "d1713fe1-fb38-4537-8624-a560e1e8d06d"}
2025-03-07T17:11:55.681948729Z stderr F 2025-03-07T17:11:55.681633625Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "dd40499e-dc43-4a9f-a5c5-8d60af4d7998", "pod": {"name":"sts-2","namespace":"sts-e2e-xpspm"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:11:55.682442456Z stderr F 2025-03-07T17:11:55.681674796Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "4bbed08b-5281-494d-8cb1-71b5fe3dc1dd", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.682567387Z stderr F 2025-03-07T17:11:55.682440426Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-xpspm"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-xpspm"}, "uid": "2e987d24-d210-4127-9115-057a9e10ad09"}
2025-03-07T17:11:55.682983213Z stderr F 2025-03-07T17:11:55.682536827Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "4bbed08b-5281-494d-8cb1-71b5fe3dc1dd", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.682994083Z stderr F 2025-03-07T17:11:55.682614788Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "4bbed08b-5281-494d-8cb1-71b5fe3dc1dd", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.683050344Z stderr F 2025-03-07T17:11:55.681739307Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "dd40499e-dc43-4a9f-a5c5-8d60af4d7998", "pod": {"name":"sts-0","namespace":"sts-e2e-xpspm"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:11:55.683065124Z stderr F 2025-03-07T17:11:55.682851711Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "dac5401e-04f2-46f8-94c6-5f24297d7431", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.683070034Z stderr F 2025-03-07T17:11:55.682967083Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "dac5401e-04f2-46f8-94c6-5f24297d7431", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.683075034Z stderr F 2025-03-07T17:11:55.683008043Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "dac5401e-04f2-46f8-94c6-5f24297d7431", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.684912978Z stderr F 2025-03-07T17:11:55.684581834Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-2","namespace":"sts-e2e-xpspm"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-xpspm"}, "uid": "bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"}
2025-03-07T17:11:55.685412095Z stderr F 2025-03-07T17:11:55.685247962Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "35a0e41c-7a56-4f0c-901f-a6d279a075f0", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.685966612Z stderr F 2025-03-07T17:11:55.68583246Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "35a0e41c-7a56-4f0c-901f-a6d279a075f0", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.686207055Z stderr F 2025-03-07T17:11:55.686072583Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-xpspm", "name": "statefulset-sts-18b6e", "reconcileID": "35a0e41c-7a56-4f0c-901f-a6d279a075f0", "job": "group/sts-e2e-xpspm/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:11:55.699467487Z stderr F 2025-03-07T17:11:55.698626746Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "dd40499e-dc43-4a9f-a5c5-8d60af4d7998", "error": "Operation cannot be fulfilled on pods \"sts-2\": the object has been modified; please apply your changes to the latest version and try again"}
2025-03-07T17:11:55.704694995Z stderr F 2025-03-07T17:11:55.704135117Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-xpspm"}, "namespace": "sts-e2e-xpspm", "name": "sts", "reconcileID": "587984c0-5fca-4cfb-888c-192a27e45056"}
```

Note the error on the line before the last.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-11T19:17:33Z

End of the logs for the 2nd failed test (only lines for namespace sts-e2e-dkpsn), for [STEP: Waiting for replicas is ready](https://github.com/kubernetes-sigs/kueue/blob/65b4d527f868620a0d90a155a348dccb9b0e0296/test/e2e/singlecluster/statefulset_test.go#L370-L376):
```log
2025-03-07T17:12:42.901101616Z stderr F 2025-03-07T17:12:42.898008896Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-dkpsn"}, "namespace": "sts-e2e-dkpsn", "name": "sts", "reconcileID": "b3e19a07-4a7f-4ba4-9670-7d8ef81ac598"}
2025-03-07T17:12:43.065890307Z stderr F 2025-03-07T17:12:43.065705245Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-dkpsn"}, "namespace": "sts-e2e-dkpsn", "name": "sts", "reconcileID": "4fd12063-580f-4d03-a10f-181f738055f6"}
2025-03-07T17:12:43.06606889Z stderr F 2025-03-07T17:12:43.065894597Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-dkpsn"}, "namespace": "sts-e2e-dkpsn", "name": "sts", "reconcileID": "4fd12063-580f-4d03-a10f-181f738055f6", "pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:12:43.125013415Z stderr F 2025-03-07T17:12:43.124531829Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-dkpsn"}, "uid": "a034e8cc-5fa6-4314-9fa5-ca3e69f44c97"}
2025-03-07T17:12:43.125047926Z stderr F 2025-03-07T17:12:43.124751572Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "164190c0-0888-47cb-b9fe-84b5adbe830e", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.125089486Z stderr F 2025-03-07T17:12:43.124852753Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "164190c0-0888-47cb-b9fe-84b5adbe830e", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.125097556Z stderr F 2025-03-07T17:12:43.124887504Z	LEVEL(-2)	jobframework/reconciler.go:540	Running job is not admitted by a cluster queue, suspending	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "164190c0-0888-47cb-b9fe-84b5adbe830e", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.151298167Z stderr F 2025-03-07T17:12:43.151042244Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-dkpsn"}, "uid": "a034e8cc-5fa6-4314-9fa5-ca3e69f44c97"}
2025-03-07T17:12:43.294875662Z stderr F 2025-03-07T17:12:43.294622269Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-dkpsn"}, "uid": "a034e8cc-5fa6-4314-9fa5-ca3e69f44c97"}
2025-03-07T17:12:43.41704286Z stderr F 2025-03-07T17:12:43.416653615Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-dkpsn"}, "uid": "a034e8cc-5fa6-4314-9fa5-ca3e69f44c97"}
2025-03-07T17:12:43.418011633Z stderr F 2025-03-07T17:12:43.41777489Z	DEBUG	events	recorder/recorder.go:104	Not admitted by cluster queue	{"type": "Normal", "object": {"kind":"Pod","namespace":"sts-e2e-dkpsn","name":"sts-0","uid":"a034e8cc-5fa6-4314-9fa5-ca3e69f44c97","apiVersion":"v1","resourceVersion":"3401"}, "reason": "Stopped"}
2025-03-07T17:12:43.418028793Z stderr F 2025-03-07T17:12:43.41783534Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "e2f81cfc-2f62-4f7f-a011-5ff8e0dbb421", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.418647821Z stderr F 2025-03-07T17:12:43.417954622Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "e2f81cfc-2f62-4f7f-a011-5ff8e0dbb421", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.418662621Z stderr F 2025-03-07T17:12:43.417999993Z	LEVEL(-2)	jobframework/reconciler.go:540	Running job is not admitted by a cluster queue, suspending	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "e2f81cfc-2f62-4f7f-a011-5ff8e0dbb421", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.512917375Z stderr F 2025-03-07T17:12:43.512698493Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-dkpsn"}, "namespace": "sts-e2e-dkpsn", "name": "sts", "reconcileID": "d413cd88-3d65-4bc2-80c2-638272fadd26"}
2025-03-07T17:12:43.610977039Z stderr F 2025-03-07T17:12:43.61031154Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-dkpsn"}, "uid": "a034e8cc-5fa6-4314-9fa5-ca3e69f44c97"}
2025-03-07T17:12:43.61102036Z stderr F 2025-03-07T17:12:43.610510043Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "a6c069f2-d801-4c79-a6cc-bb9828d345a0", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.61102645Z stderr F 2025-03-07T17:12:43.610605634Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "a6c069f2-d801-4c79-a6cc-bb9828d345a0", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:43.61103169Z stderr F 2025-03-07T17:12:43.610638085Z	LEVEL(-2)	jobframework/reconciler.go:540	Running job is not admitted by a cluster queue, suspending	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "a6c069f2-d801-4c79-a6cc-bb9828d345a0", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:48.60982805Z stderr F 2025-03-07T17:12:48.608058807Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-dkpsn"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-dkpsn"}, "uid": "a034e8cc-5fa6-4314-9fa5-ca3e69f44c97"}
2025-03-07T17:12:48.60987332Z stderr F 2025-03-07T17:12:48.608816557Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "c3e59325-dada-4f22-8eba-5f56e8ccc396", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:48.609879781Z stderr F 2025-03-07T17:12:48.609253792Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "c3e59325-dada-4f22-8eba-5f56e8ccc396", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:48.609887121Z stderr F 2025-03-07T17:12:48.609306973Z	LEVEL(-2)	jobframework/reconciler.go:540	Running job is not admitted by a cluster queue, suspending	{"controller": "v1_pod", "namespace": "group/sts-e2e-dkpsn", "name": "statefulset-sts-18b6e", "reconcileID": "c3e59325-dada-4f22-8eba-5f56e8ccc396", "job": "group/sts-e2e-dkpsn/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:12:48.669560866Z stderr F 2025-03-07T17:12:48.668656454Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-dkpsn"}, "namespace": "sts-e2e-dkpsn", "name": "sts", "reconcileID": "53ce8c04-e542-42a4-9de3-6f7165ae0a50"}
2025-03-07T17:13:27.921237932Z stderr F 2025-03-07T17:13:27.920719916Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-dkpsn"}, "namespace": "sts-e2e-dkpsn", "name": "sts", "reconcileID": "de6fb557-3c5b-4f57-80be-ca9412935596"}
2025-03-07T17:13:27.939285037Z stderr F 2025-03-07T17:13:27.939025244Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:170LocalQueue delete event	{"localQueue": {"name":"sts-lq","namespace":"sts-e2e-dkpsn"}}
```

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-11T19:23:25Z

End of the logs for the 3rd failed test (only lines for namespace sts-e2e-dkpsn), for [STEP: Check all pods are deleted](https://github.com/kubernetes-sigs/kueue/blob/65b4d527f868620a0d90a155a348dccb9b0e0296/test/e2e/singlecluster/statefulset_test.go#L420-L426):
```log
2025-03-07T17:13:36.477622005Z stderr F 2025-03-07T17:13:36.477357351Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts", "reconcileID": "9fdd53b9-9a1b-444e-a1de-b27c3c23768e"}
2025-03-07T17:13:36.477770317Z stderr F 2025-03-07T17:13:36.477576054Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts", "reconcileID": "9fdd53b9-9a1b-444e-a1de-b27c3c23768e", "pod": {"name":"sts-0","namespace":"sts-e2e-zprbh"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:13:36.478090491Z stderr F 2025-03-07T17:13:36.477852788Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts", "reconcileID": "9fdd53b9-9a1b-444e-a1de-b27c3c23768e", "pod": {"name":"sts-1","namespace":"sts-e2e-zprbh"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:13:36.536831794Z stderr F 2025-03-07T17:13:36.536464449Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0d7ac2a5-a5ed-43d0-b915-5325b8509c48", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.536856014Z stderr F 2025-03-07T17:13:36.536605721Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0d7ac2a5-a5ed-43d0-b915-5325b8509c48", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.536881615Z stderr F 2025-03-07T17:13:36.536639022Z	LEVEL(-2)	jobframework/reconciler.go:503	Job admitted, unsuspending{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0d7ac2a5-a5ed-43d0-b915-5325b8509c48", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.537018046Z stderr F 2025-03-07T17:13:36.536819254Z	DEBUG	events	recorder/recorder.go:104	Admitted by clusterQueue sts-cq	{"type": "Normal", "object": {"kind":"Pod","namespace":"sts-e2e-zprbh","name":"sts-1","uid":"557f3f37-df35-4ed7-b77a-1e5464da2220","apiVersion":"v1","resourceVersion":"3688"}, "reason": "Started"}
2025-03-07T17:13:36.53732811Z stderr F 2025-03-07T17:13:36.536994186Z	LEVEL(-3)	pod/pod_controller.go:313	Starting pod in group	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0d7ac2a5-a5ed-43d0-b915-5325b8509c48", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod", "podInGroup": {"name":"sts-1","namespace":"sts-e2e-zprbh"}}
2025-03-07T17:13:36.626491749Z stderr F 2025-03-07T17:13:36.626223565Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-zprbh"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "uid": "3d3510b8-1da7-4a66-939b-e7c30f87fb43"}
2025-03-07T17:13:36.628173571Z stderr F 2025-03-07T17:13:36.627930437Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts", "reconcileID": "9fdd53b9-9a1b-444e-a1de-b27c3c23768e", "error": "Operation cannot be fulfilled on pods \"sts-1\": the object has been modified; please apply your changes to the latest version and try again"}
2025-03-07T17:13:36.633251396Z stderr F 2025-03-07T17:13:36.632985193Z	ERROR	jobframework/reconciler.go:506	Unsuspending job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0d7ac2a5-a5ed-43d0-b915-5325b8509c48", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod", "error": "Operation cannot be fulfilled on pods \"sts-1\": the object has been modified; please apply your changes to the latest version and try again"}
2025-03-07T17:13:36.633326147Z stderr F 2025-03-07T17:13:36.633103254Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0d7ac2a5-a5ed-43d0-b915-5325b8509c48", "error": "Operation cannot be fulfilled on pods \"sts-1\": the object has been modified; please apply your changes to the latest version and try again"}
2025-03-07T17:13:36.633368118Z stderr F 2025-03-07T17:13:36.633105864Z	LEVEL(-2)	statefulset/statefulset_reconciler.go:61	Reconcile StatefulSet	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts", "reconcileID": "ba4276f4-87b0-47dd-a08f-a24b508222d2"}
2025-03-07T17:13:36.633386928Z stderr F 2025-03-07T17:13:36.633246816Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "bdde3b93-03be-47f0-bd8b-ea500248606a", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.63354277Z stderr F 2025-03-07T17:13:36.633357748Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "bdde3b93-03be-47f0-bd8b-ea500248606a", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.63355409Z stderr F 2025-03-07T17:13:36.633407058Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "bdde3b93-03be-47f0-bd8b-ea500248606a", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.633679622Z stderr F 2025-03-07T17:13:36.633329337Z	LEVEL(-3)	statefulset/statefulset_reconciler.go:103	Finalizing pod in group	{"controller": "statefulset", "controllerGroup": "apps", "controllerKind": "StatefulSet", "StatefulSet": {"name":"sts","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts", "reconcileID": "ba4276f4-87b0-47dd-a08f-a24b508222d2", "pod": {"name":"sts-1","namespace":"sts-e2e-zprbh"}, "group": "statefulset-sts-18b6e"}
2025-03-07T17:13:36.640074495Z stderr F 2025-03-07T17:13:36.639606279Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "d7420764-7625-4679-abfb-d5b88ffc3a22", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.640099405Z stderr F 2025-03-07T17:13:36.63972682Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "d7420764-7625-4679-abfb-d5b88ffc3a22", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.640104705Z stderr F 2025-03-07T17:13:36.639759361Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "d7420764-7625-4679-abfb-d5b88ffc3a22", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.790738143Z stderr F 2025-03-07T17:13:36.79050519Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-0","namespace":"sts-e2e-zprbh"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "uid": "3d3510b8-1da7-4a66-939b-e7c30f87fb43"}
2025-03-07T17:13:36.790759553Z stderr F 2025-03-07T17:13:36.790631512Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-1","namespace":"sts-e2e-zprbh"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "uid": "557f3f37-df35-4ed7-b77a-1e5464da2220"}
2025-03-07T17:13:36.790967386Z stderr F 2025-03-07T17:13:36.790786544Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "6760b1e1-d637-45b5-a8b3-30f57d3e3e7e", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.791050017Z stderr F 2025-03-07T17:13:36.790905625Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "6760b1e1-d637-45b5-a8b3-30f57d3e3e7e", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.791076677Z stderr F 2025-03-07T17:13:36.790952556Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "6760b1e1-d637-45b5-a8b3-30f57d3e3e7e", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.791337451Z stderr F 2025-03-07T17:13:36.791093348Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "5176b200-2c87-4e42-8152-c8c335f14fa6", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.791347071Z stderr F 2025-03-07T17:13:36.791161378Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "5176b200-2c87-4e42-8152-c8c335f14fa6", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.791351521Z stderr F 2025-03-07T17:13:36.791184289Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "5176b200-2c87-4e42-8152-c8c335f14fa6", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.843135593Z stderr F 2025-03-07T17:13:36.84289072Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-1","namespace":"sts-e2e-zprbh"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "uid": "557f3f37-df35-4ed7-b77a-1e5464da2220"}
2025-03-07T17:13:36.843409057Z stderr F 2025-03-07T17:13:36.843301785Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "ea268d90-5fa3-4675-89c4-80aaab68fd35", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.84368029Z stderr F 2025-03-07T17:13:36.843525438Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "ea268d90-5fa3-4675-89c4-80aaab68fd35", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:36.843943744Z stderr F 2025-03-07T17:13:36.843772711Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "ea268d90-5fa3-4675-89c4-80aaab68fd35", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.010646839Z stderr F 2025-03-07T17:13:37.010349735Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-1","namespace":"sts-e2e-zprbh"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "uid": "557f3f37-df35-4ed7-b77a-1e5464da2220"}
2025-03-07T17:13:37.010749161Z stderr F 2025-03-07T17:13:37.010608009Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "24368c1c-af5c-4e7f-92fa-f35ff4a54043", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.010897923Z stderr F 2025-03-07T17:13:37.01074008Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "24368c1c-af5c-4e7f-92fa-f35ff4a54043", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.010906543Z stderr F 2025-03-07T17:13:37.010793981Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "24368c1c-af5c-4e7f-92fa-f35ff4a54043", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.032391112Z stderr F 2025-03-07T17:13:37.032181539Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"sts-1","namespace":"sts-e2e-zprbh"}, "store": "finalizedPods", "key": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "uid": "557f3f37-df35-4ed7-b77a-1e5464da2220"}
2025-03-07T17:13:37.032725746Z stderr F 2025-03-07T17:13:37.032595174Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0c84818d-f079-4a88-a420-d31a1d6fc713", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.033064771Z stderr F 2025-03-07T17:13:37.032922619Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0c84818d-f079-4a88-a420-d31a1d6fc713", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.033217463Z stderr F 2025-03-07T17:13:37.03301419Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "0c84818d-f079-4a88-a420-d31a1d6fc713", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.090535327Z stderr F 2025-03-07T17:13:37.090262144Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:690	Workload update event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "queue": "sts-lq", "status": "admitted", "clusterQueue": "sts-cq"}
2025-03-07T17:13:37.090580738Z stderr F 2025-03-07T17:13:37.090421206Z	LEVEL(-2)	jobframework/reconciler.go:356	Reconciling Job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "a8d4a5cc-41f5-4667-a788-f34db6be9304", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.090595408Z stderr F 2025-03-07T17:13:37.090447746Z	LEVEL(-2)	multikueue/workload.go:158	Reconcile Workload	{"controller": "multikueue_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "f9b9c421-e0d8-4457-b0e2-0ff5a99ca58b"}
2025-03-07T17:13:37.090605898Z stderr F 2025-03-07T17:13:37.090518047Z	LEVEL(-2)	core/workload_controller.go:145	Reconcile Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "5fc68004-53ec-4114-9760-dab246362686"}
2025-03-07T17:13:37.090611148Z stderr F 2025-03-07T17:13:37.090555887Z	LEVEL(-2)	multikueue/workload.go:184	Skip Workload	{"controller": "multikueue_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "f9b9c421-e0d8-4457-b0e2-0ff5a99ca58b", "isDeleted": false}
2025-03-07T17:13:37.090888452Z stderr F 2025-03-07T17:13:37.09074302Z	LEVEL(-3)	jobframework/reconciler.go:442	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "a8d4a5cc-41f5-4667-a788-f34db6be9304", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.090899752Z stderr F 2025-03-07T17:13:37.09078965Z	LEVEL(-3)	jobframework/reconciler.go:549	Job running with admitted workload, nothing to do	{"controller": "v1_pod", "namespace": "group/sts-e2e-zprbh", "name": "statefulset-sts-18b6e", "reconcileID": "a8d4a5cc-41f5-4667-a788-f34db6be9304", "job": "group/sts-e2e-zprbh/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-03-07T17:13:37.455331167Z stderr F 2025-03-07T17:13:37.455115534Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconcile LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"sts-lq","namespace":"sts-e2e-zprbh"}, "namespace": "sts-e2e-zprbh", "name": "sts-lq", "reconcileID": "c1bf8abd-d478-4cf2-9569-a6b00d447b80"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T10:11:04Z

> Note the error on the line before the last.

cc @mbobrovskyi PTAL
Could it be that the finalizer removal failed on the `sts-2` Pod due to "the object has been modified", and was not retried, for the STS? I'm speculating, but maybe we could try to repro the situation when the first finalizing request to the pod fails, and see if the the controller in Kueue would retry.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-13T09:51:26Z

I gathered Kueue logs for the first fail `End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should allow to scale up after scale down to zero` from the start of the test till the moment of failure / end of `Wait for ReadyReplicas < 3` step.
Log from the bad run:
https://gist.github.com/nasedil/3851560a1c243c56d76a47edf3fc2696
Log from the good run:
https://gist.github.com/nasedil/d9172108d1ec49c8d8624d77ebc6f9b9

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-13T09:55:30Z

> but maybe we could try to repro the situation when the first finalizing request to the pod fails, and see if the the controller in Kueue would retry.

@mimowo could I make it programmatically somehow?

Regarding the "the object has been modified" error, it appears in successful logs twice, but for the `sts-lq` object, not for the 'sts-2`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T10:01:42Z

This error means that the controller tried to modify object (like Pod in this case), but passed old "ResourceVersion" - another controller, probably Kubelet modified the pod in the meanwhile. Such situations in a distributed system like k8s happen all the time, so it is not an indication of a code bug by itself. The controller which failed to apply its patch should retry in the next "sync". However, in  the attached logs I don't see any indication the operation was "retried". 

> @mimowo could I make it programmatically somehow?

No easy answer unfortunately.

Maybe just somehow skip the attempt to Patch the pod, and return error, say with probabliliy 50%. Then, you should expect runs which fail on the first attempt but would succeed on the second.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-13T11:03:33Z

> Maybe just somehow skip the attempt to Patch the pod, and return error, say with probabliliy 50%. Then, you should expect runs which fail on the first attempt but would succeed on the second.

Error points to `controller/controller.go:316`, but I cannot find this file in both Kueue and Kubernetes.  Also, where do you think the patching instruction is in the [statefulset_test.go](https://github.com/kubernetes-sigs/kueue/blob/65b4d527f868620a0d90a155a348dccb9b0e0296/test/e2e/singlecluster/statefulset_test.go#L278-L320)?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T11:07:10Z

this is code in controller-runtime, it means that one of our reoncilers returned error in the Reconcile function, for example here: https://github.com/kubernetes-sigs/kueue/blob/a454f0e133682887c8043b10cc360bc24f7d3924/pkg/controller/jobs/statefulset/statefulset_reconciler.go#L64

. This error was then handled and logged by controller-runtime.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T09:21:18Z

I looked at the kubelet logs for the sts-e2e-xpspm/sts-2 pod from https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-2715407507

```
> cat kubelet.log| grep  sts-e2e-xpspm/sts-2 | grep -e phase -e DELETE
Mar 07 17:11:53 kind-worker kubelet[250]: I0307 17:11:53.319902     250 status_manager.go:881] "Status for pod updated successfully" pod="sts-e2e-xpspm/sts-2" statusVersion=1 status={"phase":"Pending","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"startTime":"2025-03-07T17:11:53Z","containerStatuses":[{"name":"c","state":{"waiting":{"reason":"ContainerCreating"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85","imageID":"","started":false,"volumeMounts":[{"name":"kube-api-access-5djhk","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 17:11:55 kind-worker kubelet[250]: I0307 17:11:55.042482     250 status_manager.go:872] "Patch status for pod" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044" patch="{\"metadata\":{\"uid\":\"bd1216df-8ba1-4d1d-a6d3-2e836c3d1044\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-07T17:11:54Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-07T17:11:54Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-07T17:11:54Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-07T17:11:54Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-5djhk\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.2.37\",\"podIPs\":[{\"ip\":\"10.244.2.37\"}]}}"
Mar 07 17:11:55 kind-worker kubelet[250]: I0307 17:11:55.042568     250 status_manager.go:881] "Status for pod updated successfully" pod="sts-e2e-xpspm/sts-2" statusVersion=2 status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:54Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:54Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:54Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.37","podIPs":[{"ip":"10.244.2.37"}],"startTime":"2025-03-07T17:11:53Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-07T17:11:54Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f","started":true,"volumeMounts":[{"name":"kube-api-access-5djhk","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 17:11:55 kind-worker kubelet[250]: I0307 17:11:55.453402     250 kubelet.go:2423] "SyncLoop DELETE" source="api" pods=["sts-e2e-xpspm/sts-2"]
Mar 07 17:11:55 kind-worker kubelet[250]: I0307 17:11:55.977600     250 status_manager.go:691] "Ignoring same status for pod" pod="sts-e2e-xpspm/sts-2" status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:54Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:54Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:54Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.37","podIPs":[{"ip":"10.244.2.37"}],"startTime":"2025-03-07T17:11:53Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-07T17:11:54Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f","started":true,"volumeMounts":[{"name":"kube-api-access-5djhk","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 17:11:56 kind-worker kubelet[250]: I0307 17:11:56.984329     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:00 kind-worker kubelet[250]: I0307 17:12:00.908186     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:10 kind-worker kubelet[250]: I0307 17:12:10.890203     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:20 kind-worker kubelet[250]: I0307 17:12:20.890281     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:30 kind-worker kubelet[250]: I0307 17:12:30.890067     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:40 kind-worker kubelet[250]: I0307 17:12:40.890783     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:50 kind-worker kubelet[250]: I0307 17:12:50.894629     250 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:50 kind-worker kubelet[250]: I0307 17:12:50.990538     250 status_manager.go:872] "Patch status for pod" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044" patch="{\"metadata\":{\"uid\":\"bd1216df-8ba1-4d1d-a6d3-2e836c3d1044\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-07T17:12:50Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"reason\":\"PodCompleted\",\"type\":\"Initialized\"},{\"lastTransitionTime\":\"2025-03-07T17:12:50Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-07T17:12:50Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"containerID\":\"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f\",\"exitCode\":0,\"finishedAt\":\"2025-03-07T17:11:56Z\",\"reason\":\"Completed\",\"startedAt\":\"2025-03-07T17:11:54Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-5djhk\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Succeeded\"}}"
Mar 07 17:12:50 kind-worker kubelet[250]: I0307 17:12:50.990717     250 status_manager.go:881] "Status for pod updated successfully" pod="sts-e2e-xpspm/sts-2" statusVersion=4 status={"phase":"Succeeded","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:12:50Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z","reason":"PodCompleted"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:12:50Z","reason":"PodCompleted"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:12:50Z","reason":"PodCompleted"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T17:11:53Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.37","podIPs":[{"ip":"10.244.2.37"}],"startTime":"2025-03-07T17:11:53Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":0,"reason":"Completed","startedAt":"2025-03-07T17:11:54Z","finishedAt":"2025-03-07T17:11:56Z","containerID":"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://0aa2d69d5445cc675b7f95e329e0f85658d8c249594b13e6751aec971f16155f","started":false,"volumeMounts":[{"name":"kube-api-access-5djhk","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 17:12:51 kind-worker kubelet[250]: I0307 17:12:51.185685     250 status_manager.go:942] "The pod termination is finished as SyncTerminatedPod completes its execution" phase="Succeeded" localPhase="Succeeded" pod="sts-e2e-xpspm/sts-2" podUID="bd1216df-8ba1-4d1d-a6d3-2e836c3d1044"
Mar 07 17:12:51 kind-worker kubelet[250]: I0307 17:12:51.372680     250 kubelet.go:2423] "SyncLoop DELETE" source="api" pods=["sts-e2e-xpspm/sts-2"]
```
So, as the pod received DELETE request by STS at `17:11:55.453402`, and it properly terminated at `17:12:50.990538` as succeeded, but it took 55s, exceeding the LongTimeout. I've also checked another failure log, and the same happened.

So, it looks good, just slow, I think this is likely due to recent:
- addition of the AppWrapper controller running on the nodes
- using of agnhost of instead of super lightweight perf pause container

Both changes are ok, but we need to compensate for them somehow. Especially the AppWrapper would be explaining why this is not so common on the 0.10 branches, even though agnhost was cherry-picked.

Some ideas:
1. Use ExpectAllPodsInNamespaceDeleted consistently in AfterEach *as for TAS e2e tests) to reduce the noisy neighbour problems by pods coming from previous "Its" which are being deleted asynchronously currently
2. increase cpu from 100m to say 200m, and set memory Requests=Limits for all pods, because the termination is actually handled by the container itself in this case (to compensate for heavier containers). Review all tests to make sure Request and Limit is set (using new RequestAndLimit function) to reduce the "noisy neighbour problems (unless a test explicitly wants to test just Requests, but it would be minority)
3. increase the LongTimeout to full 1min

I'm leaning to actually do all of them, @tenzen-y @mszadkow @mbobrovskyi @nasedil  wdyt?

I guess we could start with (1.) and (3.) as the smallest diff.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T09:39:01Z

As proposed on slack by @mbobrovskyi I think also setting the Pod graceTerminationPeriod to 1s could help in this case, as we would SIGKILL the pod early rather than waiting for graceful termination. OTOH sigkilling a pod is not being nice, so I'm ok with that as a pragmatic idea, but we should reduce the "noisy neighbours".

Another idea is just to increase the resources in test-infra, but again I would like to start by reducing the noise on kubelet whcih is under control of kueue tests code.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-14T09:40:49Z

1. for sure 100%.
3. is not bad, shouldn't hurt for duration of tests, but secure such situations.
2. Maybe we could decrease graceful termination period to 0, if the pods are not killed by the agnhost request and just dies out on their own after deletion.
(I see I was 1 minute late with the idea ;) )

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T09:45:32Z

I would like to start only (1) and (2). After we observe this flakiness again, we want to take (3).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T09:50:38Z

> I would like to start only (1) and (2). After we observe this flakiness again, we want to take (3).

we can, though (3.) might be pragmatic before release. But I think we still have a week so can explore (1.) and (2.).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T09:52:36Z

> Maybe we could decrease graceful termination period to 0, if the pods are not killed by the agnhost request and just dies out on their own after deletion.

Yeah, I'm ok with setting grace termination period to 1s or whatever small for the most flaky tests. However, generally using sigkill should be exception when other ideas fail, rather than a "best practice" :)  

But again - I'm ok to do so for a subset of selected tests which are most flaky due to this reason of very long graceful termination.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T09:56:21Z

I think flaky test alerting is not a bad signal. That is a good opportunity to fix potential regressions.
So, it would be better to avoid bumping timeout just for silencing alerts.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-14T10:17:29Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-17T14:51:18Z

/unassign
/assign @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:13:13Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:13:18Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-2735676084):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-08T10:29:42Z

/reopen

We observed this one again in https://github.com/kubernetes-sigs/kueue/pull/7205
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7205/pull-kueue-test-e2e-main-1-34/1975862374690721792

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-08T10:29:47Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-3380861022):

>/reopen
>
>We observed this one again in https://github.com/kubernetes-sigs/kueue/pull/7205
>https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7205/pull-kueue-test-e2e-main-1-34/1975862374690721792


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-10T12:03:29Z

I think we are back at - https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-2717345798

Because what I observe in [kube-controller-manager](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7205/pull-kueue-test-e2e-main-1-34/1975862374690721792/artifacts/run-test-e2e-singlecluster-1.34.0/kind-control-plane/pods/kube-system_kube-controller-manager-kind-control-plane_59db7f9c8cb80cab934b711df6195f61/kube-controller-manager/0.log)

``` 
2025-10-08T10:14:12.830511303Z stderr F I1008 10:14:12.830222       1 garbagecollector.go:501] "Processing item" logger="garbage-collector-controller" item="[kueue.x-k8s.io/v1beta1/Workload, namespace: sts-e2e-pldgc, name: statefulset-sts-18b6e, uid: cf557a79-97ba-4a79-bf09-93c05c7fe666]" virtual=false
2025-10-08T10:14:12.852030482Z stderr F I1008 10:14:12.851513       1 garbagecollector.go:567] "item has at least one existing owner, will not garbage collect" logger="garbage-collector-controller" item="[kueue.x-k8s.io/v1beta1/Workload, namespace: sts-e2e-pldgc, name: statefulset-sts-18b6e, uid: cf557a79-97ba-4a79-bf09-93c05c7fe666]" owner=[{"apiVersion":"v1","kind":"Pod","name":"sts-0","uid":"f0814f86-4e5b-411a-baec-c71afd04bbcc"}]
2025-10-08T10:14:12.852063422Z stderr F I1008 10:14:12.851574       1 garbagecollector.go:574] "remove dangling references and waiting references for item" logger="garbage-collector-controller" item="[kueue.x-k8s.io/v1beta1/Workload, namespace: sts-e2e-pldgc, name: statefulset-sts-18b6e, uid: cf557a79-97ba-4a79-bf09-93c05c7fe666]" dangling=[{"apiVersion":"v1","kind":"Pod","name":"sts-1","uid":"2e2e7d07-4a7e-4154-b2d9-83ba18d714dc"}] waitingForDependentsDeletion=null
2025-10-08T10:14:12.852069292Z stderr F I1008 10:14:12.851787       1 event.go:389] "Event occurred" logger="statefulset-controller" object="sts-e2e-pldgc/sts" fieldPath="" kind="StatefulSet" apiVersion="apps/v1" type="Normal" reason="SuccessfulDelete" message="delete Pod sts-0 in StatefulSet sts successful"
2025-10-08T10:14:14.948391768Z stderr F I1008 10:14:14.948076       1 garbagecollector.go:501] "Processing item" logger="garbage-collector-controller" item="[kueue.x-k8s.io/v1beta1/Workload, namespace: sts-e2e-pldgc, name: statefulset-sts-18b6e, uid: cf557a79-97ba-4a79-bf09-93c05c7fe666]" virtual=false
2025-10-08T10:14:14.959795236Z stderr F I1008 10:14:14.959605       1 garbagecollector.go:640] "Deleting item" logger="garbage-collector-controller" item="[kueue.x-k8s.io/v1beta1/Workload, namespace: sts-e2e-pldgc, name: statefulset-sts-18b6e, uid: cf557a79-97ba-4a79-bf09-93c05c7fe666]" propagationPolicy="Background"
2025-10-08T10:14:15.026350694Z stderr F I1008 10:14:15.026130       1 event.go:389] "Event occurred" logger="statefulset-controller" object="sts-e2e-pldgc/sts" fieldPath="" kind="StatefulSet" apiVersion="apps/v1" type="Normal" reason="SuccessfulCreate" message="create Pod sts-0 in StatefulSet sts successful"
```

kubelet:
```
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.833495     228 status_manager.go:1038] "Patch status for pod" pod="sts-e2e-pldgc/sts-0" podUID="6066b861-eabc-41d9-bcd5-2c90f9a0433b" patch="{\"metadata\":{\"uid\":\"6066b861-eabc-41d9-bcd5-2c90f9a0433b\"}}"
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.833556     228 status_manager.go:1045] "Status for pod is up-to-date" pod="sts-e2e-pldgc/sts-0" statusVersion=4
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.833579     228 status_manager.go:1103] "Delaying pod deletion as the phase is non-terminal" phase="Pending" localPhase="Pending" pod="sts-e2e-pldgc/sts-0" podUID="6066b861-eabc-41d9-bcd5-2c90f9a0433b"
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.847893     228 manager.go:1037] Destroyed container: "/kubelet.slice/kubelet-kubepods.slice/kubelet-kubepods-burstable.slice/kubelet-kubepods-burstable-pod6066b861_eabc_41d9_bcd5_2c90f9a0433b.slice" (aliases: [], namespace: "")
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.848691     228 status_manager.go:610] "Marking terminal pod as failed" oldPhase="Pending" pod="sts-e2e-pldgc/sts-0" podUID="6066b861-eabc-41d9-bcd5-2c90f9a0433b"
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.848904     228 pod_workers.go:971] "Pod worker has stopped" podUID="6066b861-eabc-41d9-bcd5-2c90f9a0433b"
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.869115     228 status_manager.go:1038] "Patch status for pod" pod="sts-e2e-pldgc/sts-0" podUID="6066b861-eabc-41d9-bcd5-2c90f9a0433b" patch="{\"metadata\":{\"uid\":\"6066b861-eabc-41d9-bcd5-2c90f9a0433b\"},\"status\":{\"containerStatuses\":[{\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.57\",\"imageID\":\"\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"exitCode\":137,\"finishedAt\":null,\"message\":\"The container could not be located when the pod was terminated\",\"reason\":\"ContainerStatusUnknown\",\"startedAt\":null}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-k2dgt\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Failed\"}}"
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.869859     228 status_manager.go:1047] "Status for pod updated successfully" pod="sts-e2e-pldgc/sts-0" statusVersion=5 status={"observedGeneration":3,"phase":"Failed","conditions":[{"type":"TerminationTarget","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-10-08T10:14:15Z","reason":"NoMatchingWorkload","message":"Missing Workload; unable to restore pod templates"},{"type":"PodReadyToStartContainers","observedGeneration":3,"status":"False","lastProbeTime":null,"lastTransitionTime":"2025-10-08T10:14:15Z"},{"type":"Initialized","observedGeneration":3,"status":"True","lastProbeTime":null,"lastTransitionTime":"2025-10-08T10:14:15Z"},{"type":"Ready","observedGeneration":3,"status":"False","lastProbeTime":null,"lastTransitionTime":"2025-10-08T10:14:15Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"ContainersReady","observedGeneration":3,"status":"False","lastProbeTime":null,"lastTransitionTime":"2025-10-08T10:14:15Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"PodScheduled","observedGeneration":3,"status":"True","lastProbeTime":null,"lastTransitionTime":"2025-10-08T10:14:15Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"startTime":"2025-10-08T10:14:15Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":137,"reason":"ContainerStatusUnknown","message":"The container could not be located when the pod was terminated","startedAt":null,"finishedAt":null}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.57","imageID":"","started":false,"volumeMounts":[{"name":"kube-api-access-k2dgt","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.870411     228 status_manager.go:1108] "The pod termination is finished as SyncTerminatedPod completes its execution" phase="Failed" localPhase="Failed" pod="sts-e2e-pldgc/sts-0" podUID="6066b861-eabc-41d9-bcd5-2c90f9a0433b"
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.881643     228 kubelet.go:2530] "SyncLoop DELETE" source="api" pods=["sts-e2e-pldgc/sts-0"]
Oct 08 10:14:16 kind-worker kubelet[228]: I1008 10:14:16.881901     228 status_manager.go:1076] "Pod fully terminated and removed from etcd" pod="sts-e2e-pldgc/sts-0"
```

 and [scheduler](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7205/pull-kueue-test-e2e-main-1-34/1975862374690721792/artifacts/run-test-e2e-singlecluster-1.34.0/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_14095e8558fd689c940f507d032d4780/kube-scheduler/0.log)

```
2025-10-08T10:14:15.026454215Z stderr F I1008 10:14:15.026355       1 eventhandlers.go:135] "Add event for unscheduled pod" pod="sts-e2e-pldgc/sts-0"
2025-10-08T10:14:15.063186133Z stderr F I1008 10:14:15.062951       1 schedule_one.go:100] "Attempting to schedule pod" pod="sts-e2e-pldgc/sts-0"
2025-10-08T10:14:15.063850657Z stderr F I1008 10:14:15.063668       1 pod_binding.go:51] "Attempting to bind pod to node" pod="sts-e2e-pldgc/sts-0" node="kind-worker"
2025-10-08T10:14:15.073269923Z stderr F I1008 10:14:15.073035       1 schedule_one.go:346] "Successfully bound pod to node" pod="sts-e2e-pldgc/sts-0" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-10-08T10:14:15.074146728Z stderr F I1008 10:14:15.073970       1 eventhandlers.go:219] "Delete event for unscheduled pod" pod="sts-e2e-pldgc/sts-0"
2025-10-08T10:14:15.074274899Z stderr F I1008 10:14:15.074131       1 eventhandlers.go:260] "Add event for scheduled pod" pod="sts-e2e-pldgc/sts-0"
2025-10-08T10:14:15.294822085Z stderr F I1008 10:14:15.290930       1 httplog.go:134] "HTTP" verb="GET" URI="/readyz" latency="115.301µs" userAgent="kube-probe/1.34" audit-ID="" srcIP="127.0.0.1:42166" resp=200
2025-10-08T10:14:16.275310365Z stderr F I1008 10:14:16.275095       1 httplog.go:134] "HTTP" verb="GET" URI="/readyz" latency="144.181µs" userAgent="kube-probe/1.34" audit-ID="" srcIP="127.0.0.1:42182" resp=200
2025-10-08T10:14:16.865131383Z stderr F I1008 10:14:16.864854       1 eventhandlers.go:355] "Delete event for scheduled pod" pod="sts-e2e-pldgc/sts-0"
```
is that there is one pod recreated and deleted just afterwards...

Could it be related to garbage collector?
Nevertheless after  `sts-0` creation it was deleted due to missing workload.

```
2025-10-08T10:14:15.043448255Z stderr F 2025-10-08T10:14:15.042494709Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:763	Workload delete event	{"workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-pldgc"}, "queue": "sts-lq", "status": "admitted"}
```

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-10T14:26:23Z

Looking at the timeline, workload was deleted (10:14:15.042494709) before pod was successfully created (10:14:15.073035) and that caused pod to fail.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T16:25:14Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7389/pull-kueue-test-e2e-main-1-32/1981745144096886784

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T16:26:52Z

/close
It is a different assert now, and https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-3380861022 was also different assert, likely different root cause. Let me start fresh

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-24T16:26:58Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-3443990854):

>/close
>It is a different assert now, and https://github.com/kubernetes-sigs/kueue/issues/4520#issuecomment-3380861022 was also different assert, likely different root cause. Let me start fresh


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T16:29:11Z

Opened new one: https://github.com/kubernetes-sigs/kueue/issues/7390
