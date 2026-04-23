# Issue #6022: Allow for 0 flavors in a ClusterQueue

**Summary**: Allow for 0 flavors in a ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6022

**Last updated**: 2026-03-27T15:28:56Z

---

## Metadata

- **State**: open
- **Author**: [@LarsSven](https://github.com/LarsSven)
- **Created**: 2025-07-18T14:29:32Z
- **Updated**: 2026-03-27T15:28:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
When you try to create the following ClusterQueue:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "container-runtime"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
    - coveredResources: ["cpu_cores", "memory", "disk"]
      flavors: []
```

You get: `Invalid value: 0: spec.resourceGroups[0].flavors in body should have at least 1 items`. It would be nice to be able to deploy the ClusterQueue mentioned above without the validation failing.

**Why is this needed**:
We have a setup where we have a microservice that is dynamically adding/removing flavors based on requests of new flavors registering themselves. It would be really helpful to be able to deploy an empty ClusterQueue that the microservice can then patch new flavors into on the fly.

Making the microservice also deal with creating a ClusterQueue when the first flavor registers itself creates a lot of opportunities for race conditions, and creates issues if someone is submitting workloads when a flavor is still yet to register itself. We would prefer if a workload would then be awaiting a flavor joining the ClusterQueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T09:33:45Z

I see the use-case of being able to adjust the flavors / RGs by automation, and sometimes stop.

However, IIUC such a CQ should not be able to admit workloads. So, I would like to make it inactive (Active = False). See how we do it in here for other soft validation cases: https://github.com/kubernetes-sigs/kueue/blob/593af625fb1100df9d9ee526f7d44e3a1ba8332f/pkg/cache/cache.go#L347

For you use case, would it work, instead of removing all flavors to just make the CQ stopPolicy=Hold?

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-07-21T09:47:25Z

Thanks a lot for the PR!

> For you use case, would it work, instead of removing all flavors to just make the CQ stopPolicy=Hold?

Could you clarify what you mean with this? We don't really have a usecase for completely stopping the Queue. Our main usecase is that we can instantiate a ClusterQueue empty, such that automation can add flavors on the fly. In practice, Flavors will always have been added by the time the workloads start coming in, so we don't care too much about the behaviour of the CQ when there are no flavors registered to it, as long as we can instantiate it empty and then dynamically add a few flavors.

The behaviour of making the CQ not admit workloads when there are no flavors seems like the logical behaviour indeed, but I'm not entirely sure what the question is. What would the default behaviour be with flavors = 0 that would be problematic without stopPolicy=Hold?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T09:55:18Z

> I'm not entirely sure what the question is. What would the default behaviour be with flavors = 0 that would be problematic without stopPolicy=Hold?

No, my question was: Do you need to use zero flavors - would it work for you instead to set `.spec.stopPolicy=Hold`, keeping some flavors, but the hold will prevent admission?

### Comment by [@mayooot](https://github.com/mayooot) — 2025-07-21T10:04:16Z

> > I'm not entirely sure what the question is. What would the default behaviour be with flavors = 0 that would be problematic without stopPolicy=Hold?
> 
> No, my question was: Do you need to use zero flavors - would it work for you instead to set `.spec.stopPolicy=Hold`, keeping some flavors, but the hold will prevent admission?

I think that doesn't really align with human intuition -- especially for people like me who aren't very familiar with `Kueue`.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-07-21T10:06:12Z

We do need 0 flavors yeah.

We need it for initial infrastructure setup. Our workflow is essentially as follows:
1. Create Kubernetes cluster
2. Deploy Kueue
3. Create ClusterQueue with 0 flavors
4. Deploy application that dynamically adds new flavors to the clusterqueue
5. Spin up a few flavors, that register themselves with the application in step 4, which then adds the flavors to the ClusterQueue
6. Workloads start coming in that schedule themselves onto the flavors.

So at no point are we holding workloads because of 0 flavors. By the time we get workloads, we already have flavors that registered themselves. We just don't want the application in step 4 to be responsible for CQ creation and want to move that to infrastructure setup, because CQ creation when also trying to add new flavors gets very racy very easily.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-07-21T10:07:22Z

Right now we solve it through deploying the following manifest at infrastructure setup:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "container-runtime"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
    - coveredResources: ["cpu_cores", "memory", "disk"]
      flavors:
        - name: "blank"
          resources:
            - name: "cpu_cores"
              nominalQuota: 0
            - name: "memory"
              nominalQuota: 0
            - name: "disk"
              nominalQuota: 0
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-19T10:47:52Z

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

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-10-24T14:16:22Z

Would there be a possibility for me to pick up this MR?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-23T14:38:18Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-24T04:27:55Z

/remove-lifecycle rotten

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-27T14:55:30Z

> Would there be a possibility for me to pick up this MR?

Yes please free to take this over.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-25T15:02:59Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-27T15:28:53Z

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
