# Issue #7366: Flaky E2E test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods created by a StatefulSet in the test namespace without queue-name label

**Summary**: Flaky E2E test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods created by a StatefulSet in the test namespace without queue-name label

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7366

**Last updated**: 2025-12-05T17:28:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-10-23T12:21:27Z
- **Updated**: 2025-12-05T17:28:59Z
- **Closed**: 2025-12-05T17:28:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

`End To End Custom Configs handling Suite: kindest/node:v1.34.0: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods created by a StatefulSet in the test namespace without queue-name label` failed in CI.

```shell
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:657 with:
Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:657 with:
Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:658 @ 10/23/25 11:18:28.239
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://github.com/kubernetes-sigs/kueue/pull/7356
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7356/pull-kueue-test-e2e-customconfigs-main/1981316427394584576

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:21:40Z

/kind flake

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-05T12:56:07Z

This issue has the same root cause as #6883 and will be fixed by #4799. 
#4799 adds StatefulSet as the owner of the workload (when `replicas > 0`). This prevents the workload from being garbage collected during queue name changes, eliminating the race condition.
