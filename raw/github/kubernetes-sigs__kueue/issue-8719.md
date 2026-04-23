# Issue #8719: *v1beta1.ResourceFlavor is not convertible to *v1beta2.ResourceFlavor

**Summary**: *v1beta1.ResourceFlavor is not convertible to *v1beta2.ResourceFlavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8719

**Last updated**: 2026-01-22T07:24:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@thejoeejoee](https://github.com/thejoeejoee)
- **Created**: 2026-01-21T14:17:21Z
- **Updated**: 2026-01-22T07:24:52Z
- **Closed**: 2026-01-22T07:24:52Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

Migration v1beta1 -> v2beta2 is broken for existing Resource Flavors

**What you expected to happen**:

ResourceFlavors are converted from v1beta1 to v1beta2

**How to reproduce it (as minimally and precisely as possible)**:

1. install 0.14.8
2. place ResourceFlavor to cluster
3. install 0.15.3
4. get resource flavors
5. k8s API returns: `failed to list resources: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor failed: *v1beta1.ResourceFlavor is not convertible to *v1beta2.ResourceFlavor`

**Anything else we need to know?**:

#7318 enabled conversion for other resource, but ResourceFlavor has been left with no enabled conversion, since this kustomization patch is commented:

https://github.com/kubernetes-sigs/kueue/blob/dc4e0aeedabf0c542724ddb64a373061f2f5c89c/config/components/crd/kustomization.yaml#L18-L27

why is that? the webhook server itself is configured to convert ResourceFlavors:

https://github.com/kubernetes-sigs/kueue/blob/dc4e0aeedabf0c542724ddb64a373061f2f5c89c/pkg/webhooks/webhooks.go#L33-L35

**Environment**:
- Kubernetes version (use `kubectl version`): 1.34
- Kueue version (use `git describe --tags --dirty --always`): 0.14.8/0.15.3
- Cloud provider or hardware configuration: 
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools: 
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T16:38:09Z

cc @sohankunkerkar @mbobrovskyi ptal

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-21T17:09:03Z

~wow! thanks for catching that!~
~This was an oversight during the incremental `v1beta2` migration in PR #7318, which explicitly noted it was "a subset of conversions" with more to follow. ResourceFlavor was left for a follow-up that never happened, and our conversion integration tests only cover Workload, so this gap wasn't caught.~

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T17:30:51Z

hold on, I thought we need conversion we hooks only for resources which changed between v1beta1 and v1beta2. Again, I'm puzzled why we don't see the problem in e2e tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T17:32:39Z

also, we already have users who migrated their environments to v0.15 without reporting the issue. I'm not saying there is no issue, but I'm wondering about the scope of the problem

### Comment by [@thejoeejoee](https://github.com/thejoeejoee) — 2026-01-21T17:42:43Z

> also, we already have users who migrated their environments to v0.15 without reporting the issue. I'm not saying there is no issue, but I'm wondering about the scope of the problem 

probably I should clarify we have our RF versioned as v1beta1, so the issue appeared when existing v1beta1/RF migrated from 0.14.8 CRD to 0.15.3 CRD

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T17:48:06Z

I see, so you essentially forked RF. We don't have policy on supporting forks.

However I think if you port your customizations to v1beta2 so that it remains identical with your v1beta1, then I don't see need for conversion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-21T18:04:44Z

Yeah,  @mimowo is right.

>probably I should clarify we have our RF versioned as v1beta1, so the issue appeared when existing v1beta1/RF migrated from 0.14.8 CRD to 0.15.3 CRD

Can you paste the output for `kubectl get crd resourceflavors.kueue.x-k8s.io -o yaml | grep -A15 "spec:" | head -20`?

In v0.15.x, the CRD should use `strategy: None` by default (no conversion section), which works fine for identical schemas.

### Comment by [@thejoeejoee](https://github.com/thejoeejoee) — 2026-01-22T07:24:52Z

Oh, now I see the issue; our ArgoCD does not applied change `.spec.strategy` to `None` during upgrade, so the webhook configuration stayed there.

That's why it's the same for 0.14.8 and 0.15.3:

```
kubectl get crd resourceflavors.kueue.x-k8s.io -o json | jq '.metadata.annotations["controller-gen.kubebuilder.io/version"], .spec.conversion'
```

```json
"v0.19.0"
{
  "strategy": "Webhook",
  "webhook": {
    "clientConfig": {
      "caBundle": "...",
      "service": {
        "name": "kueue-webhook-service",
        "namespace": "kueue-system",
        "path": "/convert",
        "port": 443
      }
    },
    "conversionReviewVersions": [
      "v1"
    ]
  }
}
```

So no issue here, I'll split the #8722 to upgrade the kueueviz part, but no explicit conversion is needed.
