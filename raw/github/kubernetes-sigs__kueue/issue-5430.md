# Issue #5430: Inconsistent `certDir` handling between Kueue configuration and cert-manager rotator.

**Summary**: Inconsistent `certDir` handling between Kueue configuration and cert-manager rotator.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5430

**Last updated**: 2025-06-04T04:28:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-05-31T00:38:07Z
- **Updated**: 2025-06-04T04:28:39Z
- **Closed**: 2025-06-04T04:28:39Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

Currently, Kueue allows configuring an alternative `webhook.certDir` via the manager configuration.
However, the internal cert-manager rotator still uses the default constant value:
`/tmp/k8s-webhook-server/serving-certs`.

As a result, if `webhook.certDir` is set to a custom value in the configuration, the Kueue manager fails to start successfully. This issue is particularly impactful when running the Kueue manager with webhook support in local mode, where custom certificate paths are often required.

Expected behavior:
When a custom webhook.certDir is configured, the cert-manager rotator should respect and use that same directory, ensuring compatibility and successful startup.


**What happened**:
The Kueue manager failed to start when a custom (non-default) `certDir` was specified.

**What you expected to happen**:
The Kueue manager should start successfully with the provided custom `certDir`.

**How to reproduce it (as minimally and precisely as possible)**:
Start the Kueue manager with a configuration that sets webhook.certDir to a custom path (different from the default `/tmp/k8s-webhook-server/serving-certs`).

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-31T17:09:29Z

Thanks for reporting this! Do you want to investigate ways to fix this?
