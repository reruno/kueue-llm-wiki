# Issue #7587: Commonize the handling of setting the Finished condition

**Summary**: Commonize the handling of setting the Finished condition

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7587

**Last updated**: 2025-11-12T06:36:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-07T16:27:30Z
- **Updated**: 2025-11-12T06:36:56Z
- **Closed**: 2025-11-12T06:36:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

This is follow up to https://github.com/kubernetes-sigs/kueue/pull/7582 as commented in https://github.com/kubernetes-sigs/kueue/pull/7582#issuecomment-3503486675

- use SSA with fallback to patch consistently
- use strict mode consistently
- use force ownership consistently

**Why is this needed**:

There is no reason to handle setting the condition differently from different places, and the differences are just legacy craft. We should align with what we do for Eviction which is very similar case - use SSA by default, but fallback to Patch in configured by FG.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T16:27:56Z

/assign @mszadkow 
tentatively
cc @amy
