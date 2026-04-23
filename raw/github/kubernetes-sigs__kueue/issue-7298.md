# Issue #7298: Support CEL expressions in the DRA support

**Summary**: Support CEL expressions in the DRA support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7298

**Last updated**: 2026-03-08T20:08:50Z

---

## Metadata

- **State**: open
- **Author**: [@harche](https://github.com/harche)
- **Created**: 2025-10-16T13:41:17Z
- **Updated**: 2026-03-08T20:08:50Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@harche](https://github.com/harche), [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Upstream k8s allows [downstream components to evaluate CEL expressions](https://kubernetes.slack.com/archives/C0409NGC1TK/p1760556948412779?thread_ts=1760556528.438029&cid=C0409NGC1TK), so this should enable `kueue` to allow support for CEL expressions in the `ResourceClaimTemplates` 

**Why is this needed**:
CEL expression allow efficient filtering 

**Completion requirements**:
Kueue should be able to process `ResourceClaimTemplate` with the CEL expression 

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@harche](https://github.com/harche) — 2025-10-16T13:41:30Z

cc @alaypatel07

### Comment by [@harche](https://github.com/harche) — 2025-10-16T21:01:47Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-19T17:10:00Z

cc @sohankunkerkar @PannagaRao @MaysaMacedo

### Comment by [@harche](https://github.com/harche) — 2025-11-19T17:29:34Z

/assign @sohankunkerkar

### Comment by [@harche](https://github.com/harche) — 2026-02-06T16:40:32Z

cel expressions are used in partitionable devices https://github.com/kubernetes/enhancements/blob/bfb40c4e95274d42b8528421c8e56a5fea2fb79e/keps/sig-scheduling/4815-dra-partitionable-devices/README.md#dynamic-allocation-of-multi-instance-gpus-mig-on-nvidia-hardware. 

cc @sohankunkerkar

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-10T16:42:10Z

CEL expressions are also useful for DRANET (cc @aojea).

https://dranet.dev/docs/user/nvidia-dranet/

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-06T02:40:16Z

I drafted an example showing how you could use cel expressions with the example dra driver.

https://github.com/kubernetes-sigs/dra-example-driver/pull/155

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-08T20:08:50Z

I opened up this PR to resolve this issue. Please let me know what you think: https://github.com/kubernetes-sigs/kueue/pull/9742
