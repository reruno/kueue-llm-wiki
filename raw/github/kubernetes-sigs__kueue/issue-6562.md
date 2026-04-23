# Issue #6562: [Flaky E2E] Job reconciliation with ManagedJobsNamespaceSelectorAlwaysRespected should reconcile a job in managed namespace and create a workload

**Summary**: [Flaky E2E] Job reconciliation with ManagedJobsNamespaceSelectorAlwaysRespected should reconcile a job in managed namespace and create a workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6562

**Last updated**: 2026-01-19T07:39:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-08-12T14:01:15Z
- **Updated**: 2026-01-19T07:39:25Z
- **Closed**: 2026-01-19T07:39:24Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:
End To End Custom Configs handling Suite: kindest/node:v1.33.1: [It] Job reconciliation with ManagedJobsNamespaceSelectorAlwaysRespected should reconcile a job in managed namespace and create a workload 

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/reconcile_test.go:118 with:
Expected
    <[]v1beta1.Workload | len:0, cap:0>: []
to have length 1 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/reconcile_test.go:118 with:
Expected
    <[]v1beta1.Workload | len:0, cap:0>: []
to have length 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/reconcile_test.go:119 @ 08/11/25 13:52:47.895
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6528/pull-kueue-test-e2e-customconfigs-main/1954899181080416256

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-12T19:27:46Z

cc @PannagaRao

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-10T19:29:09Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T19:32:43Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T07:39:19Z

/close
1. we no longer have logs to investigate
2. it has not re-occurred for long
3. we made a number of improvements to stabilize Kueue reloading in the "customconfig" suites. Maybe the failure was related to Kueue not being properly restarted - but we don't have logs to know now.

We will open another ticket if that re-occurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-19T07:39:25Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6562#issuecomment-3766897413):

>/close
>1. we no longer have logs to investigate
>2. it has not re-occurred for long
>3. we made a number of improvements to stabilize Kueue reloading in the "customconfig" suites. Maybe the failure was related to Kueue not being properly restarted - but we don't have logs to know now.
>
>We will open another ticket if that re-occurs.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
