# Issue #1466: Generate SLSA Attestations with new releases

**Summary**: Generate SLSA Attestations with new releases

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1466

**Last updated**: 2025-02-18T03:41:38Z

---

## Metadata

- **State**: open
- **Author**: [@sec-jeff](https://github.com/sec-jeff)
- **Created**: 2023-12-15T18:25:30Z
- **Updated**: 2025-02-18T03:41:38Z
- **Closed**: —
- **Labels**: `kind/feature`, `good first issue`, `help wanted`, `sig/release`
- **Assignees**: [@OMNARAYANYU](https://github.com/OMNARAYANYU)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
SLSA Attestation Generated with new releases. 

**Why is this needed**:

SLSA's are resources that show evidence that the release consumers receive has not been tampered with during the supply chain process.

**Completion requirements**:

Implementation of a tool such as https://github.com/kubernetes-sigs/tejolote into the CI process for builds. This will generate the SLSA and attach it to the release.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@sec-jeff](https://github.com/sec-jeff) — 2023-12-15T18:26:45Z

Tagging @upodroid from K8 Security Slam 2023 #SecuritySlam

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2023-12-15T21:01:32Z

/cc @puerco

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2023-12-15T21:01:45Z

/sig release

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-14T21:07:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T21:21:57Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-12T22:12:52Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T16:58:23Z

/remove-lifecycle stale
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-13T16:58:24Z

@tenzen-y: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1466):

>/remove-lifecycle stale
>/good-first-issue
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tannerjones4075](https://github.com/tannerjones4075) — 2024-06-17T16:53:30Z

I would like to help and contribute :) There is an open-source provenance tool called [Witness](https://github.com/in-toto/witness) that can generate attestations. There is a Github [action](https://github.com/marketplace/actions/witness-run) that could be implemented in the CI process. Thoughts?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-20T06:23:41Z

> I would like to help and contribute :) There is an open-source provenance tool called [Witness](https://github.com/in-toto/witness) that can generate attestations. There is a Github [action](https://github.com/marketplace/actions/witness-run) that could be implemented in the CI process. Thoughts?

Sure, feel free to take this issue with `/assign` comment.

### Comment by [@OMNARAYANYU](https://github.com/OMNARAYANYU) — 2025-02-18T03:41:37Z

/assign
