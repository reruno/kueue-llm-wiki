# Issue #1258: Some integration tests don't set all indexes

**Summary**: Some integration tests don't set all indexes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1258

**Last updated**: 2023-10-26T11:47:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-25T19:50:20Z
- **Updated**: 2023-10-26T11:47:11Z
- **Closed**: 2023-10-26T11:47:11Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What happened**:

In integration tests logs, you might find the following errors:
```
Index with name field:.metadata.parentWorkload does not existUnable to list child jobs
```

```
  2023-10-25T19:42:43.924182458Z	ERROR	workload-reconciler	workload/resources.go:112	Failed adjusting requests for LimitRanges	{"workload": {"name":"pod-test-pod-9fd67","namespace":"pod-namespace-wxtrr"}, "queue": "test-queue", "status": "admitted", "clusterQueue": "cluster-queue", "error": "Index with name field:spec.hasContainerType does not exist"}
```

Although the test succeeds (probably because the test doesn't depend on these reconcilers), this pollutes the logs.

**What you expected to happen**:

No errors related to indexes

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-25T19:50:28Z

/assign @trasc
