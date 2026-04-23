# Issue #7846: [flaky test] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not admit child jobs and jobset even if the child job and jobset has a queue-name label

**Summary**: [flaky test] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not admit child jobs and jobset even if the child job and jobset has a queue-name label

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7846

**Last updated**: 2025-11-25T01:46:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T12:29:12Z
- **Updated**: 2025-11-25T01:46:36Z
- **Closed**: 2025-11-25T01:46:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 8

## Description

**What happened**:

failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7835/pull-kueue-test-e2e-customconfigs-main/1992927930895831040

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:498 with:
Expected
    <string>: 
to equal
    <string>: Completed failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:498 with:
Expected
    <string>: 
to equal
    <string>: Completed
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:499 @ 11/24/25 12:19:51.505
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T12:29:51Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T13:55:37Z

This is a different test than the one we just fixed btw.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T14:05:24Z

I took a look at the logs.

https://github.com/kubernetes-sigs/jobset/issues/1094

It looks like for the test we hit an error on modifying an out of date job.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T14:11:40Z

Interesting, shouldn't we then retry on the error until the update succeeds? Is it a recent regression in JobSet? I haven't seen this before. Also, I'm wondering if we really need then to wait for the JobSet to finish. It is not really the intention of the test, so as fixing the flake we could just remove the assert, and verify the JobSet is unsuspended.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T17:38:06Z

The flake seemed rare.

I'm open to restricting the test to what we actually care about. Waiting for complettion can be slow so if we don't need it I would suggest we don't check on it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T18:10:50Z

sgtm

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T19:21:14Z

https://github.com/kubernetes-sigs/kueue/pull/7862

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T19:21:19Z

/assign
