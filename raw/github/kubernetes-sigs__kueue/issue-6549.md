# Issue #6549: Move "cache" and "queues" packages to make them self-explanatory

**Summary**: Move "cache" and "queues" packages to make them self-explanatory

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6549

**Last updated**: 2025-08-28T07:15:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-11T17:34:38Z
- **Updated**: 2025-08-28T07:15:12Z
- **Closed**: 2025-08-28T07:15:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Move / rename the "cache" and "queues" packages as follows:
- `pkg/cache` -> `pkg/cache/reserving`
- `pkg/queues` -> `pkg/cache/pending`
- `pkg/hierarchy` -> `pkg/cache/hierarchy`

**Why is this needed**:

- The names for the packages are confusing, because "queues" is also a cache, but just for pending workloads.
Whereas "cache" is used for reserving workloads.  I would like to better reflect this in naming, making it self-explanatory.
- In the future we would have a natural place to put common part of the caches, like `pkg/cache/shared`, or the `pkg/cache/hierarchy` which is only shared between the two, so it belongs conceptually as "cache".

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T17:34:50Z

cc @tenzen-y @gabesaba @PBundyra wdyt?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-12T08:49:15Z

I support the rename, but i'm not sure about self-explanatory-ness of reserving/pending. How about the following?

`pkg/cache` -> `pkg/cache/scheduling` - since it is the main representation used during scheduling cycle
`pkg/queues` -> `pkg/cache/queueing` - since it manages queueing/ordering/backoff of workloads within CQs/LQs 
`pkg/hierarchy` -> `pkg/cache/shared/hierarchy`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T10:56:50Z

sgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-12T12:20:37Z

> I support the rename, but i'm not sure about self-explanatory-ness of reserving/pending. How about the following?
> 
> `pkg/cache` -> `pkg/cache/scheduling` - since it is the main representation used during scheduling cycle
> `pkg/queues` -> `pkg/cache/queueing` - since it manages queueing/ordering/backoff of workloads within CQs/LQs
> `pkg/hierarchy` -> `pkg/cache/shared/hierarchy`

I would like to select `pkg/cache/scheduler`, `pkg/cache/queue`, and `pkg/cache/hierarchy` since I think that Go prefers the simple noun over verbs. Indeed, "scheduling" and "queueing" could be nouns, but they behave as verbs as well.

xref: https://go.dev/blog/package-names

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-08-17T16:38:28Z

/assign
