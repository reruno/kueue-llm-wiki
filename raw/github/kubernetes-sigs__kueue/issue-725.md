# Issue #725: Replace component-config with our implemntation

**Summary**: Replace component-config with our implemntation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/725

**Last updated**: 2023-06-26T14:56:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-04-26T18:47:43Z
- **Updated**: 2023-06-26T14:56:31Z
- **Closed**: 2023-06-26T14:56:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We should migrate the component-config to another logic.

**Why is this needed**:
The controller-runtime community announces that the component-config (https://github.com/kubernetes-sigs/controller-runtime/tree/dca0be70fd22d5200f37d986ec83450a80295e59/pkg/config) is deprecated and will be removed in the future.

Ref:
- https://github.com/kubernetes-sigs/controller-runtime/pull/2149
- https://github.com/kubernetes-sigs/controller-runtime/issues/895

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T11:58:29Z

/remove-kind feature
/kind cleanup

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-20T20:17:52Z

@alculquicondor We need to work on this before bumping k8s module to v1.27 because controller-runtime v.0.15 doesn't populate parameters to `ctrl.Option`, and many lint errors have occurred.

ref: https://github.com/kubernetes-sigs/kueue/pull/880

If we put ` component-config` in the kueue repository, do we need to upgrade componentConfig's apiVersion to v1beta2?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-20T21:12:26Z

No, we only need to bump the version if we need to remove fields from the schema (in the CustomResourceDefinition itself)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-20T21:32:31Z

> No, we only need to bump the version if we need to remove fields from the schema (in the CustomResourceDefinition itself)

I see. Thanks!

### Comment by [@trasc](https://github.com/trasc) — 2023-06-21T08:38:07Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-21T08:46:50Z

> /assign

Thanks for taking this!
