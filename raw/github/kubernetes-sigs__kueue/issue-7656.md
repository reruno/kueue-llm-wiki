# Issue #7656: v1beta2: change default for waitForPodsReady.blockAdmission to false

**Summary**: v1beta2: change default for waitForPodsReady.blockAdmission to false

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7656

**Last updated**: 2025-11-17T07:59:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-14T09:06:32Z
- **Updated**: 2025-11-17T07:59:44Z
- **Closed**: 2025-11-17T07:59:44Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to change the default for blockAdmission to false

Before we change the logic it would be nice to send a preparatory PR to documenation which already suggests using `blockAdmission: false` in most places.

Part of https://github.com/kubernetes-sigs/kueue/issues/7113

**Why is this needed**:

blockAdmission=true is used more rarely because:
- it blocks admission during 2-phase scheduling, so it is not useable with AdmissionChecks essentially, which is surprising to users 
- it is very slow to schedule workloads sequentially completly
- blockAdmission=true was introduced to prevent deadlocks which now can be avoided better with TopologyAwareScheduling

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T09:06:40Z

cc @tenzen-y @mbobrovskyi

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-14T15:00:07Z

It sounds like you really actually want to deprecate blockAdmission: true?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T15:11:12Z

> It sounds like you really actually want to deprecate blockAdmission: true?

Good question, I didn't think about it. I think for that we need additional feedback from the community. 

However, all installations I've seen so far use `blockAdmission: false`.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-14T17:21:57Z

> blockAdmission=true was introduced to prevent deadlocks which now can be avoided better with TopologyAwareScheduling

This is saying that our recommendation would be to use TAS anyway?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T17:31:27Z

I think so, I think TAS is pretty good these days, and solves the important issue of fragmentation, essentially providing gang scheduling.

Sure some users don't know the datacenter topology, but then they can just use `kubernetes.io/hostname` as a single level.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T18:27:27Z

/assign @mbobrovskyi 
ptal

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-14T20:32:14Z

> Before we change the logic it would be nice to send a preparatory PR to documenation which already suggests using blockAdmission: false in most places.

https://github.com/kubernetes-sigs/kueue/pull/7676

We do set blockAdmission: true in WaitForPodsReady documentation but from what I can tell that is intential for our example.

So I left that one alone.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-14T20:53:42Z

I'm ok with changing the default value to `true`. But, I think that the `blockAdmission` functionality is still valuable.
So, keeping both of TAS and blockAdmission sounds reasonable.
