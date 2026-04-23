# Issue #622: Failed to call webhook -> missing ca.crt

**Summary**: Failed to call webhook -> missing ca.crt

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/622

**Last updated**: 2023-03-13T17:01:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@danielmarzini](https://github.com/danielmarzini)
- **Created**: 2023-03-12T23:25:31Z
- **Updated**: 2023-03-13T17:01:48Z
- **Closed**: 2023-03-13T17:01:47Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 14

## Description

**What happened**:
Hello folks, it seems that there's is a problem with the cert for the webhook, this happens when I try to apply the first flavor.yaml from the how-to.

Error from server (InternalError): error when creating "flavors.yaml": Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1alpha2-resourceflavor?timeout=10s": context deadline exceeded

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
I'm using GKE Standard 1.24.9-gke.3200 freshly installed.
I installed kueue as the guide, version v0.2.1 and tried to apply flavor.yaml.

This is what I see in the logs:
{"caller":"logr@v1.2.3/logr.go:279", "error":"Cert secret is not well-formed, missing ca.crt", "errorVerbose":"Cert secret is not well-formed, missing ca.crt

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-13T07:50:30Z

Hi @danielmarzini, thank you for creating this issue.

> I installed kueue as the guide, version v0.2.1 and tried to apply flavor.yaml.

Did you use the installation commands in [this doc](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version)?

> I try to apply the first flavor.yaml from the how-to.

Also, can you share with me which how-to guide?

### Comment by [@danielmarzini](https://github.com/danielmarzini) — 2023-03-13T08:20:35Z

Hello @tenzen-y, I do confirm that I used [the kueue guide](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version) and then I tested both  the steps over [kueue readme page](https://github.com/kubernetes-sigs/kueue#usage)  and the one available over the [GKE official doc](https://cloud.google.com/kubernetes-engine/docs/tutorials/kueue-intro).

The error that I got with the kueue usage page is:
`Error from server (InternalError): error when creating "config/samples/single-clusterqueue-setup.yaml": Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1alpha2-resourceflavor?timeout=10s": context deadline exceeded
Error from server (InternalError): error when creating "config/samples/single-clusterqueue-setup.yaml": Internal error occurred: failed calling webhook "mclusterqueue.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1alpha2-clusterqueue?timeout=10s": context deadline exceeded
Error from server (InternalError): error when creating "config/samples/single-clusterqueue-setup.yaml": Internal error occurred: failed calling webhook "vlocalqueue.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1alpha2-localqueue?timeout=10s": context deadline exceeded
`
One additional behaviour that I noted is that, as soon as I [apply the development version](https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version) everything start working again.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-13T09:32:03Z

Can you share with me the `kueue-mutating-webhook-configuration` with `kubectl get mutatingwebhookconfigurations.admissionregistration.k8s.io kueue-mutating-webhook-configuration -oyaml`?

### Comment by [@danielmarzini](https://github.com/danielmarzini) — 2023-03-13T09:39:59Z

**---------- v0.2.1** 
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"admissionregistration.k8s.io/v1","kind":"MutatingWebhookConfiguration","metadata":{"annotations":{},"creationTimestamp":null,"name":"kueue-mutating-webhook-configuration"},"webhooks":[{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kueue-x-k8s-io-v1alpha2-clusterqueue"}},"failurePolicy":"Fail","name":"mclusterqueue.kb.io","rules":[{"apiGroups":["kueue.x-k8s.io"],"apiVersions":["v1alpha2"],"operations":["CREATE"],"resources":["clusterqueues"]}],"sideEffects":"None"},{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kueue-x-k8s-io-v1alpha2-resourceflavor"}},"failurePolicy":"Fail","name":"mresourceflavor.kb.io","rules":[{"apiGroups":["kueue.x-k8s.io"],"apiVersions":["v1alpha2"],"operations":["CREATE"],"resources":["resourceflavors"]}],"sideEffects":"None"},{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kueue-x-k8s-io-v1alpha2-workload"}},"failurePolicy":"Fail","name":"mworkload.kb.io","rules":[{"apiGroups":["kueue.x-k8s.io"],"apiVersions":["v1alpha2"],"operations":["CREATE","UPDATE"],"resources":["workloads"]}],"sideEffects":"None"}]}
  creationTimestamp: "2023-03-13T09:35:14Z"
  generation: 2
  name: kueue-mutating-webhook-configuration
  resourceVersion: "432080"
  uid: 7dceda37-4fb5-40d2-9c4c-847594e3b6ff
webhooks:
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kueue-x-k8s-io-v1alpha2-clusterqueue
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mclusterqueue.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kueue.x-k8s.io
    apiVersions:
    - v1alpha2
    operations:
    - CREATE
    resources:
    - clusterqueues
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kueue-x-k8s-io-v1alpha2-resourceflavor
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mresourceflavor.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kueue.x-k8s.io
    apiVersions:
    - v1alpha2
    operations:
    - CREATE
    resources:
    - resourceflavors
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kueue-x-k8s-io-v1alpha2-workload
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mworkload.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kueue.x-k8s.io
    apiVersions:
    - v1alpha2
    operations:
    - CREATE
    - UPDATE
    resources:
    - workloads
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10

**---- After development version applied**

apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"admissionregistration.k8s.io/v1","kind":"MutatingWebhookConfiguration","metadata":{"annotations":{},"creationTimestamp":null,"name":"kueue-mutating-webhook-configuration"},"webhooks":[{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kueue-x-k8s-io-v1beta1-clusterqueue"}},"failurePolicy":"Fail","name":"mclusterqueue.kb.io","rules":[{"apiGroups":["kueue.x-k8s.io"],"apiVersions":["v1beta1"],"operations":["CREATE"],"resources":["clusterqueues"]}],"sideEffects":"None"},{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kueue-x-k8s-io-v1beta1-resourceflavor"}},"failurePolicy":"Fail","name":"mresourceflavor.kb.io","rules":[{"apiGroups":["kueue.x-k8s.io"],"apiVersions":["v1beta1"],"operations":["CREATE"],"resources":["resourceflavors"]}],"sideEffects":"None"},{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kueue-x-k8s-io-v1beta1-workload"}},"failurePolicy":"Fail","name":"mworkload.kb.io","rules":[{"apiGroups":["kueue.x-k8s.io"],"apiVersions":["v1beta1"],"operations":["CREATE","UPDATE"],"resources":["workloads"]}],"sideEffects":"None"},{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-batch-v1-job"}},"failurePolicy":"Fail","name":"mjob.kb.io","rules":[{"apiGroups":["batch"],"apiVersions":["v1"],"operations":["CREATE"],"resources":["jobs"]}],"sideEffects":"None"},{"admissionReviewVersions":["v1"],"clientConfig":{"service":{"name":"kueue-webhook-service","namespace":"kueue-system","path":"/mutate-kubeflow-org-v2beta1-mpijob"}},"failurePolicy":"Fail","name":"mmpijob.kb.io","rules":[{"apiGroups":["kubeflow.org"],"apiVersions":["v2beta1"],"operations":["CREATE"],"resources":["mpijobs"]}],"sideEffects":"None"}]}
  creationTimestamp: "2023-03-13T08:17:42Z"
  generation: 4
  name: kueue-mutating-webhook-configuration
  resourceVersion: "384611"
  uid: 750ab554-7b6d-4fe9-a93b-a9cfb8e6d5e6
