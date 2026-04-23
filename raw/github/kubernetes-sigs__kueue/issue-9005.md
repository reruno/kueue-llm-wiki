# Issue #9005: Metrics TLS secret not hot-reloaded

**Summary**: Metrics TLS secret not hot-reloaded

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9005

**Last updated**: 2026-02-10T17:06:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2026-02-05T12:09:02Z
- **Updated**: 2026-02-10T17:06:05Z
- **Closed**: 2026-02-10T17:06:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 1

## Description

**What happened**:

The kueue-controller-manager is failing to reload updated TLS certificates for its metrics endpoint. When cert-manager renews the certificate the controller continues to use the old, expired certificate. This results in "bad TLS handshake" errors during metrics scraping.

**What you expected to happen**:

The kueue-controller-manager should watch the mounted TLS secret and hot-reload the certificates when they are updated on disk, or the operator should trigger a rollout of the controller pods to pick up the new secret.

**How to reproduce it (as minimally and precisely as possible)**:

Deploy Kueue (v0.14/v0.15) on a cluster with cert-manager.
Configure a Certificate for the metrics endpoint (e.g., metrics-server-cert).
Wait for the certificate to reach its renewal window or manually trigger a renewal via cmctl renew.
Observe that the metrics-server-cert Secret is updated with new data.
The scrape fails with a TLS handshake error because the manager is still serving the previous certificate.
Restarting the kueue-controller-manager pod fixes the issue.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):  1.30
- Kueue version (use `git describe --tags --dirty --always`): v0.14/v0.15
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2026-02-05T12:24:23Z

/assign
