# Issue #6121: `assignFlavor` for a Workload — Runtime Complexity Analysis

**Summary**: `assignFlavor` for a Workload — Runtime Complexity Analysis

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6121

**Last updated**: 2025-12-18T18:46:12Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-07-21T16:25:29Z
- **Updated**: 2025-12-18T18:46:12Z
- **Closed**: 2025-12-18T18:46:10Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

The current `assignFlavor` logic in Kueue involves nested loops, which can lead to high runtime complexity. Here's a breakdown:

#### 🔍 Code Walkthrough

* [`for` each PodSet (P) in `Workload.TotalRequests`](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L440)

    * [`for` each Resource (R) in the PodSet](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L469)

        * [`findFlavorForPodSetResource`](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L553)

            * [`getResourceGroup`](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L560)

                * Loop through all [`ResourceGroups`](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/clusterqueue_snapshot.go#L67)
                * Check if the requested resource is in the group
            * [`for` each Flavor (F) in the group](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L579)

                * Filter based on taints
                * [`for` each Resource (R)](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L614) evaluate capacity

#### 📈 Complexity

Let:

* `P` = number of PodSets in a workload
* `R` = number of resources per PodSet
* `F` = number of flavors in a resource group

The worst-case runtime is:

> **O(P × R × F × R) → O(P × R² × F)**

This quadratic scaling with respect to `R` (resources) and linear scaling with `P` and `F` can grow quickly.

#### 🧮 Example Scenarios

* **Typical**: 3 PodSets × 4 resources × 3 flavors → `3 × 4² × 3 = 144`
* **One more flavor**: 3 × 4 × 4 → `3 × 4² × 4 = 192`
* **More resources**: 3 × 6 × 5 → `3 × 6² × 5 = 540`

These numbers can easily climb into the hundreds per workload, especially in setups with custom resources or more flavors.

#### 🛠 Suggestion

This may not be an issue today since `P`, `R`, and `F` are typically small. But the current design could be a bottleneck as workloads become more complex.

Possible improvements to consider:

* Cache repeated computations
* Reduce redundant iteration or short-circuit where possible
* Avoid cross-product loops by restructuring flavor resolution logic

Whether this justifies a refactor depends on real-world impact. I'm flagging it as something worth discussing or keeping in mind.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-19T16:48:53Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-18T17:46:13Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-18T18:46:05Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-18T18:46:12Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6121#issuecomment-3671715058):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
