# Issue #2084: Missing some validations for ConfigAPI

**Summary**: Missing some validations for ConfigAPI

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2084

**Last updated**: 2024-05-29T06:04:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-04-27T08:01:49Z
- **Updated**: 2024-05-29T06:04:13Z
- **Closed**: 2024-05-29T06:04:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The kubebuiler or controller-gen markers wouldn't work well since the ConfigAPI is not CRD.
So, we need to implement validations by ourselves, but we don't have some validations at the following APIs:

- [x] MultiKueue: #2129
https://github.com/kubernetes-sigs/kueue/blob/5401a3b55c15098795d22d0c61ddae40bdc6bf25/apis/config/v1beta1/configuration_types.go#L205-L225
- [x] InternalCertManagement: #2169
https://github.com/kubernetes-sigs/kueue/blob/5401a3b55c15098795d22d0c61ddae40bdc6bf25/apis/config/v1beta1/configuration_types.go#L271-L284
- [ ] ClusterQueueVisibility: #2309
https://github.com/kubernetes-sigs/kueue/blob/f108fef22eb4532f3918754e5a08226ac366343c/apis/config/v1beta1/configuration_types.go#L347-L354
- [x] waitForPodsReady: #2214
https://github.com/kubernetes-sigs/kueue/blob/cfd576f98e47c901e8bba25a01b4098b142cccd3/apis/config/v1beta1/configuration_types.go#L184-L196

**What you expected to happen**:
Once the KueueConfig with invalid parameters is created, the kueue-controller-manager raises the errors and stops working during booting manager.

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-27T08:01:56Z

/assign
