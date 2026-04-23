# Issue #5712: [TAS] Limit number of retries for finding replacement for a failed node

**Summary**: [TAS] Limit number of retries for finding replacement for a failed node

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5712

**Last updated**: 2025-07-16T07:01:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-06-23T09:36:11Z
- **Updated**: 2025-07-16T07:01:30Z
- **Closed**: 2025-07-16T07:01:29Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
With TAS and `TASFailedNodeReplacement` feature if a node fails, Kueue looks for a replacement so the Workload can continue to run. Currently, Kueue looks for the replacement indefinitely and I'd like to add API that would limit the number of retries and evict the Workload after no replacement was found.

**Why is this needed**:
 Right now users can WaitForPodsReady for the similar functionality but, if no replacement is even possible for certain topologies, it wastes the resource. We would like to have a quicker feedback loop, e.g. try to find replacement once and evict Workload if didn't find


**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-07-15T13:40:13Z

Hello @PBundyra, is this feature something you are taking a look at? If not, can I try to help with it? Thanks

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T06:33:45Z

@MaysaMacedo Patryk is ooo till EOW. The issue is not assigned, but maybe it is getting addressed with  https://github.com/kubernetes-sigs/kueue/pull/5861 as the PR seems to match the description, but I'm not 100% sure.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T06:34:49Z

Maybe in the meanwhile @pajakd knows if this issue is covered with the current work-in-progress.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-07-16T06:50:26Z

yes, the issue is addressed with #5861

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T07:01:24Z

/close

Let me close it tentatively, because it looks addressed, to avoid confusion. We can re-open when Patryk is back and see there is more work here.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-16T07:01:30Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5712#issuecomment-3077183411):

>/close
>
>Let me close it tentatively, because it looks addressed, to avoid confusion. We can re-open when Patryk is back and see there is more work here.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
