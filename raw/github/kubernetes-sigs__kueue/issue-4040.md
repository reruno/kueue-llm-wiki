# Issue #4040: Extract multikueue integration tests to a dedicated CI job

**Summary**: Extract multikueue integration tests to a dedicated CI job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4040

**Last updated**: 2025-01-28T13:33:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-23T08:58:21Z
- **Updated**: 2025-01-28T13:33:25Z
- **Closed**: 2025-01-28T13:33:25Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to extract the integration multikueue tests to a dedicated suite.

**Why is this needed**:

The multikueue integration tests are quite heavy in nature, because:
- we run 3 instances of Kueue to simulate execution of 3 clusters (see [here](https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/test/integration/multikueue/suite_test.go#L236-L256))
- we install opt-in CRDs to test MultiKueue with different frameworks (see [here](https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/test/integration/multikueue/suite_test.go#L95-L98))
- they run INTEGRATION_NPROC=4 as other "lightweight" integration tests

For the experiments in the context of [Kuberay multikueue integrations tests](https://github.com/kubernetes-sigs/kueue/pull/3986) we learned that:
- increasing resources for the job for integration tests helped a little bit, but didn't fully solve the problem with running Ray (see [comment](https://github.com/kubernetes-sigs/kueue/pull/3986#issuecomment-2609155189))
- we know that setting INTEGRATION_NPROC=3 makes the tests usually pass, but it means lower parallelism enforced on the lightweight tests, which is not ideal

Another argument for the separate CI job is that the integration tests take long (around 18 min currently): https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main. 

The MK integration tests take around 1min 50s of the time, so we could offload the main integration suite and allow for lower parallelism on the MK suite.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T08:58:44Z

cc @mszadkow @mbobrovskyi 
WDYT @tenzen-y ?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-23T11:37:23Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-27T08:44:35Z

> cc [@mszadkow](https://github.com/mszadkow) [@mbobrovskyi](https://github.com/mbobrovskyi) WDYT [@tenzen-y](https://github.com/tenzen-y) ?

As we consider expanding the MultiKueue feature to support Job types more and more, I would prefer the proposed solution so that we can make developments faster.
