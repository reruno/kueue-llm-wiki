# Issue #4860: Kueue creates Workloads for child Jobs when one of the integrations in the ownership chain is disabled

**Summary**: Kueue creates Workloads for child Jobs when one of the integrations in the ownership chain is disabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4860

**Last updated**: 2025-06-19T12:25:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-02T11:57:16Z
- **Updated**: 2025-06-19T12:25:16Z
- **Closed**: 2025-06-19T12:25:15Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Kueue creates Workloads for child Jobs when one of the integrations in the ownership chain is disabled.

For example:

`Job (enabled) → JobSet (disabled) → AppWrapper (enabled)`.

**What you expected to happen**:

Create only one workload for the top level Job.

**How to reproduce it (as minimally and precisely as possible)**:

Disable `jobset.x-k8s.io/jobset` integration and enable `manageJobsWithoutQueueName` in kueue-manager-config ConfigMap:

```
controller_manager_config.yaml: |
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8443
    # enableClusterQueueResources: true
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: c1f6bfd2.kueue.x-k8s.io
    controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        Cohort.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 50
      burst: 100
    #pprofBindAddress: :8083
    #waitForPodsReady:
    #  enable: false
    #  timeout: 5m
    #  recoveryTimeout: 3m
    #  blockAdmission: false
    #  requeuingStrategy:
    #    timestamp: Eviction
    #    backoffLimitCount: null # null indicates infinite requeuing
    #    backoffBaseSeconds: 60
    #    backoffMaxSeconds: 3600
    manageJobsWithoutQueueName: true
    #managedJobsNamespaceSelector:
    #  matchExpressions:
    #    - key: kubernetes.io/metadata.name
    #      operator: NotIn
    #      values: [ kube-system, kueue-system ]
    #internalCertManagement:
    #  enable: false
    #  webhookServiceName: ""
    #  webhookSecretName: ""
    integrations:
      frameworks:
      - "batch/job"
      - "kubeflow.org/mpijob"
      - "ray.io/rayjob"
      - "ray.io/raycluster"
    #  - "jobset.x-k8s.io/jobset"
      - "kubeflow.org/paddlejob"
      - "kubeflow.org/pytorchjob"
      - "kubeflow.org/tfjob"
      - "kubeflow.org/xgboostjob"
      - "workload.codeflare.dev/appwrapper"
    #  - "pod"
    #  - "deployment" # requires enabling pod integration
    #  - "statefulset" # requires enabling pod integration
    #  - "leaderworkerset.x-k8s.io/leaderworkerset" # requires enabling pod integration
    #  externalFrameworks:
    #  - "Foo.v1.example.com"
    #fairSharing:
    #  enable: true
    #  preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
    #resources:
    #  excludeResourcePrefixes: []
    #  transformations:
    #  - input: nvidia.com/mig-4g.5gb
    #    strategy: Replace | Retain
    #    outputs:
    #      example.com/accelerator-memory: 5Gi
    #      example.com/accelerator-gpc: 4
```

Apply manifests:

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
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
---
apiVersion: workload.codeflare.dev/v1beta2
kind: AppWrapper
metadata:
  name: app-wrapper
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  components:
  - template:
      apiVersion: jobset.x-k8s.io/v1alpha2
      kind: JobSet
      metadata:
        name: jobset
      spec:
        replicatedJobs:
          - name: jobs
            replicas: 3
            template:
              spec:
                parallelism: 1
                completions: 1
                template:
                  spec:
                    containers:
                      - name: sleep
                        image: busybox
                        resources:
                          requests:
                            cpu: "1"
                        command:
                          - sleep
                        args:
                          - 100s
```

In result we have:

```
kubectl get wl
NAMESPACE   NAME                           QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
default     appwrapper-app-wrapper-2deaa   user-queue   cluster-queue   True                  4s
default     job-jobset-jobs-0-d91af                                                           4s
default     job-jobset-jobs-1-9c21b                                                           4s
default     job-jobset-jobs-2-40643                                                           4s
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.32.2
- Kueue version (use `git describe --tags --dirty --always`): 0.11.2
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-02T11:57:53Z

cc: @mimowo @dgrove-oss

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-19T12:25:11Z

/close

Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/4824.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-19T12:25:16Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4860#issuecomment-2987916674):

>/close
>
>Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/4824.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
