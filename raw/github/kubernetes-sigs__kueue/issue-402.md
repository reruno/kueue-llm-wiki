# Issue #402: Expand testgrids per test

**Summary**: Expand testgrids per test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/402

**Last updated**: 2022-11-18T15:36:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-09-19T20:47:47Z
- **Updated**: 2022-11-18T15:36:31Z
- **Closed**: 2022-11-18T15:36:31Z
- **Labels**: `help wanted`, `kind/cleanup`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 9

## Description

**What would you like to be cleaned**:

Currently, the testgrids for unit and integration tests only mark whether the entire suite passed or not.

- https://testgrid.k8s.io/sig-scheduling#pull-kueue-test-unit-main
- https://testgrid.k8s.io/sig-scheduling#pull-kueue-test-integration-main

It would useful to have rows for each test.

**Why is this needed**:

To be able to track flakiness of specific tests.

**Notes**:

I don't know how to achieve this, but here is where the presubmits are defined:

https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes-sigs/kueue/kueue-presubmits.yaml

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-19T20:47:56Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-09-19T20:47:57Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/402):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-19T21:03:10Z

It probably has to do with using the kubekins image https://github.com/kubernetes/test-infra/blob/0aef7a83d0f5d74467667e4d13eef2589c5d740d/config/jobs/kubernetes/sig-testing/make-test.yaml#L18

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-19T21:11:30Z

Or producing a junit XML report 🤷

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2022-09-19T22:44:55Z

junit xml, not kubekins

see for example https://github.com/kubernetes-sigs/kind/blob/b6bc112522651d98c81823df56b7afa511459a3b/hack/make-rules/test.sh / https://github.com/kubernetes/registry.k8s.io/blob/main/hack/make-rules/test.sh

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-19T21:42:56Z

So if I'm reading this right, we need to generate junit-xml reports for our tests.  How exactly do these artifacts get uploaded to testgrid?  

@alculquicondor Since I will be opening a PR to testgrid once I get https://github.com/kubernetes-sigs/kueue/pull/421 merged, I'll experiment with junit for that and then apply these findings to the other tests?

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2022-10-19T21:47:52Z

> So if I'm reading this right, we need to generate junit-xml reports for our tests. How exactly do these artifacts get uploaded to testgrid?

Testgrid reads junit.xml artifacts from what the CI uploads ($ARTIFACTS directory).

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-21T21:07:11Z

/assign @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-31T17:05:00Z

Hello @BenTheElder, thank you for your help.  I believe I figured out how to add testgrid per test.  

https://github.com/kubernetes-sigs/kueue/pull/423
