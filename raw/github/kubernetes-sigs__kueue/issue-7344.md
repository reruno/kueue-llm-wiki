# Issue #7344: v1beta2: Kueue does not start after upgrade to 0.15.0-rc.0

**Summary**: v1beta2: Kueue does not start after upgrade to 0.15.0-rc.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7344

**Last updated**: 2025-11-24T16:56:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Edwinhr716](https://github.com/Edwinhr716)
- **Created**: 2025-10-22T18:24:08Z
- **Updated**: 2025-11-24T16:56:39Z
- **Closed**: 2025-11-24T16:56:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 23

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When I deploy Kueue using the helm deployment at head 

```
$ git clone git@github.com:kubernetes-sigs/kueue.git
$ cd kueue/charts
$ helm install kueue kueue/ --create-namespace --namespace kueue-system
```

And deploy a localQueue, I get the following error

```
$ k get localqueue
Error from server: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": tls: failed to verify certificate: x509: certificate signed by unknown authority
```

This doesn't happen if using the released version of the helm chart.

**What you expected to happen**:
For the following command to return without an error
```
$ k get localqueue
```

**How to reproduce it (as minimally and precisely as possible)**:
Follow the steps above.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.33
- Kueue version (use `git describe --tags --dirty --always`): f2aff8485
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-22T18:37:31Z

Hmm, seeing these errors make me wonder maybe it is fixed in this branch, can you try: https://github.com/kubernetes-sigs/kueue/pull/7318?

### Comment by [@Edwinhr716](https://github.com/Edwinhr716) — 2025-10-22T18:53:46Z

Tested it with that branch, still hit the same error 
```
 k get localqueue
Error from server: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": tls: failed to verify certificate: x509: certificate signed by unknown authority
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T06:04:04Z

I know what is going on. The templates in the branch are referencing main image by default, however for the conversion to work you need to deploy Kueue image built by this branch.

We do this when using the E2E_USE_HELM flag in Makefile (I have tested that locally and the Helm tests passed: https://github.com/kubernetes-sigs/kueue/pull/7318#discussion_r2452775544).  Or it will be easier to use once the PR is merged.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T16:28:05Z

As the PR https://github.com/kubernetes-sigs/kueue/pull/7318 is merged I believe helms should work  fine, can you test maybe again?

### Comment by [@Edwinhr716](https://github.com/Edwinhr716) — 2025-10-24T15:51:07Z

Now getting this error when trying to install using helm chart at head 
```
{"caller":"runtime/runtime.go:221", "error":"failed to list apiextensions.k8s.io/v1, Kind=CustomResourceDefinition: customresourcedefinitions.apiextensions.k8s.io is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "customresourcedefinitions" in API group "apiextensions.k8s.io" at the cluster scope", "level":"error", "logger":"controller-runtime.cache.UnhandledError", "msg":"Failed to watch", "reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114", "stacktrace":"k8s.io/apimachinery/pkg/util/runtime.logError
	/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:221
k8s.io/apimachinery/pkg/util/runtime.handleError
	/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:212
k8s.io/apimachinery/pkg/util/runtime.HandleErrorWithContext
	/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:198
k8s.io/client-go/tools/cache.DefaultWatchErrorHandler
	/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:205
k8s.io/client-go/tools/cache.(*Reflector).RunWithContext.func1
	/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:361
k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233
k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255
k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256
k8s.io/apimachinery/pkg/util/wait.BackoffUntil
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233
k8s.io/client-go/tools/cache.(*Reflector).RunWithContext
	/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:359
k8s.io/client-go/tools/cache.(*controller).RunWithContext.(*Group).StartWithContext.func3
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:63
k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:72", "ts":"2025-10-24T15:49:07.227199806Z", "type":"apiextensions.k8s.io/v1, Kind=CustomResourceDefinition"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T15:55:41Z

Weird, that PR introduce the required permissions here: https://github.com/kubernetes-sigs/kueue/pull/7318/files#diff-551fa6e9f4f56c712cbde8e7e176be653d8b14821f0d6d7d2e7fd86dedcd0fb7R75-R83

### Comment by [@Edwinhr716](https://github.com/Edwinhr716) — 2025-10-24T16:05:15Z

That's odd, I've been running into different issues ever since I rebased into main. I now have to disable Multikueue in all versions of Kueue that I deploy because I keep running into 
```
could not setup multikueue indexer: setting index on workloads admission checks: indexer conflict: map[field:status.admissionChecks:{}]"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T13:45:51Z

Ok, I tried today and succeeded using exactly this command, `helm install kueue kueue/ --create-namespace --namespace kueue-system`, but I had to also apply these changes: https://github.com/kubernetes-sigs/kueue/pull/7410. Please test again from that branch or main if merged.

### Comment by [@izturn](https://github.com/izturn) — 2025-11-18T10:24:14Z

something wrong:
## 1.  Install 0.14.0: 
```
helm install kueue ./kueue-0.14.0.tgz   --namespace kueue-system   --create-namespace   --wait --timeout 300s
```
 
 
 **Result:  Running**

## 2.  Create the CRs: 
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: lq
  namespace: kueue-system
spec:
  clusterQueue: cq
  stopPolicy: None

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  annotations:
    baize.io/description: ''
  generation: 1
  labels:
  name: cq
spec:
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
      flavors:
        - name: flv
          resources:
            - name: cpu
              nominalQuota: '200'
            - name: memory
              nominalQuota: '214748364800'
  stopPolicy: None

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: flv
spec:
  nodeLabels:
  tolerations:
    - effect: NoExecute
      key: node.kubernetes.io/not-ready
      operator: Exists
      tolerationSeconds: 300
    - effect: NoExecute
      key: node.kubernetes.io/unreachable
      operator: Exists
      tolerationSeconds: 300
    - effect: NoSchedule
      key: kwok.x-k8s.io/node
      operator: Exists

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: Topology
metadata:
  name: top
spec:
  levels:
    - nodeLabel: rdma-zone
    - nodeLabel: supernode

---
```
## 3. Upgrade to 0.15.0-rc.0
```
 helm upgrade --install kueue ./kueue-0.15.0-rc.0.tgz   --namespace kueue-system   --create-namespace   --wait   --timeout 300s
``` 
 **Result:  Failed**

### The log: 
```
{"level":"info","ts":"2025-11-18T10:06:58.865373665Z","logger":"setup","caller":"kueue/main.go:507","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta2\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    Pod: 5\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 5\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - ray.io/raycluster\n  - jobset.x-k8s.io/jobset\n  - trainer.kubeflow.org/trainjob\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  - kubeflow.org/jaxjob\n  - workload.codeflare.dev/appwrapper\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nwaitForPodsReady: {}\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-11-18T10:06:58.865846417Z","logger":"setup","caller":"kueue/main.go:153","msg":"Initializing","gitVersion":"v0.15.0-rc.0","gitCommit":"f6435a6d32fab03de5d05e2521473f5c60a7993d","buildDate":"2025-11-13T06:57:40Z"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.866078755Z","logger":"setup","caller":"features/kube_features.go:344","msg":"Loaded feature gates","featureGates":{"AdmissionFairSharing":true,"ConfigurableResourceTransformations":true,"DynamicResourceAllocation":false,"ElasticJobsViaWorkloadSlices":false,"FlavorFungibility":true,"FlavorFungibilityImplicitPreferenceDefault":false,"HierarchicalCohorts":true,"LendingLimit":true,"LocalQueueDefaulting":true,"LocalQueueMetrics":false,"ManagedJobsNamespaceSelectorAlwaysRespected":true,"MultiKueue":true,"MultiKueueAdaptersForCustomJobs":false,"MultiKueueAllowInsecureKubeconfigs":false,"MultiKueueBatchJobWithManagedBy":true,"ObjectRetentionPolicies":true,"PartialAdmission":true,"PrioritySortingWithinCohort":true,"ReclaimablePods":true,"SanitizePodSets":true,"TASFailedNodeReplacement":true,"TASFailedNodeReplacementFailFast":true,"TASProfileLeastFreeCapacity":false,"TASProfileMixed":true,"TASReplaceNodeOnPodTermination":true,"TopologyAwareScheduling":true,"VisibilityOnDemand":true,"WorkloadRequestUseMergePatch":false}}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.866693241Z","logger":"setup","caller":"kueue/main.go:202","msg":"K8S Client","qps":50,"burst":100}
{"level":"error","ts":"2025-11-18T10:06:58.907713982Z","logger":"setup","caller":"kueue/main.go:306","msg":"Skipping admission check controller setup: Provisioning Requests not supported (Possible cause: missing or unsupported cluster-autoscaler)","error":"no matches for kind \"ProvisioningRequest\" in version \"autoscaling.x-k8s.io/v1\"","stacktrace":"main.setupIndexes\n\t/workspace/cmd/kueue/main.go:306\nmain.main\n\t/workspace/cmd/kueue/main.go:247\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:285"}
{"level":"info","ts":"2025-11-18T10:06:58.915568922Z","logger":"setup","caller":"kueue/main.go:448","msg":"Probe endpoints are configured on healthz and readyz"}
{"level":"info","ts":"2025-11-18T10:06:58.915708883Z","logger":"setup","caller":"kueue/main.go:291","msg":"Starting manager"}
{"level":"info","ts":"2025-11-18T10:06:58.91575849Z","logger":"setup","caller":"cert/cert.go:84","msg":"Waiting for certificate generation to complete"}
{"level":"info","ts":"2025-11-18T10:06:58.915969545Z","caller":"manager/server.go:83","msg":"starting server","name":"health probe","addr":"[::]:8081"}
{"level":"info","ts":"2025-11-18T10:06:58.915882143Z","logger":"controller-runtime.metrics","caller":"server/server.go:208","msg":"Starting metrics server"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.919970473Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1.LimitRange","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.920129657Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1.Job","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.922045321Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1beta2.MultiKueueConfig","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.922265888Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1beta2.AdmissionCheck","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.923737257Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1.Node","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.92453172Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1.Pod","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.924691011Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1beta2.MultiKueueCluster","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.925247552Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1beta2.ResourceFlavor","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-11-18T10:06:58.927882486Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:436","msg":"Caches populated","type":"*v1beta2.Workload","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"error","ts":"2025-11-18T10:06:58.935678135Z","logger":"controller-runtime.cache.UnhandledError","caller":"runtime/runtime.go:221","msg":"Failed to watch","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114","type":"*v1beta2.LocalQueue","error":"failed to list *v1beta2.LocalQueue: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": tls: failed to verify certificate: x509: certificate signed by unknown authority","stacktrace":"k8s.io/apimachinery/pkg/util/runtime.logError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:221\nk8s.io/apimachinery/pkg/util/runtime.handleError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:212\nk8s.io/apimachinery/pkg/util/runtime.HandleErrorWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:198\nk8s.io/client-go/tools/cache.DefaultWatchErrorHandler\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:205\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext.func1\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:361\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:359\nk8s.io/client-go/tools/cache.(*controller).RunWithContext.(*Group).StartWithContext.func3\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:63\nk8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:72"}
{"level":"info","ts":"2025-11-18T10:06:59.025708118Z","logger":"controller-runtime.metrics","caller":"server/server.go:247","msg":"Serving metrics server","bindAddress":":8443","secure":true}
I1118 10:06:59.193884       1 serving.go:380] Generated self-signed cert (/visibility/apiserver.crt, /visibility/apiserver.key)
I1118 10:06:59.682015       1 plugins.go:157] Loaded 2 mutating admission controller(s) successfully in the following order: NamespaceLifecycle,MutatingAdmissionPolicy.
I1118 10:06:59.689500       1 handler.go:285] Adding GroupVersion visibility.kueue.x-k8s.io v1beta2 to ResourceManager
I1118 10:06:59.689954       1 handler.go:285] Adding GroupVersion visibility.kueue.x-k8s.io v1beta1 to ResourceManager
I1118 10:06:59.703155       1 requestheader_controller.go:180] Starting RequestHeaderAuthRequestController
I1118 10:06:59.703249       1 shared_informer.go:349] "Waiting for caches to sync" controller="RequestHeaderAuthRequestController"
I1118 10:06:59.703340       1 configmap_cafile_content.go:205] "Starting controller" name="client-ca::kube-system::extension-apiserver-authentication::client-ca-file"
I1118 10:06:59.703357       1 shared_informer.go:349] "Waiting for caches to sync" controller="client-ca::kube-system::extension-apiserver-authentication::client-ca-file"
I1118 10:06:59.703383       1 configmap_cafile_content.go:205] "Starting controller" name="client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
I1118 10:06:59.703395       1 shared_informer.go:349] "Waiting for caches to sync" controller="client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
I1118 10:06:59.703974       1 secure_serving.go:211] Serving securely on [::]:8082
I1118 10:06:59.704086       1 dynamic_serving_content.go:135] "Starting controller" name="serving-cert::/visibility/apiserver.crt::/visibility/apiserver.key"
I1118 10:06:59.704349       1 tlsconfig.go:243] "Starting DynamicServingCertificateController"
I1118 10:06:59.704483       1 apf_controller.go:377] Starting API Priority and Fairness config controller
{"level":"error","ts":"2025-11-18T10:06:59.77640903Z","logger":"controller-runtime.cache.UnhandledError","caller":"runtime/runtime.go:221","msg":"Failed to watch","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114","type":"*v1beta2.LocalQueue","error":"failed to list *v1beta2.LocalQueue: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": tls: failed to verify certificate: x509: certificate signed by unknown authority","stacktrace":"k8s.io/apimachinery/pkg/util/runtime.logError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:221\nk8s.io/apimachinery/pkg/util/runtime.handleError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:212\nk8s.io/apimachinery/pkg/util/runtime.HandleErrorWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:198\nk8s.io/client-go/tools/cache.DefaultWatchErrorHandler\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:205\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext.func1\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:361\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:359\nk8s.io/client-go/tools/cache.(*controller).RunWithContext.(*Group).StartWithContext.func3\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:63\nk8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:72"}
I1118 10:06:59.803504       1 shared_informer.go:356] "Caches are synced" controller="RequestHeaderAuthRequestController"
I1118 10:06:59.803618       1 shared_informer.go:356] "Caches are synced" controller="client-ca::kube-system::extension-apiserver-authentication::client-ca-file"
I1118 10:06:59.803660       1 shared_informer.go:356] "Caches are synced" controller="client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
I1118 10:06:59.806031       1 apf_controller.go:382] Running API Priority and Fairness config worker
I1118 10:06:59.806075       1 apf_controller.go:385] Running API Priority and Fairness periodic rebalancing process
{"level":"error","ts":"2025-11-18T10:07:02.324646054Z","logger":"controller-runtime.cache.UnhandledError","caller":"runtime/runtime.go:221","msg":"Failed to watch","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114","type":"*v1beta2.LocalQueue","error":"failed to list *v1beta2.LocalQueue: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": tls: failed to verify certificate: x509: certificate signed by unknown authority","stacktrace":"k8s.io/apimachinery/pkg/util/runtime.logError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:221\nk8s.io/apimachinery/pkg/util/runtime.handleError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:212\nk8s.io/apimachinery/pkg/util/runtime.HandleErrorWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:198\nk8s.io/client-go/tools/cache.DefaultWatchErrorHandler\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:205\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext.func1\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:361\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:359\nk8s.io/client-go/tools/cache.(*controller).RunWithContext.(*Group).StartWithContext.func3\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:63\nk8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:72"}
{"level":"debug","ts":"2025-11-18T10:07:05.044039429Z","logger":"controller-runtime.healthz","caller":"healthz/healthz.go:60","msg":"healthz check failed","checker":"readyz","error":"certificates are not ready"}
{"level":"info","ts":"2025-11-18T10:07:05.044301784Z","logger":"controller-runtime.healthz","caller":"healthz/healthz.go:128","msg":"healthz check failed","statuses":[{}]}
{"level":"error","ts":"2025-11-18T10:07:07.468805324Z","logger":"controller-runtime.cache.UnhandledError","caller":"runtime/runtime.go:221","msg":"Failed to watch","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114","type":"*v1beta2.LocalQueue","error":"failed to list *v1beta2.LocalQueue: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": tls: failed to verify certificate: x509: certificate signed by unknown authority","stacktrace":"k8s.io/apimachinery/pkg/util/runtime.logError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:221\nk8s.io/apimachinery/pkg/util/runtime.handleError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:212\nk8s.io/apimachinery/pkg/util/runtime.HandleErrorWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:198\nk8s.io/client-go/tools/cache.DefaultWatchErrorHandler\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:205\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext.func1\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:361\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:359\nk8s.io/client-go/tools/cache.(*controller).RunWithContext.(*Group).StartWithContext.func3\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:63\nk8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:72"}
{"level":"debug","ts":"2025-11-18T10:07:10.04631679Z","logger":"controller-runtime.healthz","caller":"healthz/healthz.go:60","msg":"healthz check failed","checker":"readyz","error":"certificates are not ready"}
{"level":"info","ts":"2025-11-18T10:07:10.046422247Z","logger":"controller-runtime.healthz","caller":"healthz/healthz.go:128","msg":"healthz check failed","statuses":[{}]}
{"level":"debug","ts":"2025-11-18T10:07:15.044177661Z","logger":"controller-runtime.healthz","caller":"healthz/healthz.go:60","msg":"healthz check failed","checker":"readyz","error":"certificates are not ready"}
{"level":"info","ts":"2025-11-18T10:07:15.0443267Z","logger":"controller-runtime.healthz","caller":"healthz/healthz.go:128","msg":"healthz check failed","statuses":[{}]}
{"level":"error","ts":"2025-11-18T10:07:19.314142527Z","logger":"controller-runtime.cache.UnhandledError","caller":"runtime/runtime.go:221","msg":"Failed to watch","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114","type":"*v1beta2.LocalQueue","error":"failed to list *v1beta2.LocalQueue: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": tls: failed to verify certificate: x509: certificate signed by unknown authority","stacktrace":"k8s.io/apimachinery/pkg/util/runtime.logError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:221\nk8s.io/apimachinery/pkg/util/runtime.handleError\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:212\nk8s.io/apimachinery/pkg/util/runtime.HandleErrorWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:198\nk8s.io/client-go/tools/cache.DefaultWatchErrorHandler\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:205\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext.func1\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:361\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/client-go/tools/cache.(*Reflector).RunWithContext\n\t/workspace/vendor/k8s.io/client-go/tools/cache/reflector.go:359\nk8s.io/client-go/tools/cache.(*controller).RunWithContext.(*Group).StartWithContext.func3\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:63\nk8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:72"}

...............
```

@mimowo pls help me to fix it

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T10:37:47Z

can you describe the `kubectl describe deploy -nkueue-system`

### Comment by [@izturn](https://github.com/izturn) — 2025-11-18T10:39:07Z

```
Name:                   kueue-controller-manager
Namespace:              kueue-system
CreationTimestamp:      Tue, 18 Nov 2025 17:55:49 +0800
Labels:                 app.kubernetes.io/component=controller
                        app.kubernetes.io/instance=kueue
                        app.kubernetes.io/managed-by=Helm
                        app.kubernetes.io/name=kueue
                        app.kubernetes.io/version=v0.15.0-rc.0
                        control-plane=controller-manager
                        helm.sh/chart=kueue-0.15.0-rc.0
                        k8slens-edit-resource-version=v1
Annotations:            deployment.kubernetes.io/revision: 4
                        meta.helm.sh/release-name: kueue
                        meta.helm.sh/release-namespace: kueue-system
Selector:               app.kubernetes.io/instance=kueue,app.kubernetes.io/name=kueue,control-plane=controller-manager     
Replicas:               1 desired | 1 updated | 2 total | 1 available | 1 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:           app.kubernetes.io/instance=kueue
                    app.kubernetes.io/name=kueue
                    control-plane=controller-manager
  Annotations:      charts.kueue.x-k8s.io/config-checksum: 95acca0b796d0bfd293b271cea2ee7ca622e18b683a05d13258541a6421fc67e
                    kubectl.kubernetes.io/default-container: manager
  Service Account:  kueue-controller-manager
  Containers:
   manager:
    Image:       us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.15.0-rc.0
    Ports:       8082/TCP, 9443/TCP, 8443/TCP
    Host Ports:  0/TCP, 0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-log-level=2
    Limits:
      cpu:     2
      memory:  512Mi
    Requests:
      cpu:        500m
      memory:     512Mi
    Liveness:     http-get http://:8081/healthz delay=15s timeout=1s period=15s #success=1 #failure=3
    Readiness:    http-get http://:8081/readyz delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /controller_manager_config.yaml from manager-config (rw,path="controller_manager_config.yaml")
      /tmp/k8s-webhook-server/serving-certs from cert (ro)
      /visibility from visibility (rw)
  Volumes:
   cert:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kueue-webhook-server-cert
    Optional:    false
   manager-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      kueue-manager-config
    Optional:  false
   visibility:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
    SizeLimit:  <unset>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    False   ProgressDeadlineExceeded
OldReplicaSets:  kueue-controller-manager-7bd58d49f7 (1/1 replicas created)
NewReplicaSet:   kueue-controller-manager-6b7d8b7d86 (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  42m   deployment-controller  Scaled up replica set kueue-controller-manager-8569448d9c from 0 to 1
  Normal  ScalingReplicaSet  41m   deployment-controller  Scaled up replica set kueue-controller-manager-59b769dc5c from 0 to 1
  Normal  ScalingReplicaSet  39m   deployment-controller  Scaled down replica set kueue-controller-manager-8569448d9c from 1 to 0
  Normal  ScalingReplicaSet  39m   deployment-controller  Scaled up replica set kueue-controller-manager-7bd58d49f7 from 0 to 1
  Normal  ScalingReplicaSet  39m   deployment-controller  Scaled down replica set kueue-controller-manager-59b769dc5c from 1 to 0
  Normal  ScalingReplicaSet  31m   deployment-controller  Scaled up replica set kueue-controller-manager-6b7d8b7d86 from 0 to 1
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T10:41:37Z

hm, it seems you have one Pod that is unavailable, maybe do:

`kubectl describe pods -nkueue-system`

### Comment by [@izturn](https://github.com/izturn) — 2025-11-19T01:53:09Z

```
Name:             kueue-controller-manager-556f858896-r6k55
Namespace:        kueue-system
Priority:         0
Service Account:  kueue-controller-manager
Node:             bms4-control-plane/172.18.0.3
Start Time:       Wed, 19 Nov 2025 09:46:50 +0800
Labels:           app.kubernetes.io/instance=kueue
                  app.kubernetes.io/name=kueue
                  control-plane=controller-manager
                  pod-template-hash=556f858896
Annotations:      charts.kueue.x-k8s.io/config-checksum: 95acca0b796d0bfd293b271cea2ee7ca622e18b683a05d13258541a6421fc67e
                  kubectl.kubernetes.io/default-container: manager
                  kubectl.kubernetes.io/restartedAt: 2025-11-19T01:46:49.845Z
Status:           Running
IP:               10.244.0.30
IPs:
  IP:           10.244.0.30
Controlled By:  ReplicaSet/kueue-controller-manager-556f858896
Containers:
  manager:
    Container ID:  containerd://a0889ea2d2b1a79d2612137cfaadacc5297a21ed94db32d3ad20c127aedfcfad
    Image:         us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.15.0-rc.0
    Image ID:      docker.io/library/import-2025-11-18@sha256:ab5155823807904394e936e62f0ac6c1df09a69a47350b67cb1140e0bc80a1f4
    Ports:         8082/TCP, 9443/TCP, 8443/TCP
    Host Ports:    0/TCP, 0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-log-level=2
    State:          Running
      Started:      Wed, 19 Nov 2025 09:46:51 +0800
    Ready:          False
    Restart Count:  0
    Limits:
      cpu:     2
      memory:  512Mi
    Requests:
      cpu:        500m
      memory:     512Mi
    Liveness:     http-get http://:8081/healthz delay=15s timeout=1s period=15s #success=1 #failure=3
    Readiness:    http-get http://:8081/readyz delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /controller_manager_config.yaml from manager-config (rw,path="controller_manager_config.yaml")
      /tmp/k8s-webhook-server/serving-certs from cert (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-47sjj (ro)
      /visibility from visibility (rw)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       False
  ContainersReady             False
  PodScheduled                True
Volumes:
  cert:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kueue-webhook-server-cert
    Optional:    false
  manager-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      kueue-manager-config
    Optional:  false
  visibility:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
    SizeLimit:  <unset>
  kube-api-access-47sjj:
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
  Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  5m49s                 default-scheduler  Successfully assigned kueue-system/kueue-controller-manager-556f858896-r6k55 to bms4-control-plane
  Normal   Pulled     5m49s                 kubelet            Container image "us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.15.0-rc.0" already present on machine
  Normal   Created    5m49s                 kubelet            Created container: manager
  Normal   Started    5m48s                 kubelet            Started container manager
  Warning  Unhealthy  41s (x63 over 5m42s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 500


Name:             kueue-controller-manager-7bd58d49f7-92wqh
Namespace:        kueue-system
Priority:         0
Service Account:  kueue-controller-manager
Node:             bms4-control-plane/172.18.0.3
Start Time:       Wed, 19 Nov 2025 09:47:49 +0800
Labels:           app.kubernetes.io/instance=kueue
                  app.kubernetes.io/name=kueue
                  control-plane=controller-manager
                  pod-template-hash=7bd58d49f7
Annotations:      charts.kueue.x-k8s.io/config-checksum: fb8e3eb0c9ff5f1b55564110b5d8387361f3e4b8bc2a7b32de4637a1f66ac92d
                  kubectl.kubernetes.io/default-container: manager
Status:           Running
IP:               10.244.0.31
IPs:
  IP:           10.244.0.31
Controlled By:  ReplicaSet/kueue-controller-manager-7bd58d49f7
Containers:
  manager:
    Container ID:  containerd://026a5c76b0c9294ca8cf0bfa0b18f3b4f1f5f9e09296c763157d0e568034e051
    Image:         us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.14.0
    Image ID:      docker.io/library/import-2025-11-18@sha256:ef9077ccda662210f93820b96c8ce5bdf2bd30ab879d6d86f987389f786eefb9
    Ports:         8082/TCP, 9443/TCP, 8443/TCP
    Host Ports:    0/TCP, 0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-log-level=2
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Wed, 19 Nov 2025 09:50:46 +0800
      Finished:     Wed, 19 Nov 2025 09:50:46 +0800
    Ready:          False
    Restart Count:  5
    Limits:
      cpu:     2
      memory:  512Mi
    Requests:
      cpu:        500m
      memory:     512Mi
    Liveness:     http-get http://:8081/healthz delay=15s timeout=1s period=15s #success=1 #failure=3
    Readiness:    http-get http://:8081/readyz delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /controller_manager_config.yaml from manager-config (rw,path="controller_manager_config.yaml")
      /tmp/k8s-webhook-server/serving-certs from cert (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-2mb4m (ro)
      /visibility from visibility (rw)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       False
  ContainersReady             False
  PodScheduled                True
Volumes:
  cert:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kueue-webhook-server-cert
    Optional:    false
  manager-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      kueue-manager-config
    Optional:  false
  visibility:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
    SizeLimit:  <unset>
  kube-api-access-2mb4m:
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
  Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  4m50s                 default-scheduler  Successfully assigned kueue-system/kueue-controller-manager-7bd58d49f7-92wqh to bms4-control-plane
  Normal   Pulled     114s (x6 over 4m49s)  kubelet            Container image "us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.14.0" already present on machine
  Normal   Created    114s (x6 over 4m49s)  kubelet            Created container: manager
  Normal   Started    113s (x6 over 4m49s)  kubelet            Started container manager
  Warning  BackOff    69s (x25 over 4m47s)  kubelet            Back-off restarting failed container manager in pod kueue-controller-manager-7bd58d49f7-92wqh_kueue-system(22f3aad9-ed17-47d4-bdfa-146d7178344d)
```

### Comment by [@izturn](https://github.com/izturn) — 2025-11-19T07:53:52Z

I retried this on a different cluster and encountered the same error.
@mimowo, any suggestions?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T08:05:41Z

I will be looking into this today, maybe there is a bug.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T17:02:11Z

I tested locally by installing 0.14.4 first, and upgrading to 0.15.0-rc.0, and it worked fine, I executed:

Install old Kueue:
```sh
❯ helm install kueue oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.14.4 \
  --namespace  kueue-system \
  --create-namespace \
  --wait --timeout 300s
```
download the RC:
```
curl -Lv https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0-rc.0.tar.gz -ohelm.tar.gz
```

upgrade
```sh
❯ helm upgrade --install kueue ./helm.tar.gz \
  --namespace kueue-system \
  --create-namespace \
  --wait --timeout 300s
```
I can create resources:
```sh
❯ k create -f cluster.yaml
resourceflavor.kueue.x-k8s.io/default-flavor created
clusterqueue.kueue.x-k8s.io/cluster-queue created
localqueue.kueue.x-k8s.io/user-queue created
```
```sh
❯ k create -f job.yaml
job.batch/sample-jobbgzkq created
```
That was tested on Kind. I will later check on GKE. can you maybe also check on Kind? What is the cluster host you are testing it on?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-19T18:26:30Z

I suspect what’s happening here is that the upgrade only works in @mimowo's workflow because the conversion webhooks are not called until the new certs settle. When LocalQueues already exist before the upgrade, the RC rotates kueue-webhook-server-cert but never updates the CRD conversion caBundle. That leaves the API server unable to reach the conversion webhook. The controller cache then loops forever and the RC pod never becomes Ready, which causes Helm’s wait to time out.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T18:43:21Z

Indeed, I replicated the issue on Kind by just creating an instance of LQ before upgrade. Let's think how to solve, and research how other projects solve this, because it shouldn't be a problem unique to Kueue.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-19T18:45:17Z

I will assign this issue to me if that's ok with you.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-19T18:45:38Z

/assign @sohankunkerkar

### Comment by [@izturn](https://github.com/izturn) — 2025-11-20T05:53:50Z

btw, This issue doesn’t occur only with `helm upgrade`; it also happens when using `kubectl apply`. @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T13:53:48Z

Yes, let me retitle
/retitle v1beta2: Kueue does not start after upgrade to 0.15.0-rc.0

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T13:59:41Z

@sohankunkerkar have you been able to confirm the hypothesis from https://github.com/kubernetes-sigs/kueue/issues/7344#issuecomment-3554091666. I'm wondering what exactly is the difference why upgrade works if LQ is not created vs. if it is created. Maybe we just need to make sure something is cleaned on startup as if the system was "clean".
