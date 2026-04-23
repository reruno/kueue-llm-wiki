# Issue #4850: Facing TLS error for Topology webhook

**Summary**: Facing TLS error for Topology webhook

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4850

**Last updated**: 2025-04-07T07:10:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@hy00nc](https://github.com/hy00nc)
- **Created**: 2025-04-01T02:07:31Z
- **Updated**: 2025-04-07T07:10:46Z
- **Closed**: 2025-04-07T07:10:46Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

After upgrading to v0.11, `kubectl get` for Topology resource is failing due to TLS certificate error. This does not happen when there are no Topology resource in the cluster, but when I create one, I fail to get it.
```yaml
# Example Topology resource created
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "default"
```
```bash
# Try to get topology resource from cluster
$ kubectl get topology                                   
Error from server: conversion webhook for kueue.x-k8s.io/v1alpha1, Kind=Topology failed: Post "https://kueue-webhook-service.mlops-services.svc:443/convert?timeout=30s": tls: failed to verify certificate: x509: certificate signed by unknown authority
```
Note that `kubectl create` is working fine. It seems to be related to new apiversion beta1v1?
Other resource, such as ResourceFlavor, does not face any issue.

Moroever, I also see a lot of TLS error in the controller logs:
```text
2025/03/31 23:55:55 http: TLS handshake error from 172.17.0.3:32593: remote error: tls: bad certificate
```

**What you expected to happen**:

Being able to send GET requests for Topology and no TLS error log in the controller.

**How to reproduce it (as minimally and precisely as possible)**:
Install Kueue v0.11.2 via Helm chart (using internalcert) and try to get Topology resources.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.29.4
- Kueue version (use `git describe --tags --dirty --always`): v0.11.2

## Discussion

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T06:36:45Z

I saw the same issue. I had to use the beta API to avoid these TLS errors

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-03T08:13:14Z

I'm wondering if this issue is maybe related to https://github.com/kubernetes-sigs/kueue/pull/4858. Are you in position to check that?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-03T09:31:37Z

Oh, this might be all related to the fact that somehow you end up with v1beta1 version of the topology API, as also discussed in https://github.com/kubernetes-sigs/kueue/issues/4861.

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T09:55:00Z

This is probably happening because the helm charts have conversion enabled for the topology CRD. Setting the strategy to None could fix this. There's no webhook for topologies being installed.

```
  conversion:
    strategy: Webhook
    webhook:
      clientConfig:
        service:
          name: {{ include "kueue.fullname" . }}-webhook-service
          namespace: '{{ .Release.Namespace }}'
          path: /convert
      conversionReviewVersions:
      - v1
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-04T07:06:19Z

It also interesting that on `kubectl api-resources` topologies using `kueue.x-k8s.io/v1beta1` API version.

```
kubectl api-resources                                                                                                 
NAME                                SHORTNAMES          APIVERSION                        NAMESPACED   KIND
topologies                                              kueue.x-k8s.io/v1beta1            false        Topology
```
