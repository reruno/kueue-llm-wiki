# Issue #7992: KueuePopulator: cleanups discovered during release

**Summary**: KueuePopulator: cleanups discovered during release

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7992

**Last updated**: 2026-04-20T06:58:22Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-28T11:06:44Z
- **Updated**: 2026-04-20T06:58:22Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 11

## Description

**What happened**:

1. Release artifacts contain test data: https://github.com/kubernetes/k8s.io/pull/8814#discussion_r2571285719
2. The image is repeated many times, please deduplicate registry.k8s.io/kubectl:v1.33.6
3. ~The hook jobs run in the "default" namespace which is not guaranteed to exist, I think we should use the kueue-system namespace to guarantee existence, and also it belongs there conceptually~

**What you expected to happen**:

Release artifacts should not contain that.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T11:06:57Z

cc @j-skiba @tenzen-y @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T11:09:08Z

Sorry, I might misunderstand that. Please correct me if this is not a valid comment.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T11:15:51Z

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T11:16:17Z

/kind  cleanup

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-28T11:16:21Z

@mimowo: The label(s) `kind/` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7992#issuecomment-3588937504):

>/kind  cleanup


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-12-01T09:26:00Z

the hook job runs in `{{ .Release.Namespace }}` namespace - https://github.com/kubernetes-sigs/kueue/blob/3a86a1d77d16df8128eff6ef5c8880ca1c98d6e2/cmd/experimental/kueue-populator/charts/kueue-populator/templates/setup-hook.yaml#L119C3-L119C38 .

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:36:07Z

Oh, you are right. I will cross it out from the points in description.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:52:13Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T11:15:52Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T06:58:20Z

/remove-lifecycle rotten
