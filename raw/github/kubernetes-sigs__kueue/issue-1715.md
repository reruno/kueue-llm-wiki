# Issue #1715: Cherry-picker should copy release notes

**Summary**: Cherry-picker should copy release notes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1715

**Last updated**: 2024-07-13T17:38:32Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-09T16:14:55Z
- **Updated**: 2024-07-13T17:38:32Z
- **Closed**: 2024-07-13T17:38:30Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Copy release notes into the cherry-pick PR.

**Why is this needed**:

To simplify the release process.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-09T16:15:04Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-02-12T10:39:10Z

@alculquicondor  in the recent generated PRs , with the exception of #1704 case in which the source PR  #1666 where the description has no `release-note` block,  the release notes are copied. Am I missing something?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T13:34:00Z

I copied them manually

### Comment by [@trasc](https://github.com/trasc) — 2024-02-12T13:40:48Z

> I copied them manually

It's strange, the implementation is in-place https://github.com/kubernetes/test-infra/blob/6d0a63230e80cf0138f83a65086f12d441756eb3/prow/external-plugins/cherrypicker/server.go#L46.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T14:02:56Z

uhm... then maybe it was only for the cherry-picks done with the script in `/hacks`

### Comment by [@trasc](https://github.com/trasc) — 2024-02-12T14:30:48Z

That one has indeed an hard-coded empty release note.

https://github.com/kubernetes-sigs/kueue/blob/4c1c6d67a3344fff3512d76b46c70aaac0bae2f5/hack/cherry_pick_pull.sh#L147-L149

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T20:51:12Z

Uhm... this code seems to point out that it indeed looks at parent PRs https://github.com/kubernetes/release/blob/355b4aad5b3593b7aa0764fe5b166660bfbdd686/pkg/notes/notes.go#L1048

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T20:54:23Z

I'll pay some attention next time I do a release to understand what I was doing wrong.

/unassign trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T14:09:13Z

/assign trasc
Based on comments in https://github.com/kubernetes/test-infra/issues/31929

### Comment by [@trasc](https://github.com/trasc) — 2024-02-14T16:31:08Z

With kubernetes/release#3468 the defaulting to the original PR's release note if not present in the current one should work for both cherry-pick methods (bit an hack script) regardless of merge method used.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-14T16:53:33Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-13T17:18:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-13T17:38:27Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-13T17:38:31Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1715#issuecomment-2227005511):

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
