# Issue #6719: Modified resource activates deactivated Workload

**Summary**: Modified resource activates deactivated Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6719

**Last updated**: 2026-01-05T15:06:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sutaakar](https://github.com/sutaakar)
- **Created**: 2025-09-03T17:44:13Z
- **Updated**: 2026-01-05T15:06:41Z
- **Closed**: 2026-01-05T15:06:41Z
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I have created PyTorchJob CR managed by Kueue, stopped the training by setting corresponding Workload `.spec.active` flag to `false`. However when I modified the PyTorchJob then corresponding Workload gets activated again.

**What you expected to happen**:
I was expecting Workload related to modified PyTorchJob to stay deactivated.

**How to reproduce it (as minimally and precisely as possible)**:
Install latest Training operator : `kubectl apply --server-side -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.9.3"`
Setup sample Kueue resources:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default-flavor
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory", "pods"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
      - name: "pods"
        nominalQuota: 5
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: lq
spec:
  clusterQueue: cluster-queue 
```

Create sample PyTorchJob:
```
apiVersion: "kubeflow.org/v1"
kind: "PyTorchJob"
metadata:
  name: "pytorch-sleep-job-small"
  labels:
    kueue.x-k8s.io/queue-name: lq
spec:
  pytorchReplicaSpecs:
    Worker:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: python:3.9-alpine
              command:
                - "python"
                - "-c"
                - "import time; print('Container started with small image, sleeping for 60s...'); time.sleep(60); print('Done sleeping.')"
```

Once corresponding training Pod starts stop the corresponding Workload:
```
for wl in $(kubectl get workload -n default -o jsonpath='{.items[*].metadata.name}'); do kubectl patch workload $wl -n default --type merge -p '{"spec":{"active":false}}'; done
```

Scale PyTorchJob:
```
kubectl patch pytorchjob pytorch-sleep-job-small --type merge -p '{"spec":{"pytorchReplicaSpecs":{"Worker":{"replicas":2}}}}'
```

Workload gets activated again.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.2
- Kueue version (use `git describe --tags --dirty --always`): v0.13.3
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): Fedora 42
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-03T17:54:34Z

Thanks for reporting

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-02T17:59:26Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T12:20:20Z

It seems this is likely fixed by https://github.com/kubernetes-sigs/kueue/issues/6711

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T12:21:08Z

wdyt @Singularity23x0 @olekzabl ?
