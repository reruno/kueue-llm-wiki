# Issue #5129: GKE; The workload backoff was finished; The workload has failed admission checks; Max nodepool size reached

**Summary**: GKE; The workload backoff was finished; The workload has failed admission checks; Max nodepool size reached

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5129

**Last updated**: 2025-07-31T11:26:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Smuger](https://github.com/Smuger)
- **Created**: 2025-04-25T20:03:57Z
- **Updated**: 2025-07-31T11:26:22Z
- **Closed**: 2025-07-31T11:26:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
**Possibly the same issue**
https://github.com/kubernetes-sigs/kueue/issues/3258

**What happened**:

On a GKE cluster workloads fail admission check for jobs that had to be queue due to max nodepool size reached. I'm also using [Dynamic Workload Scheduler](https://cloud.google.com/blog/products/compute/introducing-dynamic-workload-scheduler)

We have seen this happened the most on flavors that require more than 1 GPU. The example below comes from a run with a flavor that needs x4 A100.

```
Status:
  Admission Checks:
    Last Transition Time:  2025-04-25T16:06:34Z
    Message:               Retrying after failure: Max nodepool size reached, affected nodepools: dws-a100-40gb-4x-node-pool
    Name:                  dws-prov
    State:                 Retry
  Conditions:
    Last Transition Time:  2025-04-25T16:09:23Z
    Message:               The workload has failed admission checks
    Observed Generation:   1
    Reason:                Pending
    Status:                False
    Type:                  QuotaReserved
    Last Transition Time:  2025-04-25T16:09:23Z
    Message:               At least one admission check is false
    Observed Generation:   1
    Reason:                AdmissionCheck
    Status:                True
    Type:                  Evicted
    Last Transition Time:  2025-04-25T16:10:23Z
    Message:               The workload backoff was finished
    Observed Generation:   1
    Reason:                BackoffFinished
    Status:                True
    Type:                  Requeued
  Requeue State:
    Count:       1
    Requeue At:  2025-04-25T16:10:23Z
  Resource Requests:
    Name:  main
    Resources:
      Cpu:             1250m
      Memory:          8Gi
      nvidia.com/gpu:  4
Events:
  Type     Reason   Age                   From             Message
  ----     ------   ----                  ----             -------
  Warning  Pending  14m (x89 over 3h32m)  kueue-admission  The workload has failed admission checks
```

**What you expected to happen**:
I was expecting the backoff strategy to retry admission checks for 7 days.
```yaml
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
    backoffMaxSeconds: 604800  # 7 days in seconds
```

**How to reproduce it (as minimally and precisely as possible)**:
1. Create a GKE cluster with one nodepool of size 1 of a given flavor 
2. Create two jobs that need that flavor
3. When the first job finishes, the second will already be in a BackoffFinished state and will not attempt to run another admission check.

**Anything else we need to know?**:
This can be completely wrong and the cause of this problem but I'm assuming that I need to allow the nodepool to scale to a value one more than my quota. 

e.g.
`If I have a quota of [1] A100 I should set my autoscaling on my nodepool to 2`

`If I have a quota of [4] A100 and my favor needs four GPUs per box I need to set autoscaling on my nodepool to 8`


**Environment**:
- Kubernetes version (use `kubectl version`):
```
Client Version: v1.33.0
Kustomize Version: v5.6.0
Server Version: v1.32.3-gke.1717000
```
- Kueue version (use `git describe --tags --dirty --always`):
```
v0.11.4 (but we saw this on v0.11.3 as well. Probably also the previous ones)
```
- Cloud provider or hardware configuration:
```
Google Cloud; A100 40GB
```
- OS (e.g: `cat /etc/os-release`):
```
NAME="Container-Optimized OS"
ID=cos
PRETTY_NAME="Container-Optimized OS from Google"
HOME_URL="https://cloud.google.com/container-optimized-os/docs"
BUG_REPORT_URL="https://cloud.google.com/container-optimized-os/docs/resources/support-policy#contact_us"
GOOGLE_METRICS_PRODUCT_ID=26
KERNEL_COMMIT_ID=b09cce333d9e64d1404b4b56037dd2492722fa1e
GOOGLE_CRASH_ID=Lakitu
VERSION=117
VERSION_ID=117
BUILD_ID=18613.164.98
```
- Kernel (e.g. `uname -a`):
```
Linux gke-prod-n-r-training-kueue-node-pool-6334a200-6nv5 6.6.72+ #1 SMP PREEMPT_DYNAMIC Sun Mar 30 09:02:56 UTC 2025 x86_64 Intel(R) Xeon(R) CPU @ 2.20GHz GenuineIntel GNU/Linux
```
- Install tools:
- Others:

I was also seeing errors like this one for the jobs that were failing
```json
{
  "insertId": "qftjasvb2zeu3dc9",
  "jsonPayload": {
    "error": "clearing admission: Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"job-0d1fff4c41864c69b8f9fca17b7d4f73-35ffd\": the object has been modified; please apply your changes to the latest version and try again",
    "controllerKind": "Job",
    "reconcileID": "8ddad845-2f9e-49f2-ab0d-7295bd183b0d",
    "level": "error",
    "stacktrace": "sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224",
    "controllerGroup": "batch",
    "controller": "job",
    "namespace": "default",
    "msg": "Reconciler error",
    "Job": {
      "namespace": "default",
      "name": "0d1fff4c41864c69b8f9fca17b7d4f73"
    },
    "name": "0d1fff4c41864c69b8f9fca17b7d4f73",
    "ts": "2025-04-25T16:09:23.164778584Z",
    "caller": "controller/controller.go:316"
  },
  "resource": {
    "type": "k8s_container",
    "labels": {
      "project_id": "n-r-training",
      "cluster_name": "prod-n-r-training-cluster-us-e1",
      "pod_name": "kueue-controller-manager-5975cbd886-56vc9",
      "namespace_name": "kueue-system",
      "container_name": "manager",
      "location": "us-east1"
    }
  },
  "timestamp": "2025-04-25T16:09:23.165111880Z",
  "severity": "ERROR",
  "labels": {
    "compute.googleapis.com/resource_name": "gke-prod-n-r-training-kueue-node-pool-6334a200-6nv5",
    "k8s-pod/app_kubernetes_io/component": "controller",
    "logging.gke.io/top_level_controller_type": "Deployment",
    "k8s-pod/control-plane": "controller-manager",
    "logging.gke.io/top_level_controller_name": "kueue-controller-manager",
    "k8s-pod/pod-template-hash": "5975cbd886",
    "k8s-pod/app_kubernetes_io/name": "kueue"
  },
  "logName": "projects/n-r-training/logs/stderr",
  "receiveTimestamp": "2025-04-25T16:09:25.369575252Z"
}
```

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-26T14:09:04Z

cc @mimowo @mwielgus 

I'm not sure if this is really an upstream issue as this seems to be a GKE specific problem with the DWS admission checks.

### Comment by [@Smuger](https://github.com/Smuger) — 2025-04-28T09:21:41Z

@kannon92 

Thanks for getting back to me.

I've reached out to Google about this and will share their response here in case others are experiencing the same issue.

Please correct me if I'm wrong, but I believe the admission check should still re-run even if "dws-prov" is not right?

### Comment by [@rlia](https://github.com/rlia) — 2025-04-30T11:36:36Z

I often use GKE Autopilot for Kueue experimenting and regularly encounter problems.

Has a ProvisioningRequest been created by Kueue? If so, what is the status?
```
$ kubectl get provisioningrequest 
$ kubectl describe provisioningrequest 
```

Also, the procedure for using DWS without Kueue could be used to see if there is a problem with GKE's DWS itself.
https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest#create-provisioningrequest


---
PS
(Just a thought) 
Are you setting --num-nodes=1 when creating the node pool?
If you follow the procedure, it would look like this
```
  --num-nodes=0   
  --total-max-nodes 1
```
https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest#create-node-pool

### Comment by [@jaash7zohz](https://github.com/jaash7zohz) — 2025-06-12T16:05:48Z

Hello @Smuger !

> I've reached out to Google about this and will share their response here in case others are experiencing the same issue.
> 
> Please correct me if I'm wrong, but I believe the admission check should still re-run even if "dws-prov" is not right?

Have you got any news from Google please (or any solution) ?
Thank you !

### Comment by [@Smuger](https://github.com/Smuger) — 2025-06-18T09:04:42Z

@jaash7zohz 

Google is looking into this. It doesn’t appear to be a misconfiguration on the user’s side.

### Comment by [@SC-Turner](https://github.com/SC-Turner) — 2025-07-09T10:10:34Z

I'm having this exact problem also. Occurs on both Kueue v0.7.0 and v0.12.3. 

Notably, deleting the workload manually will retrigger an admissionCheck for the job and the job will run (If resources are now available).

Any work arounds or solutions would be much appreciated.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T09:29:25Z

So, there are two things at play here, IIUC:
1. why GKE does not provision successfully the ProvisioningRequest sometimes when using `queued-provisioning.gke.io` - I would leave this issue to the GKE support team
2. why Kueue does not retry the failure, as it is expected based on the configuration:

```yaml
  retryStrategy:
    backoffLimitCount: 15
    backoffBaseSeconds: 60
    backoffMaxSeconds: 604800  # 7 days in seconds
```
Let's focus exclusively on (2.) here.

First, indeed, the status is surprising 
```yaml
Status:
  Admission Checks:
    Last Transition Time:  2025-04-25T16:06:34Z
    Message:               Retrying after failure: Max nodepool size reached, affected nodepools: dws-a100-40gb-4x-node-pool
    Name:                  dws-prov
    State:                 Retry
  Conditions:
    Last Transition Time:  2025-04-25T16:09:23Z
    Message:               The workload has failed admission checks
    Observed Generation:   1
    Reason:                Pending
    Status:                False
    Type:                  QuotaReserved
    Last Transition Time:  2025-04-25T16:09:23Z
    Message:               At least one admission check is false
    Observed Generation:   1
    Reason:                AdmissionCheck
    Status:                True
    Type:                  Evicted
```
because the AC state should be reset back to "Pending" by [ResetChecksOnEviction](
https://github.com/kubernetes-sigs/kueue/blob/74a9dfc91cc1caf7a0ddb283e2972cd49de32e02/pkg/controller/core/workload_controller.go#L398-L399) on eviction which happened at `2025-04-25T16:09:23Z`.

So, the puzzle is - why during eviction the admission check was not flipped to "Pending" - I believe this is what is blocking the re-admission.

To help us understand the issue:
- does this happen on every run or flakes?
- does it trigger re-admission if you manually flip workload.Status.AdmissionChecks.State to pending? eg. using `kubectl edit wl/<wl-name> --subresource=status`
- can you provide full kueue logs, grepped by the workload name at the level of V(3)?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T09:30:33Z

cc @PBundyra who also worked on AdmissionChecks at some point and may have some idea on why the workload wasn't retried by Kueue

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T09:37:25Z

Actually, the reported status in Kueue looks very much like created using Kueue before this fix: https://github.com/kubernetes-sigs/kueue/pull/3323 .

Can you please confirm you observe the analogous status with the latest Kueue?

### Comment by [@pajakd](https://github.com/pajakd) — 2025-07-28T13:30:09Z

I'm not sure if this is a correct idea but I looked at the error `clearing admission: Operation cannot be fulfilled on workloads.kueue.x-k8s.io ...` The only place such error is raised is in `job_controller`, where it tries to clear the admission status of a workload:
https://github.com/kubernetes-sigs/kueue/blob/df666615ec258c583c07cd472a182f9664fb322c/pkg/controller/jobframework/reconciler.go#L544
When looking at the logs of a (probably) same issue I saw that `job_controller` and `workload_controller` were running reconcile around the same time. 

Could it happen that due to a race condition, the reconcile in `job_controller` fails to clear the admission status of a workload, which is the not retried and the workload enter some weird state and this is why its stuck?

Because soon after that I see the repeated logs `The workload has failed admission checks` for days...

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T18:44:24Z

I think I understand the issue (for now only based on static code and logs analysis). It requires interaction between 3 components: job_controller, workload_controller, provisioning_controller. 

0. (precondition) workload is admitted and ProvisioningRequest fails, eg. due to "Max nodepool size reached"
1. provisioning_controller sets `status.admissionChecks.state=Retry`
2. workload_controller sets `Evicted=True` condition and resets `status.admissionChecks.state=Pending`
3. provisioning_controller sets `status.admissionChecks.state=Retry` again, because it does not yet see `Evicted=true`
4. job_controller sets `QuotaReserved=False`
5. scheduler cannot schedule because admissionChecks are Retry so the workload admission is not re-attempted (see [here](https://github.com/kubernetes-sigs/kueue/blob/fafa17dd8c29965c7b1856fee4d038b98ce8d632/pkg/scheduler/scheduler.go#L415-L416))

This scenario is unlikely because it requires a narrow timing sequence: 1->2->3. However, this is entirely possible, because provisioning_controller at (1.) and (3.) is using SSA patch without the strict mode, see [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/provisioning/controller.go#L606), and so it is possible that "provisoniong_controller" succeeds at (3.) even though it does not have the latest workload object - it does not yet know that (2.) happened.

So, one way of fixing is to just use the strict mode for the provisioning controller. I will try to have a repro integration test with the fix. 
/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T11:46:40Z

Since the nature of the issue is very racy it is a bit tricky to reliably repro. The two existing tests repro the issue but the failure rate is very low. The most reliable repro I got is with:

```golang
for i := range 1000 {
	ginkgo.FIt(fmt.Sprintf("Issue repro %d", i), func() {
		// Repro for https://github.com/kubernetes-sigs/kueue/issues/5129
		ginkgo.By("Setting the quota reservation to the workload", func() {
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, &updatedWl)).Should(gomega.Succeed())
				g.Expect(util.SetQuotaReservation(ctx, k8sClient, &updatedWl, admission)).To(gomega.Succeed())
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
		})

		ginkgo.By("Setting the provision request-1 as Failed", func() {
			provReqKey := types.NamespacedName{
				Namespace: wlKey.Namespace,
				Name:      provisioning.ProvisioningRequestName(wlKey.Name, kueue.AdmissionCheckReference(ac.Name), 1),
			}
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, provReqKey, &createdRequest)).Should(gomega.Succeed())
				apimeta.SetStatusCondition(&createdRequest.Status.Conditions, metav1.Condition{
					Type:   autoscaling.Failed,
					Status: metav1.ConditionTrue,
					Reason: autoscaling.Failed,
				})
				g.Expect(k8sClient.Status().Update(ctx, &createdRequest)).Should(gomega.Succeed())
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
		})

		ginkgo.By("Checking the Workload is Evicted", func() {
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, &updatedWl)).To(gomega.Succeed())
				_, evicted := workload.IsEvictedByAdmissionCheck(&updatedWl)
				g.Expect(evicted).To(gomega.BeTrue())
			}, util.Timeout, time.Millisecond).Should(gomega.Succeed())
		})

		ginkgo.By("Checking the AdmissionChecks are reset to Pending and remain this way", func() {
			gomega.Consistently(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, &updatedWl)).To(gomega.Succeed())
				check := workload.FindAdmissionCheck(updatedWl.Status.AdmissionChecks, kueue.AdmissionCheckReference(ac.Name))
				g.Expect(check).NotTo(gomega.BeNil())
				g.Expect(check.State).To(gomega.Equal(kueue.CheckStatePending), fmt.Sprintf("workload status: %v, conditions: %v", updatedWl.Status, updatedWl.Status.Conditions))
			}, util.ConsistentDuration, util.ShortInterval).Should(gomega.Succeed())
		})
	})
}
```
It fails around 1/100 runs which is enough to prove the bug, but a bit tricky to merge it as a new test.

In any case I confirmed the flow from the previous comment with an extra logging inside provisioning controller where I would log the ResourceVersion additionally for Workload.

It turns out occasionally provisioning_controller runs Reconcile with the same ResourceVersion (seeing state=Pending) and updates the state to Retry. While the first request is correct, the other request operates on stale status which was in the meanwhile changed by workload_controller which added Evicted=True. Note that this is a standard behavior in k8s controllers as the informer cache may not be updated at the moment when new Reconcile starts.

I'm yet thinking about the scope of the fix - I think we should use strict mode for all requests updating status.admissionChecks, because this field is used by multiple controllers. I'm also considering extending the use of the strict mode for other requests, but we can discuss the details in the PR.

Using the strict mode for admission checks I was able to make the test pass for over 580 repeats already (tests continue running).

EDIT: the tests completed, all 1000 runs passed.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T11:23:47Z

/reopen 
There is a follow up issue that the ProvisioningRequests don't get create after second eviction, see repro by @PBundyra  https://github.com/kubernetes-sigs/kueue/pull/6322

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-31T11:23:52Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5129#issuecomment-3139545957):

>/reopen 
>There is a follow up issue that the ProvisioningRequests don't get create after second eviction, see repro by @PBundyra  https://github.com/kubernetes-sigs/kueue/pull/6322


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T11:26:17Z

It is now tracked here: https://github.com/kubernetes-sigs/kueue/issues/6323
/close

Let me close this one as it specifically mentions the state which should be not possible after the first fix:
```
Status:
  Admission Checks:
    Last Transition Time:  2025-04-25T16:06:34Z
    Message:               Retrying after failure: Max nodepool size reached, affected nodepools: dws-a100-40gb-4x-node-pool
    Name:                  dws-prov
    State:                 Retry
  Conditions:
    Message:               At least one admission check is false
    Observed Generation:   1
    Reason:                AdmissionCheck
    Status:                True
    Type:                  Evicted
    Last Transition Time:  2025-04-25T16:10:23Z
```

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-31T11:26:22Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5129#issuecomment-3139559062):

>It is now tracked here: https://github.com/kubernetes-sigs/kueue/issues/6323
>/close
>
>Let me close this one as it specifically mentions the state which should be not possible after the first fix:
>```
>Status:
>  Admission Checks:
>    Last Transition Time:  2025-04-25T16:06:34Z
>    Message:               Retrying after failure: Max nodepool size reached, affected nodepools: dws-a100-40gb-4x-node-pool
>    Name:                  dws-prov
>    State:                 Retry
>  Conditions:
>    Message:               At least one admission check is false
>    Observed Generation:   1
>    Reason:                AdmissionCheck
>    Status:                True
>    Type:                  Evicted
>    Last Transition Time:  2025-04-25T16:10:23Z
>```


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
