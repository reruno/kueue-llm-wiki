# Issue #3363: [kjobctl] Make the output of the "describe job" command a viable yaml

**Summary**: [kjobctl] Make the output of the "describe job" command a viable yaml

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3363

**Last updated**: 2024-11-12T12:49:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@BluValor](https://github.com/BluValor)
- **Created**: 2024-10-29T15:47:56Z
- **Updated**: 2024-11-12T12:49:59Z
- **Closed**: 2024-11-12T12:49:57Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Make the output of the "describe job" command a viable yaml (parsable while maintaining the same intended structure).

**Why is this needed**:
The output of this command is currently human readable but cannot be used with scripts easily. 

**Completion requirements**:
The output of the "describe job" command should be parsable by yaml. The listings should be parsed properly.
It would also be fine it this option is hidden under a flag (like "-o yaml").

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T15:50:19Z

Did you try `kjobctl list job name -o yaml`?

### Comment by [@BluValor](https://github.com/BluValor) — 2024-10-29T15:58:33Z

> Did you try `kjobctl list job name -o yaml`?

Haven't found this one, thank you. :)

It would still be nice to have this option for the "describe job", but it seems this will be enough for my use case.

Feel free to close this issue as resolved.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T16:02:06Z

We are aiming to make `kjobctl` as similar to `kubectl` as possible. Note that `kubectl describe` does not support the `-o yaml` option.

cc: @mimowo @mwysokin

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-12T12:49:53Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-12T12:49:58Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3363#issuecomment-2470449496):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
