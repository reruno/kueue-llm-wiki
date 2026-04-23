# Issue #3662: TAS: Use ResourceFlavorWrapper and TopologyWrapper for testing

**Summary**: TAS: Use ResourceFlavorWrapper and TopologyWrapper for testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3662

**Last updated**: 2024-12-11T08:48:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-27T08:22:37Z
- **Updated**: 2024-12-11T08:48:05Z
- **Closed**: 2024-12-11T08:48:05Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 8

## Description

**What would you like to be cleaned**:

Use the wrappers to setup objects for TAS testing.

**Why is this needed**:

To make the code more consistent (as we use this strategy for other tests), and the shorter.

Example lengthy code: [here](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/pkg/scheduler/scheduler_test.go#L4060-L4114).
See below the code for setting up ClusterQueue [here](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/pkg/scheduler/scheduler_test.go#L4115-L4119)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T08:22:48Z

cc @mbobrovskyi @kaisoz @tenzen-y

### Comment by [@mykysha](https://github.com/mykysha) — 2024-12-02T10:40:34Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-03T13:13:12Z

Can we add a default Topologies to be used in tests? E.g.
- `oneLevelTopology` - contains block label
- `twoLevelsTopology` - contains block and rack lables
- `threeLevelsTopology` - contains block, rack and hostname labels

And use it across the whole codebase as this is something that is often repeated?

/cc @mykysha @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T08:50:44Z

I'm good with that, but we can follow up on this separately (at least as separate PR, might be the same issue).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T09:00:12Z

One small follow up idea to improve the verbosity of creating topology: https://github.com/kubernetes-sigs/kueue/pull/3719#issuecomment-2516596274.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T09:01:56Z

@PBundyra where would you declare the topologies? would they be created maybe by functions like "MakeThreeLevelTopology", or new functions say "MakeTopology().ThreeLevels"?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-04T09:08:18Z

/reopen

For follow ups

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-04T09:08:23Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3662#issuecomment-2516630387):

>/reopen
>
>For follow ups


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
