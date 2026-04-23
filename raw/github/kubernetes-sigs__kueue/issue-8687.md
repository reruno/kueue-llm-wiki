# Issue #8687: Create statefulsets with generatedName always produce the same workload name `statefulset--d7705`

**Summary**: Create statefulsets with generatedName always produce the same workload name `statefulset--d7705`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8687

**Last updated**: 2026-03-05T14:30:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lasyard](https://github.com/lasyard)
- **Created**: 2026-01-20T10:35:35Z
- **Updated**: 2026-03-05T14:30:24Z
- **Closed**: 2026-03-05T14:30:24Z
- **Labels**: `kind/bug`
- **Assignees**: [@DavideRutigliano](https://github.com/DavideRutigliano)
- **Comments**: 5

## Description

**What happened**:

Create statefulsets with `kubectl create -f` and `metadata.generateName` in the yaml file. The generated workload is always `statefulset--d7705`, causing severe problem that you cannot run another statefulset with the same yaml file.

**What you expected to happen**:

The second statefulset run smoothly with a different generated name if there is enough resources in the queue.

**How to reproduce it (as minimally and precisely as possible)**:

1. Install kueue 0.15.2 in kubernetes 1.35
2. Enable statefulset by edit configmap `kueue-manager-config` (add `statefulset` to `integrations.frameworks`)
3. Create resourceflavor, clusterqueue, localqueue by `kubectl apply -f rf_cq_lq.yaml`
4. Run `kubectl create -f sleep_sts.yaml`, the statefulset runs successfully
5. Run `kubectl create -f sleep_sts.yaml` again, the new statefulset cannot run (come into READY state)
6. Check the existing workload name is `statefulset--d7705`
7. Delete all statefulset and recreate one, and you can see the name of workload is still `statefulset--d7705`

The mentioned `rf_cq_lq.yaml` file:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
spec:
  nodeLabels:
    node-group: default
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: test
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
    - coveredResources:
        - cpu
        - memory
        - pods
      flavors:
        - name: default
          resources:
            - name: cpu
              nominalQuota: 8
            - name: memory
              nominalQuota: 64Gi
            - name: pods
              nominalQuota: 8
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: default
  name: test
spec:
  clusterQueue: test
```

The mentioned `sleep_sts.yaml` file:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  generateName: sleep-
  labels:
    kueue.x-k8s.io/queue-name: test
spec:
  serviceName: sleep-service
  replicas: 1
  selector:
    matchLabels:
      app: sleep
  podManagementPolicy: Parallel
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
        - image: busybox:1.37.0-glibc
          imagePullPolicy: IfNotPresent
          name: sleep-busybox
          command: ["sh", "-c", "trap exit INT TERM; sleep 30s & wait"]
          resources:
            requests:
              cpu: "1"
              memory: 100Mi
            limits:
              cpu: "1"
              memory: 100Mi
```

**Anything else we need to know?**:

No.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.35.0
- Kueue version (use `git describe --tags --dirty --always`): Installed by `helm install kueue oci://registry.k8s.io/kueue/charts/kueue --version=0.15.2`
- Cloud provider or hardware configuration: 3 Nodes with 16 CPUs, 64GiB memory for each
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.5 LTS
- Kernel (e.g. `uname -a`): 5.15.0-164-generic SMP x86_64 GNU/Linux
- Install tools:
- Others:

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-20T11:22:33Z

Thanks for reporting the issue! I’ve been able to reproduce it locally and will look into it to find a fix.

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-20T11:32:37Z

I think we should change our logic and use PrebuiltWorkload, as we do in LWS. Otherwise, we won’t be able to find a unique name for the workload this way.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-20T16:27:31Z

/assign @DavideRutigliano 

Since he’s already working on it.

/unassign

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-20T16:27:35Z

@IrvingMg: GitHub didn't allow me to assign the following users: DavideRutigliano.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8687#issuecomment-3773814082):

>/assign @DavideRutigliano 
>
>Since he’s already working on it.
>
>/unassign


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@DavideRutigliano](https://github.com/DavideRutigliano) — 2026-01-20T16:49:30Z

/assign
