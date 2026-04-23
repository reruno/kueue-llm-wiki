# Issue #4180: TAS: Exclude unschedulable nodes from scheduling

**Summary**: TAS: Exclude unschedulable nodes from scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4180

**Last updated**: 2025-02-10T15:27:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-09T16:01:41Z
- **Updated**: 2025-02-10T15:27:59Z
- **Closed**: 2025-02-10T15:27:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to exclude unschedulable (`.spec.unschedulable`=`true`) nodes from scheduling.
The cluster admin can manually mark nodes as unschedulable with `kubectl drain ${NODE_NAME}` or `kubectl cordon ${NODE_NAME}` and so on.

https://kubernetes.io/docs/concepts/architecture/nodes/#manual-node-administration

This can be implementable in node client indexer and used in https://github.com/kubernetes-sigs/kueue/blob/f06389aff1d714e3804743deecba5edbcd1a4d25/pkg/cache/tas_flavor.go#L95

**Why is this needed**:
The kube-scheduler can not schedule any NEW Pods to unschedulable nodes. 

> Marking a node as unschedulable prevents the scheduler from placing new pods onto that Node but does not affect existing Pods on the Node. This is useful as a preparatory step before a node reboot or other maintenance.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-09T16:02:00Z

/assign
/cc @mimowo @gabesaba @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-10T15:17:19Z

/remove-kind feature
/kind bug
