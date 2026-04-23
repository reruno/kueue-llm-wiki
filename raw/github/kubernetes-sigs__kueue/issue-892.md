# Issue #892: KUBERNETES_CLUSTER_DOMAIN in helm chart

**Summary**: KUBERNETES_CLUSTER_DOMAIN in helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/892

**Last updated**: 2023-06-29T17:23:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rptaylor](https://github.com/rptaylor)
- **Created**: 2023-06-22T19:53:46Z
- **Updated**: 2023-06-29T17:23:39Z
- **Closed**: 2023-06-29T17:23:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

`kubernetesClusterDomain` is a configurable value in the helm chart. It sets a [dns name for the certmanager certificate](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/certmanager/certificate.yaml#L18) which makes sense but it also sets KUBERNETES_CLUSTER_DOMAIN [here](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/manager/manager.yaml#L29)  and [here](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/manager/manager.yaml#L67).

**What would you like to be cleaned**:
KUBERNETES_CLUSTER_DOMAIN in the Helm chart if it is not used, or to add some info about what it does if it is used.

**Why is this needed**:
I could not find any information about KUBERNETES_CLUSTER_DOMAIN and I did not see any results of searching the kueue code base for anything that would read this environment variable.
Also the YAML manifest does not have it
https://github.com/kubernetes-sigs/kueue/releases/download/v0.3.2/manifests.yaml
so it seems like kueue could behave differently if installed via Helm vs YAML?

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-23T11:04:00Z

/assign
