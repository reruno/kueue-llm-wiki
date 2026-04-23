# Issue #7649: Kueue is suspending JobSet that isn't supposed to manage

**Summary**: Kueue is suspending JobSet that isn't supposed to manage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7649

**Last updated**: 2025-11-19T13:14:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Created**: 2025-11-13T17:44:13Z
- **Updated**: 2025-11-19T13:14:01Z
- **Closed**: 2025-11-19T13:14:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 13

## Description

**What happened**:

When Kueue is configured like the following:

```
    manageJobsWithoutQueueName: true
    managedJobsNamespaceSelector:
      matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: NotIn
          values: [ kube-system, kueue-system , test]
```
and a JobSet is created on the test namespace, which is a namespace not managed by Kueue, the jobs ends up suspended. However, the jobset is set to` suspended: false`.

```
$ kubectl get jobset -n test
NAME              TERMINALSTATE   RESTARTS   COMPLETED   SUSPENDED   AGE
sleep-job-x5ffx                   0                      false       16m
$ kubectl get job -n test
NAME                        STATUS      COMPLETIONS   DURATION   AGE
sleep-job-x5ffx-driver-0    Suspended   0/1                      16m
sleep-job-x5ffx-workers-0   Suspended   0/1                      16m
```

The jobs created for this jobset has the following events:
```
Events:
  Type    Reason            Age                      From                        Message
  ----    ------            ----                     ----                        -------
  Normal  SuccessfulDelete  10m                      job-controller              Deleted pod: sleep-job-x5ffx-driver-0-0-qm6jk
  Normal  SuccessfulCreate  10m                      job-controller              Created pod: sleep-job-x5ffx-driver-0-0-sth7c
  Normal  SuccessfulDelete  10m                      job-controller              Deleted pod: sleep-job-x5ffx-driver-0-0-sth7c
  Normal  Suspended         10m (x2 over 10m)        job-controller              Job suspended
  Normal  SuccessfulCreate  10m                      job-controller              Created pod: sleep-job-x5ffx-driver-0-0-qm6jk
  Normal  SuccessfulDelete  10m                      job-controller              Deleted pod: sleep-job-x5ffx-driver-0-0-v6n6j
  Normal  SuccessfulCreate  10m                      job-controller              Created pod: sleep-job-x5ffx-driver-0-0-v6n6j
  Normal  SuccessfulCreate  10m                      job-controller              Created pod: sleep-job-x5ffx-driver-0-0-fgl5w
  Normal  SuccessfulDelete  10m                      job-controller              Deleted pod: sleep-job-x5ffx-driver-0-0-fgl5w
  Normal  SuccessfulCreate  10m                      job-controller              Created pod: sleep-job-x5ffx-driver-0-0-47ndl
  Normal  SuccessfulDelete  10m                      job-controller              Deleted pod: sleep-job-x5ffx-driver-0-0-47ndl
  Normal  SuccessfulCreate  10m                      job-controller              Created pod: sleep-job-x5ffx-driver-0-0-4zjv9
  Normal  SuccessfulDelete  5m13s (x337 over 9m59s)  job-controller              (combined from similar events): Deleted pod: sleep-job-x5ffx-driver-0-0-b9drd
  Normal  Resumed           13s (x3203 over 10m)     job-controller              Job resumed
  Normal  Suspended         13s (x14709 over 10m)    batch/job-kueue-controller  Kueue managed child job suspended
```

No workload is created:
```
$ kubectl get workloads -A
No resources found
```

**What you expected to happen**:

Kueue wouldn't influence jobs that are skipped in the namespace specified at `managedJobsNamespaceSelector`.

**How to reproduce it (as minimally and precisely as possible)**:

Configure Kueue like the following:

```
    manageJobsWithoutQueueName: true
    managedJobsNamespaceSelector:
      matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: NotIn
          values: [ kube-system, kueue-system , test]
```

