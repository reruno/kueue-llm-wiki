# Issue #9402: Provide a way to configure PrioritySortingWithinCohort without relying on feature gates

**Summary**: Provide a way to configure PrioritySortingWithinCohort without relying on feature gates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9402

**Last updated**: 2026-05-26T16:48:05Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-02-20T16:02:47Z
- **Updated**: 2026-05-26T16:48:05Z
- **Closed**: —
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Based on the below thread, there is still need to disable this feature in some cases.

This blocks the graduation of this feature and highlights the need for a toggle for controlling this behavior.

This work will allow us to remove this feature gate and rely on permanent control of this feature without having to leave the feature gate in the code base.
**Why is this needed**:
https://github.com/kubernetes-sigs/kueue/pull/9259#issuecomment-3929577504
**Completion requirements**:

I don't know if this needs a KEP as I'm not that well versed in this area. But with an API change we probably do want documentation updates and maybe a sketch of the approach in this issue. I'll leave the KEP decision to @mimowo and @tenzen-y though.

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-20T16:04:35Z

cc @amy

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-20T16:06:08Z

I see @tenzen-y already added this as a topic for wg-batch, Feb 26th, let's discuss then. I'm ok either with dropping the FG, or replacing with ConfigMap API. I agree it is anit-pattern to maintain feature gates forever.

cc @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-20T18:55:06Z

@amy, could you tell us if your use case can be satisfied by the cluster-scope PrioritySortingWithinCohort knob (Configuration API) or not?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-21T19:31:41Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2026-05-26T15:00:23Z

/remove-lifecycle stale

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-26T15:00:26Z

@kannon92: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9402):

>/remove-lifecycle stale
>
>/help
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@atosatto](https://github.com/atosatto) — 2026-05-26T15:07:41Z

Is there anywhere a list of use-cases around how to make this configurable? e.g. are we thinking about a global setting or do we have use-cases for which this should be configurable at the Cohort level?

cc @Amy  / @kannon92

### Comment by [@amy](https://github.com/amy) — 2026-05-26T16:48:05Z

cc/ @varunsyal @rajatphull ^ PTAL and offer guidance for this issue
