# Issue #2625: error when install kueue

**Summary**: error when install kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2625

**Last updated**: 2024-07-16T13:32:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@warjiang](https://github.com/warjiang)
- **Created**: 2024-07-16T12:33:00Z
- **Updated**: 2024-07-16T13:32:17Z
- **Closed**: 2024-07-16T13:32:17Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Follow the instructions by the website 👉🏻 https://kueue.sigs.k8s.io/docs/installation/
```shell
VERSION=v0.7.1
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/$VERSION/manifests.yaml
```

the manager workload cannot start normally, and the log is

```text
{"level":"info","ts":"2024-07-16T10:08:43.707018098Z","logger":"setup","caller":"kueue/main.go:122","msg":"Initializing","gitVersion":"v0.7.1","gitCommit":"9ad6cfe0d859be004a99e366a0c32470d512dec0"}
{"level":"info","ts":"2024-07-16T10:08:43.709294772Z","logger":"setup","caller":"kueue/main.go:378","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    Pod: 5\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 5\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - ray.io/raycluster\n  - jobset.x-k8s.io/jobset\n  - kubeflow.org/mxjob\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmetrics:\n  bindAddress: :8080\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"Level(-2)","ts":"2024-07-16T10:08:43.709471072Z","logger":"setup","caller":"kueue/main.go:138","msg":"K8S Client","qps":50,"burst":100}
{"level":"error","ts":"2024-07-16T10:08:43.713716603Z","logger":"setup","caller":"kueue/main.go:169","msg":"Unable to setup indexes","error":"setting index on queue for Workload: no matches for kind \"Workload\" in version \"kueue.x-k8s.io/v1beta1\"","stacktrace":"main.main\n\t/workspace/cmd/kueue/main.go:169\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:271"}
```

**What you expected to happen**:
expected the `manager` workload can works normally.

**How to reproduce it (as minimally and precisely as possible)**:
I use `kind` to install `kueue`

```
kind create cluster -n kueue --image kindest/node:v1.27.11
VERSION=v0.7.1
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/$VERSION/manifests.yaml
```

**Anything else we need to know?**:
I also try to install by helm, it works.  From the error log, it seems that kueue did not install `workloads` crd throught raw manifest, but helm did;

this one is from installing by raw manifest
<img width="570" alt="image" src="https://github.com/user-attachments/assets/51e2184d-8c91-49aa-95df-d239b3b246f3">

this one is from installing by helm
<img width="510" alt="image" src="https://github.com/user-attachments/assets/b3ea33e8-a054-4cb5-bcec-6efb55136c83">



**Environment**:
- Kubernetes version (use `kubectl version`):
  ```
  Client Version: v1.29.0
  Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
  Server Version: v1.27.11
   ```
- Kueue version (use `git describe --tags --dirty --always`): v0.7.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
   ```
   PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
   NAME="Debian GNU/Linux"
   VERSION_ID="12"
   VERSION="12 (bookworm)"
   VERSION_CODENAME=bookworm
   ID=debian
   HOME_URL="https://www.debian.org/"
   SUPPORT_URL="https://www.debian.org/support"
   BUG_REPORT_URL="https://bugs.debian.org/"
   ```
- Kernel (e.g. `uname -a`):  `Linux iv-yd4cwyacjkcva4fumgxy 6.1.0-13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.55-1 (2023-09-29) x86_64 GNU/Linux`
- Install tools: by raw manifest
- Others:

## Discussion

### Comment by [@warjiang](https://github.com/warjiang) — 2024-07-16T13:32:04Z

finally i've solved the problem from the document, it's the problem of `kubectl apply` command

<img width="981" alt="image" src="https://github.com/user-attachments/assets/b0c7e045-40bc-4f35-ba9e-d0f079354a14">

and i try to install again with `kubectl apply --server-side -f manifests.yaml --force-conflicts` and it works.
