# Issue #5: Add info to Queue status

**Summary**: Add info to Queue status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5

**Last updated**: 2022-03-14T13:56:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-17T22:10:03Z
- **Updated**: 2022-03-14T13:56:19Z
- **Closed**: 2022-03-14T13:56:18Z
- **Labels**: `kind/feature`, `priority/important-soon`, `size/M`
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 9

## Description

Suggestions:
- Number of pending jobs
- Number of started jobs
- Resources currently used by the queue.

/kind feature

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-18T13:46:52Z

/size M
/priority important-soon

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-21T21:02:44Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T15:25:14Z

The way we can do this is using the regular reconciler pattern in `pkg/controller/core`. The internal work queue would allow us to potentially do less API calls than the events we receive.

Implementation-wise, you just need to return `true` from the event handlers, so that the reconciler starts being called.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T16:49:54Z

Target:

- [x] Number of pending jobs
- [ ] Number of assigned jobs
- [ ] Resources currently used by the queue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T16:57:12Z

s/started/assigned

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-11T12:35:22Z

I think after https://github.com/kubernetes-sigs/kueue/pull/114, we can close this , now that `AdmittedWorkloads` will be tracked at the ClusterQueue lvl for now

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-11T20:48:25Z

Now that #114 is merged, I think we can close this issue

Thoughts otherwise? (@alculquicondor @ahg-g )

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-14T13:56:07Z

We could still add the others, but maybe it will make more sense when there is support for Queue limits

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-14T13:56:19Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5#issuecomment-1066824365):

>We could still add the others, but maybe it will make more sense when there is support for Queue limits
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
