# Issue #1814: [MultiKueue] in around 30min intervals error message is logged during normal operation

**Summary**: [MultiKueue] in around 30min intervals error message is logged during normal operation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1814

**Last updated**: 2024-03-13T08:00:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-08T10:08:20Z
- **Updated**: 2024-03-13T08:00:12Z
- **Closed**: 2024-03-13T08:00:12Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

During normal operation MultiKueue logs errors repeatedly every 30min per cluster:
```
{"level":"error","ts":"2024-03-06T08:21:44.586427722Z","caller":"multikueue/multikueuecluster.go:200","msg":"Cannot get workload key","clusterName":"multikueue-test-worker2","watchKind":"jobset.x-k8s.io/v1alpha2, Kind=JobSet","jobKind":"/, Kind=","error":"not a jobset","stacktrace":"sigs.k8s.io/kueue/pkg/controller/admissionchecks/multikueue.(*remoteClient).startWatcher.func1\n\t/workspace/pkg/controller/admissionchecks/multikueue/multikueuecluster.go:200"}
```
Longer example here: https://github.com/kubernetes-sigs/kueue/pull/1806#issuecomment-1980342324.

**What you expected to happen**:

No error logs reported during normal operation.

**How to reproduce it (as minimally and precisely as possible)**:

Run MultiKueue as described in https://github.com/kubernetes-sigs/kueue/issues/1787. Tested on GKE

**Anything else we need to know?**:

This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/1787

**Environment**:
- Kubernetes version (use `kubectl version`): 1.28.3-gke.1286000
- Kueue version (use `git describe --tags --dirty --always`): master build
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-08T10:09:40Z

/assign trasc
we discussed this already and planned as a follow up, reporting for visibility
