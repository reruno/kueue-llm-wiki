# Issue #674: Flaky test: Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Summary**: Flaky test: Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/674

**Last updated**: 2023-04-06T13:51:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-04-04T21:41:37Z
- **Updated**: 2023-04-06T13:51:50Z
- **Closed**: 2023-04-06T13:51:50Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@mcariatm](https://github.com/mcariatm)
- **Comments**: 3

## Description

**What happened**:

This integration test failed in a PR:

```
Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue
```

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/668/pull-kueue-test-integration-main/1643274100497453056

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-05T12:04:44Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-05T13:28:54Z

Failed again https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/664/pull-kueue-test-integration-main/1643603739438747648

in #664

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-05T13:29:14Z

/priority important-soon
