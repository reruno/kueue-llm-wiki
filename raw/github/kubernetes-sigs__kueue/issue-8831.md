# Issue #8831: [Flaky Perf] TestScalability/CommandStats

**Summary**: [Flaky Perf] TestScalability/CommandStats

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8831

**Last updated**: 2026-05-11T07:26:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-27T16:17:51Z
- **Updated**: 2026-05-11T07:26:10Z
- **Closed**: 2026-05-11T07:26:09Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability/CommandStats

```
{Failed  === RUN   TestScalability/WorkloadClasses/small
    checker_test.go:108: Average wait for admission 248062ms is more then expected 233000ms
--- FAIL: TestScalability/WorkloadClasses/small (0.00s)
}
```


sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability/WorkloadClasses expand_less | 0s
```
{Failed  === RUN   TestScalability/WorkloadClasses
--- FAIL: TestScalability/WorkloadClasses (0.00s)
}
```

sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability 

```
{Failed  === RUN   TestScalability
--- FAIL: TestScalability (0.01s)
}
```


```
=== Failed
=== FAIL: test/performance/scheduler/checker TestScalability/CommandStats (0.00s)
    checker_test.go:81: Wall time 493017ms is greater than maximum expected 425000ms
=== FAIL: test/performance/scheduler/checker TestScalability/WorkloadClasses/small (0.00s)
    checker_test.go:108: Average wait for admission 248062ms is more then expected 233000ms
=== FAIL: test/performance/scheduler/checker TestScalability/WorkloadClasses (0.00s)
=== FAIL: test/performance/scheduler/checker TestScalability (0.01s)
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8825/pull-kueue-test-scheduling-perf-main/2016176842435727360

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-27T17:27:42Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-27T18:27:43Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-27T19:27:41Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-11T07:26:03Z

/close
Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-11T07:26:10Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8831#issuecomment-4418414259):

>/close
>Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
