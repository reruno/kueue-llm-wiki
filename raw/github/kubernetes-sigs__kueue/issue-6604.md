# Issue #6604: [0.12] Flaky Integration Test: Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level should respect TAS usage by admitted workloads after reboot; second workload created before reboot

**Summary**: [0.12] Flaky Integration Test: Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level should respect TAS usage by admitted workloads after reboot; second workload created before reboot

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6604

**Last updated**: 2025-12-01T14:54:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-18T10:59:42Z
- **Updated**: 2025-12-01T14:54:54Z
- **Closed**: 2025-12-01T14:54:34Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The `TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level should respect TAS usage by admitted workloads after reboot; second workload created before reboot` case failed in periodic Job.

```shell
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:551 with:
pending_workloads with status=inadmissible
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:551 with:
pending_workloads with status=inadmissible
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:580 @ 08/18/25 07:44:42.779
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-12/1957343662291554304

<img width="1344" height="229" alt="Image" src="https://github.com/user-attachments/assets/b7d5527f-3e64-444b-9ca3-f1a6a60cd480" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-18T10:59:47Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-02T14:14:59Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6631/pull-kueue-test-integration-baseline-main/1962875473557983232

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-01T14:49:29Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T14:54:28Z

/close
we no longer have logs, but from the snippet it seems it is likely solved by https://github.com/kubernetes-sigs/kueue/pull/7845

This is because this PR still sets reason=inadmissible in case of a conflict:

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T14:54:35Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6604#issuecomment-3596995525):

>/close
>we no longer have logs, but from the snippet it seems it is likely solved by https://github.com/kubernetes-sigs/kueue/pull/7845
>
>This is because this PR still sets reason=inadmissible in case of a conflict:
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T14:54:43Z

Let's re-open if it happens again, or open a new one
