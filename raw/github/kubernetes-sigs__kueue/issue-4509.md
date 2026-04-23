# Issue #4509: Increase the threshold for the output size for a failed ginkgo assert

**Summary**: Increase the threshold for the output size for a failed ginkgo assert

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4509

**Last updated**: 2026-01-29T15:12:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-06T08:21:49Z
- **Updated**: 2026-01-29T15:12:59Z
- **Closed**: 2026-01-29T15:12:58Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Increase the output length in case of a failed ginkgo assert.

We need to be careful not to make it too long, as then we risk issues at the browser (client) side with rendering. However, being able to see one full output should still be ok probably for 4 pods (or at least one full). An actual research on how much a browser can handle would help to make a decision about the threshold. 

**Why is this needed**:

When ginkgo tests fail, for example due to unexpected set of pods, the output is truncated and we cannot see the status of the Pod. This would have helped with investigating 
https://github.com/kubernetes-sigs/kueue/issues/4495 and https://github.com/kubernetes-sigs/kueue/issues/4508.

Currently the output looks like:
```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/appwrapper_test.go:129 with:
Expected
    <[]v1.Pod | len:5, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "job-0-2tk5q",
                GenerateName: "job-0-",
                Namespace: "e2e-tas-aw-dnz4h",
                SelfLink: "",
                UID: "7e5b1126-3a4b-4310-9637-41e061a0de48",
                ResourceVersion: "5578",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T08:20:44Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "job-name": "job-0",
                    "kueue.x-k8s.io/podset": "appwrapper-0",
                    "kueue.x-k8s.io/tas": "true",
                    "workload.codeflare.dev/appwrapper": "appwrapper",
                    "batch.kubernetes.io/controller-uid": "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                    "batch.kubernetes.io/job-name": "job-0",
                    "controller-uid": "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "appwrapper-appwrapper-5f337",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "job-0",
                        UID: "0e203b4a-8c6d-4507-8e61-0f991d37493e",
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
                            Time: 2025-03-05T08:20:44Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/controller-uid\":{},\"f:batch.kubernetes.io/job-name\":{},\"f:controller-uid\":{},\"f:job-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:workload.codeflare.dev/appwrapper\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0e203b4a-8c6d-4507-8e61-0f991d37493e\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{},\"f:example.com/gpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{},\"f:example.com/gpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:20:45Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time:...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T08:26:52Z

cc @tenzen-y

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-04T09:08:04Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T09:09:15Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-02T09:45:34Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-02T09:47:32Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-01T10:45:25Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T10:48:20Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T15:12:54Z

/close 
This is already done in https://github.com/kubernetes-sigs/kueue/pull/8487

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-29T15:12:59Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4509#issuecomment-3818319210):

>/close 
>This is already done in https://github.com/kubernetes-sigs/kueue/pull/8487


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
