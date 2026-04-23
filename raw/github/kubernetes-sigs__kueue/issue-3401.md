# Issue #3401: TAS: exclude non-ready nodes from scheduling

**Summary**: TAS: exclude non-ready nodes from scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3401

**Last updated**: 2024-11-04T14:45:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-31T13:05:48Z
- **Updated**: 2024-11-04T14:45:30Z
- **Closed**: 2024-11-04T14:45:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

**What would you like to be added**:

Exclude non-ready nodes from scheduling.

This can be done here: https://github.com/kubernetes-sigs/kueue/blob/355fab3a2274fb257243d1bf1cf69e914354f071/pkg/cache/tas_flavor.go#L110 based on the status condition. Only Ready=True means include in scheduling calculations. Otherwise add a log line that it is excluded.

The reference https://kubernetes.io/docs/reference/node/node-status/#condition: 
`True if the node is healthy and ready to accept pods, False if the node is not healthy and is not accepting pods, and Unknown if the node controller has not heard from the node in the last node-monitor-grace-period (default is 40 seconds)`. 

**Why is this needed**:

Non-ready nodes are excluded by kube-scheduler so including them in TAS can be considered a bug - they will not be able to use in practice, and the pods will not schedule.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T13:06:00Z

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T13:08:15Z

cc @mszadkow @mbobrovskyi

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-11-01T10:39:07Z

/assign
