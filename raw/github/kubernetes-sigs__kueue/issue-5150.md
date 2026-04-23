# Issue #5150: VisibilityOnDemand: APIService FailedDiscoveryCheck

**Summary**: VisibilityOnDemand: APIService FailedDiscoveryCheck

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5150

**Last updated**: 2026-01-15T10:09:03Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@milosbw](https://github.com/milosbw)
- **Created**: 2025-05-02T20:19:36Z
- **Updated**: 2026-01-15T10:09:03Z
- **Closed**: 2025-12-07T07:32:35Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 27

## Description

**What happened**:
Tried to install kueue v0.11.4 , went well but I am facing some problem with ApiService.

**What you expected to happen**:
Everything to be up&running (without any errors) after 'helm install kueue'...

**How to reproduce it (as minimally and precisely as possible)**:
I just ran the helm install in my EKS cluster:
```sh
helm install kueue oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.11.4 \
  --namespace  kueue-system \
  --create-namespace \
  --wait --timeout 300s
```
I checked k8s resources, everything is up&running besides 'ApiService' - **FailedDiscoveryCheck**

**Anything else we need to know?**:

```sh
k get apiservice v1beta1.visibility.kueue.x-k8s.io -o yaml
```

```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  creationTimestamp: "2025-05-02T19:50:11Z"
  labels:
    app.kubernetes.io/instance: kueue
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: kueue
    app.kubernetes.io/version: v0.11.4
    argocd.argoproj.io/instance: kueue
    control-plane: controller-manager
    helm.sh/chart: kueue-0.11.4
  name: v1beta1.visibility.kueue.x-k8s.io
  resourceVersion: "5997837"
  uid: cdc7c7c2-9e6d-4291-822c-4a11d0876045
spec:
  group: visibility.kueue.x-k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: kueue-visibility-server
    namespace: kueue-system
    port: 443
  version: v1beta1
  versionPriority: 100
status:
  conditions:
  - lastTransitionTime: "2025-05-02T19:50:11Z"
    message: 'failing or missing response from https://<IP>:8082/apis/visibility.kueue.x-k8s.io/v1beta1:
      Get "https://<IP>:8082/apis/visibility.kueue.x-k8s.io/v1beta1": context
      deadline exceeded'
    reason: FailedDiscoveryCheck
    status: "False"
    type: Available
```
There are no errors in kueue-controller-manager pod's log.

**Environment**:
- Kubernetes version (use `kubectl version`): Server Version: v1.32.3-eks-4096722
- Kueue version (use `git describe --tags --dirty --always`): v0.11.4
- Cloud provider or hardware configuration: AWS EKS(arm based)
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T21:06:55Z

/retitle Helm: ApiService-FailedDiscoveryCheck

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T21:07:41Z

I guess that this is a Helm manifests generation problem. We need to check if Helm generate intended manifests.

### Comment by [@milosbw](https://github.com/milosbw) — 2025-05-03T13:26:47Z

@tenzen-y 
I am facing the same behavior with the 'kubectl apply':
```sh
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.11.4/manifests.yaml
```

This is defined ApiService manifest:

```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/name: kueue
    control-plane: controller-manager
  name: v1beta1.visibility.kueue.x-k8s.io
spec:
  group: visibility.kueue.x-k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: kueue-visibility-server
    namespace: kueue-system
  version: v1beta1
  versionPriority: 100
```

From helm(seems fine too):
```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  labels:
  {{- include "kueue.labels" . | nindent 4 }}
  name: v1beta1.visibility.kueue.x-k8s.io
spec:
  group: visibility.kueue.x-k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: '{{ include "kueue.fullname" . }}-visibility-server'
    namespace: '{{ .Release.Namespace }}'
  version: v1beta1
  versionPriority: 100
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:29:22Z

@milosbw Thank you for letting me know. Do you see the same errors as the Helm installation?

cc: @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:30:41Z

/retitle VisibilityOnDemand: APIService FailedDiscoveryCheck

### Comment by [@milosbw](https://github.com/milosbw) — 2025-05-06T06:53:51Z

> [@milosbw](https://github.com/milosbw) Thank you for letting me know. Do you see the same errors as the Helm installation?
> 
> cc: [@PBundyra](https://github.com/PBundyra)

Yes. The very same error.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T11:57:41Z

Interesting. I tried running it both on Kind and on a real GKE cluster – it seems to be working fine. Unfortunately, I don’t have an AWS account to test it on EKS.

However, when the `kueue-controller-manager` is initializing, I encountered the following error:

```yaml
status:
  conditions:
  - lastTransitionTime: "2025-05-06T11:40:10Z"
    message: endpoints for service/kueue-visibility-server in "kueue-system" have
      no addresses with port name "https"
    reason: MissingEndpoints
    status: "False"
    type: Available
```

Once the `kueue-controller-manager` is fully running:

```yaml
status:
  conditions:
  - lastTransitionTime: "2025-05-06T11:42:00Z"
    message: all checks passed
    reason: Passed
    status: "True"
    type: Available
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T11:58:53Z

Ah, I also catch this error with Kind.

```yaml
status:
  conditions:
  - lastTransitionTime: "2025-05-06T11:56:20Z"
    message: 'failing or missing response from https://10.96.127.168:443/apis/visibility.kueue.x-k8s.io/v1beta1:
      Get "https://10.96.127.168:443/apis/visibility.kueue.x-k8s.io/v1beta1": dial
      tcp 10.96.127.168:443: connect: connection refused'
    reason: FailedDiscoveryCheck
    status: "False"
    type: Available
```

But once the `kueue-controller-manager` is fully running:

```yaml
status:
  conditions:
  - lastTransitionTime: "2025-05-06T11:56:41Z"
    message: all checks passed
    reason: Passed
    status: "True"
    type: Available
```

### Comment by [@milosbw](https://github.com/milosbw) — 2025-05-06T14:32:26Z

@mbobrovskyi  what do you suggest? How should I debug this further?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T14:34:58Z

Could you please check if the error still occurs when the `kueue-controller-manager` is fully running?

### Comment by [@milosbw](https://github.com/milosbw) — 2025-05-06T15:22:17Z

> Could you please check if the error still occurs when the `kueue-controller-manager` is fully running?

It is fully running
nothing in logs (only info logs, no error)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T15:27:31Z

Do you have an error in conditions?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T12:38:31Z

@milosbw if the issue is only temporary during the startup of Kueue, then I think it is WAI. Can we close the issue, or you think there is something that goes beyond it?

### Comment by [@milosbw](https://github.com/milosbw) — 2025-05-14T13:54:25Z

> [@milosbw](https://github.com/milosbw) if the issue is only temporary during the startup of Kueue, then I think it is WAI. Can we close the issue, or you think there is something that goes beyond it?

I think it is not a temporary issue...my Kueue has been up for 11 days, still the same error... will provide more info this weekend, do not have time right now to debug it further :)

Lets keep it open a bit longer! Thanks! @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T13:57:39Z

sgtm, thanks for the input!

### Comment by [@milosbw](https://github.com/milosbw) — 2025-05-25T11:13:32Z

I deployed a new EKS cluster. Still the same issue there:

```sh
kubectl get apiservice v1beta1.visibility.kueue.x-k8s.io -o yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  creationTimestamp: "2025-05-25T10:33:01Z"
  labels:
    app.kubernetes.io/instance: kueue
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: kueue
    app.kubernetes.io/version: v0.11.4
    argocd.argoproj.io/instance: kueue
    control-plane: controller-manager
    helm.sh/chart: kueue-0.11.4
  name: v1beta1.visibility.kueue.x-k8s.io
  resourceVersion: "678781"
  uid: eeec5262-26f6-4af2-8529-ed2b59a386e5
spec:
  group: visibility.kueue.x-k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: kueue-visibility-server
    namespace: kueue-system
    port: 443
  version: v1beta1
  versionPriority: 100
status:
  conditions:
  - lastTransitionTime: "2025-05-25T10:33:01Z"
    message: 'failing or missing response from https://<IP>:8082/apis/visibility.kueue.x-k8s.io/v1beta1:
      Get "https://<IP>:8082/apis/visibility.kueue.x-k8s.io/v1beta1": context
      deadline exceeded (Client.Timeout exceeded while awaiting headers)'
    reason: FailedDiscoveryCheck
    status: "False"
    type: Available
```

The logs from the controller:
```txt
{"level":"info","ts":"2025-05-25T10:34:04.061297856Z","logger":"setup","caller":"kueue/main.go:464","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    Pod: 5\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 5\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - ray.io/raycluster\n  - jobset.x-k8s.io/jobset\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  - workload.codeflare.dev/appwrapper\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-05-25T10:34:04.061577528Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.11.4","gitCommit":"74a9dfc91cc1caf7a0ddb283e2972cd49de32e02"}
{"level":"Level(-2)","ts":"2025-05-25T10:34:04.061717717Z","logger":"setup","caller":"features/kube_features.go:289","msg":"Loaded feature gates","featureGates":{"AdmissionCheckValidationRules":false,"ConfigurableResourceTransformations":true,"ExposeFlavorsInLocalQueue":true,"FlavorFungibility":true,"HierarchicalCohorts":true,"KeepQuotaForProvReqRetry":false,"LendingLimit":true,"LocalQueueDefaulting":false,"LocalQueueMetrics":false,"ManagedJobsNamespaceSelector":true,"MultiKueue":true,"MultiKueueBatchJobWithManagedBy":false,"MultiplePreemptions":true,"PartialAdmission":true,"PrioritySortingWithinCohort":true,"ProvisioningACC":true,"QueueVisibility":false,"TASProfileLeastFreeCapacity":false,"TASProfileMixed":false,"TASProfileMostFreeCapacity":false,"TopologyAwareScheduling":false,"VisibilityOnDemand":true,"WorkloadResourceRequestsSummary":true}}
{"level":"Level(-2)","ts":"2025-05-25T10:34:04.061968139Z","logger":"setup","caller":"kueue/main.go:191","msg":"K8S Client","qps":50,"burst":100}
{"level":"error","ts":"2025-05-25T10:34:04.076774039Z","logger":"setup","caller":"kueue/main.go:264","msg":"Skipping admission check controller setup: Provisioning Requests not supported (Possible cause: missing or unsupported cluster-autoscaler)","error":"no matches for kind \"ProvisioningRequest\" in version \"autoscaling.x-k8s.io/v1beta1\"","stacktrace":"main.setupIndexes\n\t/workspace/cmd/kueue/main.go:264\nmain.main\n\t/workspace/cmd/kueue/main.go:225\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:283"}
{"level":"info","ts":"2025-05-25T10:34:04.080797514Z","logger":"setup","caller":"kueue/main.go:404","msg":"Probe endpoints are configured on healthz and readyz"}
{"level":"info","ts":"2025-05-25T10:34:04.080903094Z","logger":"setup","caller":"kueue/main.go:248","msg":"Starting manager"}
{"level":"info","ts":"2025-05-25T10:34:04.081077547Z","logger":"controller-runtime.metrics","caller":"server/server.go:208","msg":"Starting metrics server"}
{"level":"info","ts":"2025-05-25T10:34:04.095065688Z","logger":"setup","caller":"cert/cert.go:71","msg":"Waiting for certificate generation to complete"}
{"level":"info","ts":"2025-05-25T10:34:04.115199644Z","caller":"manager/server.go:83","msg":"starting server","name":"health probe","addr":"[::]:8081"}
{"level":"info","ts":"2025-05-25T10:34:04.459648418Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *v1.Secret"}
{"level":"info","ts":"2025-05-25T10:34:04.45982287Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
{"level":"info","ts":"2025-05-25T10:34:04.4598833Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
{"level":"info","ts":"2025-05-25T10:34:04.459943048Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"cert-rotator"}
{"level":"info","ts":"2025-05-25T10:34:04.460173852Z","logger":"cert-rotation","caller":"rotator/rotator.go:283","msg":"starting cert rotator controller"}
I0525 10:34:04.460312       1 leaderelection.go:257] attempting to acquire leader lease kueue-system/c1f6bfd2.kueue.x-k8s.io...
I0525 10:34:04.605552       1 leaderelection.go:271] successfully acquired lease kueue-system/c1f6bfd2.kueue.x-k8s.io
{"level":"debug","ts":"2025-05-25T10:34:04.606206443Z","logger":"events","caller":"recorder/recorder.go:104","msg":"kueue-controller-manager-98ddf684c-pz6pg_4b9c5ce2-3304-4d0b-9d68-1f178895d359 became leader","type":"Normal","object":{"kind":"Lease","namespace":"kueue-system","name":"c1f6bfd2.kueue.x-k8s.io","uid":"df629669-a29a-4bcb-b6bf-70052ca8275c","apiVersion":"coordination.k8s.io/v1","resourceVersion":"676190"},"reason":"LeaderElection"}
{"level":"info","ts":"2025-05-25T10:34:04.657079174Z","logger":"cert-rotation","caller":"rotator/rotator.go:354","msg":"no cert refresh needed"}
{"level":"info","ts":"2025-05-25T10:34:04.671270504Z","logger":"cert-rotation","caller":"rotator/rotator.go:873","msg":"certs are ready in /tmp/k8s-webhook-server/serving-certs"}
{"level":"info","ts":"2025-05-25T10:34:04.792600386Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"cert-rotator","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:04.79358275Z","logger":"cert-rotation","caller":"rotator/rotator.go:354","msg":"no cert refresh needed"}
{"level":"info","ts":"2025-05-25T10:34:04.794146431Z","logger":"cert-rotation","caller":"rotator/rotator.go:834","msg":"Ensuring CA cert","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration"}
{"level":"info","ts":"2025-05-25T10:34:04.875235756Z","logger":"cert-rotation","caller":"rotator/rotator.go:834","msg":"Ensuring CA cert","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration"}
{"level":"info","ts":"2025-05-25T10:34:05.828550211Z","logger":"cert-rotation","caller":"rotator/rotator.go:893","msg":"CA certs are injected to webhooks"}
{"level":"info","ts":"2025-05-25T10:34:05.828687529Z","logger":"setup","caller":"cert/cert.go:73","msg":"Certs ready"}
{"level":"info","ts":"2025-05-25T10:34:05.828934343Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"admissioncheck_controller"}
{"level":"info","ts":"2025-05-25T10:34:05.829001517Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"admissioncheck_controller","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:05.829144562Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"resourceflavor_controller","source":"kind source: *v1beta1.ResourceFlavor"}
{"level":"info","ts":"2025-05-25T10:34:05.829217233Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"resourceflavor_controller","source":"channel source: 0x400032ce70"}
{"level":"info","ts":"2025-05-25T10:34:05.829290635Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"resourceflavor_controller"}
{"level":"info","ts":"2025-05-25T10:34:05.829353567Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"admissioncheck_controller","source":"kind source: *v1beta1.AdmissionCheck"}
{"level":"info","ts":"2025-05-25T10:34:05.829427125Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"admissioncheck_controller","source":"channel source: 0x400032d3b0"}
{"level":"info","ts":"2025-05-25T10:34:05.829578588Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"cohort_controller"}
{"level":"info","ts":"2025-05-25T10:34:05.829638698Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"cohort_controller","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:05.851581693Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"localqueue_controller","source":"kind source: *v1beta1.ClusterQueue"}
{"level":"info","ts":"2025-05-25T10:34:05.851705678Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"localqueue_controller","source":"kind source: *v1beta1.LocalQueue"}
{"level":"info","ts":"2025-05-25T10:34:05.851788228Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"localqueue_controller","source":"channel source: 0x400032df10"}
{"level":"info","ts":"2025-05-25T10:34:05.85184938Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"localqueue_controller"}
{"level":"info","ts":"2025-05-25T10:34:05.851911286Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"cohort_controller","source":"kind source: *v1alpha1.Cohort"}
{"level":"info","ts":"2025-05-25T10:34:05.851984335Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"cohort_controller","source":"channel source: 0x40002ee1c0"}
{"level":"info","ts":"2025-05-25T10:34:05.852180713Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"workload_controller"}
{"level":"info","ts":"2025-05-25T10:34:05.852244539Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"workload_controller","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:05.852911709Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"clusterqueue_controller","source":"kind source: *v1.Namespace"}
{"level":"info","ts":"2025-05-25T10:34:05.853021771Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"clusterqueue_controller","source":"kind source: *v1beta1.ClusterQueue"}
{"level":"info","ts":"2025-05-25T10:34:05.853105018Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"clusterqueue_controller","source":"channel source: 0x40002ef810"}
{"level":"info","ts":"2025-05-25T10:34:05.853170593Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"clusterqueue_controller","source":"channel source: 0x40002ef880"}
{"level":"info","ts":"2025-05-25T10:34:05.853227026Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"clusterqueue_controller"}
{"level":"info","ts":"2025-05-25T10:34:05.853292231Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"workload_controller","source":"kind source: *v1.LimitRange"}
{"level":"info","ts":"2025-05-25T10:34:05.853352045Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"workload_controller","source":"kind source: *v1.RuntimeClass"}
{"level":"info","ts":"2025-05-25T10:34:05.853428064Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"workload_controller","source":"kind source: *v1beta1.ClusterQueue"}
{"level":"info","ts":"2025-05-25T10:34:05.853485425Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"workload_controller","source":"kind source: *v1beta1.LocalQueue"}
{"level":"info","ts":"2025-05-25T10:34:05.853544862Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"workload_controller","source":"kind source: *v1beta1.Workload"}
I0525 10:34:05.923684       1 serving.go:380] Generated self-signed cert (/tmp/apiserver.crt, /tmp/apiserver.key)
{"level":"info","ts":"2025-05-25T10:34:05.973667802Z","logger":"setup","caller":"kueue/main.go:304","msg":"Skipping provisioning controller setup: Provisioning Requests not supported (Possible cause: missing or unsupported cluster-autoscaler)"}
{"level":"Level(-2)","ts":"2025-05-25T10:34:05.973891789Z","logger":"MultiKueueGC","caller":"multikueue/multikueuecluster.go:488","msg":"Starting Garbage Collector"}
{"level":"info","ts":"2025-05-25T10:34:05.974190508Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"multikueue_admissioncheck","controllerGroup":"kueue.x-k8s.io","controllerKind":"AdmissionCheck"}
{"level":"info","ts":"2025-05-25T10:34:05.974265788Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"multikueue_admissioncheck","controllerGroup":"kueue.x-k8s.io","controllerKind":"AdmissionCheck","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:05.974931555Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"multikueuecluster","controllerGroup":"kueue.x-k8s.io","controllerKind":"MultiKueueCluster","source":"kind source: *v1beta1.MultiKueueCluster"}
{"level":"info","ts":"2025-05-25T10:34:05.975057756Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"multikueuecluster","controllerGroup":"kueue.x-k8s.io","controllerKind":"MultiKueueCluster","source":"kind source: *v1.Secret"}
{"level":"info","ts":"2025-05-25T10:34:05.975164355Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"multikueuecluster","controllerGroup":"kueue.x-k8s.io","controllerKind":"MultiKueueCluster","source":"channel source: 0x400028d8f0"}
{"level":"info","ts":"2025-05-25T10:34:05.975306776Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"multikueuecluster","controllerGroup":"kueue.x-k8s.io","controllerKind":"MultiKueueCluster","source":"channel source: 0x400028d960"}
{"level":"info","ts":"2025-05-25T10:34:05.975449165Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"multikueuecluster","controllerGroup":"kueue.x-k8s.io","controllerKind":"MultiKueueCluster"}
{"level":"info","ts":"2025-05-25T10:34:05.97589595Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"multikueue_admissioncheck","controllerGroup":"kueue.x-k8s.io","controllerKind":"AdmissionCheck","source":"kind source: *v1beta1.AdmissionCheck"}
{"level":"info","ts":"2025-05-25T10:34:05.976182254Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"multikueue_admissioncheck","controllerGroup":"kueue.x-k8s.io","controllerKind":"AdmissionCheck","source":"kind source: *v1beta1.MultiKueueConfig"}
{"level":"info","ts":"2025-05-25T10:34:05.976329181Z","caller":"controller/controller.go:132","msg":"Starting EventSource","controller":"multikueue_admissioncheck","controllerGroup":"kueue.x-k8s.io","controllerKind":"AdmissionCheck","source":"kind source: *v1beta1.MultiKueueCluster"}
{"level":"info","ts":"2025-05-25T10:34:05.97647573Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"kueue.x-k8s.io/v1beta1, Kind=Workload","path":"/mutate-kueue-x-k8s-io-v1beta1-workload"}
{"level":"info","ts":"2025-05-25T10:34:05.976894511Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kueue-x-k8s-io-v1beta1-workload"}
{"level":"info","ts":"2025-05-25T10:34:05.977033995Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"kueue.x-k8s.io/v1beta1, Kind=Workload","path":"/validate-kueue-x-k8s-io-v1beta1-workload"}
{"level":"info","ts":"2025-05-25T10:34:05.977274639Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kueue-x-k8s-io-v1beta1-workload"}
{"level":"info","ts":"2025-05-25T10:34:05.977471673Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor","path":"/mutate-kueue-x-k8s-io-v1beta1-resourceflavor"}
{"level":"info","ts":"2025-05-25T10:34:05.977910384Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kueue-x-k8s-io-v1beta1-resourceflavor"}
{"level":"info","ts":"2025-05-25T10:34:05.978085905Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor","path":"/validate-kueue-x-k8s-io-v1beta1-resourceflavor"}
{"level":"info","ts":"2025-05-25T10:34:05.978231797Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kueue-x-k8s-io-v1beta1-resourceflavor"}
{"level":"info","ts":"2025-05-25T10:34:05.978443264Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"kueue.x-k8s.io/v1beta1, Kind=ClusterQueue","path":"/mutate-kueue-x-k8s-io-v1beta1-clusterqueue"}
{"level":"info","ts":"2025-05-25T10:34:05.978952431Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kueue-x-k8s-io-v1beta1-clusterqueue"}
{"level":"info","ts":"2025-05-25T10:34:05.979348878Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"kueue.x-k8s.io/v1beta1, Kind=ClusterQueue","path":"/validate-kueue-x-k8s-io-v1beta1-clusterqueue"}
{"level":"info","ts":"2025-05-25T10:34:05.979534302Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kueue-x-k8s-io-v1beta1-clusterqueue"}
{"level":"info","ts":"2025-05-25T10:34:05.979719029Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:186","msg":"skip registering a mutating webhook, object does not implement admission.Defaulter or WithDefaulter wasn't called","GVK":"kueue.x-k8s.io/v1alpha1, Kind=Cohort"}
{"level":"info","ts":"2025-05-25T10:34:05.979825898Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"kueue.x-k8s.io/v1alpha1, Kind=Cohort","path":"/validate-kueue-x-k8s-io-v1alpha1-cohort"}
{"level":"info","ts":"2025-05-25T10:34:05.980637443Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kueue-x-k8s-io-v1alpha1-cohort"}
{"level":"info","ts":"2025-05-25T10:34:05.997549163Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","source":"kind source: *v1beta1.Workload"}
{"level":"info","ts":"2025-05-25T10:34:05.99821749Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","source":"channel source: 0x4000292460"}
{"level":"info","ts":"2025-05-25T10:34:05.998358549Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload"}
{"level":"info","ts":"2025-05-25T10:34:05.998434585Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:191","msg":"Starting webhook server"}
{"level":"info","ts":"2025-05-25T10:34:05.998862933Z","logger":"controller-runtime.certwatcher","caller":"certwatcher/certwatcher.go:211","msg":"Updated current TLS certificate"}
{"level":"info","ts":"2025-05-25T10:34:05.999001892Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:242","msg":"Serving webhook server","host":"","port":9443}
{"level":"info","ts":"2025-05-25T10:34:05.999195694Z","logger":"controller-runtime.certwatcher","caller":"certwatcher/certwatcher.go:133","msg":"Starting certificate poll+watcher","interval":10}
{"level":"info","ts":"2025-05-25T10:34:06.093620292Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"resourceflavor_controller","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:06.094161319Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"workload.codeflare.dev/v1beta2, Kind=AppWrapper","path":"/mutate-workload-codeflare-dev-v1beta2-appwrapper"}
{"level":"info","ts":"2025-05-25T10:34:06.094354054Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-workload-codeflare-dev-v1beta2-appwrapper"}
{"level":"info","ts":"2025-05-25T10:34:06.094438795Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"workload.codeflare.dev/v1beta2, Kind=AppWrapper","path":"/validate-workload-codeflare-dev-v1beta2-appwrapper"}
{"level":"info","ts":"2025-05-25T10:34:06.094634319Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-workload-codeflare-dev-v1beta2-appwrapper"}
{"level":"info","ts":"2025-05-25T10:34:06.094729932Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"workload.codeflare.dev/appwrapper"}
{"level":"info","ts":"2025-05-25T10:34:06.094923167Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"apps/v1, Kind=Deployment","path":"/mutate-apps-v1-deployment"}
{"level":"info","ts":"2025-05-25T10:34:06.095271599Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-apps-v1-deployment"}
{"level":"info","ts":"2025-05-25T10:34:06.0953658Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"apps/v1, Kind=Deployment","path":"/validate-apps-v1-deployment"}
{"level":"info","ts":"2025-05-25T10:34:06.095484312Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-apps-v1-deployment"}
{"level":"info","ts":"2025-05-25T10:34:06.095779117Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"batch/v1, Kind=Job","path":"/mutate-batch-v1-job"}
{"level":"info","ts":"2025-05-25T10:34:06.095912521Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-batch-v1-job"}
{"level":"info","ts":"2025-05-25T10:34:06.095989869Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"batch/v1, Kind=Job","path":"/validate-batch-v1-job"}
{"level":"info","ts":"2025-05-25T10:34:06.096092669Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-batch-v1-job"}
{"level":"info","ts":"2025-05-25T10:34:06.096738663Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"job","controllerGroup":"batch","controllerKind":"Job","source":"kind source: *v1.Job"}
{"level":"info","ts":"2025-05-25T10:34:06.096907833Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"job","controllerGroup":"batch","controllerKind":"Job","source":"kind source: *v1beta1.Workload"}
{"level":"info","ts":"2025-05-25T10:34:06.096973398Z","caller":"controller/controller.go:175","msg":"Starting EventSource","controller":"job","controllerGroup":"batch","controllerKind":"Job","source":"kind source: *v1beta1.Workload"}
{"level":"info","ts":"2025-05-25T10:34:06.097029438Z","caller":"controller/controller.go:183","msg":"Starting Controller","controller":"job","controllerGroup":"batch","controllerKind":"Job"}
{"level":"info","ts":"2025-05-25T10:34:06.174390788Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"jobset.x-k8s.io/v1alpha2, Kind=JobSet","path":"/mutate-jobset-x-k8s-io-v1alpha2-jobset"}
{"level":"info","ts":"2025-05-25T10:34:06.174631932Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-jobset-x-k8s-io-v1alpha2-jobset"}
{"level":"info","ts":"2025-05-25T10:34:06.174718954Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"jobset.x-k8s.io/v1alpha2, Kind=JobSet","path":"/validate-jobset-x-k8s-io-v1alpha2-jobset"}
{"level":"info","ts":"2025-05-25T10:34:06.174857568Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-jobset-x-k8s-io-v1alpha2-jobset"}
{"level":"info","ts":"2025-05-25T10:34:06.174946453Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"jobset.x-k8s.io/jobset"}
{"level":"info","ts":"2025-05-25T10:34:06.275014081Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"kubeflow.org/v1, Kind=PaddleJob","path":"/mutate-kubeflow-org-v1-paddlejob"}
{"level":"info","ts":"2025-05-25T10:34:06.275379981Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kubeflow-org-v1-paddlejob"}
{"level":"info","ts":"2025-05-25T10:34:06.275479352Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"kubeflow.org/v1, Kind=PaddleJob","path":"/validate-kubeflow-org-v1-paddlejob"}
{"level":"info","ts":"2025-05-25T10:34:06.275599374Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kubeflow-org-v1-paddlejob"}
{"level":"info","ts":"2025-05-25T10:34:06.275704455Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"kubeflow.org/paddlejob"}
{"level":"info","ts":"2025-05-25T10:34:06.349334999Z","logger":"controller-runtime.metrics","caller":"server/server.go:247","msg":"Serving metrics server","bindAddress":":8443","secure":true}
{"level":"info","ts":"2025-05-25T10:34:06.385390697Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"multikueuecluster","controllerGroup":"kueue.x-k8s.io","controllerKind":"MultiKueueCluster","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:06.405485631Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","worker count":5}
{"level":"info","ts":"2025-05-25T10:34:06.405651478Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"localqueue_controller","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:06.405731443Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"clusterqueue_controller","worker count":1}
{"level":"info","ts":"2025-05-25T10:34:06.405823454Z","caller":"controller/controller.go:217","msg":"Starting workers","controller":"job","controllerGroup":"batch","controllerKind":"Job","worker count":5}
{"level":"info","ts":"2025-05-25T10:34:06.425853273Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"kubeflow.org/v1, Kind=PyTorchJob","path":"/mutate-kubeflow-org-v1-pytorchjob"}
{"level":"info","ts":"2025-05-25T10:34:06.426054524Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kubeflow-org-v1-pytorchjob"}
{"level":"info","ts":"2025-05-25T10:34:06.426137517Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"kubeflow.org/v1, Kind=PyTorchJob","path":"/validate-kubeflow-org-v1-pytorchjob"}
{"level":"info","ts":"2025-05-25T10:34:06.426245716Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kubeflow-org-v1-pytorchjob"}
{"level":"info","ts":"2025-05-25T10:34:06.426341837Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"kubeflow.org/pytorchjob"}
{"level":"info","ts":"2025-05-25T10:34:06.486313496Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"kubeflow.org/v1, Kind=TFJob","path":"/mutate-kubeflow-org-v1-tfjob"}
{"level":"info","ts":"2025-05-25T10:34:06.486571107Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kubeflow-org-v1-tfjob"}
{"level":"info","ts":"2025-05-25T10:34:06.486657161Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"kubeflow.org/v1, Kind=TFJob","path":"/validate-kubeflow-org-v1-tfjob"}
{"level":"info","ts":"2025-05-25T10:34:06.486766008Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kubeflow-org-v1-tfjob"}
{"level":"info","ts":"2025-05-25T10:34:06.486862949Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"kubeflow.org/tfjob"}
{"level":"info","ts":"2025-05-25T10:34:06.606915991Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"kubeflow.org/v1, Kind=XGBoostJob","path":"/mutate-kubeflow-org-v1-xgboostjob"}
{"level":"info","ts":"2025-05-25T10:34:06.607189077Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kubeflow-org-v1-xgboostjob"}
{"level":"info","ts":"2025-05-25T10:34:06.60727591Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"kubeflow.org/v1, Kind=XGBoostJob","path":"/validate-kubeflow-org-v1-xgboostjob"}
{"level":"info","ts":"2025-05-25T10:34:06.607383592Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kubeflow-org-v1-xgboostjob"}
{"level":"info","ts":"2025-05-25T10:34:06.607479894Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"kubeflow.org/xgboostjob"}
{"level":"info","ts":"2025-05-25T10:34:06.64757716Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"kubeflow.org/v2beta1, Kind=MPIJob","path":"/mutate-kubeflow-org-v2beta1-mpijob"}
{"level":"info","ts":"2025-05-25T10:34:06.647776138Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-kubeflow-org-v2beta1-mpijob"}
{"level":"info","ts":"2025-05-25T10:34:06.647867845Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"kubeflow.org/v2beta1, Kind=MPIJob","path":"/validate-kubeflow-org-v2beta1-mpijob"}
{"level":"info","ts":"2025-05-25T10:34:06.647981673Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-kubeflow-org-v2beta1-mpijob"}
{"level":"info","ts":"2025-05-25T10:34:06.648084645Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"kubeflow.org/mpijob"}
{"level":"info","ts":"2025-05-25T10:34:06.64826001Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"/v1, Kind=Pod","path":"/mutate--v1-pod"}
{"level":"info","ts":"2025-05-25T10:34:06.648408889Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate--v1-pod"}
{"level":"info","ts":"2025-05-25T10:34:06.648487353Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"/v1, Kind=Pod","path":"/validate--v1-pod"}
{"level":"info","ts":"2025-05-25T10:34:06.648616778Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate--v1-pod"}
{"level":"info","ts":"2025-05-25T10:34:06.687782609Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"ray.io/v1, Kind=RayCluster","path":"/mutate-ray-io-v1-raycluster"}
{"level":"info","ts":"2025-05-25T10:34:06.687978256Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-ray-io-v1-raycluster"}
{"level":"info","ts":"2025-05-25T10:34:06.688060863Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"ray.io/v1, Kind=RayCluster","path":"/validate-ray-io-v1-raycluster"}
{"level":"info","ts":"2025-05-25T10:34:06.688200848Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-ray-io-v1-raycluster"}
{"level":"info","ts":"2025-05-25T10:34:06.688283825Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"ray.io/raycluster"}
{"level":"info","ts":"2025-05-25T10:34:06.727995614Z","caller":"webhook/builder.go:168","msg":"Registering a mutating webhook","GVK":"ray.io/v1, Kind=RayJob","path":"/mutate-ray-io-v1-rayjob"}
{"level":"info","ts":"2025-05-25T10:34:06.728174745Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-ray-io-v1-rayjob"}
{"level":"info","ts":"2025-05-25T10:34:06.728255752Z","caller":"webhook/builder.go:200","msg":"Registering a validating webhook","GVK":"ray.io/v1, Kind=RayJob","path":"/validate-ray-io-v1-rayjob"}
{"level":"info","ts":"2025-05-25T10:34:06.728357518Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-ray-io-v1-rayjob"}
{"level":"info","ts":"2025-05-25T10:34:06.728446411Z","logger":"setup","caller":"jobframework/setup.go:94","msg":"No matching API in the server for job framework, deferring setting up controller","jobFrameworkName":"ray.io/rayjob"}
{"level":"info","ts":"2025-05-25T10:34:06.728627117Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"apps/v1, Kind=StatefulSet","path":"/mutate-apps-v1-statefulset"}
{"level":"info","ts":"2025-05-25T10:34:06.728753777Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-apps-v1-statefulset"}
{"level":"info","ts":"2025-05-25T10:34:06.728826867Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"apps/v1, Kind=StatefulSet","path":"/validate-apps-v1-statefulset"}
{"level":"info","ts":"2025-05-25T10:34:06.728931226Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-apps-v1-statefulset"}
{"level":"info","ts":"2025-05-25T10:34:06.729078932Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:163","msg":"Registering a mutating webhook","GVK":"leaderworkerset.x-k8s.io/v1, Kind=LeaderWorkerSet","path":"/mutate-leaderworkerset-x-k8s-io-v1-leaderworkerset"}
{"level":"info","ts":"2025-05-25T10:34:06.729197822Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/mutate-leaderworkerset-x-k8s-io-v1-leaderworkerset"}
{"level":"info","ts":"2025-05-25T10:34:06.729275957Z","logger":"controller-runtime.builder","caller":"builder/webhook.go:202","msg":"Registering a validating webhook","GVK":"leaderworkerset.x-k8s.io/v1, Kind=LeaderWorkerSet","path":"/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset"}
{"level":"info","ts":"2025-05-25T10:34:06.729378044Z","logger":"controller-runtime.webhook","caller":"webhook/server.go:183","msg":"Registering webhook","path":"/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset"}
I0525 10:34:08.676938       1 plugins.go:157] Loaded 2 mutating admission controller(s) successfully in the following order: NamespaceLifecycle,MutatingAdmissionPolicy.
I0525 10:34:08.679612       1 handler.go:286] Adding GroupVersion visibility.kueue.x-k8s.io v1beta1 to ResourceManager
I0525 10:34:08.687297       1 secure_serving.go:213] Serving securely on [::]:8082
I0525 10:34:08.687447       1 requestheader_controller.go:180] Starting RequestHeaderAuthRequestController
I0525 10:34:08.687503       1 shared_informer.go:313] Waiting for caches to sync for RequestHeaderAuthRequestController
I0525 10:34:08.687580       1 dynamic_serving_content.go:135] "Starting controller" name="serving-cert::/tmp/apiserver.crt::/tmp/apiserver.key"
I0525 10:34:08.687736       1 tlsconfig.go:243] "Starting DynamicServingCertificateController"
I0525 10:34:08.688145       1 apf_controller.go:377] Starting API Priority and Fairness config controller
I0525 10:34:08.688297       1 configmap_cafile_content.go:205] "Starting controller" name="client-ca::kube-system::extension-apiserver-authentication::client-ca-file"
I0525 10:34:08.688359       1 shared_informer.go:313] Waiting for caches to sync for client-ca::kube-system::extension-apiserver-authentication::client-ca-file
I0525 10:34:08.688434       1 configmap_cafile_content.go:205] "Starting controller" name="client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
I0525 10:34:08.688480       1 shared_informer.go:313] Waiting for caches to sync for client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file
I0525 10:34:08.788526       1 shared_informer.go:320] Caches are synced for client-ca::kube-system::extension-apiserver-authentication::client-ca-file
I0525 10:34:08.788690       1 shared_informer.go:320] Caches are synced for client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file
I0525 10:34:08.788779       1 shared_informer.go:320] Caches are synced for RequestHeaderAuthRequestController
I0525 10:34:08.788932       1 apf_controller.go:382] Running API Priority and Fairness config worker
I0525 10:34:08.788986       1 apf_controller.go:385] Running API Priority and Fairness periodic rebalancing process
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-23T12:12:00Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-22T12:51:52Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-22T13:19:57Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-22T13:20:03Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5150#issuecomment-3432337012):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-11-07T01:21:06Z

@kubernetes-sigs/kueue-maintainers - is this resolved? 
If not, can we reopen this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T06:38:55Z

> @kubernetes-sigs/kueue-maintainers - is this resolved?

I have no idea, I don't observe the issue on GKE or Kind where I have easy access to.

Let me reopen so that maybe some EKS can re-check. @milosbw any update on that?

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-07T06:39:00Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5150#issuecomment-3500973444):

>> @kubernetes-sigs/kueue-maintainers - is this resolved?
>
>I have no idea, I don't observe the issue on GKE or Kind where I have easy access to.
>
>Let me reopen so that maybe some EKS can re-check. @milosbw any update on that?
>
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-07T07:32:30Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-07T07:32:36Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5150#issuecomment-3621782931):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ollie-bell](https://github.com/ollie-bell) — 2026-01-15T10:02:58Z

In my case the issue was solved by ensuring a security group rule is set up to allow for ingress on 8082/TCP from the k8s API server / control plane to the worker nodes

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T10:08:51Z

Thank you @ollie-bell  for sharing the information

cc @olekzabl who is enountering some configuration issues for VisibilityOnDemand, maybe this is related
