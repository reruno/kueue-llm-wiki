# Issue #429: Run unit/integration/e2e tests on a daily basis.

**Summary**: Run unit/integration/e2e tests on a daily basis.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/429

**Last updated**: 2023-03-26T12:58:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-11-21T20:07:48Z
- **Updated**: 2023-03-26T12:58:43Z
- **Closed**: 2023-03-26T12:58:42Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: [@AxeZhan](https://github.com/AxeZhan), [@Sajiyah-Salat](https://github.com/Sajiyah-Salat)
- **Comments**: 29

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Since it is now possible to view all unit/integration/e2e tests in the testgrid, we can now run these tests periodically so we can detect fickle tests. 
**Why is this needed**:

Running tests on a scheduled basis will allow us to detect fickle tests.  
**Completion requirements**:

Prow is able to run Unit/Integration/E2E tests on a scheduled basis.  


Note:

I believe that we could follow something similar as https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes-sigs/kind/kind-release-blocking.yaml.

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-11-21T20:08:11Z

@kannon92: The label(s) `kind/good-first-issue, kind/help-wanted` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/429#issuecomment-1322583917):

>/kind good-first-issue
>/kind help-wanted


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-21T21:43:19Z

/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-11-21T21:43:21Z

@kannon92: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/429):

>/help
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@carlory](https://github.com/carlory) — 2022-11-22T17:58:18Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-25T22:23:34Z

Hey @carlory thanks for taking the issue. Let us know if you need any help. I think you’ll need to open a PR on the test infra repo so just like that here in this issue.

### Comment by [@carlory](https://github.com/carlory) — 2022-12-01T06:13:46Z

@kannon92 sorry for too late reply, I will do it in this week.

### Comment by [@indevi](https://github.com/indevi) — 2022-12-11T04:37:24Z

Are you still working on it? I would like to take this up

### Comment by [@carlory](https://github.com/carlory) — 2022-12-11T11:50:37Z

/unassign

@ShivamTyagi12345  you can pick up

### Comment by [@indevi](https://github.com/indevi) — 2022-12-11T11:51:15Z

Thanks

### Comment by [@Sajiyah-Salat](https://github.com/Sajiyah-Salat) — 2023-02-17T02:05:18Z

/assign

### Comment by [@Sajiyah-Salat](https://github.com/Sajiyah-Salat) — 2023-02-17T02:06:25Z

Hello @ShivamTyagi12345 are you still working on this. if not Have you worked before? Do you have some insights to share?

### Comment by [@Sajiyah-Salat](https://github.com/Sajiyah-Salat) — 2023-02-17T02:07:56Z

I got the issue. But do you have some guide to solution? Its a confusion for me. Thank you.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-17T13:22:39Z

Our presubmits configurations live here: https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes-sigs/kueue/kueue-presubmits.yaml

As stated by @kannon92, we probably need to add a new file for periodic runs, following a pattern similar to https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes-sigs/kind/kind-release-blocking.yaml

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-12T10:05:52Z

Submit this [file](https://github.com/kubernetes/test-infra/blob/dc2befd47deffb0e801ced41153af1a6ad1ceb20/config/jobs/kubernetes-sigs/kueue/kueue-release-blocking.yaml) to test-infra?
I'm not familar with both test-infra and kueue. So I'd like to post it here to let you guys check it first.
Here're something that I'm not very clear:

1. our `testgrid-alert-email` ?
2. can `testgrid-dashboards` and `testgrid-tab-name` have the same name with tests in `kueue-presubmits.yaml`?

### Comment by [@kannon92](https://github.com/kannon92) — 2023-03-12T13:19:08Z

I think that’s good enough to open on test-infra for a review. Not sure on the answers to your questions but it’s easier to review on a PR imo.

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-12T13:42:02Z

> I think that’s good enough to open on test-infra for a review. Not sure on the answers to your questions but it’s easier to review on a PR imo.

/assign
Created [#28999](https://github.com/kubernetes/test-infra/pull/28999)

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-15T08:51:56Z

Sorry guys, a mistake has been made by me, and the tests are continuously failing.
Created [#29050](https://github.com/kubernetes/test-infra/pull/29050)  to fix this.

### Comment by [@kannon92](https://github.com/kannon92) — 2023-03-15T11:46:36Z

> Sorry guys, a mistake has been made by me, and the tests are continuously failing.
> Created [#29050](https://github.com/kubernetes/test-infra/pull/29050) to fix this.

Thank you for your due diligence on following up!

### Comment by [@kannon92](https://github.com/kannon92) — 2023-03-15T12:24:19Z

Should we include 1.26 in our tests?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T14:14:59Z

yes please, I guess we can add it both to presubmit and periodic

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-15T14:31:42Z

I can add that, I think we are using this env to control kubernetes version in ci. What's the value of it for 1.26? `v1.26.?`
```
        env:
        - name: E2E_KIND_VERSION
          value: kindest/node:v1.24.7
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T14:41:19Z

use the latest possible https://hub.docker.com/r/kindest/node/tags

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-15T14:42:56Z

also should we remove `pull-kueue-test-e2e-main-1-23` from presubmit?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T14:45:18Z

yes

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-15T15:08:18Z

created [#29053](https://github.com/kubernetes/test-infra/pull/29053)

### Comment by [@kannon92](https://github.com/kannon92) — 2023-03-25T18:18:51Z

Can we close this issue and mark it as done?

### Comment by [@AxeZhan](https://github.com/AxeZhan) — 2023-03-26T04:48:42Z

I'm +1 with close it.

### Comment by [@kannon92](https://github.com/kannon92) — 2023-03-26T12:58:38Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-26T12:58:43Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/429#issuecomment-1484088959):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
