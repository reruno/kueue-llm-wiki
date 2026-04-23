# Issue #902: ClusterQueue update events continue to fire forever

**Summary**: ClusterQueue update events continue to fire forever

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/902

**Last updated**: 2023-06-27T18:06:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-06-26T16:10:44Z
- **Updated**: 2023-06-27T18:06:34Z
- **Closed**: 2023-06-27T18:06:34Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
`ClusterQueueStatus.flavorsUsage.resources` with random order continues to fire ClusterQueue update events forever, and the number of reconciles will explode.
Therefore kueue-controller-manager much increases the load of kube-apiserver and etcd.

**What you expected to happen**:
ClusterQueues aren't updated if the old and the new ones have the same usage.

**How to reproduce it (as minimally and precisely as possible)**:


**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25
- Kueue version (use `git describe --tags --dirty --always`): v0.3.2
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-26T16:10:51Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-26T16:13:08Z

The problem part: https://github.com/kubernetes-sigs/kueue/blob/b4635731cad8ec334d622ff4db60bfe1fbc13f77/pkg/cache/cache.go#L867-L881

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-26T16:22:22Z

Are we triggering a reconcile even if the usage didn't change?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-26T16:26:37Z

> Are we triggering a reconcile even if the usage didn't change?

Yes.
if the order of ClusterQueueStatus.flavorsUsage.resources is changed, it fires an update event.

For example, in the following diffs fire update event:

```yaml
status:
...
  flavorsUsage:
  - name: foo
    resources:
    - borrowed: "0"
      name: "cpu"
      total: "4"
    - borrowed: "0"
      name: "memory"
      total: "4"
```

```yaml
status:
...
  flavorsUsage:
  - name: foo
    resources:
    - borrowed: "0"
      name: "memory"
      total: "4"
    - borrowed: "0"
      name: "cpu"
      total: "4"
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-26T16:35:44Z

This issue will often happen in the HPC cluster. Because in HPC cluster, pods have multiple SR-IOV Virtual functions in resources.Resources like this:

```yaml
resources:
  requests:
    cpu: 256
    memory: 512Gi
    example.com/gpu: 8
    example.com/vf-0: 1
    example.com/vf-1: 1
    example.com/vf-2: 1
    example.com/vf-3: 1
    example.com/vf-4: 1
    example.com/vf-5: 1
    example.com/vf-6: 1
    example.com/vf-7: 1
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-26T16:53:24Z

ah I see. we should probably do an internal alphabetical sort

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-26T18:26:58Z

> ah I see. we should probably do an internal alphabetical sort

Right. I will sort `outFlvUsage.Resources` according to resourceName in https://github.com/kubernetes-sigs/kueue/blob/b4635731cad8ec334d622ff4db60bfe1fbc13f77/pkg/cache/cache.go#L850.

Also, I will apply this way to the localQueue usage as well.
