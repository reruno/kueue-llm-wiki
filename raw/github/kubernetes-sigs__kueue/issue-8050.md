# Issue #8050: Enable pod-based integrations  (LWS in particular) by default

**Summary**: Enable pod-based integrations  (LWS in particular) by default

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8050

**Last updated**: 2025-12-05T16:16:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-03T07:42:05Z
- **Updated**: 2025-12-05T16:16:57Z
- **Closed**: 2025-12-05T16:16:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to enable in the configMap all pod-based integrations by default: https://github.com/kubernetes-sigs/kueue/blob/ee02f0f736db312875aaffd2bc911806a94e72dc/charts/kueue/values.yaml#L155-L158

I think historically we disabled all pod-based integrations for two reasons:
1. performance - they require registering a pod controller which needs to process events for all pods, which could be costly
2. maturity - they were added late, and we wanted to have some grace period for testing.

(1.) does not introduce that much of a difference since Kueue already enables Pod-based controller by default for TopologyAwareScheduling. So, enabling another does not seem to make a qualitative difference here. Users who are very performance-sensitive and don't want the extra controllers can disable them.

(2.) The pod based integrations, LWS in particular are already for a number of releases. We also know from users that the pod integration is already used a lot.

So I think it makes sense to make it easier for the users. 

**Why is this needed**:

To make the integration with LWS simpler, allowing to skip this step: https://github.com/kubernetes-sigs/lws/pull/682/files#diff-a2888ec0ab9c7aad3645255fa0c6879981c524939a7036bee9f881aa18e44bedR33-R48

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-03T07:43:07Z

cc @tenzen-y @j-skiba  @amy @kannon92 @mwielgus 

Let me know if there are any concerns here?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T17:35:14Z

I know that @varshaprasad96 and @dgrove-oss ran into a lot of problems enabling pod integration by default.

A lot of the reasoning behind things like ManagedJobsNamespaceSelector and labeling namespaces was the only path we found to sanely enabling this without breaking system services.

If we make pod based integrations default we should include these kind of options also.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T17:36:45Z

cc @PannagaRao @sohankunkerkar @MaysaMacedo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-03T17:44:18Z

Indeed I think the enabling of pod integrations was tricky before we introduced manageJobsNamespaceSelector, because the selector for pods was different than for other Jobs. With the standardized selector I'm not seeing any gaps.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T18:53:09Z

> Indeed I think the enabling of pod integrations was tricky before we introduced manageJobsNamespaceSelector, because the selector for pods was different than for other Jobs. With the standardized selector I'm not seeing any gaps.

Do we recommend a default for managedJobsNamespaceSelector? 

For Openshift, we essentially require that jobs that Kueue manges must have a kueue labeled namespace. This is so we can easily separate system services from user services.

I wasn't as clear if this is the recommendation for Kueue upstream though.

But honestly, people are free to change these defaults so I am +1 on making this supported by default if it makes sense to you all.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-03T19:03:59Z

> Do we recommend a default for managedJobsNamespaceSelector?

We dont have a recommendation, but we have a default which excludes kube-system and kueue-system namespaces.

> For Openshift, we essentially require that jobs that Kueue manges must have a kueue labeled namespace. This is so we can easily separate system services from user services.

This is quite reasonable. 

> I wasn't as clear if this is the recommendation for Kueue upstream though.

It is one of the supported deployment strategies. We have it documented.

> But honestly, people are free to change these defaults (...)

This proposal is not changing that. Enabling by default the integrations just means that LWS with the "queue-name" label starts to be scheduled by Kueue. Currently even if you have "queue-name" set on LWS theb the LWS is ignored by Kueue even if it matches managedJobsNamespaceSelector, because the whole integration is disabled.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-04T00:53:02Z

/assign @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-04T15:36:46Z

FYI that was discussed during wg-batch Dec 4th and no objections, so I assume we can proceed.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-12-04T15:41:52Z

Sorry to be late to comment and missing the wg-batch call today.  

I agree that with `manageJobsNamespaceSelector` we should have all the technical controls in place.  The defaults on vanilla Kubernetes are reasonable.  The defaults need to be different on OpenShift (ie, namespaces opt-in to being managed instead of opt-out), but that's a pure configuration/documentation item.
