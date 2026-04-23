# Issue #6517: Priodic Jobs for s390x and ppc64le are failing

**Summary**: Priodic Jobs for s390x and ppc64le are failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6517

**Last updated**: 2025-08-13T09:17:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-11T07:53:18Z
- **Updated**: 2025-08-13T09:17:50Z
- **Closed**: 2025-08-13T09:17:50Z
- **Labels**: `kind/bug`, `priority/important-soon`, `triage/accepted`
- **Assignees**: _none_
- **Comments**: 9

## Description

**What happened**:

The Jobs are failing: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-build-s390x-ppc64le-main

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-main/1954796352214929408

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

They were enabled by the PR: https://github.com/kubernetes/test-infra/pull/35175

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T07:54:20Z

cc @Deepali1999 @kannon92 @mbobrovskyi ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-11T08:01:36Z

Why we have this test?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T08:05:17Z

IIUC this was the preparatory step for https://github.com/kubernetes-sigs/kueue/issues/5166#issuecomment-2865199715 which aims to move the custom architectures only to nightly and release builds, thus offloading the presubmit builds. 

Wdyt? In any case if this is not ready I'm ok to revert temporarily.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-11T08:20:46Z

> Wdyt? In any case if this is not ready I'm ok to revert temporarily.

Ah, I got. Instead of building for each commit, we can test periodically.

### Comment by [@Deepali1999](https://github.com/Deepali1999) — 2025-08-11T08:51:18Z

@mbobrovskyi I have raised this PR https://github.com/kubernetes/test-infra/pull/35296 to address job failure.

## Root Cause
The periodic job environment doesn't have Docker buildx driver enabled, which is required for multi-platform builds (`linux/s390x,linux/ppc64le`).

## Solution
For Temporary fix removed the 'ppc64le' arch from the job till the multi arch builds are enabled.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-11T13:08:13Z

/triage accepted
/priority important-soon

### Comment by [@Deepali1999](https://github.com/Deepali1999) — 2025-08-13T07:15:01Z

Jobs are Completed Successfully.

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-main/1955521135508459520
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-release-0-12/1955521135600734208
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-release-0-13/1955521135693008896

PR reference: https://github.com/kubernetes/test-infra/pull/35296

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-13T09:17:44Z

> Jobs are Completed Successfully.
> 
> https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-main/1955521135508459520 https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-release-0-12/1955521135600734208 https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-release-0-13/1955521135693008896
> 
> PR reference: [kubernetes/test-infra#35296](https://github.com/kubernetes/test-infra/pull/35296)

Thank you for checking those.
Let us close this one so far.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-13T09:17:50Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6517#issuecomment-3182911981):

>> Jobs are Completed Successfully.
>> 
>> https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-main/1955521135508459520 https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-release-0-12/1955521135600734208 https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-build-s390x-ppc64le-release-0-13/1955521135693008896
>> 
>> PR reference: [kubernetes/test-infra#35296](https://github.com/kubernetes/test-infra/pull/35296)
>
>Thank you for checking those.
>Let us close this one so far.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
