# Issue #2416: JobSet fails to create when MultiKueue enabled and ClusterQueue does not exist

**Summary**: JobSet fails to create when MultiKueue enabled and ClusterQueue does not exist

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2416

**Last updated**: 2024-06-17T16:10:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-06-17T08:33:12Z
- **Updated**: 2024-06-17T16:10:35Z
- **Closed**: 2024-06-17T16:10:35Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

**What happened**:

When MultiKueue is enabled, and clusterQueue does not exist, then the JobSet creation is rejected. 
This is inconsistent with other Job CRDs.

**What you expected to happen**:

The JobSet gets created.

**How to reproduce it (as minimally and precisely as possible)**:

0: Install JobSet and Kueue
1. Enable the MultiKueue feature gate.
2. Create a LocalQueue, but without Cluster Queue
3. Create a JobSet pointing to the Local Queue
Issue: JobSet creation fails with error similar to this:

`Error from server (Forbidden): error when creating "jobset.yaml": admission webhook "mjobset.kb.io" denied the request: queue doesn't exist`

**Anything else we need to know?**:

Here is the [code](https://github.com/kubernetes-sigs/kueue/blob/8b217c67c6cfb2a588a90107a63d3cf19182b191/pkg/controller/jobs/jobset/jobset_webhook.go#L78). It should not fail when the cluster queue does not exist.

Tested on Kueue 0.7.0. It has been noticed when working on https://github.com/kubernetes-sigs/kueue/pull/2401

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-17T08:33:32Z

/assign @vladikkuzn
