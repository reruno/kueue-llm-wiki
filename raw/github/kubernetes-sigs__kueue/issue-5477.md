# Issue #5477: Investigate and fix if there is a bug when workload is evicted in CQ using AdmissionCheckStrategy

**Summary**: Investigate and fix if there is a bug when workload is evicted in CQ using AdmissionCheckStrategy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5477

**Last updated**: 2025-10-03T16:47:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-03T13:48:23Z
- **Updated**: 2025-10-03T16:47:48Z
- **Closed**: 2025-10-03T16:47:47Z
- **Labels**: _none_
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 22

## Description

Consider the following setup CQ with two flavors:
1. reservation (no AC)
2. provisioning (using AdmissionCheckStrategy).

Now assume the workload "wl2" is admitted to the provisioning flavor (because reservation was occupied by "wl1").

Then in case of eviction (e.g. preemption) of "wl2" we will set the status of admission checks to Pending https://github.com/kubernetes-sigs/kueue/blob/310626e3a403d92a72ed8e471db53a1255ca0c8b/pkg/scheduler/preemption/preemption.go#L188

However, if "wl1" is finished in the meanwhile, then "wl2" will be requeued and scheduled into the "reservation" flavor. As a result it will be admitted to flavor without AC, but with admissionChecks state as Pending.

**Note**: this is just thought experiment I ran over with @PBundyra , and we both think it is "real".

Part of the task is to repro the scenario on a real cluster on in integration tests. If this is confirmed, then probably the best way of fixing is to reset the entire `status.admissionChecks` on eviction. To be determined.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T13:50:17Z

This might be affecting in particular users using the setup for TAS as fixed in https://github.com/kubernetes-sigs/kueue/pull/5426.

However, the issue seems to be outside of TAS scope, and more related to AdmissionCheckStrategy

cc @mbobrovskyi @PBundyra

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-03T14:38:06Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-01T14:41:34Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-02T12:33:41Z

/remove-lifecycle stale

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-09T10:54:38Z

@mbobrovskyi Are you (or have you been) working on this? Would it be fine for you if I took it?

(I'm in a group onboarding into Kueue, and we got a list of "suitable starting tasks", including this one on the condition that it's ok for you to hand it over - that's why I'm asking).

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-09T11:28:50Z

Yes, please, take a look at it.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-09T11:29:13Z

/unassign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-09T13:59:09Z

Thank you!
/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-18T11:30:52Z

Status update:

I'm exploring this, and tried to reproduce this scenario both "in real" and in integration tests.
Initial findings:

1.  Running an integration test (a new one which I wrote for this purpose), the problem seems already addressed here:
    https://github.com/kubernetes-sigs/kueue/blob/cb56759cb451386e5f26afae1b0e541b7f63c3b9/pkg/controller/core/workload_controller.go#L332
    Inside this call, `AdmissionChecks` are reset whenever the workload has empty `Admission`, unless AdmissionChecks cover all flavors in the ClusterQueue:
   https://github.com/kubernetes-sigs/kueue/blob/cb56759cb451386e5f26afae1b0e541b7f63c3b9/pkg/workload/workload.go#L1065-L1075
    This code is executed _noticeably after_ `ResetChecksOnEviction` - e.g. in my integration test the workload had its `AdmissionCheck` in the `Pending` state for around 5 scheduling cycles.
    Still, `AdmissionChecks` became cleared before re-admitting the Workload.

    So I'm not sure if this behavior diverges from what's intended. @mimowo @PBundyra WDYT?

    Regardless of whether it works as intended, I can polish my integration test and send a PR with it, if it's of any value. (Opinions?)

