# Issue #3480: TAS: Add e2e test Job which will have larger strcuture (multiple blocks and racks)

**Summary**: TAS: Add e2e test Job which will have larger strcuture (multiple blocks and racks)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3480

**Last updated**: 2024-11-15T09:58:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-07T12:19:37Z
- **Updated**: 2024-11-15T09:58:54Z
- **Closed**: 2024-11-15T09:58:54Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

**What would you like to be added**:

Currently we only have a sanity e2e tests for TAS using a single node. 
Also, we should use JobSet & Job, as JobSet let's us have multiple pods.

For the started I think we can have 4 nodes: 2 blocks divided into 2 racks each, two nodes per rack.

I think we can have another job on test-infra for that, analogous as we do for multikueue.

**Why is this needed**:

With the current sanity tests we cannot test more complex scenarios. 
This is particularly important as users start report issues: https://github.com/kubernetes-sigs/kueue/issues/3211#issuecomment-2458900114

This is a follow up discussed under: https://github.com/kubernetes-sigs/kueue/pull/3284
and captured in the [spreadsheet](https://docs.google.com/spreadsheets/d/1MXCjKZtAfqBTb61bJo46u7jIUqRIlu1NrYj1L8Xz-UU/edit?resourcekey=0-gr1ML2A1Axi8s6Lxr-Zhlw&gid=0#gid=0)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T12:19:58Z

/assign @mszadkow 
tentatively
/cc @mbobrovskyi @tenzen-y

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-11-08T09:05:01Z

I assume all of the nodes are part of 1 cluster.
There other options to consider, but I don't think it's the matter of this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T09:11:15Z

Yes, one cluster
