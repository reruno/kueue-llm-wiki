# Issue #8637: MultiKueue: Implement marker-based validation and defaulting tests

**Summary**: MultiKueue: Implement marker-based validation and defaulting tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8637

**Last updated**: 2026-02-16T10:49:45Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-16T14:51:41Z
- **Updated**: 2026-02-16T10:49:45Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I'd propose adding tests for [MultiKueueCluster](https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/apis/kueue/v1beta2/multikueue_types.go#L113) and [MultiKueueConfig](https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/apis/kueue/v1beta2/multikueue_types.go#L156) to verify marker-based validations and defaultings.

Contributors can learn how to implement those by existing cases like https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/test/integration/singlecluster/webhook/core/cohort_test.go#L43

**Why is this needed**:

Stabilize the MultiKueue validation mechanism.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T14:53:20Z

I think that the possible place is https://github.com/kubernetes-sigs/kueue/tree/3250572ddbdc351dc27f73f70b713822abed1cc5/test/integration/singlecluster/webhook/core for  multikueue_config_test.go and multikueue_cluster_test.go.

@mimowo @gabesaba Any preference?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T15:56:35Z

> I think that the possible place is https://github.com/kubernetes-sigs/kueue/tree/3250572ddbdc351dc27f73f70b713822abed1cc5/test/integration/singlecluster/webhook/core for multikueue_config_test.go and multikueue_cluster_test.go.

This seems reasonable, this is where we also test some limits on the ClusterQueues eg. https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/test/integration/singlecluster/webhook/core/clusterqueue_test.go#L264-L274

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T16:09:36Z

> This seems reasonable, this is where we also test some limits on the ClusterQueues eg.

SGTM, thank you for double-checking those.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:24:43Z

/priority important-longterm

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:49:43Z

/area multikueue
