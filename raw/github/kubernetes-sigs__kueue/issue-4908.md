# Issue #4908: Flaky e2e test: TopologyAwareScheduling for LeaderWorkerSet [AfterEach] when creating a LeaderWorkerSet should place pods based on the ranks-ordering

**Summary**: Flaky e2e test: TopologyAwareScheduling for LeaderWorkerSet [AfterEach] when creating a LeaderWorkerSet should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4908

**Last updated**: 2025-04-15T13:23:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-08T07:48:03Z
- **Updated**: 2025-04-15T13:23:08Z
- **Closed**: 2025-04-15T13:23:08Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4800/pull-kueue-test-e2e-tas-main/1909451143222661120#1:build-log.txt

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
[FAILED] [49.464 seconds]
TopologyAwareScheduling for LeaderWorkerSet [AfterEach] when creating a LeaderWorkerSet should place pods based on the ranks-ordering
  [AfterEach] /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/leaderworkerset_test.go:70
  [It] /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/leaderworkerset_test.go:80
  [FAILED] Timed out after 45.001s.
  The function passed to Eventually failed at /usr/local/go/src/reflect/value.go:581 with:
  Expected
      <[]v1.Pod | len:1, cap:1>: [
          {
              TypeMeta: {Kind: "", APIVersion: ""},
push_pin
              ObjectMeta: {
                  Name: "lws-1-1",
                  GenerateName: "lws-1-",
                  Namespace: "e2e-tas-lws-m6mz9",
                  SelfLink: "",
                  UID: "58046cf2-3730-45ad-9273-a8dd80a9db2a",
                  ResourceVersion: "4150",
                  Generation: 0,
                  CreationTimestamp: {
                      Time: 2025-04-08T03:56:52Z,
                  },
                  DeletionTimestamp: {
                      Time: 2025-04-08T03:56:55Z,
                  },
                  DeletionGracePeriodSeconds: 1,
                  Labels: {
                      "kueue.x-k8s.io/queue-name": "test-queue",
                      "kueue.x-k8s.io/tas": "true",
                      "leaderworkerset.sigs.k8s.io/group-index": "1",
                      "leaderworkerset.sigs.k8s.io/group-key": "af6322ca96c1f8f22931b676e083fe433446e054",
                      "leaderworkerset.sigs.k8s.io/name": "lws",
                      "kueue.x-k8s.io/managed": "true",
                      "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-1-cf2ee",
                      "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-1-cf2ee",
                      "leaderworkerset.sigs.k8s.io/template-revision-hash": "59cc57b4f4",
                      "leaderworkerset.sigs.k8s.io/worker-index": "1",
                      "statefulset.kubernetes.io/pod-name": "lws-1-1",
                      "apps.kubernetes.io/pod-index": "1",
                      "controller-revision-hash": "lws-1-5fb989dcf9",
                      "kueue.x-k8s.io/podset": "main",
                  },
                  Annotations: {
                      "kueue.x-k8s.io/pod-group-total-count": "3",
                      "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                      "kueue.x-k8s.io/podset-required-topology": "cloud.provider.com/topology-block",
                      "kueue.x-k8s.io/role-hash": "main",
                      "kueue.x-k8s.io/workload": "leaderworkerset-lws-1-cf2ee",
                      "leaderworkerset.sigs.k8s.io/leader-name": "lws-1",
                      "leaderworkerset.sigs.k8s.io/size": "3",
                      "kueue.x-k8s.io/pod-group-serving": "true",
                  },
                  OwnerReferences: [
                      {
                          APIVersion: "apps/v1",
                          Kind: "StatefulSet",
                          Name: "lws-1",
                          UID: "0a34788f-f766-4002-be66-22711ca7f871",
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
                              Time: 2025-04-08T03:56:52Z,
                          },
                          FieldsType: "FieldsV1",
                          FieldsV1: {
                              Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:kueue.x-k8s.io/podset-required-topology\":{},\"f:leaderworkerset.sigs.k8s.io/leader-name\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/group-index\":{},\"f:leaderworkerset.sigs.k8s.io/group-key\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0a34788f-f766-4002-be66-22711ca7f871\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},...
  Gomega truncated this representation as it exceeds 'format.MaxLength'.
  Consider having the object provide a custom 'GomegaStringer' representation
  or adjust the parameters in Gomega's 'format' package.
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T07:48:10Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T07:48:19Z

cc @mbobrovskyi @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T07:48:51Z

Maybe we need to wait a bit longer, or something went wrong?
