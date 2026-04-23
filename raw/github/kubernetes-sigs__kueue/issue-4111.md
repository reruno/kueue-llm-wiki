# Issue #4111: Increase log level for Kubernetes components

**Summary**: Increase log level for Kubernetes components

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4111

**Last updated**: 2025-02-03T08:47:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-30T15:35:36Z
- **Updated**: 2025-02-03T08:47:00Z
- **Closed**: 2025-02-03T08:46:59Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What would you like to be added**:

Increasing log-level for Kubernetes componets (including Kubelet) to V(3).

The effort is started in PR: https://github.com/kubernetes-sigs/kueue/pull/4095

**Why is this needed**:

Having more logs from K8s components could be helpful for investigations of flakes as discussed in https://github.com/kubernetes-sigs/kueue/issues/4056#issuecomment-2621145423. 

I also think that with tighter integration between kueue and kubernetes (like in TAS) the logs will be helpful to investigate some rare failures.

Also, any additional logs will be helpful for complex features like MultiKueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T15:36:00Z

/remove-kind feature
/kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T15:36:16Z

cc @mbobrovskyi @PBundyra
