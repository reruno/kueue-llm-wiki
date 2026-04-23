# Issue #6797: controller-manager is stuck in a CrashLoopBackOff state when a different release name is used.

**Summary**: controller-manager is stuck in a CrashLoopBackOff state when a different release name is used.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6797

**Last updated**: 2025-09-12T07:34:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@buraksekili](https://github.com/buraksekili)
- **Created**: 2025-09-11T14:26:19Z
- **Updated**: 2025-09-12T07:34:10Z
- **Closed**: 2025-09-12T07:34:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If you use a release name other than "kueue" while installing Kueue, the controller-manager will be stuck in a CrashLoopBackOff state.

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

```
$ helm upgrade --install something oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.13.3 \
  --namespace  kueue \
  --create-namespace \
  --wait --timeout 300s
```

```
$ k get po -n kueue         
NAME                                                  READY   STATUS             RESTARTS      AGE
something-kueue-controller-manager-595cf866fb-gr7pj   0/1     CrashLoopBackOff   5 (48s ago)   3m37s
```

Now uninstall the failed release, and install again with "kueue" release name:
```
$ helm uninstall -n kueue something 
release "something" uninstalled

$ helm upgrade --install kueue oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.13.3 \
  --namespace  kueue \
  --create-namespace \
  --wait --timeout 300s

$ k get po -n kueue
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-864ddb8d8b-22ssk   1/1     Running   0          6m13s

```



**Anything else we need to know?**:

Logs of failed release:
<details>

```
{"level":"info","ts":"2025-09-11T14:20:52.485575817Z","logger":"setup","caller":"kueue/main.go:482","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    Pod: 5\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 5\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - ray.io/raycluster\n  - jobset.x-k8s.io/jobset\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  - kubeflow.org/jaxjob\n  - workload.codeflare.dev/appwrapper\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwaitForPodsReady: {}\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-09-11T14:20:52.485742674Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.3","gitCommit":"0d74c06edafeb143736e7e6768cba24635a33cf7","buildDate":"2025-08-22T12:20:19Z"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.48586062Z","logger":"setup","caller":"features/kube_features.go:317","msg":"Loaded feature gates","featureGates":{"AdmissionFairSharing":false,"ConfigurableResourceTransformations":true,"ElasticJobsViaWorkloadSlices":false,"ExposeFlavorsInLocalQueue":true,"FlavorFungibility":true,"FlavorFungibilityImplicitPreferenceDefault":false,"HierarchicalCohorts":true,"LendingLimit":true,"LocalQueueDefaulting":true,"LocalQueueMetrics":false,"ManagedJobsNamespaceSelector":true,"ManagedJobsNamespaceSelectorAlwaysRespected":false,"MultiKueue":true,"MultiKueueBatchJobWithManagedBy":false,"ObjectRetentionPolicies":true,"PartialAdmission":true,"PrioritySortingWithinCohort":true,"ProvisioningACC":true,"QueueVisibility":false,"TASFailedNodeReplacement":false,"TASFailedNodeReplacementFailFast":false,"TASProfileLeastFreeCapacity":false,"TASProfileMixed":false,"TASReplaceNodeOnPodTermination":false,"TopologyAwareScheduling":false,"VisibilityOnDemand":true}}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.486147431Z","logger":"setup","caller":"kueue/main.go:196","msg":"K8S Client","qps":50,"burst":100}
{"level":"error","ts":"2025-09-11T14:20:52.506185001Z","logger":"setup","caller":"kueue/main.go:294","msg":"Skipping admission check controller setup: Provisioning Requests not supported (Possible cause: missing or unsupported cluster-autoscaler)","error":"no matches for kind \"ProvisioningRequest\" in version \"autoscaling.x-k8s.io/v1\"","stacktrace":"main.setupIndexes\n\t/workspace/cmd/kueue/main.go:294\nmain.main\n\t/workspace/cmd/kueue/main.go:234\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:283"}
{"level":"info","ts":"2025-09-11T14:20:52.507875561Z","logger":"setup","caller":"kueue/main.go:423","msg":"Probe endpoints are configured on healthz and readyz"}
{"level":"info","ts":"2025-09-11T14:20:52.507968159Z","logger":"setup","caller":"kueue/main.go:278","msg":"Starting manager"}
{"level":"info","ts":"2025-09-11T14:20:52.507974504Z","logger":"setup","caller":"cert/cert.go:70","msg":"Waiting for certificate generation to complete"}
{"level":"info","ts":"2025-09-11T14:20:52.508115671Z","logger":"controller-runtime.metrics","caller":"server/server.go:208","msg":"Starting metrics server"}
{"level":"info","ts":"2025-09-11T14:20:52.508706505Z","caller":"manager/server.go:83","msg":"starting server","name":"health probe","addr":"[::]:8081"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.511637244Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1beta1.MultiKueueConfig","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.512359327Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1beta1.MultiKueueCluster","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.512656931Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1beta1.AdmissionCheck","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.512750575Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1.LimitRange","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.513125254Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1beta1.LocalQueue","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.513275694Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1.Job","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.516085201Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1beta1.Workload","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"info","ts":"2025-09-11T14:20:52.6093736Z","logger":"cert-rotation","caller":"rotator/rotator.go:290","msg":"starting cert rotator controller"}
I0911 14:20:52.609535       1 leaderelection.go:257] attempting to acquire leader lease kueue/c1f6bfd2.kueue.x-k8s.io...
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.647993933Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.659947794Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"*v1.Secret","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"Level(-2)","ts":"2025-09-11T14:20:52.664329453Z","logger":"controller-runtime.cache","caller":"cache/reflector.go:430","msg":"Caches populated","type":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
{"level":"error","ts":"2025-09-11T14:20:52.70994724Z","logger":"cert-rotation","caller":"rotator/rotator.go:293","msg":"could not refresh cert on startup","error":"acquiring secret to update certificates: Secret \"kueue-webhook-server-cert\" not found","errorVerbose":"Secret \"kueue-webhook-server-cert\" not found\nacquiring secret to update certificates\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded.func1\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:331\nk8s.io/apimachinery/pkg/util/wait.runConditionWithCrashProtection\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:150\nk8s.io/apimachinery/pkg/util/wait.ExponentialBackoff\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:477\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:364\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).Start\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:292\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/manager/runnable_group.go:226\nruntime.goexit\n\t/usr/local/go/src/runtime/asm_amd64.s:1700","stacktrace":"github.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).Start\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:293\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/manager/runnable_group.go:226"}
{"level":"info","ts":"2025-09-11T14:20:52.710070416Z","logger":"cert-rotation","caller":"rotator/rotator.go:294","msg":"stopping cert rotator controller"}
{"level":"info","ts":"2025-09-11T14:20:52.710099684Z","caller":"manager/internal.go:538","msg":"Stopping and waiting for non leader election runnables"}
{"level":"info","ts":"2025-09-11T14:20:52.710166085Z","caller":"manager/internal.go:542","msg":"Stopping and waiting for leader election runnables"}
{"level":"info","ts":"2025-09-11T14:20:52.710233626Z","caller":"manager/internal.go:550","msg":"Stopping and waiting for caches"}
{"level":"info","ts":"2025-09-11T14:20:52.710431402Z","caller":"manager/internal.go:554","msg":"Stopping and waiting for webhooks"}
{"level":"info","ts":"2025-09-11T14:20:52.710464056Z","caller":"manager/internal.go:557","msg":"Stopping and waiting for HTTP servers"}
{"level":"info","ts":"2025-09-11T14:20:52.710493338Z","caller":"manager/server.go:68","msg":"shutting down server","name":"health probe","addr":"[::]:8081"}
W0911 14:20:53.051911       1 requestheader_controller.go:204] Unable to get configmap/extension-apiserver-authentication in kube-system.  Usually fixed by 'kubectl create rolebinding -n kube-system ROLEBINDING_NAME --role=extension-apiserver-authentication-reader --serviceaccount=YOUR_NS:YOUR_SA'
{"level":"error","ts":"2025-09-11T14:20:53.051939699Z","logger":"setup","caller":"kueue/main.go:267","msg":"Unable to create and start visibility server","error":"unable to apply VisibilityServerOptions: unable to load configmap based request-header-client-ca-file: configmaps \"extension-apiserver-authentication\" is forbidden: User \"system:serviceaccount:kueue:something-kueue-controller-manager\" cannot get resource \"configmaps\" in API group \"\" in the namespace \"kube-system\"","stacktrace":"main.main.func3\n\t/workspace/cmd/kueue/main.go:267"}
```

</details>

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-11T15:03:04Z

/assign

### Comment by [@buraksekili](https://github.com/buraksekili) — 2025-09-12T06:35:00Z

@mbobrovskyi thank you for your quick action! Is it possible to mitigate this issue until the fix is released?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-12T06:42:33Z

> Is it possible to mitigate this issue until the fix is released?

Yeah, I think we should include this changes on the next release. 
@mimowo WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T06:44:53Z

We are planning to release today, hope the fix can be merged then. I will review today

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T07:02:45Z

cc @tenzen-y it looks like another case where we cannot verify without e2e tests, because the yaml itself is correct.

x-ref: https://github.com/kubernetes-sigs/kueue/issues/5145
