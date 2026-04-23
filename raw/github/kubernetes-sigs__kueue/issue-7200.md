# Issue #7200: Improve running time of e2e and integration tests

**Summary**: Improve running time of e2e and integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7200

**Last updated**: 2026-01-09T14:00:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-08T07:06:40Z
- **Updated**: 2026-01-09T14:00:03Z
- **Closed**: 2026-01-09T14:00:02Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 9

## Description

**e2e tests**

Currently around 25min: https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34

Ideas:
- split into slow and fast suites, as we did for integration tests, corresponding to "extended" and "baseline" test suites
- run them "in parallel" (might be more involving to make sure we avoid collisions)

**integration tests**

Currently around "baseline" suite 24min: https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main

However the "extended" suite (long tests) is only 11min: https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/pr-logs/directory/pull-kueue-test-integration-extended-main

Ideas:
- better balance between the "baseline" and "extended" by revisiting the time threshold. Note that currently "baseline" means "fast" while "extended" is "long". The original threshold was around 10s probably, so we may check the balance when updating according to the threshold again, or revisit updating the threshold.

On top of both we should also revisit increasing CPU & memory for the test suites. This [dashboard](https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=1759477142489&to=1759477841942&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-e2e-main-1-34&var-build=All) can be useful assessing the impact.

Certainly more ideas are welcome.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T07:06:49Z

cc @tenzen-y @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T07:06:55Z

cc @mwysokin

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-10-22T06:53:09Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T13:50:05Z

/kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:46:48Z

/priority important-soon

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T13:42:36Z

@j-skiba what is yet missing here? 

When adding a new PR please always reference the issue, it improves finding the PR much better. Let me reference the main ones already:
- https://github.com/kubernetes-sigs/kueue/pull/8255
- https://github.com/kubernetes-sigs/kueue/pull/8327

### Comment by [@j-skiba](https://github.com/j-skiba) — 2026-01-09T13:46:35Z

It's done, it can be closed. I don't have permission to close it manually

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T13:59:57Z

/close 
Nice gain especially for the e2e tests, thank you 👍  

Still, keeping the build time under control needs to be an ongoing effort, so if need ideas pop up never hesitate to open the PR or Issue towards that goal.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-09T14:00:03Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7200#issuecomment-3729024728):

>/close 
>Nice gain especially for the e2e tests, thank you 👍  
>
>Still, keeping the build time under control needs to be an ongoing effort, so if need ideas pop up never hesitate to open the PR or Issue towards that goal.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
