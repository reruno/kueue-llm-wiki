# Issue #1658: Flaky Multikueue E2E tests

**Summary**: Flaky Multikueue E2E tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1658

**Last updated**: 2024-02-01T20:26:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-26T18:19:24Z
- **Updated**: 2024-02-01T20:26:51Z
- **Closed**: 2024-02-01T20:26:51Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 16

## Description

**What happened**:

It looks like the Kueue managers start properly, but somehow they crash later.
As a result, we observe:

```
Internal error occurred: failed calling webhook "mclusterqueue.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-clusterqueue?timeout=10s": dial tcp 10.96.160.164:443: connect: connection refused
```

In `End To End MultiKueue Suite: kindest/node:v1.28.0: [It] MultiKueue when Creating a multikueue admission check Should run a job on worker if admitted`

**What you expected to happen**:

Kueue managers to continue to run properly

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1607/pull-kueue-test-e2e-main-1-28/1750942764473782272

Note that this PR only changes documentation, so the flakiness is definitely on the multikueue code.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T18:19:36Z

/assign @trasc 
cc @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T20:00:44Z

I think this is duplicated with #1649.
We can close one of these.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T23:27:18Z

/kind flaky

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-26T23:27:20Z

@tenzen-y: The label(s) `kind/flaky` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1658#issuecomment-1912823378):

>/kind flaky


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T23:27:28Z

/kind flake

### Comment by [@trasc](https://github.com/trasc) — 2024-01-29T07:46:04Z

For this behavior, I wold expect the kueue controller manager to be crushed, since before starting the suite it is checked that all the clusters are able to create a resource flavor. 

So , very likely this is happening due to the heavy load in multikueue case.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T13:56:57Z

As discussed under https://github.com/kubernetes-sigs/kueue/pull/1659 I run experiments looping the e2e multikueue tests. 

First, I was able to repro the issue locally with a failure rate around 1 out of 4, which is close to the one on GH CI.

Second, when running on existing clusters I don't get any failures (37 passes in a row, interrupted manually), which suggests the issue is only during startup.

Third, with the following code change I eliminated the failures locally (30 passes in a row, still running):

```golang
func KueueReadyForTesting(ctx context.Context, client client.Client) {
	resourceKueue := utiltesting.MakeResourceFlavor("default").Obj()
	gomega.Eventually(func() error {
		return client.Create(ctx, resourceKueue)
	}, StartUpTimeout, Interval).Should(gomega.Succeed())

	cqKueueTest := utiltesting.MakeClusterQueue("q1").
		ResourceGroup(
			*utiltesting.MakeFlavorQuotas("default").
				Resource(corev1.ResourceCPU, "1").
				Obj(),
		).
		Obj()

	gomega.Eventually(func() error {
		return client.Create(ctx, cqKueueTest)
	}, StartUpTimeout, Interval).Should(gomega.Succeed())

	ExpectClusterQueueToBeDeleted(ctx, client, cqKueueTest, true)
	ExpectResourceFlavorToBeDeleted(ctx, client, resourceKueue, true)
}
```
This suggests also the issue is only on startup. Further, it suggests that for multikueue, where the system is loaded there might be a signifficant difference when the ResourceFlavor webhooks and the ClusterQueue webhooks are functional. This also appears to explain why the PR https://github.com/kubernetes-sigs/kueue/pull/1659 is stable.

IIUC there is another ongoing effort by @trasc to see if we can have a more generic solution: https://github.com/kubernetes-sigs/kueue/pull/1674.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T15:07:27Z

Ok, I got failure on 32st loop, but on creating LocalQueue, because the localqueue_webhook wasn't ready. This reinforces the statement that the webhooks become ready at different points in time. However, this also means that we would need to add creating LocalQueues to `KueueReadyForTesting` (and virtually any object).

### Comment by [@trasc](https://github.com/trasc) — 2024-01-30T15:24:16Z

> Ok, I got failure on 32st loop, but on creating LocalQueue, because the localqueue_webhook wasn't ready. This reinforces the statement that the webhooks become ready at different points in time. However, this also means that we would need to add creating LocalQueues to `KueueReadyForTesting` (and virtually any object).

