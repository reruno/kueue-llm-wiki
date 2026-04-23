# Issue #5374: Unable to install kueue v0.12.0 in GKE

**Summary**: Unable to install kueue v0.12.0 in GKE

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5374

**Last updated**: 2025-05-27T16:16:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GonzaloSaez](https://github.com/GonzaloSaez)
- **Created**: 2025-05-27T12:39:00Z
- **Updated**: 2025-05-27T16:16:18Z
- **Closed**: 2025-05-27T16:16:18Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When installing or upgrading to kueue v0.12.0 in GKE standard or autopilot, the following error is returned

```
Error from server (Forbidden): admission webhook "flowcontrol-guardrails.common-webhooks.networking.gke.io" denied the request: can't recognize the priority level configuration "kueue-visibility" used within flow-schema "kueue-visibility
```

**What you expected to happen**:

No error should happen

**How to reproduce it (as minimally and precisely as possible)**:

- Create a GKE cluster (standard or autopilot)
- Obtain the credentials for the newly created GKE cluster
- `kubectl apply -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.12.0/manifests.yaml`

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.31.x
- Kueue version (use `git describe --tags --dirty --always`): v0.12.0
- Cloud provider or hardware configuration: GKE
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T12:43:35Z

cc @mwysokin @mbobrovskyi @tenzen-y 
Some details are on the slack discussion https://kubernetes.slack.com/archives/C032ZE66A2X/p1748328823580939

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T13:06:49Z

I think if this is problematic to fix then I would suggest to make the configuration opt-in,  basically revert https://github.com/kubernetes-sigs/kueue/pull/5043

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T13:42:10Z

I have also reproduced this on my cluster

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T15:19:57Z

cc @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-27T15:24:14Z

> I think if this is problematic to fix then I would suggest to make the configuration opt-in, basically revert [#5043](https://github.com/kubernetes-sigs/kueue/pull/5043)

I discussed with @mimowo offline.
In conclusion, we agreed to revert https://github.com/kubernetes-sigs/kueue/pull/5043.
However, we should mention the recommendation to install APF manifests in our documentation when they want to enable Visibility On-Demand.
If they do not install them, the visibility requests could occupy the API Server global seats, which could lead to cluster disruption in some situations.
