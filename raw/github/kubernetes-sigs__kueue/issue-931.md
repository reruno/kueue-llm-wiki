# Issue #931: ResourceFlavor nodeLabels not added to .nodeSelector field on Pods

**Summary**: ResourceFlavor nodeLabels not added to .nodeSelector field on Pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/931

**Last updated**: 2023-06-29T16:55:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@jtorrex](https://github.com/jtorrex)
- **Created**: 2023-06-29T15:23:34Z
- **Updated**: 2023-06-29T16:55:11Z
- **Closed**: 2023-06-29T16:55:11Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

- Based on the documentation: https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/, the expected behavior is that `nodeLabels` defined in each ResourceFlavor will be propagated to the `.spec.template.spec.nodeSelector` field for any Pod when is executed in the same queue.
- After configuring a ResourceFlavor with a `nodeLabel` defined and linked to the ClusterQueue, and running jobs in this queue, the nodeLabels seem that are not propagated to the `.spec.template.spec.nodeSelector` of each Pod.

**What you expected to happen**:

- `nodeLabels` defined on the ResourceFlavor should appear on the nodeSelector field of the Pods.

**How to reproduce it (as minimally and precisely as possible)**:

- Create a manifest (**gpu-clusterqueue.yaml**) defining all the Kueue components: ClusterQueue, LocalQueue, ResourceFlavor

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "gpu-flavor"
spec:
  nodeLabels:
    karpenter.k8s.aws/instance-gpu-count: "1"
    karpenter.k8s.aws/instance-gpu-name: t4
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "gpu-clusterqueue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "gpu-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 16
      - name: "memory"
        nominalQuota: 32Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "kueue-system"
  name: "gpu-queue"
spec:
  clusterQueue: "gpu-clusterqueue"
```

- Create a manifest (**sample-job-gpu.yaml**) for a Job definition, adding the appropriate annotation (**kueue.x-k8s.io/queue-name: gpu-queue**) to run the Job in the previous queue configuration.

```
apiVersion: batch/v1
kind: Job
metadata:
  namespace: kueue-system
  name: sample-job-gpu
  annotations:
    kueue.x-k8s.io/queue-name: gpu-queue
spec:
  parallelism: 3
  completions: 3 
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        args: ["3600s"]
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
      restartPolicy: Never
```
- Execute the previous Job definition:

```
$ kubectl create -f sample-job-gpu.yaml 
job.batch/sample-job-gpu created
```
- Verify that Pods are running
```
$ kubectl get pods
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-84b7595fbd-bflgt   2/2     Running   0          81m
sample-job-gpu-98hlr                        1/1     Running   0          15s
sample-job-gpu-dwwln                        1/1     Running   0          15s
sample-job-gpu-kqpsj                        1/1     Running   0          15s
```
- Describe one Pod running from the previous execution and verify that the nodeSelector field remains as `<none>`
```
kubectl describe pod sample-job-gpu-98hlr 
Name:             sample-job-gpu-98hlr
Namespace:        kueue-system
Priority:         0
Service Account:  default
Node:             (censored)
Start Time:       Thu, 29 Jun 2023 14:56:06 +0000
Labels:           controller-uid=401eaa8d-3985-43a6-9f53-61d731efcca8
                  job-name=sample-job-gpu
Annotations:      kubernetes.io/psp: eks.privileged
Status:           Running
IP:               (censored)
IPs:
  IP:            (censored)
Controlled By:  Job/sample-job-gpu
Containers:
  dummy-job:
    Container ID:  containerd://ac5e7421bad6916e168edbdcbc45ae2444500943602e4a582499d192ef7b44c1
    Image:         gcr.io/k8s-staging-perf-tests/sleep:latest
    Image ID:      gcr.io/k8s-staging-perf-tests/sleep@sha256:00ae8e01dd4439edfb7eb9f1960ac28eba16e952956320cce7f2ac08e3446e6b
    Port:          <none>
    Host Port:     <none>
    Args:
      3600s
    State:          Running
      Started:      Thu, 29 Jun 2023 14:56:07 +0000
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:        100m
      memory:     512Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-92jlf (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-():
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  42s   default-scheduler  Successfully assigned kueue-system/sample-job-gpu-98hlr to  (censored)
  Normal  Pulling    41s   kubelet            Pulling image "gcr.io/k8s-staging-perf-tests/sleep:latest"
  Normal  Pulled     41s   kubelet            Successfully pulled image "gcr.io/k8s-staging-perf-tests/sleep:latest" in 417.789009ms
  Normal  Created    41s   kubelet            Created container dummy-job
  Normal  Started    41s   kubelet            Started container dummy-job
```

**Anything else we need to know?**:

- Reproduced this on releases v0.3.1 and v0.3.2
- The install was patched to allow MPIJob framework from Kubeflow, and to avoid interferences with other namespaces using Karpenter. (Described at the bottom)

**Environment**:
- Kubernetes version (use `kubectl version`): 
```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.4", GitCommit:"872a965c6c6526caa949f0c6ac028ef7aff3fb78", GitTreeState:"clean", BuildDate:"2022-11-09T13:36:36Z", GoVersion:"go1.19.3", Compiler:"gc", Platform:"linux/amd64"}
Kustomize Version: v4.5.7
Server Version: version.Info{Major:"1", Minor:"24+", GitVersion:"v1.24.14-eks-c12679a", GitCommit:"05d192f0de17608d98e17761ad3cffa9a6407f2f", GitTreeState:"clean", BuildDate:"2023-05-22T23:41:27Z", GoVersion:"go1.19.9", Compiler:"gc", Platform:"linux/amd64"}
```
- Kueue version (use `git describe --tags --dirty --always`):
Tested both on: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.3.2 and https://github.com/kubernetes-sigs/kueue/releases/tag/v0.3.1 

- Cloud provider or hardware configuration:
AWS EKS
- OS (e.g: `cat /etc/os-release`):

```
System Info:
  Kernel Version:              5.4.226-129.415.amzn2.x86_64
  OS Image:                    Amazon Linux 2
  Operating System:            linux
  Architecture:                amd64
  Container Runtime Version:   containerd://1.6.6
  Kubelet Version:             v1.24.7-eks-fb459a0
  Kube-Proxy Version:          v1.24.7-eks-fb459a0
```
- Kernel (e.g. `uname -a`):
Kernel Version: 5.4.226-129.415.amzn2.x86_64
- Install tools:
Kueue deployed via ARGOCD (**kustomization.yaml**) following the instructions here: https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version 

```
namespace: kueue-system
resources:
- https://github.com/kubernetes-sigs/kueue/releases/download/v0.3.2/manifests.yaml
- ondemand-clusterqueue-setup.yaml
- spot-clusterqueue-setup.yaml
- gpu-clusterqueue-setup.yaml
configMapGenerator:
- namespace: kueue-system
  name: kueue-manager-config
  behavior: replace
  files:
  - controller_manager_config.yaml
patches:
  - path: kueue-karpenter-patch.yaml
    target:
      group: admissionregistration.k8s.io
      name: kueue-mutating-webhook-configuration
      kind: MutatingWebhookConfiguration
      version: v1

```

Controller configuration modified to allow the MPIJob framework (controller_manager_config.yaml):

```
apiVersion: config.kueue.x-k8s.io/v1beta1
kind: Configuration
health:
  healthProbeBindAddress: :8081
metrics:
  bindAddress: :8080
webhook:
  port: 9443
leaderElection:
  leaderElect: true
  resourceName: c1f6bfd2.kueue.x-k8s.io
controller:
  groupKindConcurrency:
    Job.batch: 5
    LocalQueue.kueue.x-k8s.io: 1
    ClusterQueue.kueue.x-k8s.io: 1
    ResourceFlavor.kueue.x-k8s.io: 1
    Workload.kueue.x-k8s.io: 1
clientConnection:
  qps: 50
  burst: 100
#waitForPodsReady:
#  enable: true
#manageJobsWithoutQueueName: true
#namespace: ""
#internalCertManagement:
#  enable: false
#  webhookServiceName: ""
#  webhookSecretName: ""
integrations:
  frameworks:
  - "kubeflow.org/mpijob"
```
Karpenter patch to avoid interfering with other namespaces when the cluster downscales (**kueue-karpenter-patch.yaml**):

```
- op: replace
  path: /webhooks/0/namespaceSelector
  value:
    matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: NotIn
      values:
      - karpenter
```

- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-29T15:32:18Z

It looks like `batch/job` is dropped. Can you update controller_manager_config like this?

```diff
apiVersion: config.kueue.x-k8s.io/v1beta1
kind: Configuration
health:
  healthProbeBindAddress: :8081
metrics:
  bindAddress: :8080
webhook:
  port: 9443
leaderElection:
  leaderElect: true
  resourceName: c1f6bfd2.kueue.x-k8s.io
controller:
  groupKindConcurrency:
    Job.batch: 5
    LocalQueue.kueue.x-k8s.io: 1
    ClusterQueue.kueue.x-k8s.io: 1
    ResourceFlavor.kueue.x-k8s.io: 1
    Workload.kueue.x-k8s.io: 1
clientConnection:
  qps: 50
  burst: 100
#waitForPodsReady:
#  enable: true
#manageJobsWithoutQueueName: true
#namespace: ""
#internalCertManagement:
#  enable: false
#  webhookServiceName: ""
#  webhookSecretName: ""
integrations:
  frameworks:
    - "kubeflow.org/mpijob"
+   - "batch/job"
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-29T16:55:07Z

/close
user error :)

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-06-29T16:55:11Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/931#issuecomment-1613529917):

>/close
>user error :)


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
