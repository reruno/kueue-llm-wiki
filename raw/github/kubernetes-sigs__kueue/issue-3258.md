# Issue #3258: Add retry mechanism for AdmissionChecks in Kueue

**Summary**: Add retry mechanism for AdmissionChecks in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3258

**Last updated**: 2025-11-17T10:45:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-10-17T15:46:21Z
- **Updated**: 2025-11-17T10:45:40Z
- **Closed**: 2025-11-17T10:45:40Z
- **Labels**: `kind/feature`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Retry mechanism for AdmissionChecks.

**Why is this needed**:
Currently there is no retry mechanism for AdmissionChecks. There is a deprecated field `admissionCheckSpec.retryDelayMinutes` which was never supported and will be remove in API v1beta2. In the AdmissionCheck API there is the `Retry`, however the workload controller evicts the Workload without retrying it. Hence, there is a lot of improvement potential for the retry mechanism.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-15T16:42:09Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-16T10:06:09Z

/remove-lifecycle stale

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-01-23T08:37:05Z

/assign @PBundyra  is this issue still opened ?

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-01-23T12:58:22Z

@PBundyra  can you specify in `AdmissionCheck` API  where is  `Retry` ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T13:58:57Z

`Retry` is one of the [states](https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/apis/kueue/v1beta1/admissioncheck_types.go#L26-L30) an AdmissionCheck could be in.

We set in some scenarios, such as ProvisioningRequest Retry (see [here](https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/pkg/controller/admissionchecks/provisioning/controller.go#L552). However, currently the retry mechanism is coupled to ProvisioningRequest. It means if there are some external ACs they need to retry on their own. 

The issue will require designing the API for a generic mechanism for retrying an AC. However, I believe the issue was created as one of the alternatives to retry ProvisioningRequests (see [Support for configurable ProvisioningRequest retries](https://github.com/kubernetes-sigs/kueue/issues/1353)). In other words: the actual business need of being able to retry ProvisioningRequests had these two competing approaches. Since we started to support retries at the ProvisioningRequest-level I think the relative priority of this issue has decreased. 

While still the mechanism could be useful for other AdmissionChecks, I would like to hear first in the community how much of a need there remains, before investing time into development and reviews.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2025-02-10T23:55:08Z

> `Retry` is one of the [states](https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/apis/kueue/v1beta1/admissioncheck_types.go#L26-L30) an AdmissionCheck could be in.
> 
> We set in some scenarios, such as ProvisioningRequest Retry (see [here](https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/pkg/controller/admissionchecks/provisioning/controller.go#L552). However, currently the retry mechanism is coupled to ProvisioningRequest. It means if there are some external ACs they need to retry on their own.
> 
> The issue will require designing the API for a generic mechanism for retrying an AC. However, I believe the issue was created as one of the alternatives to retry ProvisioningRequests (see [Support for configurable ProvisioningRequest retries](https://github.com/kubernetes-sigs/kueue/issues/1353)). In other words: the actual business need of being able to retry ProvisioningRequests had these two competing approaches. Since we started to support retries at the ProvisioningRequest-level I think the relative priority of this issue has decreased.
> 
> While still the mechanism could be useful for other AdmissionChecks, I would like to hear first in the community how much of a need there remains, before investing time into development and reviews.

Hi @mimowo , thanks for documenting this. Retry serves an important role for external admission check to work properly. Imho, the fact it only works with internal provision requests would limit Kueue's applicabilty.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T07:36:53Z

> the fact it only works with internal provision requests would limit Kueue's applicabilty.

Right, thanks for emphasizing the need for the feature to support external AdmissionChecks. I believe the retry delay still could be hacked as in ProvisioningRequest AdmissionCheck, but I'm aware it means duplicating and maintaining complex code. 

cc @mwielgus @mwysokin

### Comment by [@dhenkel92](https://github.com/dhenkel92) — 2025-04-02T19:54:11Z

We are currently in the process of introducing Kueue to our infrastructure. One reason why we picked it is the ability to run custom admission checks to have more control over whether a workload can/should be run in a cluster or not.

For example: We've created a check that detects if the Kubernetes control-plane of that cluster is overloaded. In this case, the workload should be delayed until the control-plane is healthy again.

Unfortunately, without retries, Kueue will constantly reconcile the workload, which does not help the control-plane recover.
Right now, we've built a workaround for the missing capability by misusing the `.status.requeueState` in our admission checks.
However, this is not maintainable, so it would be great to have a proper solution long term.

In case you have higher priorities, we would love to help.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-02T20:03:19Z

cc @mwielgus 

yes, I fully understand support for retries is required when you use external ACs, and this is also hacked in the ProvReq controller.

Regarding the priorities - yes it does not seem to be top priority now as we have fixed ProvReq, but we would welcome a contribution.

I think we will need some API for that, so we need KEP. One question is how to merry the retries at the AC level with the retries at the ProvReq level (or other controllers).

### Comment by [@dhenkel92](https://github.com/dhenkel92) — 2025-04-03T21:05:03Z

Sounds great. 

> I think we will need some API for that, so we need KEP. One question is how to merry the retries at the AC level with the retries at the ProvReq level (or other controllers).

We'll start a KEP and can discuss further there. Is there anything else you think we should take into consideration?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-04T07:46:29Z

Not at the moment, maybe @PBundyra has some suggestions.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-09T09:25:14Z

Hi @dhenkel92, thanks for the follow-up on this. You may also take a look on that slack thread https://kubernetes.slack.com/archives/C032ZE66A2X/p1729787805510569
I believe one of your colleague also tried a similar issue so maybe he could also give some piecie of advice

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-08T10:21:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T10:50:45Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-06T11:42:22Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T11:49:42Z

/remove-lifecycle stale
