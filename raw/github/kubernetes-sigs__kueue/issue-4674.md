# Issue #4674: Flaky Test: LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up LeaderCreatedStartupPolicy

**Summary**: Flaky Test: LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up LeaderCreatedStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4674

**Last updated**: 2025-03-18T17:22:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-18T15:16:31Z
- **Updated**: 2025-03-18T17:22:03Z
- **Closed**: 2025-03-18T17:13:13Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky Test on an unrelated branch for `LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up LeaderCreatedStartupPolicy`

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:341 with:
Expected
    <[]v1.Pod | len:6, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-b95kh",
                SelfLink: "",
                UID: "7b729dde-8470-4569-be61-82f7363b56a8",
                ResourceVersion: "3809",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-17T09:56:36Z,
                },
                DeletionTimestamp: {
                    Time: 2025-03-17T09:57:11Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-0da4e",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-0da4e",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "84bd55cb4b",
                    "apps.kubernetes.io/pod-index": "0",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/queue-name": "lws-lq",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/group-key": "e35504d6b0a2a997f10d741e846ea07fcd584b88",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                    "controller-revision-hash": "lws-6bd56dfc7f",
                    "kueue.x-k8s.io/managed": "true",
                },
                Annotations: {
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-0da4e",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "c3820f56-37c4-4090-a6b3-080d5cb76d5f",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "kueue.x-k8s.io/managed",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-17T09:56:36Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"c3820f56-37c4-4090-a6b3-080d5cb76d5f\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:341 with:
Expected
    <[]v1.Pod | len:6, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-b95kh",
                SelfLink: "",
                UID: "7b729dde-8470-4569-be61-82f7363b56a8",
                ResourceVersion: "3809",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-17T09:56:36Z,
                },
                DeletionTimestamp: {
                    Time: 2025-03-17T09:57:11Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-0da4e",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-0da4e",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "84bd55cb4b",
                    "apps.kubernetes.io/pod-index": "0",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/queue-name": "lws-lq",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/group-key": "e35504d6b0a2a997f10d741e846ea07fcd584b88",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                    "controller-revision-hash": "lws-6bd56dfc7f",
                    "kueue.x-k8s.io/managed": "true",
                },
                Annotations: {
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-0da4e",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "c3820f56-37c4-4090-a6b3-080d5cb76d5f",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "kueue.x-k8s.io/managed",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-17T09:56:36Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"c3820f56-37c4-4090-a6b3-080d5cb76d5f\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:342 @ 03/17/25 09:57:26.28
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4638/pull-kueue-test-e2e-main-1-31/1901570063836647424

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T15:16:42Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T17:03:53Z

This failure was from yesterday, meaning before https://github.com/kubernetes/test-infra/pull/34529 as discussed here: https://github.com/kubernetes-sigs/kueue/issues/4669.

and it is capped by 8 cpu still: 

![Image](https://github.com/user-attachments/assets/69023fab-f4b2-4f65-993a-e3a8a17b3671)

For refernce, Job ID: 43b6ea05-3167-463e-ac41-0339836b28ef

and monitoring link: https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=1742204700936&to=1742205558285&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-e2e-main-1-31&var-build=All

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T17:13:08Z

Oh, good call. In that case, let's close this for now, then if we face the same issue, we can reopen this.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-18T17:13:13Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734083152):

>Oh, good call. In that case, let's close this for now, then if we face the same issue, we can reopen this.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T17:16:26Z

> Oh, good call. In that case, let's close this for now, then if we face the same issue, we can reopen this.

I would even consider full reset and close all e2e-related tests attributed to slow termination.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T17:22:02Z

> > Oh, good call. In that case, let's close this for now, then if we face the same issue, we can reopen this.
> 
> I would even consider full reset and close all e2e-related tests attributed to slow termination.
> 

SGTM
