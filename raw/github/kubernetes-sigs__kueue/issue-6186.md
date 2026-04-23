# Issue #6186: MK Dispatcher: Test for possible race condition on AC and ClusterName set

**Summary**: MK Dispatcher: Test for possible race condition on AC and ClusterName set

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6186

**Last updated**: 2025-12-17T10:24:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2025-07-25T13:12:16Z
- **Updated**: 2025-12-17T10:24:31Z
- **Closed**: 2025-12-17T10:24:30Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

As mentioned [here](https://github.com/kubernetes-sigs/kueue/pull/5782#discussion_r2230404869)
We need to test and possibly fix the race condition that could happen:

>  when the nominatedClusterNames is changed preventing setting clusterName, but not preventing setting AC as Ready, and admitting the workload

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T13:26:30Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-22T14:25:17Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T10:24:25Z

/close
To avoid distractions. The code has evolved a lot since then, and I'm not even sure I was right back then. I can see currently we set the AC=Ready and the status.clusterName in the same request, so I don't expect a race here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/multikueue/workload.go#L639-L648

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-17T10:24:31Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6186#issuecomment-3664680340):

>/close
>To avoid distractions. The code has evolved a lot since then, and I'm not even sure I was right back then. I can see currently we set the AC=Ready and the status.clusterName in the same request, so I don't expect a race here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/multikueue/workload.go#L639-L648


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
