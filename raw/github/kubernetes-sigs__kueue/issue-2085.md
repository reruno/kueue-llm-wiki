# Issue #2085: ServiceMonitor CRD should be installed first before apply prometheus.yaml

**Summary**: ServiceMonitor CRD should be installed first before apply prometheus.yaml

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2085

**Last updated**: 2024-05-22T17:17:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lowang-bh](https://github.com/lowang-bh)
- **Created**: 2024-04-28T13:15:42Z
- **Updated**: 2024-05-22T17:17:05Z
- **Closed**: 2024-05-22T17:17:05Z
- **Labels**: `kind/feature`
- **Assignees**: [@lowang-bh](https://github.com/lowang-bh)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Note about ServiceMonitor CRD at`github.com/prometheus-operator/kube-prometheus/manifests/setup/0servicemonitorCustomResourceDefinition.yaml` should be installed first.

**Why is this needed**:
There is a error indicates CRDs should be installed first when follow the docs to deploy kueue, 
```sh
VERSION=v0.6.2
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/$VERSION/prometheus.yaml

role.rbac.authorization.k8s.io/kueue-prometheus-k8s serverside-applied
rolebinding.rbac.authorization.k8s.io/kueue-prometheus-k8s serverside-applied
error: resource mapping not found for name: "kueue-controller-manager-metrics-monitor" namespace: "kueue-system" from "https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/prometheus.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
ensure CRDs are installed first
```

What's more, the same error will occur when install from source code via `make promethuse`

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2024-04-29T00:27:31Z

/assign
