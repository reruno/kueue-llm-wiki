# Issue #5302: [Flaky test]  WaitForPodsReady Job Controller E2E when WaitForPodsReady has a tiny Timeout and no RecoveryTimeout should evict and requeue workload when pods readiness timeout is surpassed

**Summary**: [Flaky test]  WaitForPodsReady Job Controller E2E when WaitForPodsReady has a tiny Timeout and no RecoveryTimeout should evict and requeue workload when pods readiness timeout is surpassed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5302

**Last updated**: 2025-05-23T11:14:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-20T14:48:20Z
- **Updated**: 2025-05-23T11:14:36Z
- **Closed**: 2025-05-23T11:14:36Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 6

## Description

**What happened**:

Failure on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5300/pull-kueue-test-e2e-customconfigs-main/1924833078941847552

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:


ci

**Anything else we need to know?**:
 
```
{Timed out after 133.023s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:355 with:
Unexpected error:
    <exec.CodeExitError>: 
    command terminated with exit code 28
    {
        Err: <*errors.errorString | 0xc000264040>{
            s: "command terminated with exit code 28",
        },
        Code: 28,
    }
occurred failed [FAILED] Timed out after 133.023s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:355 with:
Unexpected error:
    <exec.CodeExitError>: 
    command terminated with exit code 28
    {
        Err: <*errors.errorString | 0xc000264040>{
            s: "command terminated with exit code 28",
        },
        Code: 28,
    }
occurred
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/waitforpodsready_test.go:174 @ 05/20/25 14:34:09.404
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T14:48:27Z

/kind flake

### Comment by [@mykysha](https://github.com/mykysha) — 2025-05-21T08:31:01Z

/assign

### Comment by [@mykysha](https://github.com/mykysha) — 2025-05-21T13:02:40Z

Seems to appear quite often and is easily reproducible locally, working on finding the reason. Looks like the helper pod for retrieving metrics is failing

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T09:11:39Z

it happen again https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-main/1925318387680940032

This seems very common

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T09:13:06Z

> Looks like the helper pod for retrieving metrics is failing

This is surprising, could it be that the kueue pod is crashing, and thus it does not serve metrics while restarting? If you have a local repro then please check `kubectl get po -nkueue-system` and check if there are any restarts.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-22T11:38:46Z

Another one: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5287/pull-kueue-test-e2e-customconfigs-main/1925512230246289408
