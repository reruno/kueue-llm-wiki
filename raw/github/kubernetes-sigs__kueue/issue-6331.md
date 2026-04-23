# Issue #6331: [ProvReq] Clean up integration tests

**Summary**: [ProvReq] Clean up integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6331

**Last updated**: 2026-03-05T12:08:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-07-31T15:05:41Z
- **Updated**: 2026-03-05T12:08:14Z
- **Closed**: 2026-03-05T12:08:13Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I'd like the provisioning request integration tests to be cleaned up:
- use wrappers
- double check if there are any redundant fields/variables
- double check the suite description if it's align with what the test actually does
- double check if any parts of the tests could be commonized

**Why is this needed**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:17:34Z

As mentioned under https://github.com/kubernetes-sigs/kueue/pull/6408#discussion_r2251649819 I think it would be great to introduce helpers as `ExpectAdmissionCheck` and `HasEventAppeared`.

They would work towards the direct goal of this issue, and be helpful for other suites.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-05T08:30:03Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T08:31:59Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-03T09:16:42Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T09:22:32Z

cc @PBundyra @kshalot ptal, maybe we could already close, because there was many improvement PRs, some of them didn't reference the Issue, so maybe all the points are already addressed

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-03T10:30:18Z

> As mentioned under [#6408 (comment)](https://github.com/kubernetes-sigs/kueue/pull/6408#discussion_r2251649819) I think it would be great to introduce helpers as `ExpectAdmissionCheck` and `HasEventAppeared`.
> 
> They would work towards the direct goal of this issue, and be helpful for other suites.

@mimowo

From my POV:
* "use wrappers":
    * addressed in #6369
* "double check if there are any redundant fields/variables":
    * I'm not sure if it was explicitly addressed. I glanced at the code and it might not be an issue, but I may be wrong.
    * cc @PBundyra 
* "double check the suite description if it's align with what the test actually does":
    * I'm not sure about that one. If "suite description" means the "ginkgo.Describe" block then maybe it's a non issue.
    * cc @PBundyra 
* "double check if any parts of the tests could be commonized":
    * I looked at #7021 and it seems it is still not addressed, i.e. `ExpectAdmissionCheckState` is not delivered. There are some helpers like `ExpectAdmissionChecksToBeActive` but they are not used in the provisioning test.

I CC'd @PBundyra in the two places where he might have more context (I don't remember how this test looked in the past so it's hard to judge).

From my POV, the "double check if any parts of the tests could be commonized" issue is not addressed, but IMO we could close this issue and use #7021 to track it instead.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T10:53:20Z

Oh I think this PR addresses the issue largely: https://github.com/kubernetes-sigs/kueue/pull/7266/, I somehow missed, could you please complete the reviewing there. It looks quite reasonable.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-05T11:50:40Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T12:06:34Z

/remove-lifecycle rotten
To track the remaining effort in https://github.com/kubernetes-sigs/kueue/pull/7266

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T12:08:07Z

/close
https://github.com/kubernetes-sigs/kueue/pull/7266 is already tracked by the more scoped issue https://github.com/kubernetes-sigs/kueue/issues/7021

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-05T12:08:13Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6331#issuecomment-4004605978):

>/close
>https://github.com/kubernetes-sigs/kueue/pull/7266 is already tracked by the more scoped issue https://github.com/kubernetes-sigs/kueue/issues/7021
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
