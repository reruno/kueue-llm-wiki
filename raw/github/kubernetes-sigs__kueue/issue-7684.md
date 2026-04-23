# Issue #7684: According to the documentation, the `kueue.x-k8s.io/v1beta1` CRD will be installed.

**Summary**: According to the documentation, the `kueue.x-k8s.io/v1beta1` CRD will be installed.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7684

**Last updated**: 2025-11-17T05:09:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kennygt51](https://github.com/kennygt51)
- **Created**: 2025-11-17T02:07:03Z
- **Updated**: 2025-11-17T05:09:38Z
- **Closed**: 2025-11-17T05:09:38Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:

to follow readme kubectl apply single-clusterqqueue-setup.yaml, so there is below error messages.
I think the reason why this is a diff CRD version example yaml and CRD applied.

According to the [docs](https://kueue.sigs.k8s.io/docs/installation/), I ran `kubectl apply -f single-clusterqueue-setup.yaml`, but I got the following error messages.  
I think the issue is caused by a difference between the CRD version in the example YAML and the one that was actually applied.

```bash
> kubectl apply -f single-clusterqueue-setup.yaml
resource mapping not found for name: "default-flavor" namespace: "" from "single-clusterqueue-setup.yaml": no matches for kind "ResourceFlavor" in version "kueue.x-k8s.io/v1beta2"
ensure CRDs are installed first
resource mapping not found for name: "cluster-queue" namespace: "" from "single-clusterqueue-setup.yaml": no matches for kind "ClusterQueue" in version "kueue.x-k8s.io/v1beta2"
ensure CRDs are installed first
resource mapping not found for name: "user-queue" namespace: "default" from "single-clusterqueue-setup.yaml": no matches for kind "LocalQueue" in version "kueue.x-k8s.io/v1beta2"
ensure CRDs are installed first
```

**What you expected to happen**:

The correct kind/version (kueue.x-k8s.io/v1beta2) will be installed through the getting started procedure.

**How to reproduce it (as minimally and precisely as possible)**:

Install it according to the documentation.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-17T04:13:03Z

It’s because we updated the examples on the main branch to use the `v1beta2` version (see https://github.com/kubernetes-sigs/kueue/pull/7409). You can apply it using the `release-0.14` branch or the `website` branch.

We should probably update the links to use version-agnostic URLs, similar to what we do here: https://kueue.sigs.k8s.io/docs/installation/#install-by-kubectl.
