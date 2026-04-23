# Issue #8190: Provide the ability to configure TLS settings like TLSMinVersion and Ciphersuites on kueue servers

**Summary**: Provide the ability to configure TLS settings like TLSMinVersion and Ciphersuites on kueue servers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8190

**Last updated**: 2026-01-23T15:25:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-12-11T20:48:32Z
- **Updated**: 2026-01-23T15:25:30Z
- **Closed**: 2026-01-23T15:25:30Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

All kueue apiservers (webhooks, metrics, controller, visibility) should provide an ability to set tls min versions and cipher suite.

There should be a configuration that allows one to set minTLSVersion and ciphersuites for servers that we pass into the TLSOpts for apiservers.

**Why is this needed**:

In a Go project, explicitly configuring the accepted TLS ciphers and the minimum TLS version, typically using a tls.Config struct, is crucial for security, compatibility, and compliance.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-15T16:12:55Z

KEP: https://github.com/kubernetes-sigs/kueue/pull/8246

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T07:52:12Z

ack, tentatively adding to the plan for 0.16: https://github.com/kubernetes-sigs/kueue/issues/8019

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:36:36Z

/priority important-soon
