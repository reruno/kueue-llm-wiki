# Issue #234: Trigger the movement of workload in ClusterQueue by ns event

**Summary**: Trigger the movement of workload in ClusterQueue by ns event

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/234

**Last updated**: 2022-07-18T18:25:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@denkensk](https://github.com/denkensk)
- **Created**: 2022-04-29T04:11:34Z
- **Updated**: 2022-07-18T18:25:16Z
- **Closed**: 2022-07-18T18:25:16Z
- **Labels**: `kind/bug`, `kind/feature`, `priority/critical-urgent`
- **Assignees**: [@denkensk](https://github.com/denkensk), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Watch the event of ns and trigger the movement of workload in ClusterQueue with BestFIFO.

**Why is this needed**:
https://github.com/kubernetes-sigs/kueue/pull/227#discussion_r854973997_

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-30T20:33:05Z

/kind bug

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-30T20:33:33Z

@ahg-g: The label(s) `priority/important-critical` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/234#issuecomment-1114049898):

>/priority important-critical
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-02T13:39:54Z

/priority critical-urgent

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-02T23:02:22Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-03T01:04:46Z

Actually @denkensk do you want to take this one?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-05-03T01:10:06Z

Yes, you can assign it to me.  @ahg-g

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-03T02:32:59Z

/assign @denkensk

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-03T02:33:10Z

/unassign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-15T10:56:02Z

@denkensk any progress on this one?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-06-15T12:28:08Z

> @denkensk any progress on this one?

@ahg-g  Sorry. I didn't have enough time last month. Will continue working on this this week.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-15T14:27:20Z

/assign
