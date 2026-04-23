# Issue #5505: Promote Cohort API to Beta

**Summary**: Promote Cohort API to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5505

**Last updated**: 2025-06-20T17:20:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-04T17:26:37Z
- **Updated**: 2025-06-20T17:20:53Z
- **Closed**: 2025-06-20T17:20:53Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 29

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to propose a more stable Cohort API version, beta.

**Why is this needed**:
The Cohort API was introduced in Kueue v0.9 as a part of the Hierarchical Cohort feature https://github.com/kubernetes-sigs/kueue/blob/c47505f90ea356ed6fbf1c2238a28eaf5551d9f3/keps/79-hierarchical-cohorts

However, the Cohort API is still an alpha API (https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1alpha1/cohort_types.go). 

I believe that we do not have any plans coupled with critical breaking changes.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T17:27:31Z

@mimowo @gabesaba Do you plan to change the Cohort API with breaking changes?
If not, could we promote the API version to Beta?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-05T09:25:07Z

No plans for breaking changes. The only thing we want to do eventually is unify name of `Parent` field between CQ/Cohort, but that may not even require a change here - see https://github.com/kubernetes-sigs/kueue/issues/768#issuecomment-2706664536

I support promoting it

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T09:49:49Z

> No plans for breaking changes. The only thing we want to do eventually is unify name of `Parent` field between CQ/Cohort, but that may not even require a change here - see [#768 (comment)](https://github.com/kubernetes-sigs/kueue/issues/768#issuecomment-2706664536)
> 
> I support promoting it

This issue aims to promote only Cohort API from alpha to v1beta1. So, the CQ still has `Parent` even though Cohort has `parentCohort`. Are you ok with that?

- CQ v1beta1: `cohort`
- Cohort
  -  v1alpha1: `parent`
  -  v1beta1: `parentCohort`

Additionally, promoting alpha API to beta indicate to remove alpha API. Are you ok with removing alpha API? Or do you want to have a migration period?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T10:04:19Z

> `v1alpha1: cohort`

This is "Parent" actually https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1alpha1/cohort_types.go#L37

When promoting I'm ok with either "Parent" and "ParentCohort", but my slight preference is just "Parent", for conciseness. I think "cohort" is already implied, so no need to repeat.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T10:06:15Z

> > `v1alpha1: cohort`
> 
> This is "Parent" actually https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1alpha1/cohort_types.go#L37

Good point, I updated the above list.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T10:52:23Z

> When promoting I'm ok with either "Parent" and "ParentCohort", but my slight preference is just "Parent", for conciseness. I think "cohort" is already implied, so no need to repeat.

I think that the point is whether or not we request users' CQ - Cohort knowledge, which means Cohort users need to understand in advance that Cohort has a Tree structure, and parent and children are only Cohort.

If we do not have any plan to support another parenting mechanism other than Cohort, we might want to have `parent` instead of `parentCohort`.

@gabesaba Do you still want to add `cohort` suffix to `parent` field?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-06T09:12:47Z

> [@gabesaba](https://github.com/gabesaba) Do you still want to add `cohort` suffix to `parent` field?

Let's leave as Parent.

> Additionally, promoting alpha API to beta indicate to remove alpha API. Are you ok with removing alpha API? Or do you want to have a migration period?

I don't have a strong preference. How have we done this in the past?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T09:25:42Z

> I don't have a strong preference. How have we done this in the past?

The only example I'm recollecting was MultiKueue which was promoted to Beta without any conversion. 

Generally conversion is not required by the k8s rules. From https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-stages, "The API may change in incompatible ways in a later software release without notice", so we are free to just drop Alpha.

However, we may prefer adding conversion if there is such interest among users.

I'm not aware of such interest at the moment, so for simplicity, I would support just dropping Alpha and replacing with Beta. I think we could follow the example of MultiKueue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0 with the "Upgrading steps" section.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-06T09:40:36Z

> > [@gabesaba](https://github.com/gabesaba) Do you still want to add cohort suffix to parent field?
> 
> Let's leave as Parent.

LGTM

> > I don't have a strong preference. How have we done this in the past?
> 
> The only example I'm recollecting was MultiKueue which was promoted to Beta without any conversion.
> 
> Generally conversion is not required by the k8s rules. From https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-stages, "The API may change in incompatible ways in a later software release without notice", so we are free to just drop Alpha.
> 
> However, we may prefer adding conversion if there is such interest among users.
> 
> I'm not aware of such interest at the moment, so for simplicity, I would support just dropping Alpha and replacing with Beta. I think we could follow the example of MultiKueue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0 with the "Upgrading steps" section.

SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-06T09:41:22Z

I will try to work on this for the next minor version.

/assign

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-06-06T13:50:10Z


> I'm not aware of such interest at the moment, so for simplicity, I would support just dropping Alpha and replacing with Beta. I think we could follow the example of MultiKueue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0 with the "Upgrading steps" section.

This did cause some minor downstream pain when OpenShift AI upgraded from Kueue 0.8 to Kueue 0.10 and had to deal with the removal of the alpha multikueue CRDs.  I was only tangentially involved, but maybe @kannon92 has some thoughts based on that experience.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-06T14:03:51Z

> > I'm not aware of such interest at the moment, so for simplicity, I would support just dropping Alpha and replacing with Beta. I think we could follow the example of MultiKueue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0 with the "Upgrading steps" section.
> 
> This did cause some minor downstream pain when OpenShift AI upgraded from Kueue 0.8 to Kueue 0.10 and had to deal with the removal of the alpha multikueue CRDs. I was only tangentially involved, but maybe [@kannon92](https://github.com/kannon92) has some thoughts based on that experience.

Basically, we follow https://kubernetes.io/docs/reference/using-api/deprecation-policy/. So, we remove Alpha API w/o any backward compatibility. I asked them to confirm since I wanted to know if there are any specific users who depend on Alpha API.

https://github.com/kubernetes-sigs/kueue?tab=readme-ov-file#production-readiness-status

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-06T15:22:17Z

So using alpha APIs and expecting SLA around that is a recipe for pain.

Due to this, we have started not installing alpha APIs from Kueue and we will only include beta APIs for our operator.

AFAIK we do not have any users of these API (cc @varshaprasad96) in Openshift land.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-06-06T15:32:49Z

> So using alpha APIs and expecting SLA around that is a recipe for pain.
> 
> Due to this, we have started not installing alpha APIs from Kueue and we will only include beta APIs for our operator.
> 
> AFAIK we do not have any users of these API (cc [@varshaprasad96](https://github.com/varshaprasad96)) in Openshift land.

Yeah, that's what I thought the outcome was.  So the invariant the downstream needs is that all references to any alpha API are properly guarded by feature gates so that Kueue will still work as expected when they are not installed.   Maybe we should have an e2e test of Kueue that doesn't install the alpha APIs to keep us honest.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-06T15:40:14Z

For openshift-kueue-operator, we do have [that](https://github.com/openshift/kueue-operator/blob/release-1.0/test/e2e/e2e_operator_test.go#L142).

And I have added a feature gate to guard Cohorts for these reason.

> Maybe we should have an e2e test of Kueue that doesn't install the alpha APIs to keep us honest.
I am not sure if you mean upstream or downstream here but I don't know if we want to not install these CRDs for Alpha as that would block folks from actually testing/using alpha features from upstream.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-06-06T16:00:45Z

Opened https://github.com/kubernetes-sigs/kueue/issues/5545 to track the idea of an additional testing configuration.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T11:49:13Z

Thank you for the feedback!
Then, let's promote this one.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T11:13:41Z

I revisited the `.spec.parent` field name in Cohort API.
In conclusion, I would like to replace `.spec.parent` with `.spec.parentRef` to align with API recomendations:

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#naming-of-the-reference-field

So, my proposals are as follows:

- CQ
  -  v1beta1: `cohort`
  -  v1beta2: `cohortRef`
- Cohort
  -  v1alpha1: `parent`
  -  v1beta1: `parentRef`

@mimowo @gabesaba @kannon92 @dgrove-oss Any objections?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T11:24:44Z

tbh, I don't see a need to change it, especially at the cost of extra work. 

I might be wrong. but the convention does not seem followed closely inside core k8s API.  Could you provide some core examples where this convention was used?

For example, is the recently added API for DRA following it? For example I can see [DeviceClassName](https://github.com/kubernetes/kubernetes/blob/master/pkg/apis/resource/types.go#L658C2-L658C17) refering to DeviceClass.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T11:46:56Z

> tbh, I don't see a need to change it, especially at the cost of extra work.
> 
> I might be wrong. but the convention does not seem followed closely inside core k8s API. Could you provide some core examples where this convention was used?
> 
> For example, is the recently added API for DRA following it? For example I can see [DeviceClassName](https://github.com/kubernetes/kubernetes/blob/master/pkg/apis/resource/types.go#L658C2-L658C17) refering to DeviceClass.

Interesting. Thank you for reporting DRA case. I can see the following examples:

- We can find some of xxxRef fields under [`CSIPersistentVolumeSource`](https://github.com/kubernetes/kubernetes/blob/da502386e53c1be6d476af8352337d82deb470aa/pkg/apis/core/types.go#L1921)
- `SecretRef` in [ISCSIVolumeSource](https://github.com/kubernetes/kubernetes/blob/da502386e53c1be6d476af8352337d82deb470aa/pkg/apis/core/types.go#L983C2-L983C11)
- [`ClaimRef`](https://github.com/kubernetes/kubernetes/blob/da502386e53c1be6d476af8352337d82deb470aa/pkg/apis/core/types.go#L383)
- The Gateway API is not core API, but it is good example API. 
  - HTTPRoute [ParentRef](https://github.com/kubernetes-sigs/gateway-api/blob/270d637886ff72a5c24431dba45e0f4b88fdeb17/apisx/v1alpha1/xlistenerset_types.go#L50)
  - HTTPRoute [BackendRef](https://github.com/kubernetes-sigs/gateway-api/blob/270d637886ff72a5c24431dba45e0f4b88fdeb17/apis/v1/httproute_types.go#L1584)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T11:55:17Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-10T11:55:23Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5505#issuecomment-2958916945):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T10:55:31Z

> > tbh, I don't see a need to change it, especially at the cost of extra work.
> > I might be wrong. but the convention does not seem followed closely inside core k8s API. Could you provide some core examples where this convention was used?
> > For example, is the recently added API for DRA following it? For example I can see [DeviceClassName](https://github.com/kubernetes/kubernetes/blob/master/pkg/apis/resource/types.go#L658C2-L658C17) refering to DeviceClass.
> 
> Interesting. Thank you for reporting DRA case. I can see the following examples:
> 
> * We can find some of xxxRef fields under [`CSIPersistentVolumeSource`](https://github.com/kubernetes/kubernetes/blob/da502386e53c1be6d476af8352337d82deb470aa/pkg/apis/core/types.go#L1921)
> * `SecretRef` in [ISCSIVolumeSource](https://github.com/kubernetes/kubernetes/blob/da502386e53c1be6d476af8352337d82deb470aa/pkg/apis/core/types.go#L983C2-L983C11)
> * [`ClaimRef`](https://github.com/kubernetes/kubernetes/blob/da502386e53c1be6d476af8352337d82deb470aa/pkg/apis/core/types.go#L383)
> * The Gateway API is not core API, but it is good example API.
>   
>   * HTTPRoute [ParentRef](https://github.com/kubernetes-sigs/gateway-api/blob/270d637886ff72a5c24431dba45e0f4b88fdeb17/apisx/v1alpha1/xlistenerset_types.go#L50)
>   * HTTPRoute [BackendRef](https://github.com/kubernetes-sigs/gateway-api/blob/270d637886ff72a5c24431dba45e0f4b88fdeb17/apis/v1/httproute_types.go#L1584)

@mimowo I asked the WG Device Management folks and API reviewers the reason why the DRA has `deviceClassName` instead of `deviceClassRef` in https://github.com/kubernetes/kubernetes/issues/132206.

In conclusion, it is called `deviceClassName` because the field does not provide the functionalities to specify struct having a set of fields. This means that if it has only functionality to specify only one identity like `name`, we should use `${resource_name}Name` rather than `${resource_name}Ref`.

So, we could consider replace `parent` with `CohortParentName`. However, the parent indicates the same Resource API name, Cohort. In that case, we should use the `parentName` for Cohort.

OTOH, CQ has currently has `cohort` field which does not align with the the API manner.
So, my final proposal is the beflow:

- CQ
  - v1beta1: cohort
  - v1beta2: cohortName
- Cohort
  - v1alpha1: parent
  - v1beta1: parentName

However, we can discuss the CQ field name in the future v1beta2 issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T10:59:21Z

> - CQ
>   - v1beta1: cohort
>   - v1beta2: cohortName
> - Cohort
>   - v1alpha1: parent
>   - v1beta1: parentName

@mimowo Do you have other objections to `parentName` in Cohort?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T11:06:02Z

Thank you for the investigation @tenzen-y . This is very insightful. 

I like the {field}Name convention, as we used in TopologyName.

The proposal as parentName and cohortName feels reasonable. Tbh I don't see benefit of parentCohortName., as it is longer.

However, I would only consider it for v1beta2. For now I would say cohort and parent make sense, as defined. 

Renaming for v1beta2 will also be bringing risks, so I would be careful about it, but open to it as a possibility.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T11:12:01Z

> Renaming for v1beta2 will also be bringing risks, so I would be careful about it, but open to it as a possibility.

Why don't you change the Cohort API field `parent` to `parentName` in Beta promotion?
The alpha API does not support backward compatibility in promotion. This is the main reason why we want to start from alpha API instead of Beta API.

Do you follow any other guidance?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T11:17:14Z

> Why don't you change the Cohort API field parent to parentName in Beta promotion?

I'm ok to do so. I just felt it would be better to keep the naming strategy consistent for `Cohort` and `Parent` fields in v1beta1. 

Especially if we are not certain about renaming `cohort` to `cohortName` in v1beta2.

However, this is just a minor concern, I'm ok calling it `parentName` in v1beta1.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T11:25:24Z

> I'm ok to do so. I just felt it would be better to keep the naming strategy consistent for `Cohort` and `Parent` fields in v1beta1.
> 
> Especially if we are not certain about renaming `cohort` to `cohortName` in v1beta2.
> 
> However, this is just a minor concern, I'm ok calling it `parentName` in v1beta1.

I believe that we can convert `cohort` to `cohortName` in ClusterQueue since we should provide a conversion webhook for Beta API promotion, which means avoiding breaking the user environment.

Additionally, if we replace `parent` with `parentName` in Cohort API now, we can avoid to implement conversion webhook for that when we promote v1beta1 to v1beta2 (or directly promote it to GA).
I believe that this is a big advantage for introducing `parentName` for Cohort API, now.

Anyway, for now, let us focus on Cohort API promotion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T11:48:06Z

> I believe that we can convert cohort to cohortName in ClusterQueue since we should provide a conversion webhook for Beta API promotion, which means avoiding breaking the user environment.

Right, but I wouldn't do conversion webhooks just for the rename. If we have other API changes requiring conversion webhooks, then +1 on also including the rename.

> I believe that this is a big advantage for introducing parentName for Cohort API, now.
> Anyway, for now, let us focus on Cohort API promotion.

ack, no objections here.
