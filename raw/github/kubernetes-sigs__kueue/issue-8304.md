# Issue #8304: [LWS] E2E tests for Failure Handling and Restart Policies

**Summary**: [LWS] E2E tests for Failure Handling and Restart Policies

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8304

**Last updated**: 2026-01-16T05:15:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@anahas-redhat](https://github.com/anahas-redhat)
- **Created**: 2025-12-17T14:57:08Z
- **Updated**: 2026-01-16T05:15:12Z
- **Closed**: 2026-01-16T05:15:12Z
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@anahas-redhat](https://github.com/anahas-redhat)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**: I'd like to ask if E2E tests for Failure Handling and Restart Policies can be added for LeaderWorkerSet.
I'm asking this because, by checking LeaderWorkerSet test suite - test/e2e/singlecluster/leaderworkerset_test.go - I was not able to find any test related to restartPolicy. 

**Why is this needed**: I have manually checked this with [Kueue Operator ](https://github.com/openshift/kueue-operator) and, it seems to be working fine. However, it would be good to have restartPolicy being checked as part of automation suite, so we won't need to do manual testing to check it.

Thank you.
cc @kannon92

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T15:01:13Z

sgtm, would you like to have some list of scenarios you would like to cover?

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2025-12-17T15:04:48Z

I think if we can add two:

- restartPolicy: RecreateGroupOnPodRestart - Simulate a failure in a pod and check if the whole group is restarted.
- restartPolicy: None - Simulate a failure in a pod and check if only the pod that is presenting a problem is restarted.

I can help automating this scenarios, if it sounds good.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T15:35:53Z

sgtm, would you prefer testing with TAS or just quota based? Asking cause in case of failures TAS also has the NodeHotSwap which could be at play in some scenarios

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-17T15:47:12Z

> sgtm, would you prefer testing with TAS or just quota based? Asking cause in case of failures TAS also has the NodeHotSwap which could be at play in some scenarios

We still haven't figured out how to enable TAS in our cloud environments so for now it would be quota based.

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2025-12-17T17:06:40Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:31:10Z

/priority important-longterm
