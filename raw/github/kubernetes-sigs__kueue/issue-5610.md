# Issue #5610: Guard Visibility APIService with VisibilityOnDemand feature gate

**Summary**: Guard Visibility APIService with VisibilityOnDemand feature gate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5610

**Last updated**: 2026-01-22T18:40:37Z

---

## Metadata

- **State**: open
- **Author**: [@xiongzubiao](https://github.com/xiongzubiao)
- **Created**: 2025-06-10T17:11:49Z
- **Updated**: 2026-01-22T18:40:37Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The Visibility APIService and its related objects should not be created when the VisibilityOnDemand feature gate is disabled.

**Why is this needed**:

It causes problems like https://github.com/kubernetes-sigs/kueue/issues/3943. Although it is documented:
```
If you disable the feature, you also need to remove the associated APIService from your cluster by doing kubectl delete APIService v1beta1.visibility.kueue.x-k8s.io.
```
It is more graceful to not ask user to manually remove it.

**Completion requirements**:

The Visibility APIService and its related objects are not created when the VisibilityOnDemand feature gate is disabled.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-10T18:55:04Z

Good idea! Though the implementation of this is tricky with our current setup..

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-06-19T14:07:02Z

I found that the guard existed before https://github.com/kubernetes-sigs/kueue/pull/3084. The guard removal is a side effect of enabling visibility be default.

I am not sure how to implement the guard for the manifest installation. But for the helm installation, I think the guard should be kept.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T06:35:47Z

> I am not sure how to implement the guard for the manifest installation. But for the helm installation, I think the guard should be kept.

Yes, I don't think this is possible for manifests, but for Helm it makes perfect sense to keep the guard to allow not installing it. 

Do you have any use-case for not installing VisibilityOnDemand? If so, I would be happy to support that change.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T07:05:08Z

> > I am not sure how to implement the guard for the manifest installation. But for the helm installation, I think the guard should be kept.
> 
> Yes, I don't think this is possible for manifests, but for Helm it makes perfect sense to keep the guard to allow not installing it.
> 
> Do you have any use-case for not installing VisibilityOnDemand? If so, I would be happy to support that change.

I am with @mimowo opinion. For kustomize users, they can easily exclude the VisibilityOndemand relarated manifests by kustomize delete patch. For Helm users, we might want to provide an exclusion way.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-06-23T16:08:34Z

> Do you have any use-case for not installing VisibilityOnDemand? If so, I would be happy to support that change.

Yes, in my company Kueue is used as a middleware. The model presented to the end user is a simplified version of Kueue with some customization. So we prefer not enabling the VisibilityOnDemand feature, because it exposes internal constructs. We might end up with another API that is customized with our user-facing models and terminologies.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-23T16:17:29Z

> Do you have any use-case for not installing VisibilityOnDemand? If so, I would be happy to support that change.

We also disable this feature in our environments.

There are two reasons for us:

- APIService causes some contention with our own apiserver so there are concerns how to enable this safely.
- Secure ways to enable APIService. AFAIK it is using an Insecure settings which is a security risk for us.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T16:22:02Z

Interesting, so there are two things
1. I understand why you dont't want to expose the visibility API to end users, but can't you just ignore it or prohibit by RBAC?
2. If there are good reasons to disable it (other than bugs) then we need another mechanism for disabling than feature gate, because feature gates are only temporary by design when they get graduated to GA

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-23T16:44:58Z

> I understand why you dont't want to expose the visibility API to end users, but can't you just ignore it or prohibit by RBAC?

Our issue is the deployment of the APIService in some environments is not allowed. Specially if the control plane is managed. We don't want user workloads interfering with priority of APIServer requests at all.

Also: https://github.com/kubernetes-sigs/kueue/issues/4433

The lack of time to investigate proper handling of Auth was the reason why we disabled it at first.

I agree. I think a proper configuration that disables this without relying on feature gate is important.

Config Knob:
- Controls deploying APIService, service, and visbility metrics.
- Controls starting the controller

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-21T17:25:49Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T13:14:19Z

/remove-lifecycle stale

It looks like this is still valid enhancement request.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T13:44:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-21T14:33:34Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T15:54:13Z

/remove-lifecycle rotten

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-21T16:05:13Z

TBH with https://github.com/kubernetes-sigs/kueue/issues/4433 implemented we have no reason to disable this anymore.

@xiongzubiao could you check if you still need to disable this feature?

Ideally we can enhance this so that it is useful for your use case.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2026-01-22T18:40:37Z




> TBH with [#4433](https://github.com/kubernetes-sigs/kueue/issues/4433) implemented we have no reason to disable this anymore.
> 
> [@xiongzubiao](https://github.com/xiongzubiao) could you check if you still need to disable this feature?
> 
> Ideally we can enhance this so that it is useful for your use case.

Yes we are still disabling VisibilityOnDemand feature gate because of the reason I described at https://github.com/kubernetes-sigs/kueue/issues/5610#issuecomment-2997072220.
