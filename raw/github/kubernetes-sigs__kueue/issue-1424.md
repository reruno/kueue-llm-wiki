# Issue #1424: Flaky admission checks integration tests

**Summary**: Flaky admission checks integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1424

**Last updated**: 2024-04-24T08:19:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2023-12-08T09:57:15Z
- **Updated**: 2024-04-24T08:19:34Z
- **Closed**: 2024-04-24T08:19:33Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Admission checks provisioning integration tests failed

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1415/pull-kueue-test-integration-main/1733054915275657216

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T15:25:26Z

/kind flake

### Comment by [@trasc](https://github.com/trasc) — 2023-12-12T15:06:46Z

This seems to be a test runner issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-19T09:30:12Z

> https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1415/pull-kueue-test-integration-main/1733054915275657216

It seems right. It seems that CPU throttling sometimes happens (limit 4core, used 6core):

https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-integration-main&var-build=All&refresh=30s

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-18T09:41:58Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-17T10:02:57Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-24T08:19:29Z

/close
we probably don't have any logs from this run anyway, let's open a new one if re-occurs. 

For the runner we bumped the resources recently: https://github.com/kubernetes/test-infra/pull/32150

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-24T08:19:33Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1424#issuecomment-2074364463):

>/close
>we probably don't have any logs from this run anyway, let's open a new one if re-occurs. 
>
>For the runner we bumped the resources recently: https://github.com/kubernetes/test-infra/pull/32150


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