2.  I also tried to reproduce this on real cluster - but so far I observed the workload to be _stuck while becoming preempted_.
    (I'm planning to experiment a bit more to see if it's a real bug or some misconfiguration on my side - if the former, I'll report it as a separate issue).

    The deepest cause I could observe so far is the following error thrown by the Job Controller (emitted from [here](https://github.com/kubernetes-sigs/kueue/blob/3fc7927d3d7f3a746f34b075e5ec8a343c209220/vendor/sigs.k8s.io/controller-runtime/pkg/client/typed_client.go#L277)):
    ```
    \"Workload.kueue.x-k8s.io \\\"job-sample-job-11-79-5gzv2-a5bcc\\\" is invalid:
    [status.admission.podSetAssignments: Invalid value: \\\"null\\\": admission.podSetAssignments in body must be of type array: \\\"null\\\",
    status.admission.clusterQueue: Required value, \\u003cnil\\u003e: Invalid value: \\\"null\\\": some validation rules were not checked because the object was invalid; correct the existing errors to complete validation
    ]\"
    ```
    which is surprising to me because - as far as I could track Kueue code - it just sets `nil`, not `"null"`.
    (Could some intermediate library translate one to the other?)

    I can't imagine how a YAML misconfiguration on my side could lead to an error happening so deep down the stack.
    OTOH I so far failed to reproduce this in integration tests. Will keep investigating.

    I'm mentioning this here in case someone could know right away what this may be about.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-19T22:27:46Z

Updates on the issue described in point 2 in my previous comment:

- I reproduced this in integration tests. ([Here](https://github.com/olekzabl/kueue/blob/c1da99a2fd52777e2bd4323eeecdef2156ec83b5/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1498) is an unpolished branch with this).
- The triggering factor for this error to occur seems to be that:

  - The main job under concern (being evicted from AC flavor to a non-AC flavor) specifies a memory request, and...
  - ... that memory request uses **decimal unit prefixes** (`k`, `M` or `G`) and not binary ones (`Ki`, `Mi` or `Gi`).
 
  (I know it may sound strange - but it really looks like this. FTR [here](https://github.com/olekzabl/kueue/blob/c1da99a2fd52777e2bd4323eeecdef2156ec83b5/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1733-L1753) is the current set of my test cases).
- My "real life" observations aren't that rich but are consistent with that. \
  In particular, I have 2 setups which differ _only_ in replacing `M` with `Mi` in requests (with no influence on actual fitting inside limits; I left some buffer there), where `M` suffers from the above error while `Mi` works as intended.

- I still have no idea what's the root cause. \
  (For the good, integration test repro allowed me to play with Go debugger - but no success yet).

- Not sure if it has _anything to do_ with AdmissionChecks.
  (It's not that simple that "`M`-suffixed requests are _always_ mishandled"; jobs of that sort sometimes get scheduled well. \
  But it could be e.g. about preempting them, regardless of the preemption reason. \
  I'm planning to explore this).

At this point, it seems like an issue with Kueue (unless it can be attributed to some "deeper" K8s component).
So I am planning to file it separately - though first I'd like to try to better identify the "minimal repro scenario".

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-22T09:42:33Z

Quick update on the observed validation error:

- It seems _somehow_ related to AdmissionChecks - at least, when I remove `admissionChecksStrategy` from the ClusterQueue, things start working correctly.
- Apparently, it is **not** about decimal vs. binary prefix.
  Rather, about the raw number of memory bytes requested. \
  The _basic_ rule is "error if bytes **divisible** by 1000" - however, there are **exceptions** (AFAICS, 1000 itself and multiplicities of 128 000 bytes - feels quite weird, doesn't it? :)
- My attempts to debug this with a Go debugger have failed.

My next planned steps:
- Gather more reproducible examples of when the error does / does not happen. (Current set is [here](https://github.com/olekzabl/kueue/blob/6ed0a0726e5fa1bba553c8976dc523c2f80790e4/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1771-L1860)). \
  In particular, check if it's specific to memory, or maybe reproducible with "2000 CPU" or "2000 mCPU" etc.
- Do _not_ attempt to debug this any further.
- File a new issue describing what I know, and what are the obstacles in debugging this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-22T11:01:22Z

@olekzabl thank you for investigating the issue wrt the error handling of ACs. 

I think your integration test is "on track" of reproducing the issue. Feel free to open a PR, even if this works fine, then merging the test if worth it. We could also see where it fails exactly.

From the investigation points you raised:
1. I really don't think it is about the `CPU` vs `mCPU` , or memory. I think these are likely some distractions which prevent the test from playing well if not setup properly. Inducing priotity-based preemption is sometimes tricky.
2. IIUC the the implemenation, the test is currently expected to fail on ["await for the Workload to be Admitted on the Non-AC flavor"](https://github.com/olekzabl/kueue/blob/c1da99a2fd52777e2bd4323eeecdef2156ec83b5/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1705-L1731) or ["await for the Workload to have AdmissionCheck status cleared"](https://github.com/olekzabl/kueue/blob/c1da99a2fd52777e2bd4323eeecdef2156ec83b5/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1726C14-L1731). If it fails on the latter, then it is not "too bad", because it gets admitted from the user perspective, but probably it would not work well if we had two AC flavors (each flavor using another AC). In that case we may need to pivot the issue scope / description.

cc @PBundyra who is also pretty familiar with ACs

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-22T12:36:16Z

Thank you for your reponse. Some comments:

> I really don't think it is about the `CPU` vs `mCPU` , or memory. I think these are likely some distractions which prevent the test from playing well if not setup properly. Inducing priotity-based preemption is sometimes tricky.

Please keep in mind that I also reproduced the same validation error (`Job is invalid`) on a _real cluster_, multiple times. \
I wrote the integration test only to have the reproduction easier, "codified", and (hopefully) debuggable. \
But the test mimics reality - so I don't think it's just an issue with the test setup.

In a new issue, I'll document the "real life" repro steps as well.

> IIUC the the implemenation, the test is currently expected to fail on ["await for the Workload to be Admitted on the Non-AC flavor"](https://github.com/olekzabl/kueue/blob/c1da99a2fd52777e2bd4323eeecdef2156ec83b5/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1705-L1731) or ["await for the Workload to have AdmissionCheck status cleared"](https://github.com/olekzabl/kueue/blob/c1da99a2fd52777e2bd4323eeecdef2156ec83b5/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1726C14-L1731). If it fails on the latter, then it is not "too bad", because it gets admitted from the user perspective.

No, it fails _even earlier_ than the former.

Today, I updated my branch with specific checks "where it fails if it does", and it's now evident that we have failures in all these points:
* [await wl2 to have QuotaReserved](https://github.com/olekzabl/kueue/blob/6ed0a0726e5fa1bba553c8976dc523c2f80790e4/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1713-L1717)
* [await for the Workload to be Admitted on the Non-AC flavor](https://github.com/olekzabl/kueue/blob/6ed0a0726e5fa1bba553c8976dc523c2f80790e4/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1739-L1743)
* [await for the Workload to have AdmissionCheck status cleared](https://github.com/olekzabl/kueue/blob/6ed0a0726e5fa1bba553c8976dc523c2f80790e4/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1751-L1755)

In other words, from the user's perspective, it's a **deadlock** - wl2 never gets scheduled, and wl1 has its original Pods killed but the new Pods also never get scheduled on the new flavor. \
And that is also what I observed on a real cluster.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-22T15:37:53Z

An improved collection of test cases: [link](https://github.com/olekzabl/kueue/blob/38eef366ed6a3e6b64b08ab8c9800abc20d5cca3/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1848-L1977).

CPU seems to have no role. (Only memory matters so far).
Detaching AdmissionChecks from the scenario seems to remove the error.

Next step: file a new issue, documenting this test, real repro steps, and where I ended up debugging.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-23T10:28:03Z

Hi @olekzabl, thanks for the tremendous work. Do you have any findings on why removing AdmissionChecks from the scenario seems to remove the error? I think this is crucial to find out what are the next steps

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-24T21:56:26Z

The "spin-off" issue (validation error) discussed in a few comments above has been reported separately, as issue #6966.
I propose to continue all discussions on it there (it already has more context).

(In particular, @PBundyra I'm assuming your question just above is about this, so I [replied](https://github.com/kubernetes-sigs/kueue/issues/6966#issuecomment-3330837643) to it there).

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-24T22:40:03Z

Coming back to the original topic of this issue:

_When a workload is evicted from flavor X (covered by an AC) and admitted into another flavor Y (not covered by that AC) - will its original AC status remain "Pending"? Can this be problematic?_

My answer is that:

* Yes, the status of the original AC will be set to `Pending`, but **only temporarily**. \
  The original AC will be then removed from workload's status by the Workload Controller.

* I observed this on real cluster, having checked 2 cases:
 
  * when Flavor Y is covered by _another_ AC;
  * when Flavor Y is not covered by _any_ AC.

  In both cases, the final outcome was as expected:

  * workload got successfully admitted to Flavor Y;
  * there was no mention of the original AC in its status.

* I also wrote an integration test (viewable [here](https://github.com/olekzabl/kueue/blob/00e211b0379d00639f3131cf12888c622ea967a2/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L1946-L1949), soon to become a PR) verifying this outcome in both considered cases.

* FTR, down-to-the-code explanation why (I think) it works this way:

  The starting point is this line of the `Reconcile` method of Workload Controller:

  https://github.com/kubernetes-sigs/kueue/blob/cb56759cb451386e5f26afae1b0e541b7f63c3b9/pkg/controller/core/workload_controller.go#L332

  which inside does this:

  https://github.com/kubernetes-sigs/kueue/blob/cb56759cb451386e5f26afae1b0e541b7f63c3b9/pkg/controller/core/workload_controller.go#L489-L493

  where the first function call starts with this:

  https://github.com/kubernetes-sigs/kueue/blob/19ebce0290ff2b1b7fa149c82037ca180ff93cdf/pkg/workload/workload.go#L1073-L1093

  In our case, `allFlavors` will be false (because the AC on flavor X does not cover all flavors, and that's enough). \
  As a result, we won't `return` in line 1084, and hence we'll `return nil` in line 1092 as soon as workload's `Admission` has been cleared (i.e. once it has been successfully preempted, reconciled etc.)

  Then, unless `.Status.AdmissionChecks` have been already cleared, the next function

  https://github.com/kubernetes-sigs/kueue/blob/cb56759cb451386e5f26afae1b0e541b7f63c3b9/pkg/controller/core/workload_controller.go#L599-L602

  will return `nil, true`. 
  This means we'll enter the `if` in line 491 and clear `Status.AdmissionChecks` in line 493.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-24T22:51:36Z

Summing up - the _ultimate outcome_ is as intended, but an inconsistent state may exist _temporarily_. \
I don't have a good understanding how bad that could be.

The action originally suggested by @mimowo 

> probably the best way of fixing is to reset the entire status.admissionChecks on eviction

may be still worth doing - though here I don't know how much we could lose by doing it. (A slight performance loss?)

FTR, from a conversation with @mimowo and @PBundyra I understood that, once my integration test is approved & merged, this issue will become "closeable, or at least treatable with a lower priority".

So my next step is to send the integration test PR. \
(And then, I may need advice on how to further handle this ticket).

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-25T08:52:14Z

Thank you @olekzabl, this is an excellent investigation and the analysis here: https://github.com/kubernetes-sigs/kueue/issues/5477#issuecomment-3330929574 makes perfect sense to me

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-25T15:13:56Z

Update: the integration test has been sent out for review (as #7010 ).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T16:47:42Z

/close
This can be already close as the PR with the test is merged. It turned out all good but uncovered another related problem https://github.com/kubernetes-sigs/kueue/issues/6966

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-03T16:47:48Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5477#issuecomment-3366423001):

>/close
>This can be already close as the PR with the test is merged. It turned out all good but uncovered another related problem https://github.com/kubernetes-sigs/kueue/issues/6966 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
