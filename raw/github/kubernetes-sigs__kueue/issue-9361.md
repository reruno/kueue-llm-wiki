# Issue #9361: [TAS] Supporting Preferred and Required constraints for different topology levels

**Summary**: [TAS] Supporting Preferred and Required constraints for different topology levels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9361

**Last updated**: 2026-02-25T19:21:57Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2026-02-19T08:54:08Z
- **Updated**: 2026-02-25T19:21:57Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We want to enable a scenario with TAS such that the workload can be _preferred_ to be scheduled within a domain at a specific topology level while being strictly required to be scheduled within a domain at a higher topology level. Eg. a workload can be annotated such that all its pods are scheduled within a single block as a hard requirement, however, it should prefer to have all its pods within a single rack within the block only as a soft requirement. 

Today, if we add 2 annotations: `kueue.x-k8s.io/podset-required-topology` and `kueue.x-k8s.io/podset-preferred-topology` on a workload it throws a validation error.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x ] API change
- [x ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mwysokin](https://github.com/mwysokin) — 2026-02-25T19:21:57Z

TLDR; Even though you cannot use both using just the required annotation at the higher level should trigger the right behavior (compact placement/bin-packing) at the lower levels (like with the additional preferred pointing to the lower levelss).

It is not possible today although you should get the same behavior with BestFit (which is the default) and just the required annotation. It'll try to compact and bin pack everything so you shouldn't need the preferred one. I can give you an example. Imagine that you have this situation:

```
0-NAME                                         0-BLOCK                            0-SUBBLOCK                         0-HOST
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-zfs9   f0db290a73411eb4711d7624b49633f8   950d4ae505c017837f05e37593181869   2510116c39e68345a4e8303d93226b10
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-6ks8   f0db290a73411eb4711d7624b49633f8   950d4ae505c017837f05e37593181869   60b3d1a6b45f3911044d6058c542321f
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-n649   f0db290a73411eb4711d7624b49633f8   950d4ae505c017837f05e37593181869   c4d8e90b606daaef416dbc257d64aa0a
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-8r6z   f0db290a73411eb4711d7624b49633f8   950d4ae505c017837f05e37593181869   e2dda2500016f4480efbd8bacd59021f
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-j6b9   f0db290a73411eb4711d7624b49633f8   950d4ae505c017837f05e37593181869   fd8843fa0684d4b232dfea6c83aab232
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-xwr2   f729025594c5a515f820739576efa596   0164eceb1ac7a1578167cfe9b8c43e88   70757e64e256d6b976534e5dbd8505d4
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-dbk9   f729025594c5a515f820739576efa596   0164eceb1ac7a1578167cfe9b8c43e88   7512b6ab8663be9c0d1f693503f6d009
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-kl6f   f729025594c5a515f820739576efa596   0164eceb1ac7a1578167cfe9b8c43e88   87e9e44e46bd9f857cbe383ff5f5ddf9
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-mfkm   f729025594c5a515f820739576efa596   816f59b2d7c64cec45c77f41bc28bd8d   de6bfa6c739ab5a8017b61428b47e998
gke-cpu-tas-cluster-tas-pool-1-4eea6ff2-48xv   f729025594c5a515f820739576efa596   816f59b2d7c64cec45c77f41bc28bd8d   f937bbd8205f6e6b042cd136c5e7662c
```

Now let's say that I have a five-node workload, and I care about performance (our general assumption in TAS is that we optimize for everyone's performance) I'd set required to block because that's my lowest acceptable bar. As a result I'll get hosts from subblock 950d4ae505c017837f05e37593181869 instead of 2 subblocks every single time, so it works as preferred subblock, required block with only the second part specified. Is this what you'd expect?
