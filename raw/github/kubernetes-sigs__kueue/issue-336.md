# Issue #336: Add a User Agent

**Summary**: Add a User Agent

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/336

**Last updated**: 2022-08-17T21:08:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-16T20:02:11Z
- **Updated**: 2022-08-17T21:08:48Z
- **Closed**: 2022-08-17T21:08:48Z
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 3

## Description

**What would you like to be added**:

It should like this:

```
kueue-manager/v0.2.0 (linux/amd64)
```

The version should be fed using ldflags https://www.digitalocean.com/community/tutorials/using-ldflags-to-set-version-information-for-go-applications

**Why is this needed**:

For proper logging in apiserver.

Also, the first part of the user agent (kueue-manager) would be added as a Manager when using ServerSideApply.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-16T20:02:17Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-16T20:02:18Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/336):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-17T19:04:03Z

/help cancel
/assign
