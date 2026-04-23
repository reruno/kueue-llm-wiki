# Issue #6681: kueue label should be set in template not metadata.labels in the deployment integration doc

**Summary**: kueue label should be set in template not metadata.labels in the deployment integration doc

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6681

**Last updated**: 2026-01-08T08:00:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Ruixuan](https://github.com/Ruixuan)
- **Created**: 2025-08-27T19:57:42Z
- **Updated**: 2026-01-08T08:00:47Z
- **Closed**: 2026-01-08T08:00:46Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

something like this will work (the one in the doc won't)

template:
    metadata:
      labels:
        kueue.x-k8s.io/queue-name: test-queue

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T06:39:16Z

@Ruixuan would you like to point the doc page, and submit a PR fixing the issue?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-09T07:06:32Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-08T07:55:02Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T08:00:40Z

/close
I think the issue was opened against some old version of Kueue before setting queue-name label was supported at the Deployment level. Currently it is supported as shown by the e2e test: https://github.com/kubernetes-sigs/kueue/blob/ddfc8bfd09cec30665038862ba687d218ae63cc6/test/e2e/singlecluster/deployment_test.go#L173

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-08T08:00:46Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6681#issuecomment-3722595727):

>/close
>I think the issue was opened against some old version of Kueue before setting queue-name label was supported at the Deployment level. Currently it is supported as shown by the e2e test: https://github.com/kubernetes-sigs/kueue/blob/ddfc8bfd09cec30665038862ba687d218ae63cc6/test/e2e/singlecluster/deployment_test.go#L173


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
