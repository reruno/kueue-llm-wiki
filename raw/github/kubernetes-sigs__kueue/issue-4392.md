# Issue #4392: Misleading error message when cohort has no parent and have borrowingLimit

**Summary**: Misleading error message when cohort has no parent and have borrowingLimit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4392

**Last updated**: 2025-04-08T14:30:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nasedil](https://github.com/nasedil)
- **Created**: 2025-02-25T10:44:47Z
- **Updated**: 2025-04-08T14:30:43Z
- **Closed**: 2025-04-08T14:30:42Z
- **Labels**: `kind/bug`
- **Assignees**: [@nasedil](https://github.com/nasedil)
- **Comments**: 1

## Description

**What happened**:
When defining a cohort that has no parent cohort and has `borrowingLimit` the following error message is shown:
```
admission webhook "vcohort.kb.io" denied the request: spec.resourceGroups[0].flavors[0].resources[0].borrowingLimit: Invalid value: "0": must be nil when cohort is empty
```
The message is misleading because clusterQueue object has `cohort` field for its parent cohort while cohort object has `parent` field for it's parent cohort.  And the error message is same for both cases.
**What you expected to happen**:
The message could end with `must be nil when parent is empty` or`must be nil when parent cohort is empty`.
**How to reproduce it (as minimally and precisely as possible)**:
Applying the following YAML file:
```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: pod-performance-resource-flavor
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: test-cohort
spec:
  # there is no parent cohort
  # parent: ~
  resourceGroups:
    - coveredResources: ["pods"]
      flavors:
        - name: "pod-performance-resource-flavor"
          resources:
            - name: "pods"
              nominalQuota: 1
              borrowingLimit: 0
...
```
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.31.5
- Kueue version (use `git describe --tags --dirty --always`):  v0.11.0-devel-244-gfd6a5206
- Cloud provider or hardware configuration: GCP GKE
- OS (e.g: `cat /etc/os-release`): Debian GNU/Linux
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@nasedil](https://github.com/nasedil) — 2025-02-25T10:45:52Z

/assign
