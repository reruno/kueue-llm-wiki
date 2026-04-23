# Issue #5118: Improve Rolling Updates

**Summary**: Improve Rolling Updates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5118

**Last updated**: 2025-04-25T23:18:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Gab-Menezes](https://github.com/Gab-Menezes)
- **Created**: 2025-04-25T05:36:33Z
- **Updated**: 2025-04-25T23:18:02Z
- **Closed**: 2025-04-25T23:18:01Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**: Rolling Updates on resource constrained environments to not disturb other workloads.

**Why is this needed**: Rolling Updates, can behave weird (but still the intended behavior) when you are running close the the queue limits.

For example:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  preemption:
    withinClusterQueue: LowerPriority
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 3
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: prod-priority
value: 1000
description: "Priority class for prod jobs"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: dev-priority
value: 100
description: "Priority class for development jobs"
```

Now create 2 workloads, one with higher priority than the other:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-1
  labels:
    app: nginx
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/priority-class: dev-priority
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
          image: registry.k8s.io/nginx-slim:0.27
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "500m"
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-2
  labels:
    app: nginx
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/priority-class: prod-priority
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
          image: registry.k8s.io/nginx-slim:0.27
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "500m"
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 0
```

In the current system doing `kubectl rollout restart deployment nginx-deployment-2` will disturb `nginx-deploymen-1` pods, even though it's possible not to. Since Kubernetes allows new pods to be created while the old ones are in `Terminating` state this leads to a unnecessary disruption of `nginx-deploymen-1`.

If instead we somehow only admit a new pod after the old one is completely delete this would avoid the problem. Or maybe allow for rolling update to slightly exceed the nominal quota, because in this case the new pod would get to a ready state avoiding disturbing other pods.

I know this is kinda the intended behavior and not a bug. I also know that if you are running your queues == cluster capacity this will not help, because even though the pod is admitted it might no have resources to schedule (only if the pod has higher priority and is allowed to evict other pods).

Also it should be obvious but still a gotcha: if for example `maxUnavailable: 0` and `maxSurge: 1` will lead to a deadlock state, so maybe worth documenting.

**Completion requirements**: A system/feature flag that allows Rolling Updates to not disturb other pods.

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-25T19:49:06Z


> If instead we somehow only admit a new pod after the old one is completely delete this would avoid the problem. Or maybe allow for rolling update to slightly exceed the nominal quota, because in this case the new pod would get to a ready state avoiding disturbing other pods.

https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/3973-consider-terminating-pods-deployment

### Comment by [@Gab-Menezes](https://github.com/Gab-Menezes) — 2025-04-25T23:18:01Z

Fair, closing the issue