What was the error?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T15:34:32Z

> What was the error?

```
2024-01-30 15:06:10.751971   [FAILED] Expected success, but got an error:
2024-01-30 15:06:10.751998       <*errors.StatusError | 0xc000593360>: 
2024-01-30 15:06:10.752025       Internal error occurred: failed calling webhook "vlocalqueue.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-localqueue?timeout=10s": dial tcp 10.244.1.4:9443: connect: connection refused
2024-01-30 15:06:10.752054       {
2024-01-30 15:06:10.752083           ErrStatus: {
2024-01-30 15:06:10.752110               TypeMeta: {Kind: "", APIVersion: ""},
2024-01-30 15:06:10.752138               ListMeta: {
2024-01-30 15:06:10.752166                   SelfLink: "",
2024-01-30 15:06:10.752193                   ResourceVersion: "",
2024-01-30 15:06:10.752220                   Continue: "",
2024-01-30 15:06:10.752247                   RemainingItemCount: nil,
2024-01-30 15:06:10.752276               },
2024-01-30 15:06:10.752304               Status: "Failure",
2024-01-30 15:06:10.752331               Message: "Internal error occurred: failed calling webhook \"vlocalqueue.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-localqueue?timeout=10s\": dial tcp 10.244.1.4:9443: connect: connection refused",
2024-01-30 15:06:10.752360               Reason: "InternalError",
2024-01-30 15:06:10.752387               Details: {
2024-01-30 15:06:10.752414                   Name: "",
2024-01-30 15:06:10.752440                   Group: "",
2024-01-30 15:06:10.752467                   Kind: "",
2024-01-30 15:06:10.752494                   UID: "",
2024-01-30 15:06:10.752521                   Causes: [
2024-01-30 15:06:10.752548                       {
2024-01-30 15:06:10.752575                           Type: "",
2024-01-30 15:06:10.752602                           Message: "failed calling webhook \"vlocalqueue.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-localqueue?timeout=10s\": dial tcp 10.244.1.4:9443: connect: connection refused",
2024-01-30 15:06:10.752630                           Field: "",
2024-01-30 15:06:10.752657                       },
2024-01-30 15:06:10.752687                   ],
2024-01-30 15:06:10.752714                   RetryAfterSeconds: 0,
2024-01-30 15:06:10.752765               },
2024-01-30 15:06:10.752793               Code: 500,
2024-01-30 15:06:10.752820           },
2024-01-30 15:06:10.752846       }
2024-01-30 15:06:10.752873   In [BeforeEach] at: /.../src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:162 @ 01/30/24 15:06:08.444
```

### Comment by [@trasc](https://github.com/trasc) — 2024-01-30T15:37:41Z

I expect `connect: connection refused` to be a L4 error and no be impacted by the handlers the webhook server has registered at some point.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T15:51:04Z

> I expect connect: connection refused to be a L4 error and no be impacted by the handlers the webhook server has registered at some point.

Not sure I understand to be able to follow up. Do you suggest that this is not caused by webhooks, or that there is a bug in API server that 500 is returned in this case?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-30T20:00:55Z

I wonder if the `connection refused` is caused because the `caBundle` is still not set in the ValidatingWebhookConfiguration or MutatingWebhookConfiguration objects.

That might be consistent with @mimowo's observations.

However, when we added the MK tests, we didn't increase resource requests in the E2E jobs, did we? Perhaps we can start there?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-30T22:09:34Z

I think we should do both #1674 and increasing the requests.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-31T08:59:40Z

I think I understand now what was happening. Described here: https://github.com/kubernetes-sigs/kueue/pull/1659#issuecomment-1918658045. Essentially, with 2 replicas running the registered webhooks are distributed randomly between the two replicas. With the `KueueReadyForTesting` we would only make sure a subset of webhooks is working, but if unlucky some webooks which are supported by the other replica would fail.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-31T09:04:11Z

I have also opened an alternative proposal using probes to wait for the ready replicaes: https://github.com/kubernetes-sigs/kueue/pull/1676. Seems to pass consitently, but going to yet test more.
