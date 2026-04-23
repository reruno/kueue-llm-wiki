# Issue #360: ☂️ Requirements for release 0.3

**Summary**: ☂️ Requirements for release 0.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/360

**Last updated**: 2023-04-06T21:29:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-26T15:07:34Z
- **Updated**: 2023-04-06T21:29:16Z
- **Closed**: 2023-04-06T21:29:14Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 8

## Description

```[tasklist]
### Tasks
- [x] https://github.com/kubernetes-sigs/kueue/issues/45
- [x] https://github.com/kubernetes-sigs/kueue/issues/83
- [x] https://github.com/kubernetes-sigs/kueue/issues/425
- [ ] https://github.com/kubernetes-sigs/kueue/issues/349
- [ ] https://github.com/kubernetes-sigs/kueue/issues/23
```









Nice to have:





```[tasklist]
### Tasks
- [ ] https://github.com/kubernetes-sigs/kueue/issues/312
- [x] https://github.com/kubernetes-sigs/kueue/issues/61
- [x] https://github.com/kubernetes-sigs/kueue/issues/45
- [ ] https://github.com/kubernetes-sigs/kueue/issues/541
```









I open the floor for further suggestions, but I think those two high level items are big enough for a release.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-26T15:10:14Z

cc @ahg-g @kerthcet @denkensk @ArangoGutierrez

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-26T16:10:58Z

Yes, that should be enough material improvements for a release.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-29T02:25:20Z

Maybe also add e2e test https://github.com/kubernetes-sigs/kueue/issues/61

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:47:21Z

we may also want to consider https://github.com/kubernetes-sigs/kueue/issues/312 because it can help with reducing chances of preemption.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T20:10:51Z

We could also consider #62, but I'm concerned that we might not have enough capacity. Preemption seems more important.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T21:42:30Z

Added #245 (as bugfix) and #349.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T21:29:10Z

/close

Thank you all for contributing!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-04-06T21:29:15Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/360#issuecomment-1499651241):

>/close
>
>Thank you all for contributing!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
