# Issue #9361: [TAS] Supporting Preferred and Required constraints for different topology levels

**Summary**: [TAS] Supporting Preferred and Required constraints for different topology levels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9361

**Last updated**: 2026-10-07T20:59:00Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2026-02-19T08:54:08Z
- **Updated**: 2026-10-07T20:59:00Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-26T19:40:46Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-25T20:27:16Z

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

### Comment by [@amy](https://github.com/amy) — 2026-07-19T01:39:26Z

@varunsyal bump. Curious if you're looking for behavior similar to kai's hierarchical gangs: https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/

### Comment by [@amy](https://github.com/amy) — 2026-07-19T01:40:32Z

/remove-lifecycle rotten

### Comment by [@kannon92](https://github.com/kannon92) — 2026-10-06T20:56:14Z

cc @sohankunkerkar @mimowo @tenzen-y @kshalot @olekzabl 

This came up with the Kueue integration with Grove (https://github.com/ai-dynamo/grove/issues/871) and I'm curious if we have an alternative for this issue.

Seems this didn't get much traction.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-10-07T07:26:28Z

So the idea is `required=block` and `preferred=rack` ? 

You get this behavior already relying on our BestFit bin-packing by setting just `required=block` , because the bin-packing will try to squeeze under one "rack" if possible - if not possible it will spill over to the neighbour rack within the same block, so this is the expected behavior IIUC.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-10-07T20:33:37Z

IIUC, I don't think `required: block` alone covers it. BestFit picks the block by its total free capacity and ignores how that capacity is split across racks. So a job can span two racks in the tightest block while another block has a rack that fits it whole. I'd keep that default and let users opt into rack locality with `required: block` + `preferred: rack`.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-10-07T20:44:18Z

> BestFit picks the block by its total free capacity and ignores how that capacity is split across racks. So a job can span two racks in the tightest block while another block has a rack that fits it whole.

true, though this is a bit of a corner case. I'm wondering if this scenario what indeed the intention for the issue.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-10-07T20:54:22Z

Yeah, I can't tell what the original intent was, because the issue doesn't say why it's needed. What brought it back is Grove (ai-dynamo/grove#871). Grove lets users set `required: block` and `preferred: rack` on the same group, and Kueue can't take both today, so the Grove backend has to reject it or drop one. I think that's the real reason to support the pair, more than this placement case.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-10-07T20:59:00Z

forgot to tag @alaypatel07
