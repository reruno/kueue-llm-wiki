# Issue #1407: nodeLabels from ResourceFlavor not added as Node-Selector values to Kubeflow PytorchJobs

**Summary**: nodeLabels from ResourceFlavor not added as Node-Selector values to Kubeflow PytorchJobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1407

**Last updated**: 2023-12-15T19:09:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@jrleslie](https://github.com/jrleslie)
- **Created**: 2023-12-05T16:52:34Z
- **Updated**: 2023-12-15T19:09:41Z
- **Closed**: 2023-12-15T17:59:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 41

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: 
When submitting a kubeflow pytorch job to a localqueue. The pods associated with pytorch job never get the `Node-Selectors` values specified via nodeLabels in the ResourceFlavor added to the pod. The Node-Selectors get set as `<none>`  .

Fwiw I tested this with a batch/v1 job and the Node-Selectors were applied correctly. 

<img width="496" alt="image" src="https://github.com/kubernetes-sigs/kueue/assets/14949272/c38803a6-4098-45f4-947b-5d93ec550758">

**What you expected to happen**:
Pytorch job gets the proper Node-Selectors added to the associated pytorch master and worker pods.

**How to reproduce it (as minimally and precisely as possible)**:
Submit kubeflow pytorch job to localqueue with an associated resourceflavor that has nodeLabels set in it. 

**Anything else we need to know?**:
kueue-manager-config has the following enabled
```
integrations:
  frameworks:
  - "kubeflow.org/pytorchjob" 
```

**Environment**:
- Kubernetes version (use `kubectl version`):
Client Version: v1.24.13
Server Version: v1.24.13

- Kueue version (use `git describe --tags --dirty --always`): 
v0.5.1-1-g69c236f-dirty

- Cloud provider or hardware configuration: 
AWS

- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T18:07:23Z

@tenzen-y have you observed this?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T19:29:38Z

I just double checked and we have integration tests for this.

Can you share your PyTorchJob yaml?
Is it possible that you didn't define requests for your pods?

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-05T20:25:19Z

@alculquicondor can't share the full yaml, but the master and worker pytorch pods both have requests specified. See here                    
![image](https://github.com/kubernetes-sigs/kueue/assets/14949272/9696e9a2-3c9c-4fb1-af38-372510e7b952)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T20:30:42Z

Can you share the status of the Workload object associated with your PyTorchJob?

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-05T20:42:45Z

<img width="878" alt="image" src="https://github.com/kubernetes-sigs/kueue/assets/14949272/fc627788-c741-41e6-8340-e7279cc6c375">

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-05T20:45:57Z

If you're looking for a particular stanza, let me know and I can pull it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T20:47:36Z

I actually wanted to see the flavor assignments.... But it looks like the flavors got something assigned, so no problem on that side.

Definitely some problem passing the flavor information into the PyTorchJob.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T20:49:45Z

Do all resources (cpu, memory, etc) share the same flavor or are they different ones? Are both master and worker pods missing the node labels?

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-05T20:53:16Z

Yep, single flavor.  Everything that's redacted is just the single flavor name.

Both pytorchjob master and worker pods are missing the node label.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T02:21:46Z

> @tenzen-y have you observed this?

No, I haven't seen this issue never.
Let me investigate this issue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-06T14:03:04Z

/assign @tenzen-y

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-06T19:01:21Z

@tenzen-y any luck replicating this behavior on your end?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T05:51:36Z

> any luck replicating this behavior on your end?

I'm trying to reproduce this. Please give me some time.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T13:24:24Z

@jrleslie I couldn't reproduce this issue. If you submit PyTorchJob with nodeSelecotr without a Kueue label, do pods have nodeSelectors?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T13:35:39Z

Also, which versions do you use the training-operator?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T14:39:13Z

Oh, I can reproduce this issue in the following steps:

```shell
# 1. Create a new cluster
$ kind create cluster --image kindest/node:v1.24.13
# 2. Deploy Kueue
$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.5.1/manifests.yaml
# 3. Set up single clusterqueue
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/admin/single-clusterqueue-setup.yaml
# 4. Add nodeSlecotor to resourceFlavor
$ cat <<EOF| kubectl apply -f -
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
spec:
  nodeLabels:
    kubernetes.io/arch: arm64
EOF
# 5. Deploy training-operator
$ kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"
# 6. Submit a PytorchJob
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/jobs/sample-pytorchjob.yaml
```

@jrleslie Once you use `ytenzen/kueue-manager:debug`, this issue will be resolved.
I will create a PR to apply a patch to the upstream.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T14:40:53Z

However, I could not reproduce this issue in any of our unit/integraiton tests :(

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-07T16:30:43Z

> Also, which versions do you use the training-operator?

We're using v1.70 for training-operator. 

> @jrleslie Once you use ytenzen/kueue-manager:debug, this issue will be resolved.

What is this a reference to? Is it a docker image or config that needs be set somewhere. Can't find it anywhere.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T04:23:15Z

> What is this a reference to? Is it a docker image or config that needs be set somewhere. Can't find it anywhere.

This is a patch image for the kueue-controller-manager:

https://hub.docker.com/layers/ytenzen/kueue-manager/debug/images/sha256-937b71c1053ba19415c72ae17028ddf21dd794f54e96ff62e2382ff407ddff66?context=repo

You can verify this patch image resolve this issue once you modify the kueue-controller-manager deployment's image to this patch image.
Please let me know if this issue isn't resolved even if you replaced the kueue-controller-manager deployment's image with `ytenzen/kueue-manager:debug`.

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-08T14:52:52Z

Thank you @tenzen-y. Will test and let you know shortly.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T15:08:26Z

> Oh, I can reproduce this issue in the following steps:
> 
> ```shell
> # 1. Create a new cluster
> $ kind create cluster --image kindest/node:v1.24.13
> # 2. Deploy Kueue
> $ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.5.1/manifests.yaml
> # 3. Set up single clusterqueue
> $ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/admin/single-clusterqueue-setup.yaml
> # 4. Add nodeSlecotor to resourceFlavor
> $ cat <<EOF| kubectl apply -f -
> apiVersion: kueue.x-k8s.io/v1beta1
> kind: ResourceFlavor
> metadata:
>   name: "default-flavor"
> spec:
>   nodeLabels:
>     kubernetes.io/arch: arm64
> EOF
> # 5. Deploy training-operator
> $ kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"
> # 6. Submit a PytorchJob
> $ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/jobs/sample-pytorchjob.yaml
> ```
> 
> @jrleslie Once you use `ytenzen/kueue-manager:debug`, this issue will be resolved. I will create a PR to apply a patch to the upstream.

Oh, these reproducing steps are invalid. If I used the following steps, no error occurred.

```shell
# 1. Create a new cluster
$ kind create cluster --image kindest/node:v1.24.13
# 2. Deploy training-operator
# ################################################################################## #                                            
# [IMPORTANT] We need to deploy training-operator before deploying kueue [IMPORTANT] #
# ################################################################################## #
$ kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"
# 3. Deploy Kueue
$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.5.1/manifests.yaml
# 4. Set up single clusterqueue
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/admin/single-clusterqueue-setup.yaml
# 5. Add nodeSlecotor to resourceFlavor
$ cat <<EOF| kubectl apply -f -
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
spec:
  nodeLabels:
    kubernetes.io/arch: arm64
EOF
# 6. Submit a PytorchJob
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/jobs/sample-pytorchjob.yaml
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T15:11:37Z

> Thank you @tenzen-y. Will test and let you know shortly.

@jrleslie Sorry, due to reproducing steps being invalid, the above image won't fix this error.

So, Can I get an answer about orders for deploying components? Did you deploy the training operator before deploying Kueue?

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-12T21:17:45Z

@tenzen-y Is it possible there's a diff between the kueue helm chart and the direct manifest you are using in your steps above? You are correct in that your steps above show it working, which I validated. But when I attempted to use the helm chart, I see the same behavior where there are no Node-Selectors added to the pytorch job. 

Would you be able to test using the v0.5.1 helm chart?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T13:59:30Z

@jrleslie the key question is whether you installed kubeflow training-operator (more specifically, the CRDs) before installing kueue.

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-13T14:22:50Z

yep - kubeflow training operator and crds are always installed prior to kueue being installed.

I've tested this on a local kind cluster using @tenzen-y steps above and our ec2 based clusters and I replicated the behavior on both. When I replace the manifest install step with installation using the kueue helm chart, the node selectors are never applied to the pytorch jobs. 

`
git checkout tags/0.5.1
cd kueue/charts
helm install kueue kueue/ --create-namespace --namespace kueue-system
`

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-13T14:24:50Z

```
git checkout tags/0.5.1 
cd kueue/charts 
helm install kueue kueue/ --create-namespace --namespace kueue-system
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T15:46:31Z

Can you share the first ~20 lines of the logs when the kueue-manager first starts? Any errors?

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-13T21:22:23Z

There are two errors related to the certs that I see popping up in the log. 

```
+ kueue-controller-manager-9bf76c49b-7dmsg › manager
+ kueue-controller-manager-9bf76c49b-7dmsg › kube-rbac-proxy
kueue-controller-manager-9bf76c49b-7dmsg kube-rbac-proxy I1213 21:12:18.407344       1 main.go:190] Valid token audiences: 
kueue-controller-manager-9bf76c49b-7dmsg kube-rbac-proxy I1213 21:12:18.407412       1 main.go:262] Generating self signed cert as no cert is provided
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.101351918Z","logger":"setup","caller":"kueue/main.go:120","msg":"Initializing","gitVersion":"","gitCommit":""}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.171114607Z","logger":"setup","caller":"kueue/main.go:385","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 1\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - jobset.x-k8s.io/jobset\n  - kubeflow.org/mxjob\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 0s\n  renewDeadline: 0s\n  resourceLock: \"\"\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 0s\nmanageJobsWithoutQueueName: false\nmetrics:\n  bindAddress: :8080\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
kueue-controller-manager-9bf76c49b-7dmsg kube-rbac-proxy I1213 21:12:18.877680       1 main.go:311] Starting TCP socket on 0.0.0.0:8443
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"Level(-2)","ts":"2023-12-13T21:12:12.171289465Z","logger":"setup","caller":"kueue/main.go:136","msg":"K8S Client","qps":50,"burst":100}
kueue-controller-manager-9bf76c49b-7dmsg kube-rbac-proxy I1213 21:12:18.878056       1 main.go:318] Listening securely on 0.0.0.0:8443
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.183155239Z","logger":"setup","caller":"kueue/main.go:315","msg":"Probe endpoints are configured on healthz and readyz"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.183204448Z","logger":"setup","caller":"kueue/main.go:180","msg":"Starting manager"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.183244475Z","logger":"setup","caller":"kueue/main.go:217","msg":"Waiting for certificate generation to complete"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.183257387Z","logger":"controller-runtime.metrics","caller":"server/server.go:185","msg":"Starting metrics server"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.183348647Z","logger":"controller-runtime.metrics","caller":"server/server.go:224","msg":"Serving metrics server","bindAddress":":8080","secure":false}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.183392167Z","caller":"manager/server.go:50","msg":"starting server","kind":"health probe","addr":"[::]:8081"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.284173856Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *v1.Secret"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.284202121Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.284209548Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:12.284215077Z","caller":"controller/controller.go:186","msg":"Starting Controller","controller":"cert-rotator"}
kueue-controller-manager-9bf76c49b-7dmsg manager I1213 21:12:12.284293       1 leaderelection.go:250] attempting to acquire leader lease kueue-system/c1f6bfd2.kueue.x-k8s.io...
kueue-controller-manager-9bf76c49b-7dmsg manager I1213 21:12:29.976211       1 leaderelection.go:260] successfully acquired lease kueue-system/c1f6bfd2.kueue.x-k8s.io
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"debug","ts":"2023-12-13T21:12:29.97627738Z","logger":"events","caller":"recorder/recorder.go:104","msg":"kueue-controller-manager-9bf76c49b-7dmsg_a43b8fc1-8a15-4b3e-b391-57ecc71ef9c9 became leader","type":"Normal","object":{"kind":"Lease","namespace":"kueue-system","name":"c1f6bfd2.kueue.x-k8s.io","uid":"6c646dca-3b67-4d65-84cf-188eb716d32f","apiVersion":"coordination.k8s.io/v1","resourceVersion":"21205702"},"reason":"LeaderElection"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:30.077207156Z","logger":"cert-rotation","caller":"rotator/rotator.go:263","msg":"starting cert rotator controller"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:30.077272733Z","caller":"controller/controller.go:220","msg":"Starting workers","controller":"cert-rotator","worker count":1}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:30.077309642Z","logger":"cert-rotation","caller":"rotator/rotator.go:307","msg":"refreshing CA and server certs"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:30.077383589Z","logger":"cert-rotation","caller":"rotator/rotator.go:307","msg":"refreshing CA and server certs"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:31.692365042Z","logger":"cert-rotation","caller":"rotator/rotator.go:313","msg":"server certs refreshed"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"error","ts":"2023-12-13T21:12:31.880151587Z","logger":"cert-rotation","caller":"rotator/rotator.go:309","msg":"could not refresh CA and server certs","error":"Operation cannot be fulfilled on secrets \"kueue-webhook-server-cert\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"github.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded.func1\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:309\nk8s.io/apimachinery/pkg/util/wait.runConditionWithCrashProtection\n\t/go/pkg/mod/k8s.io/apimachinery@v0.28.3/pkg/util/wait/wait.go:145\nk8s.io/apimachinery/pkg/util/wait.ExponentialBackoff\n\t/go/pkg/mod/k8s.io/apimachinery@v0.28.3/pkg/util/wait/backoff.go:461\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:337\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:756\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"info","ts":"2023-12-13T21:12:31.901579576Z","logger":"cert-rotation","caller":"rotator/rotator.go:334","msg":"no cert refresh needed"}
kueue-controller-manager-9bf76c49b-7dmsg manager {"level":"error","ts":"2023-12-13T21:12:31.901610299Z","logger":"cert-rotation","caller":"rotator/rotator.go:770","msg":"secret is not well-formed, cannot update webhook configurations","error":"Cert secret is not well-formed, missing ca.crt","errorVerbose":"Cert secret is not well-formed, missing ca.crt\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.buildArtifactsFromSecret\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:488\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:768\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227\nruntime.goexit\n\t/usr/local/go/src/runtime/asm_amd64.s:1650","stacktrace":"github.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:770\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227"}
```

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-13T21:23:39Z

```
{"level":"error","ts":"2023-12-13T17:00:01.51310104Z","logger":"cert-rotation","caller":"rotator/rotator.go:309","msg":"could not refresh CA and server certs","error":"Operation cannot be fulfilled on secrets \"kueue-webhook-server-cert\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"github.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded.func1\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:309\nk8s.io/apimachinery/pkg/util/wait.runConditionWithCrashProtection\n\t/go/pkg/mod/k8s.io/apimachinery@v0.28.3/pkg/util/wait/wait.go:145\nk8s.io/apimachinery/pkg/util/wait.ExponentialBackoff\n\t/go/pkg/mod/k8s.io/apimachinery@v0.28.3/pkg/util/wait/backoff.go:461\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:337\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:756\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227"}
kueue-controller-manager-859c9597fb-5wddx manager {"level":"info","ts":"2023-12-13T17:00:01.532163215Z","logger":"cert-rotation","caller":"rotator/rotator.go:334","msg":"no cert refresh needed"}
kueue-controller-manager-859c9597fb-5wddx manager {"level":"error","ts":"2023-12-13T17:00:01.532199684Z","logger":"cert-rotation","caller":"rotator/rotator.go:770","msg":"secret is not well-formed, cannot update webhook configurations","error":"Cert secret is not well-formed, missing ca.crt","errorVerbose":"Cert secret is not well-formed, missing ca.crt\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.buildArtifactsFromSecret\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:488\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:768\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227\nruntime.goexit\n\t/usr/local/go/src/runtime/asm_amd64.s:1650","stacktrace":"github.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:770\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227"}```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T18:04:46Z

Not sure if related, but other problems related to the cert-rotator are being looked at https://github.com/kubernetes-sigs/kueue/issues/1445#issuecomment-1856265087

That said, I don't see how that could be related to the pytorch reconciler. And why wouldn't jobs be affected.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T18:08:28Z

Do you see any log line saying `Certs ready`?
Or `No matching API server for job framework, skip to create controller and webhook`.

Also, are you creating your pytorch jobs with the suspend field set? I have the feeling that these jobs are just bypassing kueue altogether.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T14:12:57Z

I found the helm chart doesn't have webhookConfigurations for kubeflowjobs. I will create a PR.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-15T14:25:20Z

uhm... I hope we can make the webhook files synchronization part of the checks, but I remember it was hard as we needed some overrides.

Worth thinking about it after a hotfix

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T14:27:18Z

> uhm... I hope we can make the webhook files synchronization part of the checks, but I remember it was hard as we needed some overrides.
> 
> Worth thinking about it after a hotfix

I agree. We should add script in follow ups.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T14:32:34Z

Created: #1460

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-15T15:40:57Z

@jrleslie can you test the helm installation using this branch? https://github.com/kubernetes-sigs/kueue/tree/release-0.5/charts/kueue

We can maybe do an official release right after New Year's.

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-15T15:53:53Z

Yep - I can test on my side. Give me a few minutes.

### Comment by [@jrleslie](https://github.com/jrleslie) — 2023-12-15T17:22:21Z

@alculquicondor @tenzen-y I think that may have resolved it. Ran the test scenario above end-to-end on both a local kind cluster and our ec2 based cluster and things look good with the node-selectors. 

I was originally seeing some inconsistencies with the crds on the ec2 based cluster, but I think that may have been caused by a race condition where crds were still being removed and running test scenarios too quickly back-to-back.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-15T17:59:06Z

/close
Feel free to reopen if you find any other problems

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-15T17:59:11Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1407#issuecomment-1858279259):

>/close
>Feel free to reopen if you find any other problems


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T19:09:40Z

> @alculquicondor @tenzen-y I think that may have resolved it. Ran the test scenario above end-to-end on both a local kind cluster and our ec2 based cluster and things look good with the node-selectors.
> 
> I was originally seeing some inconsistencies with the crds on the ec2 based cluster, but I think that may have been caused by a race condition where crds were still being removed and running test scenarios too quickly back-to-back.

It's great to hear. Thanks.
