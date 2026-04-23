# Issue #4342: The workload active.spec field does not work properly for StatefulSet

**Summary**: The workload active.spec field does not work properly for StatefulSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4342

**Last updated**: 2025-12-05T17:28:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-21T11:23:28Z
- **Updated**: 2025-12-05T17:28:58Z
- **Closed**: 2025-12-05T17:28:58Z
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

**What happened**:

When the `spec.active` field is switched to `false` the workload is getting deleted. As the result the workload is  re-created with `spec.active=true`, and re-admitted. This makes the field useless for users, and will also confuse Kueue when trying to deactivate the Workload, for example due to waitForPodsReady.

**What you expected to happen**:

The workload should not be deleted after setting the field to false.

**How to reproduce it (as minimally and precisely as possible)**:

Create the Stateful set, for example:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-statefulset
  labels:
    app: nginx
    kueue.x-k8s.io/queue-name: user-queue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: registry.k8s.io/nginx-slim:0.26
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
  serviceName: "nginx"
```
2. Find the created workload and edit the field to false with `k edit wl`
3. Observe that the workload gets deleted, and the re-created workload is re-admitted.

**Anything else we need to know?**:

I believe the correct solution is to make sure the Workload is owned by the StatefulSet, not just the StatefulSet pods.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T11:24:12Z

/cc @varshaprasad96 @mbobrovskyi 
Created the issue independent of the integration with Notebook. This is problematic for manual suspend, and automated by Kueue using waitForPodsReady (but also ProviRequest).

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-26T12:06:11Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-27T12:09:58Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-27T12:19:00Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-25T12:31:02Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-25T14:11:41Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-23T14:38:18Z

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
