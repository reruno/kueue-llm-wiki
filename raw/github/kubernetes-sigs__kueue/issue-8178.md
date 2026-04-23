# Issue #8178: [TAS] Investigate LeastFreeCapacity algorithm for TAS podset groups

**Summary**: [TAS] Investigate LeastFreeCapacity algorithm for TAS podset groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8178

**Last updated**: 2026-01-14T09:09:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-12-11T09:36:34Z
- **Updated**: 2026-01-14T09:09:36Z
- **Closed**: 2026-01-14T09:09:36Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
During static analysis, I've encountered piece of code that I think may lead to undesired behavior of LeastFreeCapacity algorithm when using podset groups. When using LeastFreeCapacity In `sortedDomainsWithLeader` function we don't sort ascending by the `stateWithLeader` field which I believe we should:

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L1308-L1319

This need confirmation and then unit tests to ensure it wai.  

**What you expected to happen**:

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T09:39:45Z

+1, the context from me is that we suppose the "unconstrained" mode does not work well for LWS as this code https://github.com/kubernetes-sigs/kueue/blob/c5063426e936c2f53a1c398344d49e804c01938a/pkg/cache/scheduler/tas_flavor_snapshot.go#L1317-L1319 lacks the check for "LeastFreeCapacity" (used by "unconstrained") as done above: 
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L1309-L1313

So likely when using LWS with "unconstrained" the domains are selected from those which can accomodate most workers, while correctly we should start from domains which can accomodate least workers.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T09:40:24Z

cc @mszadkow @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-12T08:53:34Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:37:03Z

/priority important-soon
