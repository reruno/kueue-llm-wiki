# Issue #5186: Add some tests to prevent corrupted CRD versioning in helm templates

**Summary**: Add some tests to prevent corrupted CRD versioning in helm templates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5186

**Last updated**: 2026-03-06T13:34:47Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-07T11:17:20Z
- **Updated**: 2026-03-06T13:34:47Z
- **Closed**: 2026-03-06T13:34:46Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Some form of validation for the generated CRD yamls to prevent issues like https://github.com/kubernetes-sigs/kueue/issues/4850 in the future.

**Why is this needed**:

This type of error is hard to detect manually during review, because the yamls are auto-generated and rarely checked carefully.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-07T11:17:38Z

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-07T11:22:47Z

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T06:57:59Z

Thinking a bit more about this, and this is an example of a helm chart which is correct in terms of syntax, but does not work well, because for Alpha version it mentions also beta , like [here](https://github.com/kubernetes-sigs/kueue/pull/4866/files#diff-0120068b6058269b1aa9ae2f091e3023cc058c824af9eaeaec31bc8a49283f67L97). I see two options
1. a dedicated rule in the Makefile to verify the generated Yaml 
2. e2e test for Kueue installed form helm, say `helm-e2e`, analogous to customconfigs-e2e

(2.) could be covered as part of https://github.com/kubernetes-sigs/kueue/issues/5145.

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T07:02:39Z

/retitle Add some tests to prevent corrupted CRD versioning in helm templates

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T10:30:51Z

I agree with having tests against generated CRD YAML files.
However, I don't think it is related to Helm.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-07T11:24:50Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-07T11:57:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T12:28:06Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T13:24:11Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-04T13:27:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-06T13:34:41Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-06T13:34:47Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5186#issuecomment-4011793064):

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
