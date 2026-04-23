# Issue #3215: Add resource limits into ResourceGroup of ClusterQueue/Cohort

**Summary**: Add resource limits into ResourceGroup of ClusterQueue/Cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3215

**Last updated**: 2025-03-13T08:14:11Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@FillZpp](https://github.com/FillZpp)
- **Created**: 2024-10-12T02:59:34Z
- **Updated**: 2025-03-13T08:14:11Z
- **Closed**: 2025-03-13T08:14:08Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Maybe a `limits` field that can be added into `ResourceGroup` struct for `ClusterQueue` or the new `Cohort` CRD.

Like this:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
spec:
  cohort: "foo"
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    limits:
      # maybe also limits to cpu/memory
      nvidia.com/gpu: 16
    flavors:
    - name: "group-0"
      resources:
      - name: "cpu"
        nominalQuota: 64
      - name: "memory"
        nominalQuota: 128Gi
      - name: "nvidia.com/gpu"
        nominalQuota: 8
    - name: "group-1"
      resources:
      - name: "cpu"
        nominalQuota: 32
      - name: "memory"
        nominalQuota: 64Gi
      - name: "nvidia.com/gpu"
        nominalQuota: 4
```

**Why is this needed**:

What we want is that even we have several flavors in a `ResourceGroup` which all have different nominalQuota/borrowingLimit and can borrow from another ClusterQueue with the same cohort, but we still need an overall limit for this `ResourceGroup` including all flavors used in it.

Does it make sense?

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-10-14T03:33:41Z

Hi, @FillZpp , is borrowingLimit enough for the use cases?

### Comment by [@FillZpp](https://github.com/FillZpp) — 2024-10-14T04:04:47Z

> Hi, @FillZpp , is borrowingLimit enough for the use cases?

Unfortunately, no. Since I have multiple flavors with different borrowingLimit, I still need an overall resource limit of this ClusterQueue, which is probably less than the sumary of all flavors' nomialQuota+borrowingLimit.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-10-14T06:30:53Z

Are limits larger than the sum of all flavors' nomialQuota?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-14T06:38:02Z

I suppose I see the use case, but in the example `resourceGroups.limits.gpu=16` is more than the total capacity of the flavors `12`. And there is no cohort, so IIUC the limit wouldn't be reached anyway. So, I'm not sure if the example is representative of your use case, is it?

### Comment by [@FillZpp](https://github.com/FillZpp) — 2024-10-14T06:59:53Z

@mimowo Oh, it does have a cohort and can borrow from another clusterqueue. It's just I simplified the yaml. Sorry for the confusion...

@KunWuLuan Not necessarily. Let's say maybe it has a total limit, but I can't clearly split its percentage for each flavors from the start, even for the nomialQuota. So that when some of the previous flavor's nomialQuota has been borrowed by another CQ, it can use more of the next flavor as possible, instead of reclaiming the borrowed resource.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-12T07:17:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-11T07:48:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-13T08:14:02Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-13T08:14:08Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3215#issuecomment-2720326722):

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
