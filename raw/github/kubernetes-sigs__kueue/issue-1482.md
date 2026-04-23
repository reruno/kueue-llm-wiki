# Issue #1482: Flaky test e2e test for pending workloads

**Summary**: Flaky test e2e test for pending workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1482

**Last updated**: 2023-12-19T17:20:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-12-18T15:35:50Z
- **Updated**: 2023-12-19T17:20:18Z
- **Closed**: 2023-12-19T17:20:18Z
- **Labels**: `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 6

## Description

This test is flaky: "Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about position of pending workloads in ClusterQueue"

Example failure: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1397/pull-kueue-test-e2e-main-1-27/1736767429989634048

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T15:41:58Z

/kind flaky

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-18T15:42:01Z

@tenzen-y: The label(s) `kind/flaky` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1482#issuecomment-1860848723):

>/kind flaky


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T15:42:45Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-19T09:58:01Z

/assign
I have a reproducible scenario by looping the test, going to investigate.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-19T10:20:43Z

The issue is that there are two competing jobs `test-job-1` and `job-lq-a-high-prio`, both with priority high. So, occasionally workload for `job-lq-a-high-prio` is admitted first. This can be seen in the logs in the namespace `e2e-bgmdh` for workloads `job-lq-a-high-prio-56f58` (got admitted), and `job-test-job-1-c3094` (remains pending).

 We can prevent this by adding a step to wait for `test-job-1` to be admitted. Will open the PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-19T17:14:52Z

> The issue is that there are two competing jobs `test-job-1` and `job-lq-a-high-prio`, both with priority high. So, occasionally workload for `job-lq-a-high-prio` is admitted first. This can be seen in the logs in the namespace `e2e-bgmdh` for workloads `job-lq-a-high-prio-56f58` (got admitted), and `job-test-job-1-c3094` (remains pending).
> 
> We can prevent this by adding a step to wait for `test-job-1` to be admitted. Will open the PR.

Thank you for the clarifications.
