# Issue #9210: Wrong pod placement when node replacement is performed

**Summary**: Wrong pod placement when node replacement is performed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9210

**Last updated**: 2026-02-16T12:50:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2026-02-13T09:22:52Z
- **Updated**: 2026-02-16T12:50:04Z
- **Closed**: 2026-02-16T12:50:04Z
- **Labels**: `kind/bug`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 1

## Description

**What happened**:

Let's consider the following scenario:

Topology:
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Topology
metadata:
  name: "default"
spec:
  levels:
  - nodeLabel: "cloud.provider.com/topology-block"
  - nodeLabel: "cloud.provider.com/topology-rack"
  - nodeLabel: "kubernetes.io/hostname"
```

Node	Topology
node1	"b1", "r1", "node1"
node2	"b1", "r1", "node2"
node3	"b1", "r1", "node3"

Jobset:
```yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: tas-jobset
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  replicatedJobs:
  - name: workers
    replicas: 1
    template:
      spec:
        parallelism: 2
        completions: 2
        backoffLimit: 10
        template:
          metadata:
            annotations:
              kueue.x-k8s.io/podset-required-topology: cloud.provider.com/topology-block
          spec:
            containers:
            - name: sleep
              image: busybox
              command: ["sleep", "100000"]
              resources:
                requests:
                  cpu: "40"
            restartPolicy: Never
```

Here's the current flow of the process:

- The 2 pods of the jobset land on `node1` and `node2`
- `node1` enters into `NotReady` state
- a pod running on the `node1` moves into terminating state
- `node_failure_controller` reacts on the change and executes node replacement procedure and `node3` is chosen as a replacement for `node1`. So the new topology assignment is [`node2`, `node3`]

The Terminating pod on the NotReady node will probably not be removed quickly because of nature of the problem with NotReady state (connection issues, kubelet problems etc.).

When the replacement pods are created they are given a scheduling gate and are handled by topology ungater - https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L160.

- `Reconcile` is called - https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L160
- https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L222 all non terminated pods are listed (Terminating pods are included in the list)
- we start assigning pods to domains - https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L243
- we try to read ranks from labels - https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L446 but it fails here https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L489 because the terminating pod occupies index 0. Because of that we fallback to greedy assignment - https://github.com/kubernetes-sigs/kueue/blob/bf5ff17e5a02c6af61509b96bbb268d4ef48fbce/pkg/controller/tas/topology_ungater.go#L354
- the pods are correctly assigned to [`node2`, node3`]

The problem is that if the terminating pod wasn't there then reading ranks from labels would succeed and we would end up with the replacement pod assigned to `node2` and the final result would be the following: `pod1` -> node2, `pod2` -> `node2`. That's because the `pod2` was running undisrupted and only the `pod1` needed to be ungated.

**What you expected to happen**:

I would expect the process to behave the same in both situations: with and without the terminating pod

**How to reproduce it (as minimally and precisely as possible)**:

Discovered when testing https://github.com/kubernetes-sigs/kueue/pull/8964 - here pods are removed quickly enough so the Terminating pods are not included when assigning domains to pods.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T10:40:28Z

/assign @j-skiba
