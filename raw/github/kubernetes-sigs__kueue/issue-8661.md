# Issue #8661: TAS without Group: TopologyUngator can not recognize rank-based ordering for LWS multi templates instance

**Summary**: TAS without Group: TopologyUngator can not recognize rank-based ordering for LWS multi templates instance

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8661

**Last updated**: 2026-02-19T13:17:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-19T12:44:39Z
- **Updated**: 2026-02-19T13:17:39Z
- **Closed**: 2026-02-19T13:17:39Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When I created a LWS with multiple templates, Kueue failed to assign topology to Pods based on the rank ordering (`leaderworkerset.sigs.k8s.io/worker-index`) as you can see kueue-controller-manager logs in the following:

```shell
{"level":"error","ts":"2026-01-19T12:23:58.569552553Z","caller":"tas/topology_ungater.go:415","msg":"failed to read rank information from Pods","controller":"tas_topology_ungater","namespace":"default","name":"leaderworkerset-leaderworkerset-multi-template-0-479d6","reconcileID":"cafe6005-621e-4f39-87ad-eb57a458c1b1","error":"incorrect label value \"3\" for Pod \"default/leaderworkerset-multi-template-0-3\": validation error: value should be less than 3","stacktrace":"sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable\n\t/workspace/pkg/controller/tas/topology_ungater.go:415\nsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains\n\t/workspace/pkg/controller/tas/topology_ungater.go:330\nsigs.k8s.io/kueue/pkg/controller/tas.(*topologyUngater).Reconcile\n\t/workspace/pkg/controller/tas/topology_ungater.go:222\nsigs.k8s.io/kueue/pkg/controller/core.(*leaderAwareReconciler).Reconcile\n\t/workspace/pkg/controller/core/leader_aware_reconciler.go:77\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
```

Especially this one: 
`"msg":"failed to read rank information from Pods","controller":"tas_topology_ungater","namespace":"default","name":"leaderworkerset-leaderworkerset-multi-template-0-479d6"`

The root cause is described in https://github.com/kubernetes-sigs/kueue/issues/8471. Please follow the pointed issue.

> [!NOTE]
> This happened only when TAS was used without Group scheduling. So, TAS with Group will not get this problem.

**What you expected to happen**:

TAS succeded to assign topologies to Pods based on rank ordering (`leaderworkerset.sigs.k8s.io/worker-index`).

**How to reproduce it (as minimally and precisely as possible)**:

The following is a step-by-step reproducible flow:

1. Setup cluster, Kueue, and LWS Operator

```shell
$ kind create cluster

$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.15.2/manifests.yaml

$ cat <<EOF | kubectl apply -f -
apiVersion: kueue.x-k8s.io/v1beta2
kind: Topology
metadata:
  name: "default"
spec:
  levels:
  - nodeLabel: "kubernetes.io/hostname"
---
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta2
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    kubernetes.io/os: linux
  topologyName: "default"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "tas-cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 100
      - name: "memory"
        nominalQuota: 100Gi
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "default"
  name: "tas-user-queue"
spec:
  clusterQueue: "tas-cluster-queue"
EOF

$ kubectl apply --server-side -f https://raw.githubusercontent.com/kubeflow/mpi-operator/v0.7.0/deploy/v2beta1/mpi-operator.yaml
```

2. Enable LWS integration in kueue-config ConfigMap

3. Create LWS with multiple templates

```shell
$ cat <<EOF | kubectl apply -f -
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: leaderworkerset-multi-template
  labels:
    kueue.x-k8s.io/queue-name: "tas-user-queue"
spec:
  replicas: 1
  leaderWorkerTemplate:
    leaderTemplate:
      spec:
        containers:
        - name: nginx2
          image: nginxinc/nginx-unprivileged:1.27
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
    size: 4
    workerTemplate:
      spec:
        containers:
        - name: nginx
          image: nginxinc/nginx-unprivileged:1.27
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
EOF
```

**Anything else we need to know?**:

This is a sibling issue as https://github.com/kubernetes-sigs/kueue/issues/8471

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T12:45:14Z

cc @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T12:48:17Z

The root reason why we keep missing this problem is https://github.com/kubernetes-sigs/kueue/issues/8634.
Once we refined the above UTs, we can keep tracking if these mechanisms (TAS without Group with rank-ordering) work well.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T12:50:46Z

Great point, it would be great to adjust the unit tests so that we have a reliable validation before e2e tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:23:47Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T19:58:21Z

Indeed, I'm working on this.
/assign
