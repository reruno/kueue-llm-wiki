# Issue #8036: [TAS] Cleanup `findTopologyAssignment` and related functions

**Summary**: [TAS] Cleanup `findTopologyAssignment` and related functions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8036

**Last updated**: 2026-04-16T05:35:49Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-12-02T11:01:30Z
- **Updated**: 2026-04-16T05:35:49Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@ShaanveerS](https://github.com/ShaanveerS)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
This list is not exhaustive, please see if you can see any room for cleanups yourself following best coding practices:

- Check if `fillInCountsHelper` needs to return 5 ints or maybe the code could rely on the `domain` argument: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L1397
- Add a new struct that would store the state of the algorithm so we can put all [this code](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L667-L734) to some kind of initialization function and avoid passing e.g. 9 parameters to `fillInCounts` func. Add helper function if needed.
- Group all functions that take `*kueue.PodSetTopologyRequest` as a parameter together so they're not scattered across the whole file
- See if we reduce the number of [parameters in the domain struct](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L71-L84) so the functions are a bit cleaner

**Why is this needed**:

## Discussion

### Comment by [@kshalot](https://github.com/kshalot) — 2025-12-02T14:17:00Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:42:12Z

/priority important-longterm

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-12T13:58:09Z

Of the four things explicitly mentioned in the issue:
1. Addressed in #8491.
2. This change is possible and easy, but seemed low impact to me at this moment. Yes, it will reduce the amount of arguments to one function call, but won't help other functions in further phases in the algorithm (for example [this](https://github.com/kubernetes-sigs/kueue/blob/e83fce915d00d098c5b1280aa19e9bf03fafc131/pkg/cache/scheduler/tas_flavor_snapshot.go#L807)). It's a very simple change and can be readily done, but I think it would be better to come back to this in the context of a broader refactor. Wrapping the initialization in a separate function might be good for readability, OTOH the state is only used in this one function, so it naturally reads top to bottom when inlined. Potentially, creating a high level function that does `phase2(phase1(initialize(...)))` could be worthwhile, but might require more changes than just moving code around.
3. Addressed in #8448.
4. I took some time to understand how the algorithm works, but I was hesitant to introduce changes here as the `domain` struct fields are all used and in many many places in the code so a refactor is tricky, as it has to cover a lot cases.

So the low hanging fruit refactors are done (some smaller not listed refactors were also part of the PRs where applicable), but 2 & 4 (and possible other cleanups) are still possible, so I'd keep this issue open. At this point I feel they would take too much time off the higher priority issues I'm working on, so I'd park this here since there is no work lost (and I wouldn't classify the time it took to dive into the algorithm wasted effort) and pick it up/leave it to be picked up sometime later.

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-12T13:58:16Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-12T14:57:47Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-16T05:31:31Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-16T05:31:37Z

/assign @ShaanveerS

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-16T05:31:40Z

@tenzen-y: GitHub didn't allow me to assign the following users: ShaanveerS.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8036#issuecomment-4257594085):

>/assign @ShaanveerS 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ShaanveerS](https://github.com/ShaanveerS) — 2026-04-16T05:35:46Z

/assign
