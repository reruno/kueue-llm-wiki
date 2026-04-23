# Issue #4967: Can't set queue-name in LeaderWorkerSet.

**Summary**: Can't set queue-name in LeaderWorkerSet.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4967

**Last updated**: 2026-04-14T05:46:49Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-14T16:50:34Z
- **Updated**: 2026-04-14T05:46:49Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 14

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When I'm trying to set queue-name on LeaderWorkerSet with `managedJobWithoutQueueName=true` I get `field is immutable` error.

```
Error from server (Forbidden): error when applying patch:
{"metadata":{"annotations":{"kubectl.kubernetes.io/last-applied-configuration":"{\"apiVersion\":\"leaderworkerset.x-k8s.io/v1\",\"kind\":\"LeaderWorkerSet\",\"metadata\":{\"annotations\":{},\"labels\":{\"app\":\"nginx\",\"kueue.x-k8s.io/queue-name\":\"user-queue\"},\"name\":\"nginx-leaderworkerset\",\"namespace\":\"default\"},\"spec\":{\"leaderWorkerTemplate\":{\"leaderTemplate\":{\"spec\":{\"containers\":[{\"image\":\"registry.k8s.io/nginx-slim:0.27\",\"name\":\"nginx-leader\",\"ports\":[{\"containerPort\":80}],\"resources\":{\"requests\":{\"cpu\":\"100m\"}}}]}},\"size\":3,\"workerTemplate\":{\"spec\":{\"containers\":[{\"image\":\"registry.k8s.io/nginx-slim:0.27\",\"name\":\"nginx-worker\",\"ports\":[{\"containerPort\":80}],\"resources\":{\"requests\":{\"cpu\":\"200m\"}}}]}}},\"replicas\":3}}\n"},"labels":{"kueue.x-k8s.io/queue-name":"user-queue"}},"spec":{"leaderWorkerTemplate":{"leaderTemplate":{"spec":{"containers":[{"image":"registry.k8s.io/nginx-slim:0.27","name":"nginx-leader","ports":[{"containerPort":80}],"resources":{"requests":{"cpu":"100m"}}}]}},"workerTemplate":{"spec":{"containers":[{"image":"registry.k8s.io/nginx-slim:0.27","name":"nginx-worker","ports":[{"containerPort":80}],"resources":{"requests":{"cpu":"200m"}}}]}}}}}
to:
Resource: "leaderworkerset.x-k8s.io/v1, Resource=leaderworkersets", GroupVersionKind: "leaderworkerset.x-k8s.io/v1, Kind=LeaderWorkerSet"
Name: "nginx-leaderworkerset", Namespace: "default"
for: "testbin/demo/sample-leaderworkerset.yaml": error when patching "testbin/demo/sample-leaderworkerset.yaml": admission webhook "vleaderworkerset.kb.io" denied the request: metadata.labels[kueue.x-k8s.io/queue-name]: Invalid value: "user-queue": field is immutable
```

**What you expected to happen**:

Allow setting the queue-name when `managedJobWithoutQueueName=true` and no queue name is specified

**How to reproduce it (as minimally and precisely as possible)**:

1. Apply kueue manifests with `managedJobWithoutQueueName=true`.

2. Create LeaderWorkerSet without queue-name.

```yaml
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: nginx-leaderworkerset
  labels:
    app: nginx
spec:
  replicas: 3
  leaderWorkerTemplate:
    size: 3
    leaderTemplate:
      spec:
        containers:
          - name: nginx-leader
            image: registry.k8s.io/nginx-slim:0.27
            resources:
              requests:
                cpu: "100m"
            ports:
              - containerPort: 80
    workerTemplate:
      spec:
        containers:
          - name: nginx-worker
            image: registry.k8s.io/nginx-slim:0.27
            resources:
              requests:
                cpu: "200m"
            ports:
              - containerPort: 80
```


3. Set queue-name on LeaderWorkerSet.

```yaml
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: nginx-leaderworkerset
  labels:
    app: nginx
    kueue.x-k8s.io/queue-name: user-queue
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.2
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T07:42:33Z

Is it to support the LQ defaulting?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-15T07:56:14Z

> Is it to support the LQ defaulting?

Currently, it only works during creation.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-16T12:46:02Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-15T13:35:41Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T06:30:42Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-14T06:48:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T06:55:55Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-12T07:51:20Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T08:16:09Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-12T08:57:46Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-04-13T05:17:17Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-13T08:38:38Z

@mbobrovskyi I know there have been many bugfixes to LWS recently, do you know if this bug remains?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-04-14T05:43:16Z

Yes, it’s still present. We don’t allow updating queueName at all.

https://github.com/kubernetes-sigs/kueue/blob/b89dae018b31ca32eed282040e19eceee09941f9/pkg/controller/jobs/leaderworkerset/leaderworkerset_webhook.go#L166-L170

However, for a StatefulSet, we allow it if it is suspended:

https://github.com/kubernetes-sigs/kueue/blob/b89dae018b31ca32eed282040e19eceee09941f9/pkg/controller/jobs/statefulset/statefulset_webhook.go#L152-L157

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-04-14T05:46:49Z

I already created PR https://github.com/kubernetes-sigs/kueue/pull/4932.
