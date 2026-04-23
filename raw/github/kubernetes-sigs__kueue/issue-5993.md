# Issue #5993: KueueViz without authorized at all

**Summary**: KueueViz without authorized at all

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5993

**Last updated**: 2026-03-06T16:44:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samzong](https://github.com/samzong)
- **Created**: 2025-07-16T07:10:55Z
- **Updated**: 2026-03-06T16:44:22Z
- **Closed**: 2026-03-06T16:44:22Z
- **Labels**: `kind/feature`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Kubeviz current without add authorized by api call to get kueue resource.

suppport need add it?

**Why is this needed**:

If we want open the dashboard for more user, we may need to consider security.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-17T06:42:28Z

/area dashboard

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-18T10:10:30Z

/retitle KueueViz without authorized at all

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-16T10:17:03Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T10:22:16Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-14T11:10:44Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T19:57:59Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T19:58:36Z

This is mentioned as important also by another user: https://github.com/kubernetes-sigs/kueue/issues/8969#issuecomment-3843317685

It would be great if we can find a contributor

### Comment by [@samzong](https://github.com/samzong) — 2026-02-04T00:50:06Z

Hi @mimowo, This is my created! I think I can go on make auth support for KueueViz. 

Write some proposal:

### Summary

Add optional **Bearer Token** auth to KueueViz backend using k8s SA tokens validated via the **TokenReview API**. This follows the same auth model as **[Kubernetes Dashboard](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/README.md)**. (in frontend add login view like Kubernetes Dashboard)

### Proposed Design

```bash
User → [Token] → KueueViz Backend → [TokenReview API] → K8s API Server
↓
Authenticated? → Yes → Serve request
→ No  → 401 Unauthorized
```

**Key decisions:**

| Aspect | Proposal |
|--------|----------|
| Auth Method | ServiceAccount tokens |
| Validation | Kubernetes TokenReview API |
| Default | **Disabled** (backward compatible) |
| Config | `KUEUEVIZ_AUTH_ENABLED=true` env var |
| WebSocket Auth | query param (`?token=xxx`) or Sec-WebSocket-Protocol |

**Backend changes:**
- New `middleware/auth.go` with `TokenAuthMiddleware`
- Requires `kubernetes.Interface` to call TokenReview API
- Extract token from `Authorization: Bearer <token>` header or `?token=` query param

**Helm values adds:**
```yaml
kueueViz:
  backend:
    auth:
      enabled: false  # opt-in
```

### some question

- Is **Bearer Token + TokenReview API** the right approach?
- Should auth be a feature gate or just env var? I'm proposing env var, becauese KueueViz is a optional.
- WebSocket token handling - query param (?token=xxx) is simple but exposes token in logs. Should I implement Sec-WebSocket-Protocol based auth instead? (maybe new PR to enhanced)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T09:46:17Z

> Is Bearer Token + TokenReview API the right approach?

IIUC this is the standard native mechanism, so it sounds reasonable. If there are alternatives we could compare pros & cons.

> Should auth be a feature gate or just env var? I'm proposing env var, becauese KueueViz is a optional.

Yeah, we would need to have feature gates for KueueViz and so env sounds reasonable.

> WebSocket token handling - query param (?token=xxx) is simple but exposes token in logs. 

Good question, I think we could avoid logging the token still inside the backend, for example by some string replacement TOKEN -> "xyz". wdyt?

> Should I implement Sec-WebSocket-Protocol based auth instead? (maybe new PR to enhanced)

Is is also Token-based, or another approach?
