# Issue #9608: Flaky E2E Test: End To End Suite: kindest/node:v1.32.8: [It] AppWrapper Should admit Workload for Job

**Summary**: Flaky E2E Test: End To End Suite: kindest/node:v1.32.8: [It] AppWrapper Should admit Workload for Job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9608

**Last updated**: 2026-03-02T10:02:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-03-02T05:29:44Z
- **Updated**: 2026-03-02T10:02:15Z
- **Closed**: 2026-03-02T10:02:15Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

End To End Suite: kindest/node:v1.32.8: [It] AppWrapper Should admit Workload for Job

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-32/2028104107457253376

**Failure message or logs**:
```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/appwrapper_test.go:113 with:
Expected
    <v1beta2.AppWrapperPhase>: Running
to equal
    <v1beta2.AppWrapperPhase>: Succeeded failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/appwrapper_test.go:113 with:
Expected
    <v1beta2.AppWrapperPhase>: Running
to equal
    <v1beta2.AppWrapperPhase>: Succeeded
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/appwrapper_test.go:114 @ 03/01/26 14:03:54.553
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T08:51:22Z

The namespace was `appwrapper-e2e-bl64j` 

From the [kubelet logs](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-32/2028104107457253376/artifacts/run-test-e2e-singlecluster-1.32.8/kind-worker/kubelet.log) we can see that, there were two pods as expected: `appwrapper-e2e-bl64j/job-0-wswdx` and `appwrapper-e2e-bl64j/job-0-4hrpw`.

Looking at the logs for one of them it started to run at, **14:03:14** see:

```
Mar 01 14:03:14 kind-worker kubelet[229]: I0301 14:03:14.736095     229 pod_startup_latency_tracker.go:172] "Mark when the pod was running for the first time" pod="appwrapper-e2e-bl64j/job-0-wswdx" rv="2746"
```
Then it terminated only at **14:03:59** (45s later). 

```
Mar 01 14:03:59 kind-worker kubelet[229]: I0301 14:03:59.382531     229 kubelet_pods.go:1826] "Generating pod status" podIsTerminal=true pod="appwrapper-e2e-bl64j/job-0-wswdx"
```
The Pod is using the `agnhost` image, using `BehaviorExitFast`, so decreasing the TerminationGrace period will not help.

However, it is only using 100m CPU. I think we observed similar e2e failures in the past for agnhost. So I propose here to also bump the requests to 200m (at least).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T08:56:31Z

/assign
