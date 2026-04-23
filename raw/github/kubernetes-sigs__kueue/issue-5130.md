# Issue #5130: Deleting pods in an unschedulable all-or-nothing pod group hangs forever

**Summary**: Deleting pods in an unschedulable all-or-nothing pod group hangs forever

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5130

**Last updated**: 2025-04-30T15:19:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nojnhuh](https://github.com/nojnhuh)
- **Created**: 2025-04-25T21:21:43Z
- **Updated**: 2025-04-30T15:19:24Z
- **Closed**: 2025-04-30T15:19:23Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Following the docs to [run a group of plain pods](https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#running-a-group-of-pods-to-be-admitted-together) with [all-or-nothing scheduling enabled](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/) when there is insufficient quota to schedule the pods, deleting the pods hangs forever. Deleting the `Workload` instead of the pods works more-or-less immediately. Deleting a plain pod not part of a pod group also happens quickly.

**What you expected to happen**:

The pods are deleted.

**How to reproduce it (as minimally and precisely as possible)**:

Copy-pasting this is enough for me to end up with two stuck deleting pods:

```
kind create cluster --wait 2m
helm install kueue oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.11.4 \
  --namespace  kueue-system \
  --create-namespace \
  --wait --timeout 300s \
  --values - <<EOF
managerConfig:
  controllerManagerConfigYaml: |-
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
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 50
      burst: 100
    #pprofBindAddress: :8083
    waitForPodsReady:
      enable: true
      timeout: 5m
      recoveryTimeout: 3m
      blockAdmission: true
      requeuingStrategy:
        timestamp: Eviction
        backoffLimitCount: null # null indicates infinite requeuing
        backoffBaseSeconds: 60
        backoffMaxSeconds: 3600
    #manageJobsWithoutQueueName: true
    managedJobsNamespaceSelector:
      matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: NotIn
          values: [ kube-system, kueue-system ]
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
      - "kubeflow.org/paddlejob"
      - "kubeflow.org/pytorchjob"
      - "kubeflow.org/tfjob"
      - "kubeflow.org/xgboostjob"
      - "workload.codeflare.dev/appwrapper"
      - "pod"
    #  - "deployment" (requires enabling pod integration)
    #  - "statefulset" (requires enabling pod integration)
    #  - "leaderworkerset.x-k8s.io/leaderworkerset" (requires enabling pod integration)
    #  externalFrameworks:
    #  - "Foo.v1.example.com"
    #fairSharing:
    #  enable: true
    #  preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
    #resources:
    #  excludeResourcePrefixes: []
    # transformations:
    # - input: nvidia.com/mig-4g.5gb
    #   strategy: Replace | Retain
    #   outputs:
    #     example.com/accelerator-memory: 5Gi
    #     example.com/accelerator-gpc: 4
EOF

kubectl apply -f- <<EOF
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
EOF

kubectl create -f- <<EOF
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-leader-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the leader pod" && sleep 3']
    resources:
      requests:
        cpu: 6
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-worker-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the worker pod" && sleep 2']
    resources:
      requests:
        cpu: 6
EOF

kubectl delete pods --all
```

 The manager config is the default with this diff:
```diff
 managerConfig:
   controllerManagerConfigYaml: |-
     apiVersion: config.kueue.x-k8s.io/v1beta1
@@ -83,22 +24,22 @@ managerConfig:
       qps: 50
       burst: 100
     #pprofBindAddress: :8083
-    #waitForPodsReady:
-    #  enable: false
-    #  timeout: 5m
-    #  recoveryTimeout: 3m
-    #  blockAdmission: false
-    #  requeuingStrategy:
-    #    timestamp: Eviction
-    #    backoffLimitCount: null # null indicates infinite requeuing
-    #    backoffBaseSeconds: 60
-    #    backoffMaxSeconds: 3600
+    waitForPodsReady:
+      enable: true
+      timeout: 5m
+      recoveryTimeout: 3m
+      blockAdmission: true
+      requeuingStrategy:
+        timestamp: Eviction
+        backoffLimitCount: null # null indicates infinite requeuing
+        backoffBaseSeconds: 60
+        backoffMaxSeconds: 3600
     #manageJobsWithoutQueueName: true
-    #managedJobsNamespaceSelector:
-    #  matchExpressions:
-    #    - key: kubernetes.io/metadata.name
-    #      operator: NotIn
-    #      values: [ kube-system, kueue-system ]
+    managedJobsNamespaceSelector:
+      matchExpressions:
+        - key: kubernetes.io/metadata.name
+          operator: NotIn
+          values: [ kube-system, kueue-system ]
     #internalCertManagement:
     #  enable: false
     #  webhookServiceName: ""
@@ -115,7 +56,7 @@ managerConfig:
       - "kubeflow.org/tfjob"
       - "kubeflow.org/xgboostjob"
       - "workload.codeflare.dev/appwrapper"
-    #  - "pod"
+      - "pod"
     #  - "deployment" (requires enabling pod integration)
     #  - "statefulset" (requires enabling pod integration)
     #  - "leaderworkerset.x-k8s.io/leaderworkerset" (requires enabling pod integration)
```

**Anything else we need to know?**:

I put some more output that might be helpful for debugging here: https://gist.github.com/nojnhuh/84105829f892401bdf870a9e12bbaf93

**Environment**:
- Kubernetes version (use `kubectl version`):
    ```
    Client Version: v1.32.3
    Kustomize Version: v5.5.0
    Server Version: v1.32.2
    ```
- Kueue version (use `git describe --tags --dirty --always`): v0.11.4
- Cloud provider or hardware configuration: kind v0.27.0 running on Ubuntu 24.04 LTS
- OS (e.g: `cat /etc/os-release`):
    ```
    % docker exec kind-control-plane cat /etc/os-release
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
- Kernel (e.g. `uname -a`):
    ```
    % docker exec -it kind-control-plane uname -a           
    Linux kind-control-plane 6.11.0-1013-azure #13~24.04.1-Ubuntu SMP Fri Mar 28 23:43:34 UTC 2025 x86_64 GNU/Linux
    ```
- Install tools:
    ```
    % helm version
    version.BuildInfo{Version:"v3.17.2", GitCommit:"cc0bbbd6d6276b83880042c1ecb34087e84d41eb", GitTreeState:"clean", GoVersion:"go1.23.7"}
    ```
- Others:

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-29T06:54:29Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-30T09:04:48Z

Hey @nojnhuh
Thanks for extensive description, it is easy to reproduce.
However I am afraid that's the desired behaviour that helps Kueue operate on group of pods.
Those pods do contain finalisers that prevents the deletion.
I hope this [part of the documentation](https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_pods/#why-arent-pods-in-a-pod-group-deleted-when-failed-or-succeeded) will help to understand the idea behind this:

```
When using Pod groups, Kueue keeps a [finalizer](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)
`kueue.x-k8s.io/managed` to prevent Pods from being deleted and to be able to track the progress of the group.
You should not modify finalizers manually.

Kueue will remove the finalizer from Pods when:
- The group satisfies the [termination](/docs/tasks/run/plain_pods/#termination) criteria, for example,
  when all Pods terminate successfully.
- For Failed Pods, when Kueue observes a replacement Pod.
- You delete the Workload object.
```

### Comment by [@nojnhuh](https://github.com/nojnhuh) — 2025-04-30T15:19:18Z

Good to know, thanks!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-30T15:19:24Z

@nojnhuh: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5130#issuecomment-2842351180):

>Good to know, thanks!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
