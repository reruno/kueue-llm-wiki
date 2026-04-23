# Issue #8969: Allow configuring KueueViz backend/frontend resource requests and limits

**Summary**: Allow configuring KueueViz backend/frontend resource requests and limits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8969

**Last updated**: 2026-02-04T13:18:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@david-gang](https://github.com/david-gang)
- **Created**: 2026-02-03T18:44:46Z
- **Updated**: 2026-02-04T13:18:35Z
- **Closed**: 2026-02-04T13:18:35Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 4

## Description

The KueueViz backend/frontend deployments have hardcoded resource limits. The backend OOMKills with the default 512Mi in larger clusters.

  Please expose resources in the helm values similar to how controllerManager.manager.resources is already configurable:

```
  kueueViz:
    backend:
      resources:
        requests:
          memory: 512Mi
        limits:
          memory: 1Gi
    frontend:
      resources: {}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T19:06:24Z

This looks quite reasonable and useful, would you like to submit a PR?

### Comment by [@david-gang](https://github.com/david-gang) — 2026-02-03T19:15:34Z

 Yes, I'd be happy to submit a PR when I have some free time.
                                                                                                                                                                                             
  By the way, while testing KueueViz I ran into a couple of other issues that are currently blocking us from using it:

  1. Ingress can't be disabled (#7659) - We use GKE Gateway API, and the unconditionally-created Ingress resources trigger NEG creation with readiness gates on our pods. Is there a
  workaround, or is a fix planned?
  2. No authentication (#5993) - This makes external exposure risky for us.

  For now we're sticking with Grafana + kubectl, but would love to use KueueViz once these are addressed. Just wanted to mention in case there are workarounds I'm missing or if these are on
   the near-term roadmap.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T19:39:23Z

> Ingress can't be disabled (https://github.com/kubernetes-sigs/kueue/issues/7659) - We use GKE Gateway API, and the unconditionally-created Ingress resources trigger NEG creation with readiness gates on our pods. Is there a
workaround, or is a fix planned?

It is not planned, but a contribution is welcome for sure.

> No authentication (https://github.com/kubernetes-sigs/kueue/issues/5993) - This makes external exposure risky for us.

IIUC you are happy with the status quo? Yeah, I think if we provide unauthorized access it would need to be a dedicated configuration, not default.

### Comment by [@david-gang](https://github.com/david-gang) — 2026-02-03T19:49:14Z

> > Ingress can't be disabled ([#7659](https://github.com/kubernetes-sigs/kueue/issues/7659)) - We use GKE Gateway API, and the unconditionally-created Ingress resources trigger NEG creation with readiness gates on our pods. Is there a
> > workaround, or is a fix planned?
> 
> It is not planned, but a contribution is welcome for sure.
> 
> > No authentication ([#5993](https://github.com/kubernetes-sigs/kueue/issues/5993)) - This makes external exposure risky for us.
> 
> IIUC you are happy with the status quo? Yeah, I think if we provide unauthorized access it would need to be a dedicated configuration, not default.

Sorry, I wasn't clear on #5993 - it's the opposite. The current KueueViz has no authentication, which makes it risky to expose externally. We would need auth to be added before we can
  safely use it.
