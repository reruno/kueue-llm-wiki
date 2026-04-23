# Issue #740: Discussion about feature gate

**Summary**: Discussion about feature gate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/740

**Last updated**: 2023-05-24T05:46:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-05-03T09:13:17Z
- **Updated**: 2023-05-24T05:46:50Z
- **Closed**: 2023-05-24T05:46:50Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 8

## Description

For some experimental features or huge changes which touch a lot of codes, we may need some protection mechanisms, the easiest way might be the config flags.
- new introduced, enable via flag
- mature, remove the flag, enable by default.

Or a really feature-gate kit.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T12:25:50Z

We should probably follow the same feature-gate pattern as k/k.

Are you thinking of a particular feature for which we need this?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-03T13:49:57Z

I'm working on the design of https://github.com/kubernetes-sigs/kueue/pull/331 , I think it would be more safe if we can provide such a mechanism, but at this point of time, we can have a flag to enable this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T14:18:40Z

#331 is backed by issue #78, which is currently assigned to @trasc. I believe he's almost done with the design.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T14:20:35Z

Regardless, feature flags might be useful. Would you want to add the framework for it? I wonder how much we can reuse from k/k.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-04T07:26:23Z

>  I believe he's almost done with the design.

That's great.

> Would you want to add the framework for it? I wonder how much we can reuse from k/k.

I may need to take a look.

### Comment by [@trasc](https://github.com/trasc) — 2023-05-04T08:45:44Z

For #78 I've opened another KEP PR #742, however , at least for the core components the implementation should be based on a optional field, which , if missing should give us the same behavior as before the implementation. 

But still we can use a feature gate to stop the `jobframework`   from populating that field.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-19T20:07:53Z

@kerthcet did you make progress with feature gates?

#771 might benefit from it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-19T21:29:39Z

I think linking this issue to #636 would be good.
