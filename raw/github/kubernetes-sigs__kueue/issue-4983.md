# Issue #4983: Implement generic strings Join util

**Summary**: Implement generic strings Join util

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4983

**Last updated**: 2025-04-30T12:49:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-04-15T13:50:56Z
- **Updated**: 2025-04-30T12:49:57Z
- **Closed**: 2025-04-30T12:49:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to implement a generic string `Join` util in https://github.com/kubernetes-sigs/kueue/tree/main/pkg/util/strings

```go
func Join[S ~string](a S, sep string) S { ... }
```

This has the same functionality with Go stdlib `strings.Join`, but this allows us to use strings type alias.

**Why is this needed**:

We have a lot of strings type alias and join those for messaging like:

- https://github.com/kubernetes-sigs/kueue/blob/b90208f86e490ef499bcfcc6d0b1242f5d880fae/pkg/config/validation.go#L277
- https://github.com/kubernetes-sigs/kueue/blob/04bee0db4000b298656c42a1ec44493e49bab5c8/pkg/cache/clusterqueue.go#L255

So, we want to generalize those.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-04-17T16:30:56Z

/assign
