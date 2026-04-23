# Issue #7247: v1beta2: Drop APIs deprecated for long

**Summary**: v1beta2: Drop APIs deprecated for long

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7247

**Last updated**: 2025-11-04T09:38:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-13T13:03:04Z
- **Updated**: 2025-11-04T09:38:40Z
- **Closed**: 2025-11-04T09:38:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@nerdeveloper](https://github.com/nerdeveloper)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

- [x] [Queue-name annotation](https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/pkg/controller/constants/constants.go#L29-L32) [DEPRECATED SINCE 0.3 at least, we use label now]
- [x] [QueueVisibility](https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/apis/config/v1beta1/configuration_types.go#L85-L90) API [DEPRECATED FOR LONG, implementation already dropped]
- [x] [retryDelayMinutes](https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/apis/kueue/v1beta1/admissioncheck_types.go#L55-L61) from the AdmissionCheck API [DEPRECATED FOR LONG, no impl]
- [x] [PodIntegrationOptions](https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/apis/config/v1beta1/configuration_types.go#L415-L419) [DEPRECATED SINCE 0.11]

**Why is this needed**:

To cleanup the API before reaching v1beta2.

## Discussion

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-10-14T20:21:15Z

/assign

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-10-14T20:21:42Z

I would like to work on this if that’s okay

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T07:34:01Z

Yes, that is great. Let's review the work TODO:
- for "Queue-name annotation" I think you could just submit a PR
- for QueueVisibility  and retryDelayMinutes they are part of the schema so require v1beta2 to be put
- PodIntegrationOptions you could already submit a PR to drop the logic, but not API. In the follow up PR we would drop the API once we have v1beta2. Here I would also like to update the documentation to clearly mention that the feature is no longer supported, and recommend users moving to the "managedJobsNamespaceSelector"

You can also consider related issue https://github.com/kubernetes-sigs/kueue/issues/6777. In the first PR we will just deprecate the field.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T14:53:15Z

The first one is done with https://github.com/kubernetes-sigs/kueue/pull/7271

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T14:37:02Z

I just marked QueueVisibility and retryDelayMinutes completed based on the PRs: 
- https://github.com/kubernetes-sigs/kueue/pull/7319 and https://github.com/kubernetes-sigs/kueue/pull/7447
- https://github.com/kubernetes-sigs/kueue/pull/7407

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T09:38:34Z

/close
The last one is done in https://github.com/kubernetes-sigs/kueue/pull/7406

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-04T09:38:40Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7247#issuecomment-3484909357):

>/close
>The last one is done in https://github.com/kubernetes-sigs/kueue/pull/7406


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
