# Issue #5971: Replace GroupVersionKind defenitioin with autoscaling one

**Summary**: Replace GroupVersionKind defenitioin with autoscaling one

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5971

**Last updated**: 2025-07-14T18:38:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-07-14T13:54:42Z
- **Updated**: 2025-07-14T18:38:25Z
- **Closed**: 2025-07-14T18:38:25Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to replace the following hardcoded GroupVersionKinds with `autoscaling.SchemeGroupVersion.WithKind("ProvisioningRequest")`.

```go
schema.GroupVersionKind{
	Group:   "autoscaling.x-k8s.io",
	Version: "v1",
	Kind:    "ProvisioningRequest"
}
```

**Why is this needed**:

Avoiding hardcoded strings would be better.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-14T18:10:59Z

/assign
