# Issue #4530: Use AdmissionCheckReference and LocalQueueReference to improve static code analysis

**Summary**: Use AdmissionCheckReference and LocalQueueReference to improve static code analysis

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4530

**Last updated**: 2025-04-28T00:21:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-10T07:31:32Z
- **Updated**: 2025-04-28T00:21:26Z
- **Closed**: 2025-04-28T00:21:26Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 6

## Description

**What would you like to be cleaned**:

I would like to use AdmissionCheckReference type rather than string, for easier reasoning about the code. 

Examples: https://github.com/kubernetes-sigs/kueue/blob/6f9663660047e08ae3b79c469d7bf93bb6ca33ac/pkg/cache/cache.go#L108C2-L108C47

Similarly, use LocalQueueReference here: https://github.com/kubernetes-sigs/kueue/blob/6f9663660047e08ae3b79c469d7bf93bb6ca33ac/pkg/cache/cache.go#L142

This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/4442

We should also follow up with WorkloadReference, but it should be a separate PR (and potentially issue) due to the volume of changes.

**Why is this needed**:

To improve readability of the code. Seeing strings as keys makes one always wonder: is it namespace / name, name/namespace, or just name, or maybe UID? With dedicated type we can just create the reference objects.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T07:31:43Z

/assign @vladikkuzn 
tentatively

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-04-18T09:02:39Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-18T09:02:44Z

@vladikkuzn: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4530#issuecomment-2814969109):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-04-18T09:03:39Z

Only AdmissionCheckReference was introduced, reopening it to add LocalQueueReference

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-04-18T11:40:53Z

@mimowo I think it's good idea to add two types for local queue:
- [namespaced prefixed local queue reference](https://github.com/kubernetes-sigs/kueue/blob/6bbcb6a9e2c313dbf4a6deb05bf35f4136b829af/pkg/cache/clusterqueue.go#L70-L71)
- [localqueue reference](https://github.com/kubernetes-sigs/kueue/blob/6bbcb6a9e2c313dbf4a6deb05bf35f4136b829af/apis/kueue/v1beta1/workload_types.go#L40-L44)

WDYT?

p.s. https://github.com/kubernetes-sigs/kueue/pull/5046/files

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-18T11:54:06Z

Ah, I see, I would propose:
- LocalQueueReference - full Namespace / Name 
- LocalQueueName - just a type for local queue name, it is not full "reference"
