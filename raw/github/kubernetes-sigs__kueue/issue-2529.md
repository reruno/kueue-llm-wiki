# Issue #2529: Flaky e2e test for Pod groups

**Summary**: Flaky e2e test for Pod groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2529

**Last updated**: 2024-07-03T18:31:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2024-07-03T17:53:05Z
- **Updated**: 2024-07-03T18:31:19Z
- **Closed**: 2024-07-03T18:31:19Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
For #2526 `End To End Suite: kindest/node:v1.30.0: [It] Pod groups when Single CQ Unscheduled Pod which is deleted can be replaced in group` failed in https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2526/pull-kueue-test-e2e-main-1-30/1808529251364769792.

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:326 with:
Expected
    <v1.PodPhase>: Pending
not to equal
    <v1.PodPhase>: Pending failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:326 with:
Expected
    <v1.PodPhase>: Pending
not to equal
    <v1.PodPhase>: Pending
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:328 @ 07/03/24 16:02:55.772
}
```
**What you expected to happen**:

Not to fail

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@trasc](https://github.com/trasc) — 2024-07-03T17:53:14Z

/assign
