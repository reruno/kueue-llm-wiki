# Issue #9594: Eliminate using features.SetEnable() in tests

**Summary**: Eliminate using features.SetEnable() in tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9594

**Last updated**: 2026-03-02T19:44:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Huang-Wei](https://github.com/Huang-Wei)
- **Created**: 2026-02-27T22:07:20Z
- **Updated**: 2026-03-02T19:44:15Z
- **Closed**: 2026-03-02T16:54:56Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@0xlen](https://github.com/0xlen)
- **Comments**: 9

## Description

**What would you like to be cleaned**:

The function `features.SetEnable()` defined at

https://github.com/kubernetes-sigs/kueue/blob/2651838047f0310ae88848b278837bfaad08ec39/pkg/features/kube_features.go#L437-L442

may confuse users - the `DefaultMutableFeatureGate` is not supposed to be modified in test envs where tests may run in parallel, see k/k's doc:

https://github.com/kubernetes-sigs/kueue/blob/c03277c969f4682cdaf119a2133664d9e76b95db/vendor/k8s.io/apiserver/pkg/util/feature/feature_gate.go#L24-L28

It's more conventional to turn all callings of `features.SetEnable()` in the following files to `features.SetFeatureGateDuringTest()`:

```
⇒  ag "features.SetEnable\(" -l
test/integration/multikueue/dra_test.go
test/integration/singlecluster/scheduler/fairsharing/suite_test.go
test/integration/singlecluster/tas/tas_test.go
```

**Why is this needed**:

Reduce possibility of flaky tests upon featuregates conflicts.

## Discussion

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-02-27T22:08:49Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-27T22:08:51Z

@Huang-Wei: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9594):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@0xlen](https://github.com/0xlen) — 2026-02-27T23:34:21Z

Hi @Huang-Wei ! I'd like to pick up this good-first-issue.

I'm new to the kueue codebase, so it may take around a week to get everything set up and tested locally. I'll keep the issue updated with progress.

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-28T12:28:44Z

Good idea!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-01T02:32:00Z

AFAIK, those `SetEnable()` function usage are not be able to be eliminated because those tests enable / disable FGs in each ginkgo Node.

So, I guess that eliminating the `SetEnable()` indicates that refactoring all those tests.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-01T04:58:01Z

> AFAIK, those `SetEnable()` function usage are not be able to be eliminated because those tests enable / disable FGs in each ginkgo Node.
> 
> So, I guess that eliminating the `SetEnable()` indicates that refactoring all those tests.

Oh, I see. As i can see, we can move the feature gate setting call to BeforeEach or AfterEach.

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-03-01T06:37:44Z

> AFAIK, those `SetEnable()` function usage are not be able to be eliminated because those tests enable / disable FGs in each ginkgo Node.

I think this is still possible, but just not qualified as a `good-first-issue`... let me craft a PR.

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-03-01T06:44:02Z

> Oh, I see. As i can see, we can move the feature gate setting call to BeforeEach or AfterEach.

Yup, exactly, and moving to BeforeEach() is enough as `features.SetFeatureGateDuringTest()` has covered the "reset featuregate back" already. I'm raising #9603 to see it passes all CIs.

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-03-02T19:44:14Z

Fixed by #9600
