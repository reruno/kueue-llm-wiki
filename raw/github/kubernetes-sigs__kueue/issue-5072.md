# Issue #5072: Helm: Prometheus ServiceMonitor does not capture all metrics

**Summary**: Helm: Prometheus ServiceMonitor does not capture all metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5072

**Last updated**: 2025-04-24T12:48:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-vizcaino](https://github.com/j-vizcaino)
- **Created**: 2025-04-23T12:43:33Z
- **Updated**: 2025-04-24T12:48:32Z
- **Closed**: 2025-04-24T12:48:32Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

Setting `enablePrometheus` in the Helm chart values creates a `ServiceMonitor` resource  that does not capture all metrics exposed by Kueue.

About 270 metric are reported (`count by(__name__) ({service="kueue-visibility-server"})`), with most metrics being `go_*`, `apiserver_*`, `rest_client_*` and `workqueue_*` related.

Kueue is running with `enableClusterQueueResources: true` in the config, but no `kueue_*` metrics are reported.

**What you expected to happen**:

Kueue related metrics should be reported in Prometheus.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

ServiceMonitor use `https`[port](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/prometheus/monitor.yaml#L13), which targets [this service, on port 8082](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/visibility/service.yaml#L13).
According to the [manager container definition](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/manager/manager.yaml#L51), the port for metrics should be 8443, not 8082 (visibility).

It seems the ServiceMonitor **label selector is not precise enough** and ends up selecting one of the `Service` in the `kueue-system` namespace, ending up with `kueue-visibility-server` and not `kueue-controller-manager-metrics-service`.

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.32.2`
- Kueue version (use `git describe --tags --dirty --always`): `0.11.3`
- Cloud provider or hardware configuration: AWS, EKS `v1.29.14-eks-bc803b4`
- Install tools: Helm Terraform provider `2.17.0`

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-23T12:45:54Z

cc @kannon92

### Comment by [@j-vizcaino](https://github.com/j-vizcaino) — 2025-04-23T13:36:16Z

Can confirm that adding `app.kubernetes.io/component: metrics` (or some other label) to both `ServiceMonitor` label selector and metrics `Service` leads to the correct behavior. Kueue metrics are now scraped and surfaced correctly.

Will open an MR to fix that.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-23T13:38:20Z

Thank you @j-vizcaino for the detailed report and a potential fix. it is greatly apprechiated.

I also noticed that our labelSelectors are a bit weird.
