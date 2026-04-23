# Issue #5939: Kubernetes compatibility table

**Summary**: Kubernetes compatibility table

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5939

**Last updated**: 2025-12-08T14:46:36Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@zhwentao](https://github.com/zhwentao)
- **Created**: 2025-07-11T06:34:42Z
- **Updated**: 2025-12-08T14:46:36Z
- **Closed**: 2025-12-08T14:46:36Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->

Hello，Does there any docs describe the Kubernetes compatibility of kueue？

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-11T13:43:14Z

Currently, we support v1.29 as a minimum version as described in https://kueue.sigs.k8s.io/docs/installation/#before-you-begin.

Basically, we support versions that upstream Kubernetes supports

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-11T13:52:53Z

Yes, currently all versions supported in Kubernetes are fully supported by Kueue.

Maybe one corner case is the JobManagedBy feature for MultiKueue, because it is enabled in kubernetes 1.32+ and is required for live Job status updates. 

Does it answer your question?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-09T14:08:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-08T14:14:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-08T14:46:31Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-08T14:46:36Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5939#issuecomment-3627279175):

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
