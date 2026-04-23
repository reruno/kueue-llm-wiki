# Issue #707: WaitForPodsReady doesn't work

**Summary**: WaitForPodsReady doesn't work

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/707

**Last updated**: 2023-04-19T12:32:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2023-04-19T06:59:06Z
- **Updated**: 2023-04-19T12:32:27Z
- **Closed**: 2023-04-19T08:55:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
WaitForPodsReady always return true when scheduling.

**What you expected to happen**:
Admission for the queue should be blocked

**How to reproduce it (as minimally and precisely as possible)**:
I install the kueue by download the manifest file and set waitForPodsReady to true.
Then I change the job requests and apply single-clusterqueue-setup.yaml and sample-job.yaml in git repo to submit the job.
The bugs occured.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
1.22.15
- Kueue version (use `git describe --tags --dirty --always`):
v0.3.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

logs:
```
➜  kueue k get clusterqueue cluster-queue -oyaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"kueue.x-k8s.io/v1beta1","kind":"ClusterQueue","metadata":{"annotations":{},"name":"cluster-queue"},"spec":{"namespaceSelector":{},"resourceGroups":[{"coveredResources":["cpu","memory"],"flavors":[{"name":"default-flavor","resources":[{"name":"cpu","nominalQuota":9},{"name":"memory","nominalQuota":"36Gi"}]}]}]}}
  creationTimestamp: "2023-04-18T11:16:42Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 1
  name: cluster-queue
  resourceVersion: "2569063"
  uid: 0e50f2be-a6d5-4e41-8acc-dfeedc57cb26
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    flavors:
    - name: default-flavor
      resources:
      - name: cpu
        nominalQuota: "9"
      - name: memory
        nominalQuota: 36Gi
status:
  admittedWorkloads: 1
  conditions:
  - lastTransitionTime: "2023-04-18T11:43:14Z"
    message: Can admit new workloads
    reason: Ready
    status: "True"
    type: Active
  flavorsUsage:
  - name: default-flavor
    resources:
    - borrowed: "0"
      name: cpu
      total: "9"
    - borrowed: "0"
      name: memory
      total: 600Mi
  pendingWorkloads: 1
➜  kueue k get job
NAME               COMPLETIONS   DURATION   AGE
sample-job-qmjh2   0/3           3m46s      19h
sample-job-rmxz4   0/3                      19h
➜  kueue k get workload
NAME                         QUEUE        ADMITTED BY     AGE
job-sample-job-qmjh2-a999a   user-queue   cluster-queue   19h
job-sample-job-rmxz4-ed723   user-queue                   19h
➜  kueue k get worklaod job-sample-job-qmjh2-a999a -ojson | jq '.status'
error: the server doesn't have a resource type "worklaod"
➜  kueue k get workload job-sample-job-qmjh2-a999a -ojson | jq '.status'
{
  "admission": {
    "clusterQueue": "cluster-queue",
    "podSetAssignments": [
      {
        "flavors": {
          "cpu": "default-flavor",
          "memory": "default-flavor"
        },
        "name": "main",
        "resourceUsage": {
          "cpu": "9",
          "memory": "600Mi"
        }
      }
    ]
  },
  "conditions": [
    {
      "lastTransitionTime": "2023-04-18T11:32:27Z",
      "message": "Not all pods are ready or succeeded",
      "reason": "PodsReady",
      "status": "False",
      "type": "PodsReady"
    },
    {
      "lastTransitionTime": "2023-04-19T06:48:14Z",
      "message": "Admitted by ClusterQueue cluster-queue",
      "reason": "Admitted",
      "status": "True",
      "type": "Admitted"
    }
  ]
}
➜  kueue k logs -nkueue-system kueue-controller-manager-86586bcdcb-kj2c2 | grep "All workloads are in the PodsReady condition"
{"level":"Level(-5)","ts":"2023-04-19T06:48:14.01293937Z","logger":"scheduler","caller":"cache/cache.go:216","msg":"All workloads are in the PodsReady condition","workload":{"name":"job-sample-job-qmjh2-a999a","namespace":"default"},"clusterQueue":{"name":"cluster-queue"}}
➜  kueue k get cm -nkueue-system kueue-manager-config -oyaml | grep -C10 wait
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
    waitForPodsReady:
      enable: true
    #manageJobsWithoutQueueName: true
    #namespace: ""
    #internalCertManagement:
    #  enable: false
    #  webhookServiceName: ""
    #  webhookSecretName: ""
    integrations:
      frameworks:
      - "batch/job"
    # - "kubeflow.org/mpijob"
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"controller_manager_config.yaml":"apiVersion: config.kueue.x-k8s.io/v1beta1\nkind: Configuration\nhealth:\n  healthProbeBindAddress: :8081\nmetrics:\n  bindAddress: :8080\nwebhook:\n  port: 9443\nleaderElection:\n  leaderElect: true\n  resourceName: c1f6bfd2.kueue.x-k8s.io\ncontroller:\n  groupKindConcurrency:\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    ClusterQueue.kueue.x-k8s.io: 1\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 1\nclientConnection:\n  qps: 50\n  burst: 100\nwaitForPodsReady:\n  enable: true\n#manageJobsWithoutQueueName: true\n#namespace: \"\"\n#internalCertManagement:\n#  enable: false\n#  webhookServiceName: \"\"\n#  webhookSecretName: \"\"\nintegrations:\n  frameworks:\n  - \"batch/job\"\n# - \"kubeflow.org/mpijob\"\n"},"kind":"ConfigMap","metadata":{"annotations":{},"name":"kueue-manager-config","namespace":"kueue-system"}}
  creationTimestamp: "2023-04-18T11:15:30Z"
  name: kueue-manager-config
  namespace: kueue-system
  resourceVersion: "2145792"
  uid: fc86cf01-fd2b-4eda-9a79-a1847224817b

```

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-19T07:00:30Z

