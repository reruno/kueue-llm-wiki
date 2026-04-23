# Issue #6658: Graduate MultiKueueBatchJobWithManagedBy to beta

**Summary**: Graduate MultiKueueBatchJobWithManagedBy to beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6658

**Last updated**: 2025-10-29T18:22:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-08-24T16:02:13Z
- **Updated**: 2025-10-29T18:22:06Z
- **Closed**: 2025-10-29T18:22:06Z
- **Labels**: _none_
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 4

## Description

https://github.com/kubernetes-sigs/kueue/blob/834c71daa68ee95a3b89b87d473793e0929645bd/pkg/features/kube_features.go#L84

Looking at our feature gates, I see this MultiKueue feature is still alpha.

Should we graduate this feature to beta?

I think we still want to graduate this feature to beta but it relies on ManagedBy being enabled in all supported versions of Kubernetes.

Looking at [ManagedBy KEP](https://github.com/kubernetes/enhancements/issues/4368), I think we can promote this to beta when 1.31 is out of support. Looking at the Kubernetes release scheduler, that should be around the 0.15 timeframe of Kueue.

1.31 will be out of support by end of October so we can graduate this feature to beta once that happens.

WDYT @tenzen-y @gabesaba?

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T09:05:38Z

> Looking at https://github.com/kubernetes/enhancements/issues/4368, I think we can promote this to beta when 1.31 is out of support. Looking at the Kubernetes release scheduler, that should be around the 0.15 timeframe of Kueue.

Yes, we can work on that in the v0.15 release cycle.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-22T11:05:20Z

This is ready to be taken in 0.15 I think

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-22T11:06:30Z

@kannon92 would you like to work on it?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-23T11:43:47Z

/assign
