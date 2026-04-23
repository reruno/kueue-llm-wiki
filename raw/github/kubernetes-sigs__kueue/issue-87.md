# Issue #87: Introduce a single heap for per ClusterQueue

**Summary**: Introduce a single heap for per ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/87

**Last updated**: 2022-03-10T19:35:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-02T18:56:29Z
- **Updated**: 2022-03-10T19:35:20Z
- **Closed**: 2022-03-10T17:39:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 4

## Description

To prevent users from hijacking a Capacity by creating multiple Queues, we should have a single heap for a Capacity (spin off from https://github.com/kubernetes-sigs/kueue/pull/80#issuecomment-1057015439)

/kind feature

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:56:34Z

/assign

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-08T01:34:24Z

/retitle  Introduce a single heap for per ClusterQueue

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T19:25:47Z

Maybe I am confused but after this issue is closed, what is left for kueue.queue to hold? 

is just a pointer to ClusterQueue , now that the head moved from Queue to Cluster Queue I don't see a point on having a Queue controller

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T19:35:20Z

https://github.com/kubernetes-sigs/kueue/pull/80#issuecomment-1055570571
