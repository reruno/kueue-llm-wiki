# Issue #2222: Pod group stuck in QuotaReserved after deactivated

**Summary**: Pod group stuck in QuotaReserved after deactivated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2222

**Last updated**: 2024-05-21T15:02:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-17T17:46:37Z
- **Updated**: 2024-05-21T15:02:00Z
- **Closed**: 2024-05-21T15:02:00Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

**What happened**:

A pod-group workload is stuck in QuotaReserved=True, with Evicted=False, after reaching the backoffLimit, when no replacement pods are sent.

This is likely because of this check
https://github.com/kubernetes-sigs/kueue/blob/ae5aaca92c5bff3c4bf06a0cbe3df2ecd72523fe/pkg/controller/jobframework/reconciler.go#L382

The pod group is considered suspended if there are no replacement pods.

That causes the reconciler to return before this:

https://github.com/kubernetes-sigs/kueue/blob/ae5aaca92c5bff3c4bf06a0cbe3df2ecd72523fe/pkg/controller/jobframework/reconciler.go#L417-L418

**What you expected to happen**:

The Evicted condition to transition to True.

**How to reproduce it (as minimally and precisely as possible)**:

1. Install kueue with the following config:

```yaml
    waitForPodsReady:
      enable: true
      timeout: 30s
      requeuingStrategy:
        timestamp: Eviction
        backoffLimitCount: 1
```

2. Apply `examples/admin/single-clusterqueue-setup.yaml`

3. Run this pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-in-group
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "1"
spec:
  restartPolicy: Never
  nodeSelector:
    foo: doesnotexist
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the leader pod" && sleep 3']
    resources:
      requests:
        cpu: 3
```

**Anything else we need to know?**:

This issue is likely fixed with #2131, so we need to cherry-pick it to the 0.6 release.

But we should also add an integration test for the pod integration that exercises the case of not sending replacement pods.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): `gcr.io/k8s-staging-kueue/kueue:v20240501-v0.6.2-12-g0a69bb7`
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T18:17:17Z

/assign @trasc 

Please check if the issue is fixed with https://github.com/kubernetes-sigs/kueue/pull/2131 and cherry-pick with an accompanying integration test.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-17T18:26:13Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T11:15:36Z

I also looked at this and can confirm that https://github.com/kubernetes-sigs/kueue/pull/2131 is the culprit.

As for cherry-picking, we probably also will need to include: https://github.com/kubernetes-sigs/kueue/pull/2172, and https://github.com/kubernetes-sigs/kueue/pull/2171, which are follow-up fixes.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-20T11:40:25Z

@mimowo I think #2171 is not required, because it's fixing #1955 (for this line https://github.com/kubernetes-sigs/kueue/pull/1955/files#diff-60dd240c20adbd6a189d018d1c216c2d296730f446c341d8bf449fa6657964ffR202).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T11:47:35Z

Ah, ok so https://github.com/kubernetes-sigs/kueue/pull/2171 is fixing code which is only in 0.7. In that case only https://github.com/kubernetes-sigs/kueue/pull/2172
