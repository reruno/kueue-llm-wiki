# Issue #4403: Execution was mistyped as Exexcution

**Summary**: Execution was mistyped as Exexcution

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4403

**Last updated**: 2025-02-27T17:27:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@arueth](https://github.com/arueth)
- **Created**: 2025-02-25T20:44:19Z
- **Updated**: 2025-02-27T17:27:24Z
- **Closed**: 2025-02-25T20:48:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

It looks like the word execution was mistyped as Exexcution:
https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20Exexcution&type=code

**Why is this needed**:

It breaks spell checkers.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T20:48:05Z

Yeah we observed that, but we can not fix it since fixing typo break backward compatibility, which means existing Workloads are broken in the cluster.

https://github.com/kubernetes-sigs/kueue/pull/4297

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T20:48:11Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-25T20:48:16Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4403#issuecomment-2683250228):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@arueth](https://github.com/arueth) — 2025-02-27T17:14:00Z

It might be worth implementing a spell check action to prevent this in the future. I've noticed there are a number of misspellings throughout the repo.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-27T17:27:22Z

> It might be worth implementing a spell check action to prevent this in the future. I've noticed there are a number of misspellings throughout the repo.

I agree with you. Do you have a recommended misspelling check tool?
If yes, could you open a separate issue? I am happy with the tool introducing PR.
