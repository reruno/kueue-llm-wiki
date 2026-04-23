# Issue #6966: Job stuck on "invalid patch" while being preempted (in unclucky cases involving Admission Checks & "round" RAM requests)

**Summary**: Job stuck on "invalid patch" while being preempted (in unclucky cases involving Admission Checks & "round" RAM requests)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6966

**Last updated**: 2025-11-06T08:08:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-09-23T14:10:19Z
- **Updated**: 2025-11-06T08:08:53Z
- **Closed**: 2025-11-06T08:08:53Z
- **Labels**: `kind/bug`
- **Assignees**: [@brejman](https://github.com/brejman)
- **Comments**: 12

## Description

**Reproduction steps**:

1. (Optional) Modify the config of `kueue-controller-manager`: set `spec.container.args.--zap-log-level` to 10. \
   (This is just to have more logs available)

2. Use [this config](https://pastebin.com/9PzLqqc1) - basically 1 ClusterQueue with the following setup:

   | Flavor name | CPU quota | RAM quota | AdmissionCheck |
   |-------------|-----------|-----------|----------------|
   | `flavor-ac` | 0.75      | 5G        | `sample-prov`  |
   | `flavor-2`  | 0.5       | 5G        | -              |

   The two flavors are attached to disjoint sets of nodes (using node labels). \
   The nodes are large enough to fit the Jobs specified below, with a safe margin. \
   (The AC is technically there but no action from the autoscaler is actually needed - the node pool is already large enough).

3. Create, in order, the following 2 Jobs:

   | Config                                | Job name             | CPU request | RAM request | Priority |
   |---------------------------------------|----------------------|-------------|-------------|----------|
   | [YAML](https://pastebin.com/EHVZXiZN) | sample-job-1-_xxxxx_ | 0.5         | 220M        | -        |
   | [YAML](https://pastebin.com/j1Wr4CUv) | sample-job-2-_xxxxx_ | 750m        | 220M        | 1000     |

   After creating Job1, wait for its Pod to be running. Only then create Job2.

**What happened**:

After creating Job1: 
* there's one running Pod, scheduled on the AC flavor.

After creating Job2:
* Kueue assigns Job2 to `flavor-ac`, because `flavor-2` is not large enough.
* Kueue decides to preempt Job1 from `flavor-ac` to give place for Job2.
   
  <img width="1917" height="888" alt="Image" src="https://github.com/user-attachments/assets/d953b22e-993a-4404-a74e-9fef44cdb155" />

* **bug:** Job1 is _stuck on being preempted_. \
  The corresponding Workload remains in the state shown in the above screenshot indefinitely. (For at least 30 minutes).
  Looking at Kueue logs (level=10) reveals an error in patching the new preempted state:

  ```
  \"message\":\"Workload.kueue.x-k8s.io \\\"job-sample-job-1-9qkhm-dfd40\\\" is invalid: [
  status.admission.podSetAssignments: Invalid value: \\\"null\\\": admission.podSetAssignments in body must be of type array: \\\"null\\\",
  status.admission.clusterQueue: Required value, \\u003cnil\\u003e: Invalid value: \\\"null\\\":
  some validation rules were not checked because the object was invalid; correct the existing errors to complete validation
  ]\"
  ```

  (a bit more logs available [here](https://pastebin.com/FziSEY1z))

* As a result, Job1 is never scheduled again. Also, Job2 is never scheduled at all, as it keeps waiting for a successful preemption of Job1:

  <img width="1917" height="888" alt="Image" src="https://github.com/user-attachments/assets/ce30c547-474d-4e35-93b5-05f104692b52" />

   So, from the user's perspective, these 2 Jobs land in a **deadlock** state.

**What you expected to happen**:

Expected outcome:

* No errors thrown by the "preempting patch" for Job1.
* Job1 successfully preempted and then re-admitted on `flavor-2` (where it fits).
* Job2 successfully running on `flavor-ac`.

**Anything else we need to know?**:

* I'm observing this deterministically - but only in rare unlucky cases (see below).
* The expected outcome does indeed happen if we are more lucky - for example, if we do _either_ of the following:
  * detach the `AdmissionCheckStrategy` from `flavor-ac`, or
  * remove RAM request from Job1, or
  * change RAM request of Job1 from `220M` to `220Mi` (!)
* I have created an integration test (available [here](https://github.com/olekzabl/kueue/blob/38eef366ed6a3e6b64b08ab8c9800abc20d5cca3/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1848-L1977), to be soon turned into a PR) which reproduces this issue, and documents a long list of cases when it does / does not happen.
  For now, the **apparent trigger** is that: 

  * `flavor-ac` uses the Admission Check, and 
  * Job1 requests RAM, and 
  * the raw byte count of its RAM request is divisible by 1000, but not equal to 1000, and not divisible by 128 000.

  (Yes, I know it sounds unbelievably weird - but please look at the test cases - they just tell it).

**Environment**:
- Kubernetes version (use `kubectl version`):
  - Client Version: v1.33.4-dispatcher
  - Kustomize Version: v5.6.0
  - Server Version: v1.33.4-gke.1134000
- Kueue version (use `git describe --tags --dirty --always`): \
  Git N/A, I used the 0.13.4 release:
  ```
  kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.13.4/manifests.yaml
  ```
- Cloud provider or hardware configuration: \
  GKE, and specifically:
  - cluster version = nodes version = 1.33.4-gke.1134000
  - node image type = `cos_containerd`
  - `flavor-ac` based on 4 nodes of type `e2-standard-2`, with GKE autoscaler set to "4-6 nodes"
  - `flavor-2` based on 2 nodes of type `n2-standard-2`
- OS (e.g: `cat /etc/os-release`): _[unable to find out right now]_
- Kernel (e.g. `uname -a`): _[unable to find out right now]_
- Install tools:
- Others:

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-23T23:12:21Z

A few more insights on this:

1. Looking at [logs](https://pastebin.com/FziSEY1z), the error occurs just after the log `The job is no longer active`, emitted from here:

   https://github.com/kubernetes-sigs/kueue/blob/0dca4d3eafa7ea691b10c9a38727936b703dae04/pkg/controller/jobframework/reconciler.go#L536-L541

   In this snippet, the following important things happen:
   * Inside `UnsetQuotaReservationWithCondition`, we [clear](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/pkg/workload/workload.go#L566) Workload's `.Status.Admission`.
   * Then, inside `ApplyAdmissionStatus`, we [send a patch](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/pkg/workload/workload.go#L855) to update the Workload accordingly.
   * ... And it is that patch that fails (the error message being labeled as emitted from [here](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/sigs.k8s.io/controller-runtime/pkg/client/typed_client.go#L277)).

2. The error message complains about:

   * `status.admission.podSetAssignments` equal to `null`, while an array was expected; \
     (this part of message apparently generated [here](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/kube-openapi/pkg/validation/errors/schema.go#L25), and then, it'd be necessarily called from [here](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/kube-openapi/pkg/validation/errors/schema.go#L231), suggesting that the `null` value was interpreted as a string, `n`, `u`, `l`, `l`);
   * `status.admission.clusterQueue` equal to `null` \
     (and for this part, I can't even find - at least within the Kueue repo incl. `/vendor/...` - where it may come from).

   This is surprising in several ways:

   * A. The patch request (as seen in [this log](https://pastebin.com/hGLb3hUC)) does _not mention_ `status.admission` at all. \
     (Quite rightly so, given that Kueue code has just set this whole field to `nil`). \
     Given that, it's surprising that the validation sees any non-trivial content (like a string `n`, `u`, `l`, `l`) at the level of _sub-fields_ of that field.

     This suggests that the request body was _not_ parsed from how we see it - but that there was some middle transforming layer (call it "Null Inserter") before it was ultimately handled.

   * B. The [request log](https://pastebin.com/hGLb3hUC) seems emitted from [here](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/client-go/rest/request.go#L1296), i.e. so deeply inside `.Patch()` that the execution has already left proper Kueue code and entered the `/vendor/...` area.

      Therefore, the Null Inserter seems to be external to the proper Kueue codebase.

   * C. Now, bring into account that the External Null Inserter activates only when the requested RAM bytes are divisible by 1000. \
     (Because otherwise the validation error does not occur; I checked it in the logs). \
     Then - what makes code external to Kueue codebase react to specific value of RAM requested bytes, which is **not present** in the patch request (again, see the [request log](https://pastebin.com/hGLb3hUC))??

      (Wild guess: does the External Null Inserter transform the patch request based also on the full current state of the K8s resource, not just on the patch request content?)

3. I tried to debug this with a Go debugger (specifically, Delve attached to VSCode), used for the "stuck" scenarios in my [integration test](https://github.com/olekzabl/kueue/blob/38eef366ed6a3e6b64b08ab8c9800abc20d5cca3/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1848-L1977). \
   This _worked partially_, in that I could _rather confirm_ that the error is indeed thrown inside [this line](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/sigs.k8s.io/controller-runtime/pkg/client/typed_client.go#L277) after the abovementioned journey from [this block](https://github.com/kubernetes-sigs/kueue/blob/0dca4d3eafa7ea691b10c9a38727936b703dae04/pkg/controller/jobframework/reconciler.go#L536-L541), and the request body is indeed logged from [here](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/client-go/rest/request.go#L1296).

   However, I failed to get a deeper understanding, due to the following obstacles:

   * A. Even though [this line](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/kube-openapi/pkg/validation/errors/schema.go#L25) looks like the only place in the Kueue repo which could generate the observe error message, I failed to observe this "in action":
     * After manually changing the format string and re-running the test, logs still contained the old one.
     * Trying to hook around [the only usage](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/kube-openapi/pkg/validation/errors/schema.go#L231) of that const, Delve refused to insert a breakpoint anywhere there:

       <img width="917" height="336" alt="Image" src="https://github.com/user-attachments/assets/3a09627c-0694-444e-b599-a7bced213bc0" />

   * B. AFAIU the Patch request is ultimately sent over HTTP - even in integration tests, though in that setup to localhost. \
     At least, after logging as much as I could from the request, I got this:
     ```
     Method:PATCH
     URL:https://127.0.0.1:45751/apis/kueue.x-k8s.io/v1beta1/namespaces/provisioning-2blj2/workloads/job-job1-d95cf/status?fieldManager=kueue-admission&force=true
     Proto:HTTP/1.1
     ```
     Then, to debug the handler of that request, I'd need to understand this quasi-fake local-HTTP setup - where is it defined, how to attach a debugger to the handler process / goroutine. So far, I'm stuck on that. \
     (Any **help** in this will be welcome!)

   * C. Even before the "HTTP barrier" where I could insert breakpoints, I observed non-deterministic response statuses. (Either of 200, 404, 422). \
     Not sure why. My rough idea is that deeper layers of the K8s client are called so often, and so concurrently, that the debugger just somehow gets "derailed" when inspecting these. (Or maybe real time passing is also a factor?)

   * D. My attempts to track "how the request body evolves through code layers" failed in 2 ways:

      * Inside the IDE, I've not found a way to see more than 100 initial characters. \
         (In particular, any watches like `string(Body)[100:200]` were refused as unsupported)

      * Extensive logging led the whole test to crash early, on sth like "too many open files".

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-24T12:33:45Z

/cc

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-24T21:55:58Z

@PBundyra has asked (in issue #5477 where discussing this originally started):

> Hi [@olekzabl](https://github.com/olekzabl), thanks for the tremendous work. Do you have any findings on why removing AdmissionChecks from the scenario seems to remove the error? I think this is crucial to find out what are the next steps

No, I don't have any findings on that.

Also, I'm not sure if _this_ question is _crucial_. \
Given all my observations (the weird dependence on RAM byte counts, also the root cause apparently lying at least partially outside the Kueue code), it seems that this bug is caused (or co-caused?) by _something_ which doesn't even know what an "admission check" is. \
So, the correlation with "AC / no AC" may be not crucial, or even just accidental.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-25T15:14:18Z

Update: the integration test has been sent out for review (as #7010 ).

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-02T07:56:53Z

Update: I verified that the `localhost:xxxxx` recipient of the rejected HTTP request (in the integration test) is a `kube-apiserver` process which is created while running the test.

However, even when knowing the PID of that process, I failed to attach a Delve debugger to it. Here is what happened:
```
$ dlv attach 827248
Could not attach to pid 827248: this could be caused by a kernel security setting, try writing "0" to /proc/sys/kernel/yama/ptrace_scope
$ sudo echo 0 > /proc/sys/kernel/yama/ptrace_scope
bash: /proc/sys/kernel/yama/ptrace_scope: Permission denied
$ sudo ls -l /proc/sys/kernel/yama/ptrace_scope
-rw-r--r-- 1 root root 0 Sep 26 13:15 /proc/sys/kernel/yama/ptrace_scope
```
So, to unblock, I'd need to write `0` to a file... which I'm not permitted to do (as root), despite having write permission 🫢 

~Any hints how to progress will be welcome.~

EDIT: Found a permitted way: `echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope`. \
(So now I understand `sudo x > y` doesn't cover the `> y` part)

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-02T09:36:57Z

I succeeded in running "Attach [Delve debugger] To Process" from VSCode. \
However, Delve complained about `kube-apiserver` not having debug info. \
Putting a breakpoint [here](https://github.com/kubernetes-sigs/kueue/blob/0db6cefdd39e6e3f07046b254367eb07d0e9ec7c/vendor/k8s.io/kube-openapi/pkg/validation/errors/schema.go#L226) still did not succeed.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-03T09:00:22Z

Wow @olekzabl! I think this one of the best and most thorough analysis made for a bug I've seen in my life. Kudos! ❤️

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T16:46:35Z

/reopen
This continues to be an issue, the scope of the merged PR was narrowed down actually.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-03T16:46:41Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6966#issuecomment-3366419630):

>/reopen
>This continues to be an issue, the scope of the merged PR was narrowed down actually.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T08:15:14Z

@olekzabl it seems the issue might be somewhere in how SSA is handled, because when I enable WorkloadRequestUseMergePatch then your integration tests pass. It is also known that SSA has some issues setting fields to nil, eg. https://github.com/kubernetes-sigs/kueue/issues/6185.

As an idea to deepen the investigation I would like to consider isolating the scenario by: 
1. install Kueue on a cluster, but disable the kueue-manager and its webhooks
2. create the workload with  `kubectl --server-side apply` request setting up the nested `status.admission`
3. send  `kubectl --server-side apply` setting `status.admission = nil`

If we can repro this way it would enable folks working in the upsteam k8s to debug much easier.

wdyt?

### Comment by [@brejman](https://github.com/brejman) — 2025-10-21T14:51:12Z

/assign

### Comment by [@brejman](https://github.com/brejman) — 2025-10-24T10:48:50Z

Here are my findings:

1. Modification (non-SSA) of a map entry's field prevents deletion of said map through SSA. This is different compared to regular arrays. It can be a bug on the SSA side
2. The "memory" field (which is a nested field in PodSetAssignments map) ends up being unintentionally modified due to issues with Quantity round-trip when serializing / deserializing JSON. This subsequently prevents deletion of the map as mentioned above.

The round-trip issue is because the quantity is initially using BinarySI format:

https://github.com/kubernetes-sigs/kueue/blob/47c65c70fc0fb2d43cfd6d7911faab319c2d1e75/pkg/resources/requests.go#L110-L111

https://github.com/kubernetes-sigs/kueue/blob/47c65c70fc0fb2d43cfd6d7911faab319c2d1e75/pkg/scheduler/scheduler.go#L618

For example if the value was initially 1G, it ends up being sent to the API as 1000000000 because it doesn't match the binary format.

Then, the controller reconciliation is triggered, which reads the workload and then sends a non-SSA patch with 1G instead of 1000000000 due to the Quantity's JSON deserialization rules, which is treated as modification. Side note: if this request was SSA, it would result in a conflict, and if forced, it wouldn't later block the removal of the field.

https://github.com/kubernetes-sigs/kueue/blob/47c65c70fc0fb2d43cfd6d7911faab319c2d1e75/pkg/controller/core/workload_controller.go#L550-L557

At this point, the internal state of the resource is corrupted and the next SSA request which removes the Admission field fails.

https://github.com/kubernetes-sigs/kueue/blob/47c65c70fc0fb2d43cfd6d7911faab319c2d1e75/pkg/controller/jobframework/reconciler.go#L545-L546
