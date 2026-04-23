# Issue #9416: E2E_MODE=dev is not working if "prometheus" is a skipped feature

**Summary**: E2E_MODE=dev is not working if "prometheus" is a skipped feature

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9416

**Last updated**: 2026-02-23T11:17:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-23T09:52:43Z
- **Updated**: 2026-02-23T11:17:36Z
- **Closed**: 2026-02-23T11:17:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

**What happened**:

I tried using the dev mode this way `GINKGO_ARGS="--label-filter=feature:kuberay" E2E_MODE=dev make kind-image-build test-e2e`



**What you expected to happen**:

no failure without prometheus, I can restrict testing to just KubeRay

**How to reproduce it (as minimally and precisely as possible)**:

`GINKGO_ARGS="--label-filter=feature:kuberay" E2E_MODE=dev make kind-image-build test-e2e`

**Anything else we need to know?**:

This worked fine: `GINKGO_ARGS="--label-filter=feature:kuberay feature:prometheus" E2E_MODE=dev make kind-image-build test-e2e`

When trying I get errors like this:

```
validatingwebhookconfiguration.admissionregistration.k8s.io/kueue-validating-webhook-configuration serverside-applied
E0221 07:44:46.212362 3388245 memcache.go:287] couldn't get resource list for visibility.kueue.x-k8s.io/v1beta1: the server is currently unable to handle the request
E0221 07:44:46.215236 3388245 memcache.go:287] couldn't get resource list for visibility.kueue.x-k8s.io/v1beta2: the server is currently unable to handle the request
E0221 07:44:46.223721 3388245 memcache.go:121] couldn't get resource list for visibility.kueue.x-k8s.io/v1beta1: the server is currently unable to handle the request
E0221 07:44:46.228240 3388245 memcache.go:121] couldn't get resource list for visibility.kueue.x-k8s.io/v1beta2: the server is currently unable to handle the request
role.rbac.authorization.k8s.io/kueue-prometheus-k8s serverside-applied
rolebinding.rbac.authorization.k8s.io/kueue-prometheus-k8s serverside-applied
error: resource mapping not found for name: "kueue-controller-manager-metrics-monitor" namespace: "kueue-system" from "STDIN": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
ensure CRDs are installed first
Switched to context "kind-kind".
Exporting logs for cluster "kind" to:
/usr/local/google/home/michalwozniak/go/src/sigs.k8s.io/kueue/bin/run-test-e2e-singlecluster-1.35.0
E0221 07:44:47.190865 3389496 memcache.go:287] couldn't get resource list for visibility.kueue.x-k8s.io/v1beta1: the server is currently unable to handle the request
E0221 07:44:47.208340 3389496 memcache.go:287] couldn't get resource list for visibility.kueue.x-k8s.io/v1beta2: the server is currently unable to handle the request
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T09:52:51Z

cc @IrvingMg ptal

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-23T09:59:51Z

/assign