And I'm working to find out whether the bug exists in the latest commit.
If it still exists, I will fix it.
/assign

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-19T07:16:18Z

```
➜  kueue k get job
NAME               COMPLETIONS   DURATION   AGE
sample-job-qmjh2   0/3           4m11s      19h
sample-job-rmxz4   0/3                      19h
➜  kueue k delete job sample-job-qmjh2
job.batch "sample-job-qmjh2" deleted
➜  kueue k get job
NAME               COMPLETIONS   DURATION   AGE
sample-job-rmxz4   0/3           3s         19h
➜  kueue k get workload
NAME                         QUEUE        ADMITTED BY     AGE
job-sample-job-rmxz4-ed723   user-queue   cluster-queue   19h
➜  kueue k get workload job-sample-job-rmxz4-ed723 -ojson | jq '.status'
{
  "admission": {
    "clusterQueue": "cluster-queue",
    "podSetAssignments": [
      {
        "flavors": {
          "cpu": "default-flavor",
          "memory": "default-flavor"
        },
        "name": "main",
        "resourceUsage": {
          "cpu": "9",
          "memory": "600Mi"
        }
      }
    ]
  },
  "conditions": [
    {
      "lastTransitionTime": "2023-04-19T07:12:32Z",
      "message": "Admitted by ClusterQueue cluster-queue",
      "reason": "Admitted",
      "status": "True",
      "type": "Admitted"
    },
    {
      "lastTransitionTime": "2023-04-18T11:34:37Z",
      "message": "Not all pods are ready or succeeded",
      "reason": "PodsReady",
      "status": "False",
      "type": "PodsReady"
    }
  ]
}
➜  kueue k logs -nkueue-system kueue-controller-manager-7c5c7f8f8d-rrlm6 | grep "Scheduler set wait for pods ready to true"
{"level":"Level(-5)","ts":"2023-04-19T07:12:32.435666331Z","logger":"scheduler","caller":"scheduler/scheduler.go:175","msg":"Scheduler set wait for pods ready to true","workload":{"name":"job-sample-job-rmxz4-ed723","namespace":"default"},"clusterQueue":{"name":"cluster-queue"}}
➜  kueue k logs -nkueue-system kueue-controller-manager-7c5c7f8f8d-rrlm6 | grep "There is a ClusterQueue with not ready workloads"
➜  kueue k logs -nkueue-system kueue-controller-manager-7c5c7f8f8d-rrlm6 | grep "All workloads are in the PodsReady condition"
{"level":"Level(-5)","ts":"2023-04-19T07:12:32.435723794Z","logger":"scheduler","caller":"cache/cache.go:216","msg":"All workloads are in the PodsReady condition","workload":{"name":"job-sample-job-rmxz4-ed723","namespace":"default"},"clusterQueue":{"name":"cluster-queue"}}
➜  kueue k get po -nkueue-system
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-7c5c7f8f8d-rrlm6   2/2     Running   0          4m12s
➜  kueue k get po -nkueue-system  kueue-controller-manager-7c5c7f8f8d-rrlm6 -oyaml | grep iamge
➜  kueue k get po -nkueue-system  kueue-controller-manager-7c5c7f8f8d-rrlm6 -oyaml | grep image
    image: xxxx/kueue:v0.4.0-devel-13-g54b0118-dirty
    imagePullPolicy: Always
    image: gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0
    imagePullPolicy: IfNotPresent
  imagePullSecrets:
    image: gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0
    imageID: gcr.io/kubebuilder/kube-rbac-proxy@sha256:db06cc4c084dd0253134f156dddaaf53ef1c3fb3cc809e5d81711baa4029ea4c
    image: xxxx/kueue:v0.4.0-devel-13-g54b0118-dirty
    imageID: xxxx/kueue@sha256:194d14c9607faa1ce4fb512d53e7f8d2d9d2a1dc789dde97c2799486a0c58cd3

```

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-19T08:55:12Z

I found the problem. I need two tasks that are allowed to run.
So this issue is not a bug actually.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-04-19T08:55:16Z

@KunWuLuan: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/707#issuecomment-1514372730):

>I found the problem. I need two tasks that are allowed to run.
>So this issue is not a bug actually.
>/close
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-19T09:22:40Z

Do you think our documentation around this could be improved? Feel free to submit a PR for that :)

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-19T12:32:27Z

Okay! Thank you for your help! I will see if there's anything I can do to help the community.
😆
