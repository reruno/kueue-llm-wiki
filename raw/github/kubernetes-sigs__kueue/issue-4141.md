# Issue #4141: Kueue mutation admission webhook should intercept specific resource instance only

**Summary**: Kueue mutation admission webhook should intercept specific resource instance only

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4141

**Last updated**: 2025-07-13T01:07:44Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@ambersun1234](https://github.com/ambersun1234)
- **Created**: 2025-02-03T17:38:12Z
- **Updated**: 2025-07-13T01:07:44Z
- **Closed**: 2025-07-13T01:07:43Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to add a label to determine whether a resource instance should be intercept by Kueue's [MutatingAdmissionWebhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#mutatingadmissionwebhook)

> reference: [webhook.yaml](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/webhook/webhook.yaml#L426C3-L445C22)

```yaml
- admissionReviewVersions:
    - v1
  clientConfig:
    service:
      name: '{{ include "kueue.fullname" . }}-webhook-service'
      namespace: '{{ .Release.Namespace }}'
      path: /validate-batch-v1-job
  failurePolicy: Fail
  name: vjob.kb.io
  objectSelector:  # <- this
    matchLabels:
      foo: bar
  rules:
    - apiGroups:
        - batch
      apiVersions:
        - v1
      operations:
        - CREATE
        - UPDATE
      resources:
        - jobs
  sideEffects: None
```

**Why is this needed**:
Currently Kueue's [MutatingAdmissionWebhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#mutatingadmissionwebhook) select **all the job from all namespaces**\
Kueue shouldn't intercept resource instance that is not intended to be managed by Kueue

In our case, when Kueue is installing(or bootstraping), there's a job(Minio provisioning) running at the same time\
since Kueue's mutating webhook select all job, the Minio provisioning job will be intercept, but I don't want it to be intercept by Kueue 

At the same moment, Kueue's webhook isn't ready, so it'll fail

But the actual root cause is incorrect setup of mutating webhook, leading webhook to intercept the unrelated resource instance

here's the simplified reproduce step(to simulate the above issue we had)
```shell
$ helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/charts/kueue --version="v0.10.1" --create-namespace --namespace=kueue-system && kubectl create job my-job --image=busybox
Pulled: us-central1-docker.pkg.dev/k8s-staging-images/charts/kueue:v0.10.1
Digest: sha256:68658378dc673d3142d8dba222739c1ae2d3ef6742876f0249d599d0634b94da
NAME: kueue
LAST DEPLOYED: Tue Feb  4 01:00:12 2025
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
error: failed to create job: Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": no endpoints available for service "kueue-webhook-service"
```

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-03T18:03:12Z

Interesting! I was actually thinking of starting a discussion about this for Kueue for this but mostly for pod integration.

For pod integration, I am leaning towards a namespace labeling approach so that webhooks could only apply if a namespace is labeled. And I would prefer to flip the Kueue webhooks to be opt-in at the namespace level rather than exclude only a small subset of a cluster.

I did not really think that this would be necessary for Jobs but I can see why this may block other operators that may rely on one-time jobs.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-03T18:08:48Z

So just to be clear, you have `manageJobsWithoutQueueName: false` and you are mainly running this due to the webhooks having issues with starting up.

### Comment by [@ambersun1234](https://github.com/ambersun1234) — 2025-02-03T18:33:57Z

I just have the default setting of Kueue(i.e. `manageJobsWithoutQueueName: false`)\
also the Minio provisioning job is created by helm subchart, I didn't modify it

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-05T16:19:46Z

So since you don't use `manageJobsWithoutQueueName` could you just look at label for queues in the job?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-06T17:20:16Z

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

### Comment by [@Smuger](https://github.com/Smuger) — 2025-05-13T18:21:56Z

@kannon92 
Not sure if this is the same issue but going from: **v0.10.5** to **v0.11.4** my Kubernetes CronJob that has nothing to do with Kueue is now trying to reach out to Kueue's webhook.

cronjob status
```
Warning  FailedCreate      9m47s (x38 over 114m)  cronjob-controller  Error creating job: Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": context deadline exceeded
``` 

This is the cronjob I'm trying to run
```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: gpu-quota-metric-job
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  jobTemplate:
    spec:
      ttlSecondsAfterFinished: 60
      template:
        spec:
          serviceAccountName: gpu-quota-reporter
          containers:
            - name: reporter
              image: <MY-IMAGE>
              resources:
                requests:
                  cpu: 100m
                  memory: 128Mi
                limits:
                  cpu: 200m
                  memory: 256Mi
          restartPolicy: OnFailure
```

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-13T18:39:48Z

@Smuger is kueue down on your cluster?

What configuration do you have for Kueue?

We didn't really address this for jobs.

cc @mimowo @tenzen-y

### Comment by [@Smuger](https://github.com/Smuger) — 2025-05-13T18:49:47Z

Hi @kannon92 

I have v0.11.4 installed and services appear to be running:

```
NAMESPACE      NAME                                               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
kueue-system   kueue-controller-manager-metrics-service           ClusterIP   34.118.230.162   <none>        8443/TCP            104m
kueue-system   kueue-visibility-server                            ClusterIP   34.118.229.97    <none>        443/TCP             104m
kueue-system   kueue-webhook-service                              ClusterIP   34.118.235.194   <none>        443/TCP             104m
```

```
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-5975cbd886-pwphp   1/1     Running   0          64m
```

This is my whole config:

```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: AdmissionCheck
metadata:
  name: dws-prov
spec:
  controllerName: kueue.x-k8s.io/provisioning-request
  parameters:
    apiGroup: kueue.x-k8s.io
    kind: ProvisioningRequestConfig
    name: dws-config
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "prod-dws-a100-40gb-4x-cluster-queue"
spec:
  namespaceSelector: {} 
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    flavors:
    - name: "dws-a100-40gb-4x"
      resources:
      - name: "cpu"
        nominalQuota: 10000  # Infinite quota.
      - name: "memory"
        nominalQuota: 10000Gi # Infinite quota.
      - name: "nvidia.com/gpu"
        nominalQuota: 188
  admissionChecks:
  - dws-prov
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "prod-dws-a100-40gb-4x-local-queue"
spec:
  clusterQueue: "prod-dws-a100-40gb-4x-cluster-queue"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ProvisioningRequestConfig
metadata:
  name: dws-config
spec:
  provisioningClassName: queued-provisioning.gke.io
  managedResources:
  - nvidia.com/gpu
  retryStrategy:
    backoffLimitCount: 15
    backoffBaseSeconds: 60
    backoffMaxSeconds: 604800
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "dws-a100-40gb-4x"
```

logs from Kueue Controller Manager
```
E0513 18:49:03.106264       1 reflector.go:166] "Unhandled Error" err="sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: Failed to watch *v1.PartialObjectMetadata: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot list resource \"cronjobs\" in API group \"batch\" at the cluster scope" logger="UnhandledError"
W0513 18:49:50.057711       1 reflector.go:569] sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "cronjobs" in API group "batch" at the cluster scope
```

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-13T23:38:53Z

Based on those logs, @Smuger I don't think this issue is related.

In fact, this sounds like https://github.com/kubernetes-sigs/kueue/issues/5235.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-13T00:16:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-13T01:07:38Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-13T01:07:44Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4141#issuecomment-3066312956):

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
