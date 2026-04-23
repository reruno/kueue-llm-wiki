# Issue #8550: [Release-0.14 Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Summary**: [Release-0.14 Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8550

**Last updated**: 2026-01-19T18:47:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-12T17:06:37Z
- **Updated**: 2026-01-19T18:47:52Z
- **Closed**: 2026-01-19T18:47:52Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
End To End Suite: kindest/node:v1.32.8: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:471 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:471 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:472 @ 01/12/26 16:56:48.831
}
```

**What you expected to happen**:
No issue

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8520/pull-kueue-test-e2e-release-0-14-1-32/2010751664939601920

**Anything else we need to know?**:

/kind flake

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T17:11:08Z

Im wondering maybe this is another issue caused by the finalizers, but havent checked. If this is the case we could close it by the pending work.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:41:26Z

Let me close it because it looks likely caused by the finalizers indeed. We can see the pod `lws-e2e-pzq9z/lws-1` was created, however the Workload was not deleted. I think likely because the finalizer was never removed from the Pod.

So this is likely fixed by https://github.com/kubernetes-sigs/kueue/pull/8530

Let's reopen if this re-occurs still.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T15:18:43Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8590/pull-kueue-test-e2e-release-0-14-1-32/2011450320491646976
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-14T15:18:49Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8550#issuecomment-3750055358):

>https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8590/pull-kueue-test-e2e-release-0-14-1-32/2011450320491646976
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T05:08:50Z

We observed this again: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-14-1-32/2011652723933450240

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T11:55:15Z

Interesting, all the failures are for 0.14 release, suggesting this is flaky only on 0.14, but I cannot recall any changes which could explain that it would be fixed in 0.15+. One candidate set of changes cherrypicked to 0.15 was around workload WPC mutability, but I'm not clear this is related here.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T07:45:43Z

This one shows now quite often on the 0.14 branch, just from the last couple of days:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-14-1-35/2013107453721317376
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-14-1-34/2012558837130727424
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-14-1-32/2012196440914268160

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T12:07:23Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T12:33:55Z

I don't think it was flaking when we started the 0.14 branch, and not it is failing pretty often. So I think instead of guessing we could also try to bisect the history of the 0.14 branch. Maybe there was some unfortunate CP.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T12:37:45Z

Yeah, first time it happens 01/12/26. Let's which PR is blame.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T12:53:42Z

Thank you for looking into this, I'm quite curious :)
