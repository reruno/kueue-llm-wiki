# Issue #6854: JobFramework Interface for Copying Workload Status to Job Status

**Summary**: JobFramework Interface for Copying Workload Status to Job Status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6854

**Last updated**: 2026-04-02T22:42:21Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-09-16T11:38:14Z
- **Updated**: 2026-04-02T22:42:21Z
- **Closed**: 2026-04-02T22:42:20Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What would you like to be added**:

Add a new optional interface `JobWithWorkloadStatusCopy` to the jobframework that allows job implementations to copy specific fields from the associated workload status to the job status. This interface would enable job frameworks to expose queue state and workload conditions through the job object, making Kueue's internal state visible to end users without requiring them to understand workload objects.

The interface should support:
1. **Selective field copying**: Allow jobs to specify which workload status fields to copy
2. **Condition mapping**: Map workload conditions to job conditions with customizable names and reasons
3. **Status field mapping**: Copy specific workload status fields (like admission info, queue state) to job status
4. **Custom transformation**: Allow custom logic for transforming workload status data before copying to job status

**Why is this needed**:

Currently, Kueue's queue state and workload conditions are only visible through the Workload object, which is an implementation detail that end users not always need to understand. This creates several problems:

1. **Suboptimal user experience**: Users must query workload objects to understand why their jobs are pending, queued, or failed
2. **Implementation leakage**: Kueue's internal concepts (workloads, cluster queues) are exposed to end users
3. **Limited observability**: Users can't easily monitor job queue state through standard job status fields

This feature would enable scenarios like:
- A custom job framework showing "Queued" status when its workload is pending admission
- A custom job framework displaying "Waiting for resources" when the workload is waiting for quota
- A custom job framework exposing admission check status through job conditions

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-16T13:56:18Z

+1 on this. We onboarded a large build platform via Kueue. People are checking the tekton pipelines and events to get information about why their job is queued. Many are not aware of Kueue's workloads and ideally they can just monitor the pipeline rather than need to view the workload.

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-09-30T05:36:20Z

@mimowo @tenzen-y any thoughts about this feature?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-03T21:34:28Z

cc @mimowo @tenzen-y 

This came up again in some calls. WDYT of this?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-01T21:55:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-03T22:22:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-02T22:42:14Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-02T22:42:21Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6854#issuecomment-4180857311):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
