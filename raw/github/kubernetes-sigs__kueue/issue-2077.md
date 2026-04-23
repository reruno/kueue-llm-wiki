# Issue #2077: [scalability] a script to automate threshold estimations

**Summary**: [scalability] a script to automate threshold estimations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2077

**Last updated**: 2024-08-02T07:40:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-26T10:06:51Z
- **Updated**: 2024-08-02T07:40:53Z
- **Closed**: 2024-07-25T14:43:20Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What would you like to be added**:

A script to automate the estimation for scalability thresholds, based on the experiment here: https://github.com/kubernetes-sigs/kueue/issues/2066#issuecomment-2079053502.

In order to make the estimations more reliable we should only use `main` branch. For that, it would be good to setup the periodic build of the main branch for perf tests.

Note: *Once the script is added, and we have data for the main branch, use it to set new values.*

**Why is this needed**:

There is no easy and reliable way to set the thresholds, it leads to flakes, and unnecessary chore.

Having an easy way to collect the data per build will also enable us to see visually if there is a drop in performance on the main branch, which isn't picked by the current automation. 

Also, we could use it to confirm our wins when we optimize the performance, by visualizing easily that there
is better performance based on historical main builds.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T10:07:42Z

/cc @alculquicondor @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-26T13:58:00Z

I don't think we should be changing the values that often.
I prefer we don't have to maintain yet another script.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T14:34:04Z

Right, there would be some maintenance cost, which makes me hesitant as well.

The idea is that currently is there is a failure it is not clear it would be not clear to me how much to bump the thresholds, and collecting the data manually takes time.

All In all, I'm ok to park it for now and see how it plays out, and invest only if bumping becomes to much chore.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-25T14:40:33Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-25T14:43:16Z

/close 
Parking the idea. It does not seem like a priority now as the tests are rather stable after a couple of bumps.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-25T14:43:21Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2077#issuecomment-2250512458):

>/close 
>Parking the idea. It does not seem like a priority now as the tests are rather stable after a couple of bumps.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-02T07:40:51Z

cross-referencing the discussion which may support re-considering adding the script: https://github.com/kubernetes-sigs/kueue/pull/2758
