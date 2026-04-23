# Issue #2182: clusterqueue_controller panics when workload has no admission

**Summary**: clusterqueue_controller panics when workload has no admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2182

**Last updated**: 2024-06-25T20:37:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@preslavgerchev](https://github.com/preslavgerchev)
- **Created**: 2024-05-10T15:39:41Z
- **Updated**: 2024-06-25T20:37:57Z
- **Closed**: 2024-06-25T20:37:55Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 22

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
We have recently updated kueue to 0.6.2. After some time the kueue manager started crashing with the following panic:
```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x18eb046]

goroutine 311 [running]:
sigs.k8s.io/kueue/pkg/controller/core.(*cqWorkloadHandler).requestForWorkloadClusterQueue(0xc0007a8398, 0xc00069b180)
	/workspace/pkg/controller/core/clusterqueue_controller.go:466 +0x106
sigs.k8s.io/kueue/pkg/controller/core.(*cqWorkloadHandler).Generic(0x2b298a0?, {0xc0008284b0?, 0x8?}, {{0x2b50680?, 0xc00069b180?}}, {0x2b3b1f0, 0xc000061900})
	/workspace/pkg/controller/core/clusterqueue_controller.go:457 +0x45
sigs.k8s.io/controller-runtime/pkg/source.(*Channel).Start.func2.1({0x2b298a0?, 0xc0008284b0?}, {0x2b29f90, 0xc0007a8398}, 0xc000c21fb0, {0x2b3b1f0, 0xc000061900})
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/source/source.go:133 +0x92
sigs.k8s.io/controller-runtime/pkg/source.(*Channel).Start.func2()
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/source/source.go:134 +0xf2

```

Upon further inspection we found that there is one workload object that has no `status.admission.clusterQueueName`:
```

apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: "2024-05-10T14:00:13Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2024-05-10T14:00:56Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 2
  labels:
    kueue.x-k8s.io/job-uid: 1e2d56d7-fd7f-491a-9c21-44f76a590195
  name: job-2ubekr94fbs28fshqol59hnkvn5o75u9m04o7p1dlbfhgebldqh0-1553e
  namespace: jobs
  ownerReferences:
  - apiVersion: batch/v1
    blockOwnerDeletion: true
    controller: true
    kind: Job
    name: 2ubekr94fbs28fshqol59hnkvn5o75u9m04o7p1dlbfhgebldqh0
    uid: 1e2d56d7-fd7f-491a-9c21-44f76a590195
  resourceVersion: "518239260"
  uid: b16437ac-d500-46c8-9688-0a8e3a1e306f
spec:
  active: true
  podSets:
  - count: 1
    name: main
  priority: 0
  priorityClassSource: ""
  queueName: lq
status:
  conditions:
  - lastTransitionTime: "2024-05-10T14:00:44Z"
    message: Quota reserved in ClusterQueue cq
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
  - lastTransitionTime: "2024-05-10T14:00:44Z"
    message: The workload is admitted
    reason: Admitted
    status: "True"
    type: Admitted
  - lastTransitionTime: "2024-05-10T14:00:56Z"
    message: Job finished successfully
    reason: JobFinished
    status: "True"
    type: Finished
```

We use kueue by assigning labels to a k8s job as described here: https://kueue.sigs.k8s.io/docs/tasks/run/jobs/

To me it seems like there's a race condition in the controller logic as we had the new version (0.6.2) running for some time until it crashed. We had to scale down the deployment, delete the validating/mutating webhooks so we can manually get rid off the workload. After restarting everything back, it worked for 2-3 hours until the same panic reoccurred.

For completeness, here's our resource flavor, local and cluster queue definitions if those are needed:
```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: sandboxed
spec:
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cq
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: sandboxed
      resources:
      - name: "cpu"
        nominalQuota: 1500m
      - name: "memory"
        nominalQuota: 12Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: jobs
  name: lq
spec:
  clusterQueue: cq # Point to the ClusterQueue cq
```

We have deployed everything as specified in the 0.6.2 manifests:
https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/manifests.yaml

The deployment's container are using the following images:
```
manager: registry.k8s.io/kueue/kueue:v0.6.2
kube-rbac-proxy: gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0
```

**Environment**:
- Kubernetes version (use `kubectl version`):  1.27.7-gke.1121002
- Kueue version (use `git describe --tags --dirty --always`): 0.6.2
- Cloud provider or hardware configuration: We're using GKE for our k8s cluster

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T17:40:34Z

Thank you for creating this issue!

1. Could you share which Kueue version you used before upgrading to v0.6.2?
2. When was the Workload without `.status.admission.clusterQueue` created? Before upgrading to v0.6.2? Or, After upgraded to v0.6.2?
3. When did the Workload without `.status.admission.clusterQueue` finish? Before upgrading to v0.6.2? Or, After upgraded to v0.6.2?

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-10T18:00:12Z

Thank you for the quick reply @tenzen-y!

1. We used kueue v0.3.0 before that, see the images we had deployed for the manager:
```
manager: gcr.io/k8s-staging-kueue/kueue:v20230214-v0.3.0-devel-253-g2d3f81a
kube-rbac-proxy: gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0
```
2. It was created after we updated to 0.6.2. The 0.6.2 kueue had been running for some time when this happened. Also worth pointing out there were also workloads that were fine, they had the `.status.admission` field being set. This was *not* the only problematic one, it was just one of the few I had grabbed the YAML output for. 
3. It finished long time after we deployed 0.6.2, the timestamps in the yaml file above indicate it only took ~30 seconds (which matches my expectations, based on the job it was).

Edit: Also worth pointing out the workload had no template in `spec.podSets[0]` which I thought must be set?

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-10T18:44:27Z

For what its worth, I found this recent PR https://github.com/kubernetes-sigs/kueue/pull/2171/ where it looks like a nil check is being added against the `.status.admission` field if that's of any help (although that's in a different controller)

### Comment by [@trasc](https://github.com/trasc) — 2024-05-14T10:16:28Z

@preslavgerchev  do you still have the spec for the job `2ubekr94fbs28fshqol59hnkvn5o75u9m04o7p1dlbfhgebldqh0`, somehow the resulting workload has no template for spec.podSets[0] and I'm puzzled about this.

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-14T10:31:05Z

@trasc sure! Here's a slightly redacted yaml spec, just the values have been substituted. I have dropped the`managedFields` for brevity, let me know if you want those too:
```
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    batch.kubernetes.io/job-tracking: ""
    kueue.x-k8s.io/queue-name: lq
  creationTimestamp: "2024-05-14T10:26:57Z"
  generation: 2
  labels:
    jobId: 43puiv1uboj90atcjnfflbhc92dd33fbn7kohq5736alneho8a1g
  name: 43puiv1uboj90atcjnfflbhc92dd33fbn7kohq5736alneho8a1g
  namespace: mondoo-job-runner-jobs
  ownerReferences:
  - apiVersion: k8s.mondoo.com/v1alpha1
    blockOwnerDeletion: true
    controller: true
    kind: SomeKind
    name: 43puiv1uboj90atcjnfflbhc92dd33fbn7kohq5736alneho8a1g
    uid: 0c116262-3e62-4f84-baa7-9449e254f890
  resourceVersion: "522584798"
  uid: 193bd7a6-2806-447c-b48a-58a6360f29ac
spec:
  activeDeadlineSeconds: 7200
  backoffLimit: 0
  completionMode: NonIndexed
  completions: 1
  parallelism: 1
  podFailurePolicy:
    rules: null
  selector:
    matchLabels:
      batch.kubernetes.io/controller-uid: 193bd7a6-2806-447c-b48a-58a6360f29ac
  suspend: false
  template:
    metadata:
      creationTimestamp: null
      labels:
        batch.kubernetes.io/controller-uid: 193bd7a6-2806-447c-b48a-58a6360f29ac
        batch.kubernetes.io/job-name: 43puiv1uboj90atcjnfflbhc92dd33fbn7kohq5736alneho8a1g
        controller-uid: 193bd7a6-2806-447c-b48a-58a6360f29ac
        job-name: 43puiv1uboj90atcjnfflbhc92dd33fbn7kohq5736alneho8a1g
    spec:
      automountServiceAccountToken: false
      containers:
      - args:
        - stuff
        command:
        - cmd
        env:
        - name: env
          value: var
        image: img
        imagePullPolicy: Always
        name: name
        resources:
          limits:
            cpu: 250m
            memory: 2000Mi
          requests:
            cpu: 250m
            memory: 2000Mi
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          privileged: false
          readOnlyRootFilesystem: false
          runAsNonRoot: true
          runAsUser: 999
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /config
          name: config
          readOnly: true
      dnsConfig:
        nameservers:
        - 8.8.8.8
        - 1.1.1.1
      dnsPolicy: None
      restartPolicy: Never
      runtimeClassName: gvisor
      schedulerName: default-scheduler
      securityContext:
        runAsNonRoot: true
        runAsUser: 999
      terminationGracePeriodSeconds: 0
      volumes:
      - name: config
        secret:
          defaultMode: 420
          optional: true
          secretName: 43puiv1uboj90atcjnfflbhc92dd33fbn7kohq5736alneho8a1g
```

### Comment by [@trasc](https://github.com/trasc) — 2024-05-14T11:11:33Z

Thanks @preslavgerchev , I'll have a deeper look on this.

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-14T11:30:46Z

> Thanks @preslavgerchev , I'll have a deeper look on this.
> 
> /assign

Thank you for taking this. I'm suspecting that QuotaReserved brought us breaking change without backward compatibility since we added it recently.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-14T13:19:12Z

@preslavgerchev is there any chance you still have `v1alpha2` kueue CRDs installed, temporary storing a workload as `v1aplpha2` will explain losing both the `spec.podSets[0].template` (which used to be a PodSpec) and `status.admission` (which used to be stored in `spec`).

@alculquicondor  have you encountered something like this?

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-14T13:34:19Z

> @preslavgerchev is there any chance you still have `v1alpha2` kueue CRDs installed, temporary storing a workload as `v1aplpha2` will explain losing both the `spec.podSets[0].template` (which used to be a PodSpec) and `status.admission` (which used to be stored in `spec`).
> 
@trasc, as part of our update flow we updated the CRD `spec.versions` to hold both `v1alpha2` and `v1beta1`. However, we did update the alpha one with `storage:false` and set `storage:true` only for the beta1 versions. However, `served` was still marked as `true`, maybe that was a problem? 

Here's a link to the CRDs as we had them deployed as part of the upgrade
https://gist.github.com/preslavgerchev/9f8ec2840a669133a535a36177d78b7e

### Comment by [@trasc](https://github.com/trasc) — 2024-05-14T13:44:16Z

> > @preslavgerchev is there any chance you still have `v1alpha2` kueue CRDs installed, temporary storing a workload as `v1aplpha2` will explain losing both the `spec.podSets[0].template` (which used to be a PodSpec) and `status.admission` (which used to be stored in `spec`).
> 
> @trasc, as part of our update flow we updated the CRD `spec.versions` to hold both `v1alpha2` and `v1beta1`. However, we did update the alpha one with `storage:false` and set `storage:true` only for the beta1 versions. However, `served` was still marked as `true`, maybe that was a problem?
> 
> Here's a link to the CRDs as we had them deployed as part of the upgrade https://gist.github.com/preslavgerchev/9f8ec2840a669133a535a36177d78b7e

Unfortunately I don't know how to dig dipper in this multiple CRD version scenario, can you remove the `v1alpha2` CRD version and check if the issue will reproduce.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T15:09:41Z

Maybe additionally confirm if there is no other old pod of Kueue running. If there is a Pod running v0.2.x, then it might be responding to webhooks and dropping fields.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-15T15:12:50Z

> Maybe additionally confirm if there is no other old pod of Kueue running. If there is a Pod running v0.2.x, then it might be responding to webhooks and dropping fields.

Unlikely, the wl has QuotaReserved condition which is more or less new.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T15:14:39Z

Yeah, but the webhook wouldn't drop conditions... it doesn't validate names of conditions, IIRC.

We see that the Workload shared by the OP has no podset template or admission fields, which are two things that changed when we released v1beta1

### Comment by [@trasc](https://github.com/trasc) — 2024-05-15T15:25:24Z

So ... we have wl admitted by the `new kueue` and the `old kueue` doing an update and dropping the template and admission .... it could be it.

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-26T15:51:32Z

hi @trasc, sorry for the late reply on this one.

I currently cannot safely drop the `v1alpha2` definition from the CRD and update as I worry there might be currently running workloads, which will be defined in the alpha version. If we were to deploy the beta controller, the same problem will occur I believe.
 
If this is the recommended approach, I will look into first stopping kueue entirely, ensuring there are no workload objects in the cluster and then upgrading.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-27T06:30:22Z

Hi @preslavgerchev,
Who is creating and managing `v1alpha2` Workloads? 
The kueue controller manager uses only `v1beta1` since v0.3.0.

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-27T06:50:16Z

> Hi @preslavgerchev, Who is creating and managing `v1alpha2` Workloads? The kueue controller manager uses only `v1beta1` since v0.3.0.

That should be the kueue controller. The only way we create jobs is by labelling k8s jobs with the `kueue.x-k8s.io/queue-name` label. We do not create the Workloads in any way.

When we upgraded, there were no workload objects in the cluster. Which means that the new kueue controller (v0.6.2) had taken a k8s job with that label and created a workload object for it with the missing admission and pod set fields

### Comment by [@preslavgerchev](https://github.com/preslavgerchev) — 2024-05-27T06:50:35Z

> Maybe additionally confirm if there is no other old pod of Kueue running. If there is a Pod running v0.2.x, then it might be responding to webhooks and dropping fields.

Can confirm, we only had one pod (v0.6.2) of the controller manager running

### Comment by [@trasc](https://github.com/trasc) — 2024-05-27T07:05:54Z

> That should be the kueue controller. The only way we create jobs is by labelling k8s jobs with the `kueue.x-k8s.io/queue-name` label. We do not create the Workloads in any way.

The newer version of kueue controller v0.3+ are only using `v1beta1` api, any job integration controller within kueue should be able to recreate the workload associated with a job in case the  podDet template is missing.

If there is no old kueue or custom controller working with `v1aplha2` there should be issue dropping the CRD.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-27T13:55:29Z

@preslavgerchev can you open a support ticket with GKE as well?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:37:51Z

/close

Please reopen if the issue persists or you find more data points.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:37:55Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2182#issuecomment-2189924923):

>/close
>
>Please reopen if the issue persists or you find more data points.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
