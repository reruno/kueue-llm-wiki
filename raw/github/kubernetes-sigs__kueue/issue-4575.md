# Issue #4575: kep-4377: Document how one can implement secure metrics

**Summary**: kep-4377: Document how one can implement secure metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4575

**Last updated**: 2025-03-19T16:24:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-03-12T16:26:36Z
- **Updated**: 2025-03-19T16:24:32Z
- **Closed**: 2025-03-19T16:24:32Z
- **Labels**: `kind/documentation`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 3

## Description

A user can either enable this with kustomize code or they can use the helm chart.

```yaml
metrics:
  prometheusNamespace: monitoring
# tls configs for serviceMonitor
  serviceMonitor:
    tlsConfig:
      serverName: kueue-controller-manager-metrics-service.kueue-system.svc
      insecureSkipVerify: false
      ca:
        secret:
          name: kueue-metrics-server-cert
          key: ca.crt
      cert:
        secret:
          name: kueue-metrics-server-cert
          key: tls.crt
      keySecret:
        name: kueue-metrics-server-cert
        key: tls.key
```

We should add an example in our installation guide to make it clear that we support secure metrics.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-12T16:26:43Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-12T22:55:58Z

/kind documentation

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-14T20:46:38Z

xref: https://github.com/kubernetes-sigs/kueue/issues/4377
