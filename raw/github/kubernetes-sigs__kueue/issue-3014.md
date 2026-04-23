# Issue #3014: Optimize waiting for API to poll REST mapper only when the CRD is installed

**Summary**: Optimize waiting for API to poll REST mapper only when the CRD is installed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3014

**Last updated**: 2024-09-09T13:04:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-09T07:41:44Z
- **Updated**: 2024-09-09T13:04:40Z
- **Closed**: 2024-09-09T13:04:39Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be added**:

An optimization to the CRD tracker https://github.com/kubernetes-sigs/kueue/blob/7fed1235a645da375c332c470ecd4b9be6971322/pkg/controller/jobframework/setup.go#L123 to start the polling for REST mapper only when the CRD is installed.

**Why is this needed**:

- reduce the amount of logging for not installed CRDs
- shorten the time for the API to be ready - currently due to the exponential backoff the detection of API is likely to take 2min (max period). if we start active polling after the CRD is installed the REST mapper will be detected quickly.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T07:41:59Z

/cc @ChristianZaccaria @alculquicondor @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T07:43:29Z

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/2574
/cc @varshaprasad96

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-09T13:00:07Z

Once we migrate from manually polling to reconcilers (https://github.com/kubernetes-sigs/kueue/issues/2837), this is not needed Isn't it?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T13:04:34Z

I would rather say this is a duplicate as I missed the other one. 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-09T13:04:39Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3014#issuecomment-2338073320):

>I would rather say this is a duplicate as I missed the other one. 
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
