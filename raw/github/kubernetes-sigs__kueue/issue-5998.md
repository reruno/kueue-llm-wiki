# Issue #5998: Wrong pods count when TAS enabled and pods quota in CQ

**Summary**: Wrong pods count when TAS enabled and pods quota in CQ

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5998

**Last updated**: 2026-03-01T08:34:40Z

---

## Metadata

- **State**: open
- **Author**: [@and-1](https://github.com/and-1)
- **Created**: 2025-07-16T17:02:19Z
- **Updated**: 2026-03-01T08:34:40Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

**What happened**:
When TopologyAwareScheduling is true and set pods quota in CQ i can't reach full pods capacity of node

**What you expected to happen**:
full pod capacity can be reached

**How to reproduce it (as minimally and precisely as possible)**:
1. Enable TopologyAwareScheduling in kueue config
2. Create CQ with pods quota
```
...
resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - pods
    flavors:
    - name: default
      resources:
      - name: cpu
        nominalQuota: 100
      - name: memory
        nominalQuota: 100Gi
      - name: pods
        nominalQuota: 100
...
```
3. Create flavor default and add one node to it
4. Create deployment with cpu - 100m, memory - 100Mi and replicas - 100

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.29
- Kueue version (use `git describe --tags --dirty --always`): v0.12.4

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-31T02:15:28Z

cc/ @ichekrygin ^

### Comment by [@amy](https://github.com/amy) — 2025-07-31T16:27:32Z

Haven't gotten a chance to play around with this issue yet. But @ichekrygin mentioned that he noticed some overhead shaved off the top. Perhaps try incrementally decreasing your cpu and memory needs in `deployment with cpu - 100m, memory - 100Mi and replicas - 100`

So something like... 99 replicas, then 98 replicas. Alternatively, try decreasing to cpu/memory per pod. But TAS probably looks at actual node utilization before scheduling. So this means, even though you've virtually declared 100 CPU and 100Gi memory of nominal quota, that may not be the actual reality of availability on the underlying nodes.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-31T16:31:49Z

I believe I ran into a similar issue while working in a kind cluster. One important detail to note is that when Kueue is running with TAS enabled, it evaluates the available capacity of individual nodes by subtracting the resource requests of all pods running on that node, not just those managed by Kueue. This can lead to unexpected behavior in environments like kind, where nodes often have non-Kueue-managed system pods consuming resources. I think it worth double-checking.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-29T17:21:03Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-28T17:23:23Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T07:10:14Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-01T07:46:39Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-01T08:34:38Z

/remove-lifecycle stale
