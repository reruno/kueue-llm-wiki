# Issue #6573: Flaky E2E: MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Summary**: Flaky E2E: MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6573

**Last updated**: 2025-11-14T18:23:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-13T13:57:35Z
- **Updated**: 2025-11-14T18:23:39Z
- **Closed**: 2025-11-14T18:23:39Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Unexpected `End To End MultiKueue Suite: kindest/node:v1.33.1: [It] MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state` failure on periodic Job

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:115 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:115 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:175 @ 08/13/25 05:31:21.359
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-13/1955496724898254848

<img width="1318" height="172" alt="Image" src="https://github.com/user-attachments/assets/0f510424-25e5-479e-a2e1-c924d18f61db" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-13T13:57:44Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-13T13:58:51Z

IIUC, this was introduced in https://github.com/kubernetes-sigs/kueue/pull/6466
@mszadkow Could you take a look at this failure?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-08-14T07:16:13Z

Actually it was the attempt (apparently not successful) to fix this issue.
I will have a look, the tricky part is that I tested it many times with repetitions and it was all fine...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T08:41:07Z

> Actually it was the attempt (apparently not successful) to fix this issue. I will have a look, the tricky part is that I tested it many times with repetitions and it was all fine...

Oh, I see. Thank you!

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-08-18T11:11:21Z

Initial research shows that at the time the deletion failed Kueue instance was not present or at least its last log was at: `2025-08-13T05:30:36.358762662Z`, while test failed at `05:31:21.359`.
Also the thing I haven't seen before (not saying it wasn't there):
```
2025-08-13T05:30:49.236394539Z stderr F E0813 05:30:49.236253       1 namespace_controller.go:164] "Unhandled Error" err="deletion of namespace multikueue-mmx6c failed: unable to retrieve the complete list of server APIs: visibility.kueue.x-k8s.io/v1beta1: stale GroupVersion discovery: visibility.kueue.x-k8s.io/v1beta1" logger="UnhandledError"
```
Which suggests that the test would probably fail earlier, but we don't check the deletion here:
```
	ginkgo.AfterEach(func() {
		gomega.Expect(util.DeleteNamespace(ctx, k8sManagerClient, managerNs)).To(gomega.Succeed())
		gomega.Expect(util.DeleteNamespace(ctx, k8sWorker1Client, worker1Ns)).To(gomega.Succeed())
		gomega.Expect(util.DeleteNamespace(ctx, k8sWorker2Client, worker2Ns)).To(gomega.Succeed())

		util.ExpectObjectToBeDeletedWithTimeout(ctx, k8sWorker1Client, worker1Cq, true, util.LongTimeout)
		util.ExpectObjectToBeDeletedWithTimeout(ctx, k8sWorker1Client, worker1Flavor, true, util.LongTimeout)
```

also it was deleted in the end:
```
2025-08-13T05:30:59.716043547Z stderr F I0813 05:30:59.715901       1 namespace_controller.go:187] "Namespace has been deleted" logger="namespace-controller" namespace="multikueue-mmx6c"
```

so maybe there is no issue for that.

About CQ that should have been deleted, at least locally when I try to run the test `cq1` gets recreated.
I don't see any sign of the same happening here...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T19:22:35Z

So, do you suspect that the Cluster deletion was triggered during performing `ginkgo.AfterEach`, right?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-08-21T10:31:13Z

I was able to easily verify this, bc locally I can run tests without cleaning up the cluster.
And still with enough repetitions it flakes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-15T05:43:30Z

We observed this again in periodic test: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-13/1966731955747688448

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:51:33Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/1988378724294201344
