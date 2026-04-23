# Issue #3195: Provisoning Reqeusts not supported

**Summary**: Provisoning Reqeusts not supported

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3195

**Last updated**: 2025-02-10T08:22:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@leipanhz](https://github.com/leipanhz)
- **Created**: 2024-10-07T20:44:30Z
- **Updated**: 2025-02-10T08:22:07Z
- **Closed**: 2025-02-10T08:22:07Z
- **Labels**: `kind/support`, `lifecycle/stale`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Provisioning Request controller can't be set up by Kueue controller manager. Related logs

`
{"level":"info","ts":"2024-10-07T20:29:27.972001653Z","logger":"setup","caller":"kueue/main.go:120","msg":"Initializing","gitVersion":"67113647-dirty","gitCommit":"67113647f48754aff6b8b2ae317cfb8c61fd0aa0"}
{"level":"info","ts":"2024-10-07T20:31:05.975593283Z","logger":"setup","caller":"kueue/main.go:120","msg":"Initializing","gitVersion":"67113647-dirty","gitCommit":"67113647f48754aff6b8b2ae317cfb8c61fd0aa0"}
{"level":"Level(-2)","ts":"2024-10-07T20:31:05.975722949Z","logger":"setup","caller":"features/kube_features.go:150","msg":"Loaded feature gates","featureGates":{"FlavorFungibility":true,"LendingLimit":true,"MultiKueue":false,"MultiKueueBatchJobWithManagedBy":false,"MultiplePreemptions":true,"PartialAdmission":true,"PrioritySortingWithinCohort":true,"ProvisioningACC":true,"QueueVisibility":false,"VisibilityOnDemand":false}}
{"level":"info","ts":"2024-10-07T20:31:05.977037616Z","logger":"setup","caller":"kueue/main.go:375","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    Pod: 5\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 5\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - ray.io/raycluster\n  - jobset.x-k8s.io/jobset\n  - kubeflow.org/mxjob\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmetrics:\n  bindAddress: :8080\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"Level(-2)","ts":"2024-10-07T20:31:05.977229574Z","logger":"setup","caller":"kueue/main.go:140","msg":"K8S Client","qps":50,"burst":100}
{"level":"error","ts":"2024-10-07T20:31:05.983115324Z","logger":"setup","caller":"kueue/main.go:209","msg":"Provisioning Requests are not supported, skipped admission check controller setup","stacktrace":"main.setupIndexes\n\t/workspace/cmd/kueue/main.go:209\nmain.main\n\t/workspace/cmd/kueue/main.go:170\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:271"}
{"level":"info","ts":"2024-10-07T20:31:05.984060116Z","logger":"setup","caller":"kueue/main.go:315","msg":"Probe endpoints are configured on healthz and readyz"}
{"level":"info","ts":"2024-10-07T20:31:05.984105533Z","logger":"setup","caller":"kueue/main.go:193","msg":"Starting manager"}
`
**What you expected to happen**:
Expecting provisining request admission check to be set up and running

**How to reproduce it (as minimally and precisely as possible)**:
Installed minikube on Mac laptop, installed Kueue 

**Anything else we need to know?**:
I have metrics-server installed and verified auto-scaling in cluster:
`
kubectl get hpa
NAME    REFERENCE          TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/nginx   cpu: <unknown>/50%   1         10        1          19m
`

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

OS: MacOS sonoma
Kubernetes: minikube

`$ git describe --tags --dirty --always
67113647-dirty`

`$ kubectl version
Client Version: v1.31.1
Kustomize Version: v5.4.2
Server Version: v1.31.0`

` $ uname -a
Darwin xx 23.5.0 Darwin Kernel Version 23.5.0: Wed May  1 20:12:58 PDT 2024; root:xnu-10063.121.3~5/RELEASE_ARM64_T6000 arm64`

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-08T08:20:53Z

Looking at the code by "Provisioning Requests are not supported, skipped admission check controller setup" leads to https://github.com/kubernetes-sigs/kueue/blob/f6f80a5b8aa7e537ac2c6293688deb13a1c048e6/pkg/controller/admissionchecks/provisioning/indexer.go#L74-L83.

@leipanhz can you check if you have CA installed on your cluster and if the ProvisioningRequest API CRDs are available?

/cc @yaroslava-serdiuk

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-08T22:32:42Z

@mimowo I followed examples in https://github.com/kubernetes-sigs/kueue/blob/main/site/static/examples/provisioning/provisioning-setup.yaml to set up ProvisiongRequest AC. Checking my cluster

$ kc get ProvisioningRequestConfig
NAME               AGE
prov-test-config   6d1h
$ kc describe ProvisioningRequestConfig prov-test-config
Name:         prov-test-config
Namespace:
Labels:       <none>
Annotations:  <none>
API Version:  kueue.x-k8s.io/v1beta1
Kind:         ProvisioningRequestConfig
Metadata:
  Creation Timestamp:  2024-10-02T21:09:11Z
  Generation:          1
  Resource Version:    522310
  UID:                 a49ca1b0-e209-41f4-a8df-1ba48581b7ba
Spec:
  Managed Resources:
    cpu
  Provisioning Class Name:  queued-provisioning.gke.io
Events:                     <none>


$ kc get MutatingWebhookConfiguration
NAME                   WEBHOOKS   AGE
cert-manager-webhook   1          26h

$ kc get ValidatingWebhookConfiguration
NAME                   WEBHOOKS   AGE
cert-manager-webhook   1          26h

Are these sufficient to enable ProvisioningRequest check?

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-08T22:38:31Z

ProvisioningRequest is enabled by default from the documentation: https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning

From logs I attached in the post, ProvisioningACC is set to true

`{"FlavorFungibility":true,"LendingLimit":true,"MultiKueue":false,"MultiKueueBatchJobWithManagedBy":false,"MultiplePreemptions":true,"PartialAdmission":true,"PrioritySortingWithinCohort":true,"ProvisioningACC":true,"QueueVisibility":false,"VisibilityOnDemand":false}}`

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-09T09:10:01Z

I think you may need to install ClusterAutoscaler as well. I suppose minikube does not do it by default.
You can check if you have the required CRDs by `kubectl get crds` and should have `provisioningrequests.autoscaling.x-k8s.io` on the list. If this is the case then @leipanhz feel free to submit a PR to update the docs to state the requirement clearly to avoid confusion in the future.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-09T15:35:25Z

@mimowo I only have provisioningrequestconfigs installed. 
`
$ kubectl get crds | grep -i provision
provisioningrequestconfigs.kueue.x-k8s.io   2024-09-17T18:16:17Z
`

Can you provide information on how to install aut-scaler on minikube? From https://kubernetes.io/docs/concepts/cluster-administration/cluster-autoscaling/, it points to https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler, however, there is no mentioning about how to install on minikube, instructions are for various cloud providers.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-09T15:42:39Z

yeah, installing the CRD is essential, but even then I dont know if minikube supports CA to allow any sensible testing.

Maybe you could ask get some help at the autoscaling slack channel, let me also cc @yaroslava-serdiuk

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-09T15:42:49Z

My purpose of experimenting provisioningrequest is to understand how AdmissionCheck controllers work with Kueue, so that we can create a custom controller to integrate with Kueue scheduling before a workload can be admitted. As I am pretty new to Kubernetes, is there another way you would suggest? Related documentations are mostly focused on provisioningrequest, and unfortunately it doesn't work with my cluster: 
https://kueue.sigs.k8s.io/docs/concepts/admission_check/
https://kueue.sigs.k8s.io/docs/tasks/dev/develop-acc/

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-11T11:15:15Z

I perfectly understand the use-case of being able to play with ProvisiningRequests for free prior to an investment. However, you are blocked on by the ClusterAutoscaler - minikube support, rather than by Kueue. From my quick search neither kind nor minikube support ClusterAutoscaler, so it might be hard. I might also be missing something thus my suggestion to seek help at the dedicated slack channels (maybe #sig-autoscaling). 

What I think we could do in Kueue is:
1. update the documentation to add a sentence in https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/ how to confirm that the necessary CRD is installed
2. update the error message: "Provisioning Requests are not supported, skipped admission check controller setup" -> 
"Provisioning Requests are not supported, please verify the necessary ProvisioningReqest CRD is installed in your cluster. Skipped admission check controller setup."

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-14T11:10:13Z

/remove-kind bug
/kind support

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-12T11:17:07Z

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

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-02-02T14:54:51Z

/assign Since this issue is not related to any bug in Kueue, but as discussed on Slack, adding a CRD check could help pinpoint the root cause. This improvement will ensure users can quickly identify the issue and avoid wasting time in the future.

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-02-02T14:55:04Z

/assign
