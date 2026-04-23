# Issue #511: Flaky integration test for  in webhook/v1alpha2/localqueue_test.go

**Summary**: Flaky integration test for  in webhook/v1alpha2/localqueue_test.go

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/511

**Last updated**: 2023-03-22T13:50:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-01-11T14:57:25Z
- **Updated**: 2023-03-22T13:50:38Z
- **Closed**: 2023-03-22T13:50:38Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Example failure on a branch which didn't touch the webhook code, so it seem not relevant.

"Webhook Suite: [It] Queue validating webhook when Updating a Queue Should allow the change of status expand_less | 0s"

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/498/pull-kueue-test-integration-main/1613143403141271552.

**What you expected to happen**:

The test does not fail.

**How to reproduce it (as minimally and precisely as possible)**:

Run tests on a PR.

^ This may not be predictive enough, a better way is to run the tests locally, but under stress:
- `stress --cpu N`, where N is the number of cores
- update Makefile to add `--until-it-fails` for integration tests
- update `localqueue_test.go` to use `Fit`:  `ginkgo.FIt("Should allow the change of status"
- `INTEGRATION_TARGET=test/integration/webhook/v1alpha2/ make test-integration`

This fails roughly 1 out of 3 on by machine.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T14:59:26Z

@cmssczy do you have bandwith to take a look?

### Comment by [@nayihz](https://github.com/nayihz) — 2023-01-12T02:27:11Z

I cannot reproduce this issue after clone your pr in my local test environment. 
And `test/integration/webhook/v1alpha2/localqueue_test.go` seems not to be affected in the previous pr about integration test cleanup.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-01-12T11:18:20Z

> I cannot reproduce this issue after clone your pr in my local test environment.
> And `test/integration/webhook/v1alpha2/localqueue_test.go` seems not to be affected in the previous pr about integration test cleanup.

Yes, I think it has nothing to do with the PR it was observed on, it can be reproduced on main branch, just under load. Updated the description with details.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-25T17:54:23Z

It failed again https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/521/pull-kueue-test-integration-main/1618300999850528768

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-17T15:51:01Z

~~Same here:~~ 
~~- https://github.com/kubernetes-sigs/kueue/pull/623~~
~~- https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/623/pull-kueue-test-integration-main/1636752086102183936~~

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-17T15:53:41Z

Error message for this test:

```
{Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/webhook/v1alpha2/localqueue_test.go:40 @ 01/11/23 12:05:11.762
}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-20T13:15:24Z

@tenzen-y do you have some time to investigate this one?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-20T17:22:31Z

> @tenzen-y do you have some time to investigate this one?

Sure. However, much time may be required since it seems that the root causes are complex.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-21T18:53:32Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-21T19:15:58Z

It seems that this is caused by updating localQueueStatus.pendingWorkloads with an incorrect value in the following steps:

1. Test directly updates LocalQueueStatus in https://github.com/kubernetes-sigs/kueue/blob/17fbec98f4a45a742d28d8cde9400134b77c8104/test/integration/webhook/localqueue_test.go#L39-L40.
2. Controller gets appropriate pendingWorkloads from the queue manager and updates status with the pendingWorkloads in https://github.com/kubernetes-sigs/kueue/blob/17fbec98f4a45a742d28d8cde9400134b77c8104/pkg/controller/core/localqueue_controller.go#L276-L278.
3. Test gets pendingWorkloads updated by the controller, not one updated by Test in https://github.com/kubernetes-sigs/kueue/blob/17fbec98f4a45a742d28d8cde9400134b77c8104/test/integration/webhook/localqueue_test.go#L43-L44.

Also, I guess when the cluster doesn't have enough resources for the K8s components, the queue manager updates the internal LocalQueue https://github.com/kubernetes-sigs/kueue/blob/17fbec98f4a45a742d28d8cde9400134b77c8104/pkg/queue/local_queue.go#L36-L42, and the controller updates the status with the appropriate value before Test gets the localQueueStatus from etcd in https://github.com/kubernetes-sigs/kueue/blob/17fbec98f4a45a742d28d8cde9400134b77c8104/test/integration/webhook/localqueue_test.go#L43-L44.

So IMO, we should create Workloads, not directly update localQueueStatus in https://github.com/kubernetes-sigs/kueue/blob/17fbec98f4a45a742d28d8cde9400134b77c8104/test/integration/webhook/localqueue_test.go#L35-L41.

@alculquicondor What do you think?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-21T20:20:59Z

Oh I see.
I think we can just remove the test.

Other tests already make sure that pendingWorkloads is kept up-to-date based on the queue manager.
This test by itself is not very useful.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-21T20:45:58Z

> Oh I see. I think we can just remove the test.
> 
> Other tests already make sure that pendingWorkloads is kept up-to-date based on the queue manager. This test by itself is not very useful.

That makes sense. I will create a PR to remove the test tomorrow :)
