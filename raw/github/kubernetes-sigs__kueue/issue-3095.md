# Issue #3095: [MultiKueue] Promote MultiKueue API and feature gate to Beta

**Summary**: [MultiKueue] Promote MultiKueue API and feature gate to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3095

**Last updated**: 2024-10-22T08:36:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-19T12:50:10Z
- **Updated**: 2024-10-22T08:36:25Z
- **Closed**: 2024-10-22T08:36:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 7

## Description

**What would you like to be added**:

Promote the MultiKueue API to Beta.

**Why is this needed**:

For the ease of use. 

The feature was first introduced in 0.6, and since then a bunch of issues have been fixed.

**Completion requirements**:

Issues I would like to get addressed before graduating (except from other graduation criteria mentioned in KEP):
- https://github.com/kubernetes-sigs/kueue/issues/3099
- https://github.com/kubernetes-sigs/kueue/issues/3094

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T12:51:28Z

/cc @mwielgus @tenzen-y @alculquicondor @trasc 

I think we should resolve https://github.com/kubernetes-sigs/kueue/issues/3094 before the gradution, but discussion is welcome.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T14:08:05Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T19:01:23Z

@mimowo @trasc Could we finalize https://github.com/kubernetes-sigs/kueue/pull/2458 before we graduate MK?
I am suspecting that the new functional requirements will be found by #2458.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-20T12:36:39Z

Thanks for the comment, I was thinking about it, but I think we don't need to block on it, here is the couple of thoughts I have:
- it is very unlikely we will be able to finalize [#2458](https://github.com/kubernetes-sigs/kueue/pull/2458) before end of November, given the load of other workstreams. The KEP proved to be challenging, and we need a proper design for it, which I think includes decoupling Job handling and ACs. 
- supporting external Jobs may will likely require new APIs, but I believe we can grow it later step by step, nothing in the current [API](https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1alpha1/multikueue_types.go) seems would be blocking the support
- in the past we supported built-in Jobs in Kueue (initially just batch Job) as Beta API, and only later we added Job framwork and expanded and support external Jobs. I believe we can repeat the pattern here, while already in Beta.
- we are already getting user feedback that the current API is useful for JobSet, but the setup still requires many steps

EDIT: also, the support for external Jobs isn't mentioned in the KEP, so I believe we can de-couple it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-24T15:22:20Z

I discussed this graduation with @mimowo offline.
During the discussion, we agreed that external Job support would take a long time since https://github.com/kubernetes-sigs/kueue/pull/2458 has not been finalized and is pending status.

Additionally, I guess that this graduation would be useful for collecting feedback from users, and we can reflect the feedback to the external Job support. Based on user feedback, we will prepare the second beta version to support additional features and external Jobs.

Anyway, I agree with this beta graduation, but for the GA graduation, I would like to wait for external Job support.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-22T08:36:19Z

/close 
The remaining work is tracked in separate issue https://github.com/kubernetes-sigs/kueue/issues/3094

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-22T08:36:24Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3095#issuecomment-2428628206):

>/close 
>The remaining work is tracked in separate issue https://github.com/kubernetes-sigs/kueue/issues/3094


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