webhooks:
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kueue-x-k8s-io-v1beta1-clusterqueue
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mclusterqueue.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kueue.x-k8s.io
    apiVersions:
    - v1beta1
    operations:
    - CREATE
    resources:
    - clusterqueues
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kueue-x-k8s-io-v1beta1-resourceflavor
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mresourceflavor.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kueue.x-k8s.io
    apiVersions:
    - v1beta1
    operations:
    - CREATE
    resources:
    - resourceflavors
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kueue-x-k8s-io-v1beta1-workload
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mworkload.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kueue.x-k8s.io
    apiVersions:
    - v1beta1
    operations:
    - CREATE
    - UPDATE
    resources:
    - workloads
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-batch-v1-job
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mjob.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - batch
    apiVersions:
    - v1
    operations:
    - CREATE
    resources:
    - jobs
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10
- admissionReviewVersions:
  - v1
  clientConfig:
    caBundle: REDACTED
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /mutate-kubeflow-org-v2beta1-mpijob
      port: 443
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: mmpijob.kb.io
  namespaceSelector: {}
  objectSelector: {}
  reinvocationPolicy: Never
  rules:
  - apiGroups:
    - kubeflow.org
    apiVersions:
    - v2beta1
    operations:
    - CREATE
    resources:
    - mpijobs
    scope: '*'
  sideEffects: None
  timeoutSeconds: 10

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-13T09:54:03Z

