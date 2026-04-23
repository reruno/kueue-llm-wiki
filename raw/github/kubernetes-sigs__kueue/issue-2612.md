# Issue #2612: Kueue with Jobset automatically suspends child job

**Summary**: Kueue with Jobset automatically suspends child job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2612

**Last updated**: 2024-07-18T14:05:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tiffzhao5](https://github.com/tiffzhao5)
- **Created**: 2024-07-15T13:22:22Z
- **Updated**: 2024-07-18T14:05:02Z
- **Closed**: 2024-07-18T14:05:00Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I'm running a simple Jobset with Kueue, and even a Kueue Workload doesn't get created (i.e. `kubectl get workloads` returns nothing found). If I run a batchv1Job with Kueue, a Workload gets successfully admitted. Is there something wrong with the configuration I'm using?

**What you expected to happen**:

A Jobset with Kueue should create a Workload and get admitted to the LocalQueue.

**How to reproduce it (as minimally and precisely as possible)**:
In `kueue.yaml`, I define the `ResourceFlavor`, `ClusterQueue`, and `LocalQueue`: 

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "spot"
spec:
  nodeLabels:
    node-lifecycle: normal
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
    - name: "spot"
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
  namespace: default
  name: test-queue
spec:
  clusterQueue: cluster-queue 
```

I define a `Jobset` through `jobset_example.yml`:

```
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: sleep-job
  labels:
    kueue.x-k8s.io/queue-name: test-queue
  
spec:
  failurePolicy:
    maxRestarts: 4
  replicatedJobs:
    - name: workers
      replicas: 1
      template:
        spec:
          template:
            spec:
              nodeSelector:
                node-lifecycle: normal
              containers:
                - name: quick-container
                  image: busybox
                  command: ["/bin/sh", "-c"]
                  args: ["sleep 1"]
```

I apply both `kubectl apply -f kueue.yaml` and `kubectl apply -f jobset_example.yml`, and no Kueue Workload is even created, where `kubectl get workloads --all-namespaces` gives me:

```
No resources found
```


When I do `kubectl describe job -n default sleep-job-workers-0`, I see the following events:

```
Events:
  Type    Reason            Age                   From                        Message
  ----    ------            ----                  ----                        -------
  Normal  SuccessfulDelete  4m9s                  job-controller              Deleted pod: sleep-job-workers-0-0-sm2gt
  Normal  SuccessfulCreate  4m9s                  job-controller              Created pod: sleep-job-workers-0-0-sm2gt
  Normal  SuccessfulCreate  4m8s                  job-controller              Created pod: sleep-job-workers-0-0-slnjd
  Normal  Suspended         4m8s (x8 over 4m9s)   job-controller              Job suspended
  Normal  SuccessfulCreate  4m8s                  job-controller              Created pod: sleep-job-workers-0-0-nq7vd
  Normal  SuccessfulDelete  4m8s                  job-controller              Deleted pod: sleep-job-workers-0-0-nq7vd
  Normal  SuccessfulCreate  4m8s                  job-controller              Created pod: sleep-job-workers-0-0-k9qhf
  Normal  SuccessfulDelete  4m8s                  job-controller              Deleted pod: sleep-job-workers-0-0-k9qhf
  Normal  Suspended         4m8s (x25 over 4m9s)  batch/job-kueue-controller  Kueue managed child job suspended
  Normal  SuccessfulDelete  4m8s                  job-controller              Deleted pod: sleep-job-workers-0-0-slnjd
  Normal  SuccessfulCreate  4m8s                  job-controller              Created pod: sleep-job-workers-0-0-cqvfc
  Normal  Resumed           4m8s (x3 over 4m8s)   job-controller              Job resumed
  Normal  SuccessfulDelete  4m8s                  job-controller              Deleted pod: sleep-job-workers-0-0-cqvfc
  Normal  SuccessfulCreate  4m8s                  job-controller              Created pod: sleep-job-workers-0-0-2h7vn
  Normal  SuccessfulDelete  4m8s                  job-controller              Deleted pod: sleep-job-workers-0-0-2h7vn
  Normal  SuccessfulCreate  4m8s                  job-controller              Created pod: sleep-job-workers-0-0-nmm8w
  Normal  SuccessfulDelete  4m8s                  job-controller              Deleted pod: sleep-job-workers-0-0-nmm8w
```    


**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):

```
Client Version: v1.29.2
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.29.4-eks-036c24b
```

- Kueue version (use `git describe --tags --dirty --always`):
Installed Kueue via helm charts:

`kubectl describe deployment kueue-controller-manager -n kueue-system` gives:

```
Name:                   kueue-controller-manager
Namespace:              kueue-system
CreationTimestamp:      Thu, 06 Jun 2024 22:41:23 +0100
Labels:                 app.kubernetes.io/instance=kueue
                        app.kubernetes.io/managed-by=Helm
                        app.kubernetes.io/name=kueue
                        app.kubernetes.io/version=v0.7.0
                        control-plane=controller-manager
                        helm.sh/chart=kueue-0.1.0
                        node-lifecycle=persistent
                        node-purpose=system
Annotations:            deployment.kubernetes.io/revision: 1
                        meta.helm.sh/release-name: kueue
                        meta.helm.sh/release-namespace: kueue-system
Selector:               app.kubernetes.io/instance=kueue,app.kubernetes.io/name=kueue,control-plane=controller-manager,node-lifecycle=persistent,node-purpose=system
```

- Cloud provider or hardware configuration:
Kueue and Jobset deployments are both running on AWS instances, and Jobsets created are also running on AWS instances that have the node label `node-lifecycle:normal`

- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-15T13:55:57Z

/cc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-15T14:58:07Z

Interesting. What the configuration of kueue manager do you have?

`kubectl get configmaps kueue-manager-config -o yaml -n kueue-system`

### Comment by [@tiffzhao5](https://github.com/tiffzhao5) — 2024-07-15T15:03:06Z

@mbobrovskyi 

> Interesting. What the configuration of kueue manager do you have?
> 
> `kubectl get configmaps kueue-manager-config -o yaml -n kueue-system`

This is what I get after running the command:

```
apiVersion: v1
data:
  controller_manager_config.yaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
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
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 50
      burst: 100
    #pprofBindAddress: :8083
    #waitForPodsReady:
    #  enable: false
    #  timeout: 5m
    #  blockAdmission: false
    #  requeuingStrategy:
    #    timestamp: Eviction
    #    backoffLimitCount: null # null indicates infinite requeuing
    #    backoffBaseSeconds: 60
    #    backoffMaxSeconds: 3600
    #manageJobsWithoutQueueName: true
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
      - "jobset.x-k8s.io/jobset"
      - "kubeflow.org/mxjob"
      - "kubeflow.org/paddlejob"
      - "kubeflow.org/pytorchjob"
      - "kubeflow.org/tfjob"
      - "kubeflow.org/xgboostjob"
    #  - "pod"
    #  externalFrameworks:
    #  - "Foo.v1.example.com"
    #  podOptions:
    #    namespaceSelector:
    #      matchExpressions:
    #        - key: kubernetes.io/metadata.name
    #          operator: NotIn
    #          values: [ kube-system, kueue-system ]
    #fairSharing:
    #  enable: true
    #  preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
    #resources:
    #  excludeResourcePrefixes: []
kind: ConfigMap
metadata:
  annotations:
    meta.helm.sh/release-name: kueue
    meta.helm.sh/release-namespace: kueue-system
  creationTimestamp: "2024-06-06T21:41:22Z"
  labels:
    app.kubernetes.io/instance: kueue
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: kueue
    app.kubernetes.io/version: v0.7.0
    control-plane: controller-manager
    helm.sh/chart: kueue-0.1.0
    node-lifecycle: persistent
    node-purpose: system
  name: kueue-manager-config
  namespace: kueue-system
  resourceVersion: "32963819"
  uid: d636ac62-e7b6-442b-bcb2-8a60dd900afe
```

### Comment by [@tiffzhao5](https://github.com/tiffzhao5) — 2024-07-15T15:07:06Z

for more context, I installed Kueue via helm charts by following these [directions](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/README.md#installing-the-chart) through a Terraform `helm_release` resource

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-16T13:54:34Z

just a guess but I notice you don’t have any field around JobSet and concurrency.

controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1

If you added jobset here would that impact anything?

### Comment by [@tiffzhao5](https://github.com/tiffzhao5) — 2024-07-16T15:34:50Z

@kannon92 I just added `Jobset.jobset.x-k8s.io: 5` and I'm still getting the same errors

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-17T08:40:04Z

Looks like the problem with helm templates. With [manifests](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version) working fine.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-17T08:41:01Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-17T21:26:50Z

@tiffzhao5 Try to restart kueue-controller-manager. Looks like you install jobset CRDs after kueue-controller-manager was run. So jobset jobframework didn't apply and can't create workloads for jobsets.

### Comment by [@tiffzhao5](https://github.com/tiffzhao5) — 2024-07-18T13:33:19Z

@mbobrovskyi Amazing that worked! Thank you so much!

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-18T14:04:56Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-18T14:05:01Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2612#issuecomment-2236625700):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
