# Issue #4242: Introduce PodSetReference type for better static code analysis

**Summary**: Introduce PodSetReference type for better static code analysis

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4242

**Last updated**: 2025-02-28T16:46:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-12T09:56:17Z
- **Updated**: 2025-02-28T16:46:57Z
- **Closed**: 2025-02-28T16:46:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 3

## Description

**What would you like to be cleaned**:

Currently PodSet name is represented just as a string in a number of places, like in [here](https://github.com/kubernetes-sigs/kueue/pull/4200/files#diff-5414dcb324187d1d853329b419691cde79632a6d77e1a7c2b503dc1a3688c081R243)

I would like to use PodSetReference when refering to pod set name, as we do for FlavorReference or TopologyReference.

**Why is this needed**:

To introduce additional compile-time checking for the types. This way we know the key represented as "string" is PodSet name, not a random string.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T09:56:48Z

cc @PBundyra @tenzen-y 

As an idea out of the comments in https://github.com/kubernetes-sigs/kueue/pull/4200/files#r1950641428

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:08:08Z

> cc [@PBundyra](https://github.com/PBundyra) [@tenzen-y](https://github.com/tenzen-y)
> 
> As an idea out of the comments in https://github.com/kubernetes-sigs/kueue/pull/4200/files#r1950641428

SGTM

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-02-26T12:29:42Z

/assign
