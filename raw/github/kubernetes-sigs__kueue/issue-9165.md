# Issue #9165: v1 API: Restructure resources field in Configuration API

**Summary**: v1 API: Restructure resources field in Configuration API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9165

**Last updated**: 2026-02-27T02:04:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-12T13:14:45Z
- **Updated**: 2026-02-27T02:04:23Z
- **Closed**: 2026-02-27T02:04:23Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We would like to investigate the new `resources` field structure for v1 API in the following

(a. 

```yaml
resources:
  excludeByPrefixes: []
  includeByPrefixes: []
```

(b. 

```yaml
resources:
  prefixes:
    // These are mutually exclusive
    excludes: []
    includes: []
```

https://github.com/kubernetes-sigs/kueue/blob/a16f48cbee72f7c629796706d689f183acd84180/apis/config/v1beta2/configuration_types.go#L458-L470

**Why is this needed**:

Making the Configuration API more understandable for limitations.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-13T19:11:52Z

Based on the discussion in https://github.com/kubernetes-sigs/kueue/pull/8396,

I'm not sure we need to restructure this.

The main option may be to deprecate `excludeResourcePrefixes` in place for the KEP in #8396.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T02:04:18Z

> Based on the discussion in [#8396](https://github.com/kubernetes-sigs/kueue/pull/8396),
> 
> I'm not sure we need to restructure this.
> 
> The main option may be to deprecate `excludeResourcePrefixes` in place for the KEP in [#8396](https://github.com/kubernetes-sigs/kueue/pull/8396).

Yeah, that's right. We changed the API design.
So, this is no longer a valid request. Let me close this one.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-27T02:04:23Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9165#issuecomment-3970292831):

>> Based on the discussion in [#8396](https://github.com/kubernetes-sigs/kueue/pull/8396),
>> 
>> I'm not sure we need to restructure this.
>> 
>> The main option may be to deprecate `excludeResourcePrefixes` in place for the KEP in [#8396](https://github.com/kubernetes-sigs/kueue/pull/8396).
>
>Yeah, that's right. We changed the API design.
>So, this is no longer a valid request. Let me close this one.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
