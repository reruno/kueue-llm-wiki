# Issue #5350: [flaky test] Creating a Job With Queueing Should allow to schedule Jobs via CronJob

**Summary**: [flaky test] Creating a Job With Queueing Should allow to schedule Jobs via CronJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5350

**Last updated**: 2025-06-11T09:37:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-26T10:35:09Z
- **Updated**: 2025-06-11T09:37:19Z
- **Closed**: 2025-06-11T09:37:18Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

**What happened**:

Failure on unreleated branch; https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5327/pull-kueue-test-e2e-main-1-31/1926944014251069440

**What you expected to happen**:
no failure

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:125 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:125 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/e2e_test.go:118 @ 05/26/25 10:25:10.353
}
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-27T15:06:26Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T08:18:33Z

/reopen 
as this occurred on 0.11 branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-11-1-31/1932601473795887104

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-11T08:18:38Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5350#issuecomment-2961682683):

>/reopen 
>as this occurred on 0.11 branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-11-1-31/1932601473795887104


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-11T09:37:13Z

/close

Due to fixed on https://github.com/kubernetes-sigs/kueue/pull/5619.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-11T09:37:19Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5350#issuecomment-2961945457):

>/close
>
>Due to fixed on https://github.com/kubernetes-sigs/kueue/pull/5619.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
