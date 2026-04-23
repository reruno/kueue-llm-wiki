# Issue #1501: Flaky: Pod controller when manageJobsWithoutQueueName is disabled when Using single pod Should stop the single pod with the queue name if workload is evicted

**Summary**: Flaky: Pod controller when manageJobsWithoutQueueName is disabled when Using single pod Should stop the single pod with the queue name if workload is evicted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1501

**Last updated**: 2024-01-08T20:50:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-21T03:25:18Z
- **Updated**: 2024-01-08T20:50:13Z
- **Closed**: 2024-01-08T20:50:13Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Failed "Pod controller when manageJobsWithoutQueueName is disabled when Using single pod Should stop the single pod with the queue name if workload is evicted".

**What you expected to happen**:
Any errors wouldn't happened.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1493/pull-kueue-test-integration-main/1737661427335827456

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-21T04:52:33Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T09:13:50Z

This flaky error happened again.

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1536/pull-kueue-test-integration-main/1742096732738555904

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-04T15:05:07Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-05T04:40:51Z

This happened because pods were removed after we verified the pod status here:

https://github.com/kubernetes-sigs/kueue/blob/1579d75e5a35bdb4ab24c64b2da4e4effa98bbc8/test/integration/controller/jobs/pod/pod_controller_test.go#L296-L299

However, it is difficult to completely prevent this flaky case since the pod controller immediately deletes target pods after updating the pod status:

https://github.com/kubernetes-sigs/kueue/blob/1579d75e5a35bdb4ab24c64b2da4e4effa98bbc8/pkg/controller/jobs/pod/pod_controller.go#L326-L331

So, we should add a finalizer to block immediate deletion only when integration test.
