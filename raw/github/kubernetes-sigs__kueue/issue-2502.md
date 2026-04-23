# Issue #2502: cleanup manipulation of CQ/Cohort resource accounting in tests

**Summary**: cleanup manipulation of CQ/Cohort resource accounting in tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2502

**Last updated**: 2024-11-20T13:43:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-06-28T15:52:36Z
- **Updated**: 2024-11-20T13:43:51Z
- **Closed**: 2024-11-20T13:43:49Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow), [@vladikkuzn](https://github.com/vladikkuzn), [@highpon](https://github.com/highpon)
- **Comments**: 13

## Description

**What would you like to be cleaned**:
We sometimes manipulate the internal accounting of ClusterQueue and Cohort snapshots. This is brittle. Quota/Lending Limit/Borrowing Limit/Usage should be set by calling public api methods, or by defining the CQs/Cohorts via API objects, adding to cache, and creating snapshot (see #2486 for an example).

See this thread https://github.com/kubernetes-sigs/kueue/pull/2486#discussion_r1658747058

**Why is this needed**:
Tests are brittle, and make cache/snapshot hard to update

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-28T17:16:23Z

Also https://github.com/kubernetes-sigs/kueue/pull/2486#discussion_r1658976669

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-08T07:38:04Z

We also test against internal state of usage/quotas/limits. I will link those cleanup PRs to this issue as well.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-15T14:45:50Z

- [ ] [clusterqueue_test.go](https://github.com/kubernetes-sigs/kueue/blob/32e3c3313439091f9db58b55ec595a9925103abe/pkg/cache/clusterqueue_test.go#L97-L315)
- [ ] [flavorassigner_test.go](https://github.com/kubernetes-sigs/kueue/blob/32e3c3313439091f9db58b55ec595a9925103abe/pkg/scheduler/flavorassigner/flavorassigner_test.go#L1954-L1957)

These are the (hopefully) last two remaining. See https://github.com/kubernetes-sigs/kueue/pull/2583 for a complete example of refactoring test, changing ClusterQueueSnapshot to API type, and representing cohort capacity/usage via use of a 2nd cluster queue.

### Comment by [@highpon](https://github.com/highpon) — 2024-07-20T17:19:25Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-22T13:20:27Z

Thanks for helping with the cleanup, @highpon! Will you also be fixing flavorassigner_test.go?

### Comment by [@highpon](https://github.com/highpon) — 2024-07-22T15:07:35Z

Yes! I would love to work with you on `flavorassigner_test.go` as well!

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-08-01T07:23:43Z

Hi @highpon, will you still cleanup `flavorassigner_test.go`? If not, I will see if @vladikkuzn can work on it

### Comment by [@highpon](https://github.com/highpon) — 2024-08-01T17:45:31Z

@gabesaba 
Sorry for the delay in responding!
I have now refactored the file up to the halfway point.
Three tests are failing. After fixing them, I will change the [PR](https://github.com/kubernetes-sigs/kueue/pull/2749) from Draft to Open.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-08-20T07:37:46Z

Discussed over Slack with @highpon. @vladikkuzn, could you complete the remaining cleanup please?

/assign @vladikkuzn

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-11T10:49:45Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-11-05T12:10:27Z

@gabesaba can we close this issue now?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-11-20T13:43:45Z

> @gabesaba can we close this issue now?

Missed this message when OOO. Yes, we can close it. Thank you for the cleanup!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-20T13:43:50Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2502#issuecomment-2488623860):

>> @gabesaba can we close this issue now?
>
>Missed this message when OOO. Yes, we can close it. Thank you for the cleanup!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
