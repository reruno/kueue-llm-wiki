# Issue #6437: [Flaky] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

**Summary**: [Flaky] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6437

**Last updated**: 2025-11-27T13:19:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-08-04T13:54:09Z
- **Updated**: 2025-11-27T13:19:55Z
- **Closed**: 2025-11-27T13:19:54Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The test failed

**What you expected to happen**:
No failure

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6421/pull-kueue-test-integration-baseline-main/1952346938187714560

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T13:54:16Z

/kind flake

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T13:54:55Z

The test continue to flake, so I'll validate my hypothesis from [here](https://github.com/kubernetes-sigs/kueue/issues/6412#issuecomment-3149829728)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T14:02:06Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T13:19:49Z

/close
We don't have logs at this point, and we also likely have addressed that with the recent fix  https://github.com/kubernetes-sigs/kueue/pull/7780
cc @IrvingMg

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-27T13:19:55Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6437#issuecomment-3585827247):

>/close
>We don't have logs at this point, and we also likely have addressed that with the recent fix  https://github.com/kubernetes-sigs/kueue/pull/7780
>cc @IrvingMg 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
