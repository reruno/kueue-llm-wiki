# Issue #6416: LocalQueue controller logs ClusterQueues

**Summary**: LocalQueue controller logs ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6416

**Last updated**: 2025-08-05T13:25:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-08-04T10:01:28Z
- **Updated**: 2025-08-05T13:25:40Z
- **Closed**: 2025-08-05T13:25:40Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In the logs of LocalQueue controller there are not only LocalQueues but also ClusterQueues 

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
E.g. see the AFS tests:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6400/pull-kueue-test-integration-baseline-main/1952288809257275392

```2025-08-04T08:55:16.610360678Z	LEVEL(-2)	core/localqueue_controller.go:152	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-q5vjw", "name": "cq1", "reconcileID": "7e5c06f6-7e33-4669-90e4-e34e0f822672"}```


**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T12:15:58Z

I've found the reason of that, and it's detail that comes from FS integration tests only. I'll create a PR to fix it
