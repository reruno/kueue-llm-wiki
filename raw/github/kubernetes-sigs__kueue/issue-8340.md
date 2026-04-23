# Issue #8340: [TAS] TAS unnecessarily reacts on Nodes heartbeats

**Summary**: [TAS] TAS unnecessarily reacts on Nodes heartbeats

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8340

**Last updated**: 2025-12-19T09:06:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-12-18T17:32:56Z
- **Updated**: 2025-12-19T09:06:34Z
- **Closed**: 2025-12-19T09:06:34Z
- **Labels**: `kind/bug`, `priority/critical-urgent`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
`checkNodeSchedulingPropertiesChanged`  return `true` if the only difference is a resourceVersion.

As a result, `tas_resource_flavor_controller` regularly called `r.queues.QueueInadmissibleWorkloads(ctx, cqNames)` when it was not needed impacting BestEffortFIFO throughput

**What you expected to happen**:
Return `true` only on changes to fields that impact scheduling

**How to reproduce it (as minimally and precisely as possible)**:
Add UT to `pkg/controller/tas/resource_flavor_test.go`:

```
		"ResourceVersion changed": {
			oldNode:     baseNode.Clone().ResourceVersion("1").Obj(),
			newNode:     baseNode.Clone().ResourceVersion("2").Obj(),
			wantChanged: false,
		},
```

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:29:20Z

/priority critical-urgent