Create the following jobset:
```
$ kubectl get jobset sleep-job-x5ffx -n test -o yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  creationTimestamp: "2025-11-13T17:25:26Z"
  generateName: sleep-job-
  generation: 1
  name: sleep-job-x5ffx
  namespace: test
  resourceVersion: "218271"
  uid: c9cd3c1e-624b-491c-98a2-fa1c3ef10779
spec:
  network:
    enableDNSHostnames: false
    publishNotReadyAddresses: true
    subdomain: some-subdomain
  replicatedJobs:
  - groupName: default
    name: workers
    replicas: 1
    template:
      metadata: {}
      spec:
        backoffLimit: 0
        completionMode: Indexed
        completions: 1
        parallelism: 1
        template:
          metadata: {}
          spec:
            containers:
            - args:
              - 10s
              command:
              - sleep
              image: busybox
              name: sleep
              resources:
                requests:
                  cpu: "1"
                  memory: 200Mi
            restartPolicy: OnFailure
  - groupName: default
    name: driver
    replicas: 1
    template:
      metadata: {}
      spec:
        backoffLimit: 0
        completionMode: Indexed
        completions: 1
        parallelism: 1
        template:
          metadata: {}
          spec:
            containers:
            - args:
              - 10s
              command:
              - sleep
              image: busybox
              name: sleep
              resources:
                requests:
                  cpu: "2"
                  memory: 200Mi
            restartPolicy: OnFailure
  startupPolicy:
    startupPolicyOrder: AnyOrder
  successPolicy:
    operator: All
  suspend: false
status:
  replicatedJobsStatus:
  - active: 0
    failed: 0
    name: workers
    ready: 0
    succeeded: 0
    suspended: 1
  - active: 0
    failed: 0
    name: driver
    ready: 0
    succeeded: 0
    suspended: 0
  restarts: 0
```
Check the jobs are suspended.

**Anything else we need to know?**:

When `manageJobsWithoutQueueName: true` is not specified, the jobs are not suspended as expected.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): v0.14.4, v0.13.9
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-11-13T17:44:29Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-13T18:00:42Z

Could you display the jobs that get created also?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-13T18:01:50Z

cc @mimowo @tenzen-y @mbobrovskyi 

Curious if you all have any ideas on what could be going wrong?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T19:04:17Z

It seems this code suspends the Job https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L365-L384

this happens because the parent JobSet does not have the Workload, rightfully.

However, I would expect the Reconcile for Job to be skipped earlier, right here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L325-L328

However, this code is under ManagedJobsNamespaceSelectorAlwaysRespected, can you check the feature gate is enabled in your env?

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-11-13T19:20:01Z

@mimowo the featuregate is not enabled as I was trying with 0.14.4.
I'm not sure I follow why we should have it enabled for a scenario where we have `manageJobsWithoutQueueName` enabled + namespace skipped on `managedJobsNamespaceSelector`.

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-11-13T19:25:57Z

I was checking the KEP about `ManagedJobsNamespaceSelectorAlwaysRespected` and it mentions:

> 1. When the feature gate is disbaled: This reflects existing behavior prior to Kueue v0.13
> -   If `manageJobsWithoutQueueName` is true, then Kueue will (a) manage all instances of supported Kinds
>     that have a `queue-name` label and (b) will manage all instances of supported Kinds that do not
>     have a `queue-name` label if they are in namespaces that match `managedJobsNamespaceSelector`.

This doesn't reflect what I noticed.

