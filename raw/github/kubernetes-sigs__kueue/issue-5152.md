# Issue #5152: Specify the platform for Ray/Raymini images using env. variable

**Summary**: Specify the platform for Ray/Raymini images using env. variable

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5152

**Last updated**: 2025-05-07T06:59:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-05T08:31:47Z
- **Updated**: 2025-05-07T06:59:18Z
- **Closed**: 2025-05-07T06:59:18Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Specify the images for Ray/Raymini images using the env. variable. We probably could introduce RAY_PLATFORMS or RAY_PLATFORM variable.

**Why is this needed**:

To avoid reading the architecture from the os, and allow choosing different architectures. This was discussed in https://github.com/kubernetes-sigs/kueue/pull/4917#discussion_r2060768176

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-05T08:33:15Z

cc @tenzen-y @mszadkow

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:01:36Z

We are using the `PLATFORMS` env vars for image buiding during E2E testings:

https://github.com/kubernetes-sigs/kueue/blob/3d4725b8553082570b86ad7b81120570c26ea5fa/Makefile#L242-L244

Do we want to introduce a separate env var? @mszadkow Do you have any concerns about reusing the `PLATFORMS`?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-06T06:16:58Z

If reusing works, I'm ok with that, even better

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-06T06:55:32Z

I will definitively check possibility to reuse this.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:58:27Z

> I will definitively check possibility to reuse this.

thank you!

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-06T13:38:57Z

/assign
