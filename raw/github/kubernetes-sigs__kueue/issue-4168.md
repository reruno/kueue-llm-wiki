# Issue #4168: begin to deprecate integrations.podOptions

**Summary**: begin to deprecate integrations.podOptions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4168

**Last updated**: 2025-02-19T19:08:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-02-06T22:12:07Z
- **Updated**: 2025-02-19T19:08:29Z
- **Closed**: 2025-02-19T19:08:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Per the discussion in #3589, we want to migrate users from using `integrations.podOptions` to `managedJobsNamespaceSelector`. 
For Kueue 0.11 we should take the next step in the process.  This goal of this issue is to decide how far we can go in 0.11.

Some possible options:
1. We just emit a warning message when the option is set to a non-default value.
2. We emit a configuration error if it is set to a non-default value and remove all the code that processes it (but leave it defined by unused in the struct).
3. Some intermediate point to be defined between these extremes? 

**Why is this needed**:

We want to not carry integrations.podOptions into the next API version of the Configuration struct. We should start encouraging people to migrate away from it.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-06T22:12:44Z

/cc @tenzen-y @mimowo

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-07T02:50:36Z

Kubernetes tend to follow relatively conservative approachs for deprecations.

I think the following plan follows k8s practices:

- 0.11 can begin marking the field as deprecated
  - We can emit a warning or event that this configuration option is deprecated and will be removed.
  - Add a comment that the field is deprecated.
- 0.12 or 0.13 we could remove the option since our config API is still beta.

If config api went v1 we would probably leave the field as deprecated but not remove.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-07T11:42:58Z

> 0.12 or 0.13 we could remove the option since our config API is still beta.

AFAIK, Beta API (not Beta feature) represents not to break API, right. So, we need to bump API version to v1beta2 instead of removal of fields.

Could you point the policy which mention allowing us to break Beta API? My beta API understanding might be not correct.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-07T12:08:20Z

I don’t know if there is anything for beta written down like that. I know that we dropped an API field for Swap in Beta that we decided was too risky to support. It was understood that this was the best option.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-07T14:40:31Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-07T14:53:25Z

> I don’t know if there is anything for beta written down like that.

Actually, I think API elements (such as fields) should never be removed within API version based on https://kubernetes.io/docs/reference/using-api/deprecation-policy/.

"Rule #1: API elements may only be removed by incrementing the version of the API group."

We can remove fields when incrementing the API version.

> I know that we dropped an API field for Swap in Beta that we decided was too risky to support. It was understood that this was the best option.

I don't know this specific case, but I can well imagine under some circumstances this is the most rational choice and this is why we have the pragmatic [Exceptions](https://kubernetes.io/docs/reference/using-api/deprecation-policy/#exceptions).

I believe in case of `integrations.podOptions` there is no urgency regarding its removal. I would suggest to depracate it -review all docs and API comments to make sure it is not suggested to users / admins. Also, make it clear to users that it will be removed on the next API update. Then, we will remove it when updating the API.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-08T16:23:38Z

> > I don’t know if there is anything for beta written down like that.
> 
> Actually, I think API elements (such as fields) should never be removed within API version based on https://kubernetes.io/docs/reference/using-api/deprecation-policy/.
> 
> "Rule [#1](https://github.com/kubernetes-sigs/kueue/pull/1): API elements may only be removed by incrementing the version of the API group."
> 
> We can remove fields when incrementing the API version.
> 
> > I know that we dropped an API field for Swap in Beta that we decided was too risky to support. It was understood that this was the best option.
> 
> I don't know this specific case, but I can well imagine under some circumstances this is the most rational choice and this is why we have the pragmatic [Exceptions](https://kubernetes.io/docs/reference/using-api/deprecation-policy/#exceptions).
> 
> I believe in case of `integrations.podOptions` there is no urgency regarding its removal. I would suggest to depracate it -review all docs and API comments to make sure it is not suggested to users / admins. Also, make it clear to users that it will be removed on the next API update. Then, we will remove it when updating the API.

Thank you for pointing the deprecation documentation. Your recommended step is what I imagined when we stopped serving fields.
