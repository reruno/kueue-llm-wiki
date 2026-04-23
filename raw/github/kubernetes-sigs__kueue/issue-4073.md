# Issue #4073: Support JAX in Kueue using training-operator 1.9

**Summary**: Support JAX in Kueue using training-operator 1.9

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4073

**Last updated**: 2025-05-15T06:28:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-28T08:56:01Z
- **Updated**: 2025-05-15T06:28:51Z
- **Closed**: 2025-05-15T06:28:51Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 6

## Description

**What would you like to be added**:

Support for the recently added JAX in the training-operator, see https://github.com/kubeflow/training-operator/issues/1619 and https://github.com/kubeflow/training-operator/issues/1619.

**Why is this needed**:

For completeness of the support in Kueue. Also, the support for JAX was long-awaited in the training-operator, and there will be a community of people willing to use it with Kueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T08:57:19Z

cc @mbobrovskyi @mszadkow 
Requires https://github.com/kubernetes-sigs/kueue/pull/4066

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-28T09:34:36Z

I'm fine with supporting JAXJob in the Kueue!

Just FYI: we did not confirm if JAXJob is compatible with TPU 😞 
Are you ok with such a JaxJob support level?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T09:46:47Z

IIUC, you haven't tested, but it does not indicate it is not working? I don't expect much of a difference between GPU and TPU, but without testing it remains unknown.

In any case I would be ok to claim the support for the GPUs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-28T09:48:24Z

> IIUC, you haven't tested, but it does not indicate it is not working? I don't expect much of a difference between GPU and TPU, but without testing it remains unknown.
> 
> In any case I would be ok to claim the support for the GPUs.

Actually, we did not have any verifications for both GPU and TPU. We verified only CPU

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T10:46:54Z

I see, getting some confirmation that the controller works with GPU or TPU would be great.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-03-04T15:57:32Z

/assign
