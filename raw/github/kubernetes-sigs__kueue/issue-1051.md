# Issue #1051: Use k8s.io/utils/ptr package

**Summary**: Use k8s.io/utils/ptr package

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1051

**Last updated**: 2023-08-11T20:43:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-09T13:34:30Z
- **Updated**: 2023-08-11T20:43:23Z
- **Closed**: 2023-08-11T20:43:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 5

## Description

**What would you like to be cleaned**:

This package uses generics to wrap values into pointers.

**Why is this needed**:

Eliminates the need for our own pkg/utils/pointer package

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2023-08-11T12:06:11Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2023-08-11T12:09:14Z

So your package does utilize this and it is mostly defining aliases to K8s pointer package.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-11T12:14:51Z

We can remove `pkg/util/pointer`, then we use `ptr.To(resource.Quantity)` each location.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-11T13:25:39Z

Yes, `ptr` is a new package, different from `pointer`

### Comment by [@kannon92](https://github.com/kannon92) — 2023-08-11T14:08:12Z

TIL I learned that pointer is deprecated.  And there is `ptr`.  That will be a lot of work to change in k/k.
