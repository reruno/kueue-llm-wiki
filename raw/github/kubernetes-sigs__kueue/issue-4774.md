# Issue #4774: Kueue install via Helm not working.

**Summary**: Kueue install via Helm not working.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4774

**Last updated**: 2025-03-26T16:42:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@LarsSven](https://github.com/LarsSven)
- **Created**: 2025-03-24T13:15:41Z
- **Updated**: 2025-03-26T16:42:35Z
- **Closed**: 2025-03-26T16:42:35Z
- **Labels**: `kind/documentation`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 7

## Description

**What happened**:
I was trying to install kueue as a helm chart via
```
helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue --version="0.11.0" --create-namespace --namespace=kueue-system
```
as instructed here:
https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/README.md#install-chart-using-helm-v30

But I got:
```
Error: INSTALLATION FAILED: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue:0.11.0: not found
```

**What you expected to happen**:
I expected this command to succeed and install Kueue into my cluster

**How to reproduce it (as minimally and precisely as possible)**:
Run `helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue --version="0.11.0" --create-namespace --namespace=kueue-system` as described in the documentation

**Anything else we need to know?**:
I would like to install Kueue as a helm chart. I assume this is a documentation issue, so would it be possible to let me know what command would work for installing Kueue using an already published helm chart?

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.3
- Kueue version (use `git describe --tags --dirty --always`): v0.11.1
- Cloud provider or hardware configuration: Local (MiniKube)
- OS (e.g: `cat /etc/os-release`): Ubuntu 24.10
- Kernel (e.g. `uname -a`): 6.11.0-19-generic
- Install tools: Helm v3.17.2
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T13:18:10Z

Try this: https://kueue.sigs.k8s.io/docs/installation/#install-by-helm for released versions

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T13:20:04Z

I think this will work with "v": 
```
helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue --version="v0.11.1" --create-namespace --namespace=kueue-system
```
so it would be good to fix the docs, but we should also add a note to discourage use of staging registry for released versions.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-03-25T15:48:16Z

Just tested and made sure `0.11.0` is correct for `registry.k8s.io`. Do we want to update the [helm installation docs](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/README.md#install-chart-using-helm-v30) to use official releases?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-25T16:33:46Z

Yes. feel free to submit a PR. We may also need to adjust the prepera-release-branch in the Makefile for updating this page when we do a new release.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-03-25T17:15:14Z

> Try this: https://kueue.sigs.k8s.io/docs/installation/#install-by-helm for released versions

Just to confirm, this does indeed work, I did not find that link but only the one I linked when I was looking for a helm deployment. Thank you

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-03-25T18:14:10Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-26T13:18:36Z

/remove-kind bug
/kind documentation
