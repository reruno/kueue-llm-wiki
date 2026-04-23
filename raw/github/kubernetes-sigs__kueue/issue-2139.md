# Issue #2139: [kueuectl] Add stop LocalQueue command

**Summary**: [kueuectl] Add stop LocalQueue command

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2139

**Last updated**: 2024-06-17T18:30:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-05-06T07:24:29Z
- **Updated**: 2024-06-17T18:30:55Z
- **Closed**: 2024-06-17T18:30:54Z
- **Labels**: `kind/feature`
- **Assignees**: [@rainfd](https://github.com/rainfd)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add stop LocalQueue command.

**Why is this needed**:
To stops execution (or just admission) of Workloads coming from the given LocalQueue. This requires adding StopPolicy to LocalQueue and enforcing its changes in ClusterQueue (#2109).

Design details https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#stop-localqueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@rainfd](https://github.com/rainfd) — 2024-06-03T03:51:13Z

/assign

### Comment by [@rainfd](https://github.com/rainfd) — 2024-06-03T20:08:36Z

I'm a new contributor to Kueue.  
Add StopPolicy for LocalQueue(#2109) is in processing. Should I wait for the completion before continuing? Or is this issue also in your implementation?
@mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-03T20:12:42Z

Yes, this issue blocked with #2173.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-10T15:51:14Z

Just to do not miss, #2173 merged.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-17T18:30:51Z

Done #2415

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-17T18:30:55Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2139#issuecomment-2174119951):

>Done #2415
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
