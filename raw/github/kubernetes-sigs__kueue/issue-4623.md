# Issue #4623: Flaky test: LeaderWorkerSet integration when LeaderWorkerSet created should admit group with leader only

**Summary**: Flaky test: LeaderWorkerSet integration when LeaderWorkerSet created should admit group with leader only

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4623

**Last updated**: 2025-08-07T08:34:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-14T17:48:04Z
- **Updated**: 2025-08-07T08:34:23Z
- **Closed**: 2025-08-07T08:31:49Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

kind/flake

**What happened**:

test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4591/pull-kueue-test-e2e-main-1-29/1900594986903146496

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.29.4: [It] LeaderWorkerSet integration when LeaderWorkerSet created should admit group with leader only expand_less	55s
{Timed out after 45.061s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:135 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-gk29d",
                SelfLink: "",
                UID: "4148fde2-6141-4052-a4a5-55b40af71bb0",
                ResourceVersion: "3874",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-14T17:22:10Z,
                },
                DeletionTimestamp: {
                    Time: 2025-03-14T17:22:42Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "kueue.x-k8s.io/queue-name": "lws-lq",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "68c67c6876",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-49423",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/group-key": "3e238779391c8fd563d42eb5af19391bdcd7c130",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "lws-86cf6f578b",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-49423",
                },
                Annotations: {
                    "leaderworkerset.sigs.k8s.io/size": "1",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "1",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-49423",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "bf05a26b-fc96-4867-943b-98d4889e8421",
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
                            Time: 2025-03-14T17:22:10Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"bf05a26b-fc96-4867-943b-98d4889e8421\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomai...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty failed [FAILED] Timed out after 45.061s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:135 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-gk29d",
                SelfLink: "",
                UID: "4148fde2-6141-4052-a4a5-55b40af71bb0",
                ResourceVersion: "3874",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-14T17:22:10Z,
                },
                DeletionTimestamp: {
                    Time: 2025-03-14T17:22:42Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "kueue.x-k8s.io/queue-name": "lws-lq",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "68c67c6876",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-49423",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/group-key": "3e238779391c8fd563d42eb5af19391bdcd7c130",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "lws-86cf6f578b",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-49423",
                },
                Annotations: {
                    "leaderworkerset.sigs.k8s.io/size": "1",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "1",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-49423",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "bf05a26b-fc96-4867-943b-98d4889e8421",
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
                            Time: 2025-03-14T17:22:10Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"bf05a26b-fc96-4867-943b-98d4889e8421\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomai...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:136 @ 03/14/25 17:22:57.07
}
```

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-12T21:20:18Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-17T11:30:35Z

/kind flake

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-17T11:52:44Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:31:44Z

/close
This is likely already fixed (there were many LWS fixes + more resources for e2e tests for CI), let's reopen if it re-occurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-07T08:31:49Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4623#issuecomment-3163084683):

>/close
>This is likely already fixed (there were many LWS fixes + more resources for e2e tests for CI), let's reopen if it re-occurs.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:34:23Z

Note that it was reported before https://github.com/kubernetes/test-infra/commit/5d436c9eee155b6db46b2dd291dab0742b2e4863
