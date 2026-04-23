# Issue #2427: Controller fails attempting to add duplicate tolerations

**Summary**: Controller fails attempting to add duplicate tolerations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2427

**Last updated**: 2024-06-28T15:23:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sam-leitch-oxb](https://github.com/sam-leitch-oxb)
- **Created**: 2024-06-17T19:17:27Z
- **Updated**: 2024-06-28T15:23:54Z
- **Closed**: 2024-06-28T15:23:54Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow), [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What happened**:

I am seeing errors in the log similar to:
```
Job.batch "job-name" is invalid: spec.template: Invalid value: core.PodTemplateSpec{...,Tolerations:[]core.Toleration{core.Toleration{Key:"nvidia.com/gpu", Operator:"Exists", Value:"", Effect:"NoSchedule", TolerationSeconds:(*int64)(nil)}, core.Toleration{Key:"nvidia.com/gpu", Operator:"Exists", Value:"", Effect:"NoSchedule", TolerationSeconds:(*int64)(nil)}}, ...}: field is immutable
```

When my ResourceFlavor has:

```
spec:
  ...
  tolerations:
  - effect: NoSchedule
    key: nvidia.com/gpu
    operator: Exists
```

And I restart the kueue-controller-manager.
 
It appears the Kueue is attempting to update the Job template to include a toleration that is already there (and is failing because the Job can't be updated)

**What you expected to happen**:

1. If a toleration already exists in the tolerations list, a duplicate should not be added.
2. Kueue should not attempt to update existing Jobs  (Updating tolerations or nodeSelectors) when the controller is restarted.

**How to reproduce it (as minimally and precisely as possible)**:

Create a ResourceFlavor with
```
spec:
  ...
  tolerations:
  - effect: NoSchedule
    key: nvidia.com/gpu
    operator: Exists
```

Create a ClusterQueue and LocalQueue using the ResourceFlavor.
Create a long running Job targeting the ResourceFlavor.
Stop the controller.
Suspend the Job.
Start the controller.
Note errors described above.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.30.1-gke.1156000
- Kueue version (use `git describe --tags --dirty --always`): 0.7.0
- Cloud provider or hardware configuration: GKE Standard Cluster
- OS (e.g: `cat /etc/os-release`): Unknown
- Kernel (e.g. `uname -a`): Unknown
- Install tools:
- Others:

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-21T14:50:19Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-06-28T13:40:31Z

/assign
