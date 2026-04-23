# Issue #3150: Cannot fix a broken kueue-controller-manager deplyment.

**Summary**: Cannot fix a broken kueue-controller-manager deplyment.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3150

**Last updated**: 2024-10-01T17:47:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2024-09-27T09:08:54Z
- **Updated**: 2024-10-01T17:47:51Z
- **Closed**: 2024-10-01T17:47:51Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

Having a broken kueue-controller-manager deployment and attempting to fix it resulted in:

```
error: deployments.apps "kueue-controller-manager" could not be patched: Internal error occurred: failed calling webhook "vdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/validate-apps-v1-deployment?timeout=10s": dial tcp 10.110.43.165:443: connect: connection refused
```

**What you expected to happen**:

Be able to fix the deployment.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

For pods, a similar situation was fixed with:
https://github.com/kubernetes-sigs/kueue/blob/425ece197331d6b0c9b6d2bf4cc82326420c9f0a/config/components/webhook/kustomization.yaml#L8-L36

and 
- https://github.com/kubernetes-sigs/kueue/pull/1247

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-09-27T09:09:06Z

/assign
