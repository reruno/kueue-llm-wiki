# Issue #9650: Visibility Server ignores APIServer flags, breaking out-of-cluster execution and custom port binding

**Summary**: Visibility Server ignores APIServer flags, breaking out-of-cluster execution and custom port binding

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9650

**Last updated**: 2026-03-17T16:23:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Nilsachy](https://github.com/Nilsachy)
- **Created**: 2026-03-03T11:14:01Z
- **Updated**: 2026-03-17T16:23:47Z
- **Closed**: 2026-03-17T16:23:47Z
- **Labels**: `kind/bug`
- **Assignees**: [@Nilsachy](https://github.com/Nilsachy)
- **Comments**: 1

## Description

**What happened**:

When attempting to run the `kueue-controller-manager` with the `VisibilityOnDemand` feature enabled and using a custom kubeconfig via the `--kubeconfig` flag, the visibility server fails to start.

It throws the following error:

```
Unable to create and start visibility server","error":"unable to apply VisibilityServerOptions: failed to get delegated authentication kubeconfig: failed to get delegated authentication kubeconfig: unable to load in-cluster configuration, KUBERNETES_SERVICE_HOST and KUBERNETES_SERVICE_PORT must be defined
```

If KUBERNETES_SERVICE_HOST and KUBERNETES_SERVICE_PORT are mocked, the error changes to:

```
open /var/run/secrets/kubernetes.io/serviceaccount/token: no such file or directory
Because the visibility server does not parse the controller's flags or expose its own genericapiserver flags, parameters like the kubeconfig path for delegated authentication and the bind port (8082) are completely ignored or hardcoded.
```

**What you expected to happen**:

The embedded visibility server should respect the flags passed to the controller manager (or expose standard APIServer flags like `--authentication-kubeconfig` and `--secure-port`). This would allow running the controller out-of-cluster for development/testing, and allow administrators to customize the visibility server's bind port.

**How to reproduce it (as minimally and precisely as possible)**:

Enable the `VisibilityOnDemand` feature gate.

Attempt to run the `kueue-controller-manager` locally (out-of-cluster) using a custom kubeconfig:

```Bash
./kueue-controller-manager --kubeconfig=/path/to/my/kubeconfig
```
Observe the startup crash from the visibility server attempting to load in-cluster credentials.

**Anything else we need to know?**:

Following discussions in [#8761](https://github.com/kubernetes-sigs/kueue/pull/8761#issuecomment-3983891127) reusing `--kubeconfig` by default seems reasonable for simplicity of users, which is done in PR #9619. For other flags, a more systematic approach is necessary, which is what this bug is intended for.

## Discussion

### Comment by [@Nilsachy](https://github.com/Nilsachy) — 2026-03-03T11:30:51Z

/assign