The manifests seem fine.
I could not reproduce the error in the kind cluster.

@alculquicondor @ahg-g Have you seen this issue on GKE?

### Comment by [@danielmarzini](https://github.com/danielmarzini) — 2023-03-13T09:57:13Z

lemme try to create a new cluster as well

### Comment by [@danielmarzini](https://github.com/danielmarzini) — 2023-03-13T10:42:33Z

@tenzen-y tried onto 2 new clusters, one standard and one autopilot, same result, this is the error that I found in the logs:
`{"caller":"logr@v1.2.3/logr.go:279", "error":"Cert secret is not well-formed, missing ca.crt", "errorVerbose":"Cert secret is not well-formed, missing ca.crt
github.com/open-policy-agent/cert-controller/pkg/rotator.buildArtifactsFromSecret
	/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.3.0/pkg/rotator/rotator.go:380
github.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile
	/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.3.0/pkg/rotator/rotator.go:635
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:121
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:320
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:273
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:234
runtime.goexit
	/usr/local/go/src/runtime/asm_amd64.s:1571", "level":"error", "logger":"cert-rotation", "msg":"secret is not well-formed, cannot update webhook configurations", "stacktrace":"github.com/go-logr/logr.Logger.Error
	/go/pkg/mod/github.com/go-logr/logr@v1.2.3/logr.go:279
github.com/open-policy-agent/cert-controller/pkg/rotator.(*ReconcileWH).Reconcile
	/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.3.0/pkg/rotator/rotator.go:637
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:121
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:320
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:273
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:234", "ts":"2023-03-13T10:29:42.244710126Z"}`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-13T10:49:08Z

The error message is expected behavior.
Can you find the message like the following? If so, the kueue-controller works well.

```shell
...
{"level":"info","ts":"2023-03-13T09:26:47.716096919Z","logger":"cert-rotation","caller":"logr@v1.2.3/logr.go:261","msg":"server certs refreshed"}
{"level":"info","ts":"2023-03-13T09:26:47.720823335Z","logger":"cert-rotation","caller":"rotator/rotator.go:685","msg":"Ensuring CA cert","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration"}
{"level":"info","ts":"2023-03-13T09:26:47.73066646Z","logger":"cert-rotation","caller":"rotator/rotator.go:685","msg":"Ensuring CA cert","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration"}
{"level":"info","ts":"2023-03-13T09:26:47.799283669Z","logger":"cert-rotation","caller":"rotator/rotator.go:685","msg":"Ensuring CA cert","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration"}
{"level":"info","ts":"2023-03-13T09:26:47.81131496Z","logger":"cert-rotation","caller":"rotator/rotator.go:685","msg":"Ensuring CA cert","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration"}
{"level":"info","ts":"2023-03-13T09:26:47.81888946Z","logger":"cert-rotation","caller":"rotator/rotator.go:685","msg":"Ensuring CA cert","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration"}
{"level":"info","ts":"2023-03-13T09:26:47.892434835Z","logger":"cert-rotation","caller":"rotator/rotator.go:685","msg":"Ensuring CA cert","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration"}
{"level":"info","ts":"2023-03-13T09:26:49.253945794Z","logger":"cert-rotation","caller":"logr@v1.2.3/logr.go:261","msg":"certs are ready in /tmp/k8s-webhook-server/serving-certs"}
{"level":"info","ts":"2023-03-13T09:26:49.254713294Z","logger":"cert-rotation","caller":"logr@v1.2.3/logr.go:261","msg":"CA certs are injected to webhooks"}
{"level":"info","ts":"2023-03-13T09:26:49.255007503Z","logger":"setup","caller":"logr@v1.2.3/logr.go:261","msg":"Certs ready"}
...
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-13T15:26:35Z

@danielmarzini I wonder if you created a private cluster

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-13T15:27:08Z

Otherwise, can you please share the `gcloud` command used to create the cluster?

### Comment by [@danielmarzini](https://github.com/danielmarzini) — 2023-03-13T15:42:50Z

Hello @alculquicondor I do confirm that I'm using 3 private clusters, with public endpoint and Cloud Nat enabled. is there anything else that I can do?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-13T17:01:39Z

Private clusters might need to add firewall rules for webhooks according to GKE docs https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#add_firewall_rules

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-13T17:01:43Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-13T17:01:47Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/622#issuecomment-1466536672):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
