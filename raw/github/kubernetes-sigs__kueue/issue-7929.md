# Issue #7929: Pod without localqueue stuck in pending

**Summary**: Pod without localqueue stuck in pending

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7929

**Last updated**: 2025-11-29T04:35:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lbadams4](https://github.com/lbadams4)
- **Created**: 2025-11-27T04:38:34Z
- **Updated**: 2025-11-29T04:35:18Z
- **Closed**: 2025-11-29T04:35:18Z
- **Labels**: `kind/bug`, `kind/support`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I have the kueue configmap setup to manage pods without a queue and to manage namespaces with a particular label

```yaml
manageJobsWithoutQueueName: true
managedJobsNamespaceSelector:
 matchLabels:
   kueue-managed: "true"
```
I have a cluster queue setup to select namespaces with this same label
```yaml
namespaceSelector:
  matchLabels:
    kueue-managed: "true"
```

When I create pod in a namespace with this label, a kueue workload is created and kueue attempts to manage the pod, but it stays in Pending and I see an error in the kueue controller
```log
"msg":"ignored an error for now","workload":{"name":"pod-debug-bf2ca","namespace":"test"},"queue":"","status": │
│ "pending","error":"localQueue doesn't exist or inactive"}
```

**What you expected to happen**:
I expect kueue to manage the pod if it doesn't declare a local queue because i have 
```yaml
manageJobsWithoutQueueName: true
```
in the kueue config map

**How to reproduce it (as minimally and precisely as possible)**:
Use the configuration described above

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.31.13-eks-3cfe0ce
- Kueue version (use `git describe --tags --dirty --always`): 0.14.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-27T15:11:00Z

/kind support

Kueue has to have a queue in the namespace. ManageJobsWithoutQueueName just means that users don't need to specify a local queue label on their workloads.

With LocalQueueDefaulting it may look for a default local queue but a local must exist in the namespace.
