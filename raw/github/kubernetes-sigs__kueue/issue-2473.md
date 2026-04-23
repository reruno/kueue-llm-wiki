# Issue #2473: Panic when FairSharing is enabled without preemption

**Summary**: Panic when FairSharing is enabled without preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2473

**Last updated**: 2024-06-24T14:38:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@xmolitann](https://github.com/xmolitann)
- **Created**: 2024-06-24T09:12:19Z
- **Updated**: 2024-06-24T14:38:25Z
- **Closed**: 2024-06-24T14:38:23Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When I enable FairSharing without preemption, I'm getting a `Observed a panic: "invalid memory address or nil pointer dereference" (runtime error: invalid memory address or nil pointer dereference)`. This happens even when there are no Workloads that would match the configuration.  See included logs [kueue-controller-manager.json](https://github.com/user-attachments/files/15952629/kueue-controller-manager.json) This also happens on both images: `gcr.io/k8s-staging-kueue/kueue:v20240619-v0.7.0-8-gaa682c90` and `gcr.io/k8s-staging-kueue/kueue:v0.7.0`

**What you expected to happen**:
kueue-controller-manager is not stuck in CrashLoopBackOff with a panic and new workloads are admitted.

**How to reproduce it (as minimally and precisely as possible)**:
ConfigMap
```apiVersion: v1
data:
  controller_manager_config.yaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    fairSharing:
      enable: true
      preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8080
    # enableClusterQueueResources: true
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: c1f6bfd2.kueue.x-k8s.io
    controller:
      groupKindConcurrency:
        Job.batch: 100
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 100
      burst: 200
    #pprofBindAddress: :8082
    #waitForPodsReady:
    #  enable: true
    #manageJobsWithoutQueueName: true
    #internalCertManagement:
    #  enable: false
    #  webhookServiceName: ""
    #  webhookSecretName: ""
    integrations:
      frameworks:
      - "batch/job"
      - "pod"
      podOptions:
        namespaceSelector:
          matchExpressions:
            - key: kubernetes.io/metadata.name
              operator: NotIn
              values: [ "cattle-system", "calico-system", "cattle-monitoring-system", "cattle-logging-system", "cattle-provisioning-capi-system", "cattle-fleet-local-system", "cattle-fleet-system", "cattle-resources-system", "cattle", "calico", "nvidia", "tigera-operator", "label-studio", "postgres-ha", "minio-operator", "minio-tenant", "kube-system", "dlf", "directpv", "cert-manager", "longhorn-system", "postgresql-ha", "labelstudio", "coder", "harbor", "kueue-system", "kueue", "kyverno", "argocd" ]
        podSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values: [ "coder-workspace" ]
kind: ConfigMap
metadata:
  creationTimestamp: "2024-06-17T09:26:13Z"
  labels:
    app.kubernetes.io/instance: kueue
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: kueue
    app.kubernetes.io/version: v0.7.0
    argocd.argoproj.io/instance: kueue
    control-plane: controller-manager
    helm.sh/chart: kueue-0.1.0
  name: kueue-manager-config
  namespace: kueue-system
  resourceVersion: "70144241"
  uid: d4b6de19-d38f-4a5c-9d49-c85d36b2b50f
```
ClusterQueues (other cq-X are the same as cq-liveness)
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cq-shared
spec:
  cohort: rad
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - ephemeral-storage
    - github.com/fuse
    - pods
    - inno.com/gpu
    flavors:
    - name: k8s-test-master0
      resources:
      - name: cpu
        nominalQuota: 3
      - name: memory
        nominalQuota: 2Gi
      - name: ephemeral-storage
        nominalQuota: 10Gi
      - name: github.com/fuse
        nominalQuota: 5k
      - name: pods
        nominalQuota: 110
      - name: inno.com/gpu
        nominalQuota: 8
    - name: k8s-test-master1
      resources:
      - name: cpu
        nominalQuota: 3
      - name: memory
        nominalQuota: 1Gi
      - name: ephemeral-storage
        nominalQuota: 10Gi
      - name: github.com/fuse
        nominalQuota: 5k
      - name: pods
        nominalQuota: 110
      - name: inno.com/gpu
        nominalQuota: 9
    - name: k8s-test-master2
      resources:
      - name: cpu
        nominalQuota: 3
      - name: memory
        nominalQuota: 1Gi
      - name: ephemeral-storage
        nominalQuota: 10Gi
      - name: github.com/fuse
        nominalQuota: 4
      - name: pods
        nominalQuota: 110
      - name: inno.com/gpu
        nominalQuota: 4
    - name: k8s-test-worker0
      resources:
      - name: cpu
        nominalQuota: 3
      - name: memory
        nominalQuota: 1Gi
      - name: ephemeral-storage
        nominalQuota: 10Gi
      - name: github.com/fuse
        nominalQuota: 5k
      - name: pods
        nominalQuota: 110
      - name: inno.com/gpu
        nominalQuota: 8

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cq-liveness
spec:
  cohort: rad
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - ephemeral-storage
    - github.com/fuse
    - pods
    - inno.com/gpu
    flavors:
    - name: k8s-test-master0
      resources:
      - name: cpu
        nominalQuota: 0
      - name: memory
        nominalQuota: 0
      - name: ephemeral-storage
        nominalQuota: 0
      - name: github.com/fuse
        nominalQuota: 0
      - name: pods
        nominalQuota: 0
      - name: inno.com/gpu
        nominalQuota: 0
    - name: k8s-test-master1
      resources:
      - name: cpu
        nominalQuota: 0
      - name: memory
        nominalQuota: 0
      - name: ephemeral-storage
        nominalQuota: 0
      - name: github.com/fuse
        nominalQuota: 0
      - name: pods
        nominalQuota: 0
      - name: inno.com/gpu
        nominalQuota: 0
    - name: k8s-test-master2
      resources:
      - name: cpu
        nominalQuota: 0
      - name: memory
        nominalQuota: 0
      - name: ephemeral-storage
        nominalQuota: 0
      - name: github.com/fuse
        nominalQuota: 0
      - name: pods
        nominalQuota: 0
      - name: inno.com/gpu
        nominalQuota: 0
    - name: k8s-test-worker0
      resources:
      - name: cpu
        nominalQuota: 0
      - name: memory
        nominalQuota: 0
      - name: ephemeral-storage
        nominalQuota: 0
      - name: github.com/fuse
        nominalQuota: 0
      - name: pods
        nominalQuota: 0
      - name: inno.com/gpu
        nominalQuota: 0
```
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.27.10+rke2r1
- Kueue version (use `git describe --tags --dirty --always`): v0.7.0
- Cloud provider or hardware configuration: onprem VMs
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.4 LTS
- Kernel (e.g. `uname -a`): 5.15.0-97-generic
- Install tools: ArgoCD
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-24T11:43:26Z

Looks like this is already fixed by #2439.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-24T12:13:51Z

@xmolitann could you try `gcr.io/k8s-staging-kueue/kueue:v20240621-v0.7.0-13-ge0b028d3`?

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-24T13:15:54Z

> @xmolitann could you try `gcr.io/k8s-staging-kueue/kueue:v20240621-v0.7.0-13-ge0b028d3`?

Thanks, that works! Does that tag also include fix for [https://github.com/kubernetes-sigs/kueue/issues/2391](https://github.com/kubernetes-sigs/kueue/issues/2391) ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-24T14:37:56Z

yes, the build is from Friday, so it contains both fixes.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-24T14:38:18Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-24T14:38:24Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2473#issuecomment-2186739375):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
