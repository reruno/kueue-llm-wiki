# Issue #4805: StatefulSet workload is marked finished when all pods are deleted

**Summary**: StatefulSet workload is marked finished when all pods are deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4805

**Last updated**: 2025-12-05T17:28:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-27T06:50:00Z
- **Updated**: 2025-12-05T17:28:58Z
- **Closed**: 2025-12-05T17:28:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

**What happened**:

When I delete all pods of a statefulSet, and the pods succeed, then the workload is marked finished. 

Also, this is inconsistent, because if the Pods fail, then we don't mark the workload as finished.

It is also inconsistent with Jobs, where a deleted Pods is just recreated, but the workload continues to run.

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

1. create the STS: 
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
2. Track the workload status 
3. Delete all pods `kubectl delete --all pods`
Issue: the workload got finished:`kubectl get workloads -w --output-watch-events`

```
> kubectl get workloads -w --output-watch-events                     
EVENT      NAME                                  QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
ADDED      statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True                  12m
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True       True       12m
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True       True       12m
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True       True       12m
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True       True       12m
DELETED    statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True       True       12m
ADDED      statefulset-nginx-statefulset-ed050   user-queue                                         0s
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue                                         0s
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True                  0s
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True                  1s
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True                  2s
MODIFIED   statefulset-nginx-statefulset-ed050   user-queue   cluster-queue   True                  2s
```

The analogous is true for LWS:
```
> kubectl get workloads -w --output-watch-events       
EVENT      NAME                                                     QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
ADDED      leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True                  19s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True       True       33s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True       True       33s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True       True       33s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True       True       33s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True       True       33s
DELETED    leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True       True       33s
ADDED      leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue                                         1s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue                                         1s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True                  1s
MODIFIED   leaderworkerset-leaderworkerset-multi-template-0-57ed8   user-queue   cluster-queue   True                  1s
```

**Anything else we need to know?**:

The fact that the workload is re-created is also a problem (even more important), but hopefully we can decouple the fix to make it easier to track, see my comment here: https://github.com/kubernetes-sigs/kueue/pull/4799/files#r2015748155.

I believe this is the proper fix, but we need an e2e test case for this: https://github.com/kubernetes-sigs/kueue/pull/4799/files#diff-dfb49586a8522fa91d733051fd3b7e4b3ff174907898cf249ab16e2620976a5dR338-R340

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T06:50:36Z

/assign @mbobrovskyi 
As already working on the closely related https://github.com/kubernetes-sigs/kueue/issues/4342

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-25T07:09:52Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-25T07:22:18Z

@mbobrovskyi any progress on that, or the issue is maybe fixed already?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-25T07:22:32Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-25T10:07:27Z

We’ve already fixed this for LWS: https://github.com/kubernetes-sigs/kueue/pull/4790. The StatefulSet PR is still under review: https://github.com/kubernetes-sigs/kueue/issues/4805.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-25T10:31:23Z

/retitle StatefulSet workload is marked finished when all pods are deleted
Scoping to STS since the LWS is solved per https://github.com/kubernetes-sigs/kueue/issues/4805#issuecomment-3004195651

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-23T10:36:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T11:38:10Z

/remove-lifecycle stale