[github.com/kubernetes-sigs/kueue/blob/main/keps/3589-manage-jobs-selectively/README.md?plain=1#L104-L106](https://github.com/kubernetes-sigs/kueue/blob/main/keps/3589-manage-jobs-selectively/README.md?plain=1#L104-L106)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T19:38:13Z

> @mimowo the featuregate is not enabled as I was trying with 0.14.4.

Please try enabling and see if this helps.

> I'm not sure I follow why we should have it enabled for a scenario where we have manageJobsWithoutQueueName enabled + namespace skipped on managedJobsNamespaceSelector.

Enabling the feature gate is required to step into https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L325-L328
When the feature gate is disabled the code below executes, resulting in the event you observe "Kueue managed child job suspended" (in the issue description)

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-13T19:39:36Z

Yea I think we are probably hitting a unrelated bug.

https://github.com/kubernetes-sigs/kueue/blob/release-0.14/pkg/controller/jobframework/reconciler.go#L379

I think we may need to move this check up before the TopLevel job check.

In this case, we should hit:

```golang
	// when manageJobsWithoutQueueName is enabled, standalone jobs without queue names
	// are still not managed if they don't match the namespace selector.
	if r.manageJobsWithoutQueueName && QueueName(job) == "" {
		ns := corev1.Namespace{}
		err := r.client.Get(ctx, client.ObjectKey{Name: job.Object().GetNamespace()}, &ns)
		if err != nil {
			log.Error(err, "failed to get job namespace")
			return ctrl.Result{}, err
		}
		if !r.managedJobsNamespaceSelector.Matches(labels.Set(ns.GetLabels())) {
			log.V(3).Info("namespace selector does not match, ignoring the job", "namespace", ns.Name)
			return ctrl.Result{}, nil
		}
	}
```

We hit this code and skip reconciler for this job.

I think QueueName(job) should be empty in your case since you don't have any labels

We do not want to fall into in this case.

```golang
	// if this is a non-toplevel job, suspend the job if its ancestor's workload is not found or not admitted.
	if !isTopLevelJob {
		_, _, finished := job.Finished()
		if !finished && !job.IsSuspended() {
			if ancestorWorkload, err := r.getWorkloadForObject(ctx, ancestorJob); err != nil {
				log.Error(err, "couldn't get an ancestor job workload")
				return ctrl.Result{}, err
			} else if ancestorWorkload == nil || !workload.IsAdmitted(ancestorWorkload) {
				if err := clientutil.Patch(ctx, r.client, object, func() (client.Object, bool, error) {
					job.Suspend()
					return object, true, nil
				}); err != nil {
					log.Error(err, "suspending child job failed")
					return ctrl.Result{}, err
				}
				r.record.Event(object, corev1.EventTypeNormal, ReasonSuspended, "Kueue managed child job suspended")
			}
		}
		return ctrl.Result{}, nil
	}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T19:41:00Z

> This doesn't reflect what I noticed.
> [github.com/kubernetes-sigs/kueue/blob/main/keps/3589-manage-jobs-selectively/README.md?plain=1#L104-L106](https://github.com/kubernetes-sigs/kueue/blob/main/keps/3589-manage-jobs-selectively/README.md?plain=1#L104-L106)

Yeah, the KEP focused on the simple scenarios I think, but we missed the hierarchical Jobs like JobSet. So I think with disabled ManagedJobsNamespaceSelectorAlwaysRespected the behavior might be just buggy and not well documented.

If this is confirmed, we could consider backporting the enablement of the feature gate as a bugfix.

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-11-13T21:05:54Z

@mimowo with `ManagedJobsNamespaceSelectorAlwaysRespected: true` on 0.14.4 we don't hit the issue.
We also don't hit the issue with @kannon92's suggestion.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-13T21:24:21Z

> If this is confirmed, we could consider backporting the enablement of the feature gate as a bugfix.


TBH I don't like the idea of backporting enabling alpha feature gates. 

For Openshift Kueue we would prefer this feature gate to be enabled in 0.14 but I don't want to encourage enabling alpha feature gates on patch releases.

My proposal would be to add a e2e test that verifies this works. Apply my suggestion (move check before toplevel Job) and carry that PR to 0.14 and 0.13.

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-11-13T23:45:53Z

@kannon92 That makes sense to me. Let's see what @mimowo thinks.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T07:35:17Z

the proposal from @kannon92 to scope the code changes to bugfix sounds even better to me, plus e2e test
