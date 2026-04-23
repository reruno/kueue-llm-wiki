# Issue #5312: KueueViz: Workload filtering

**Summary**: KueueViz: Workload filtering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5312

**Last updated**: 2025-05-26T15:02:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@shaharelys](https://github.com/shaharelys)
- **Created**: 2025-05-22T12:09:17Z
- **Updated**: 2025-05-26T15:02:18Z
- **Closed**: 2025-05-26T15:02:18Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Options to filter by `namespace`, `status`, `started time`

**Why is this needed**:
That's basic feature. I use KueueViz and I would use such a feature a lot.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@shaharelys](https://github.com/shaharelys) — 2025-05-22T12:14:32Z

@mimowo Hey! That's something we need. I would like to start contributing working on that issue. Is that cool?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T12:16:07Z

>  I would like to start contributing working on that issue. Is that cool?

Awesome, cc @akram @kannon92

### Comment by [@shaharelys](https://github.com/shaharelys) — 2025-05-22T13:23:15Z

Hey guys! Thinking about the architecture, I am having a hard time deciding where the filtering logic should be placed. Should it be under the frontend or under the backend? 

I have almost no experience with FS design :)

From what I read, there are some considerations for either solution. Would appreciate your input @mimowo @akram @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T18:31:20Z

I would be pragmatic about it, and start simple. My guess is that frontend filtering is simpler, especially if frontend already has the complete list of workloads (to be checked). We can move it to backend when we hit scalability limits of the approach.
