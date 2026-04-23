# Issue #8208: [Flaky E2E] Topology Aware Scheduling when Single TAS Resource Flavor when ProvisioningRequest is used uses exponential second-pass backoff for the workload admission

**Summary**: [Flaky E2E] Topology Aware Scheduling when Single TAS Resource Flavor when ProvisioningRequest is used uses exponential second-pass backoff for the workload admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8208

**Last updated**: 2025-12-22T09:04:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-12-12T11:35:46Z
- **Updated**: 2025-12-22T09:04:34Z
- **Closed**: 2025-12-22T09:04:34Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Single TAS Resource Flavor when ProvisioningRequest is used uses exponential second-pass backoff for the workload admission [slow] 

```
{Expected
    <int32>: 0
to be >=
    <int>: 3 failed [FAILED] Expected
    <int32>: 0
to be >=
    <int>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/tas/tas_test.go:2860 @ 12/12/25 11:12:19.15
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8206/pull-kueue-test-integration-extended-main/1999434302667886592

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T12:30:57Z

cc @mykysha ptal
iirc you worked on the test for exponential backoff

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T16:48:32Z

Interesting, so looking at the logs we see that the Consistently finished immediately, we have:
- `2025-12-12T11:12:18.129281224Z` for "ProvisioningRequest as Provisioned (start of the backoff window)"
- `2025-12-12T11:12:19.130035177Z` for "observe at least three SecondPassFailed events while the node is NotReady (≈1s, 2s, 4s backoffs)"

So just 1s later. I think this is because we are using Consistently wrongly, IIUC it should return something in the function, and we should check its value. We basically have a function which always ends with nil, so maybe Consistently is free to optimize out for conditions which are always true. 

In any case, I think it is better to use Eventually here rather than consistently, wdyt @mykysha ?

### Comment by [@mykysha](https://github.com/mykysha) — 2025-12-16T08:53:20Z

/assign

### Comment by [@mykysha](https://github.com/mykysha) — 2025-12-16T09:10:00Z

Consistently can be removed, but the test still requires that 10s wait to be relevant - if we remove the 10s wait between provisioning and make the observation of 3-5 failures with Eventually using LongTimeout, it will work both with and without the backoff. Will look into ways to make Consistently more robust, i.e. make the function return something

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-18T14:24:58Z

I think I create this PR by mistake. I already reverted this changes on the PR https://github.com/kubernetes-sigs/kueue/pull/8206. And we have exactly 10 seconds which is correct. 

But I would propose to add at least some comment if we are using some specific timeout duration.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T15:07:05Z

> if we remove the 10s wait between provisioning and make the observation of 3-5 failures with Eventually using LongTimeout, it will work both with and without the backoff

To verify we used backoff we could check additionally that the amount of time passed is >4s.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:36:11Z

/priority important-soon
