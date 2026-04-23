# Issue #6774: [FS] Workloads submitted to 0 weight ClusterQueue may end up in infinite preemption cycle

**Summary**: [FS] Workloads submitted to 0 weight ClusterQueue may end up in infinite preemption cycle

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6774

**Last updated**: 2025-09-22T12:34:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-09T14:57:32Z
- **Updated**: 2025-09-22T12:34:18Z
- **Closed**: 2025-09-22T12:34:18Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 24

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
When there are two CQs with weight 0 that point to the same Cohort, Kueue may end up in an infinite cycle of preemption. This is because the DRS share is always `maxInt`, no matter how many Workloads are submitted/preempted to a given CQ

I've also reproduced this with a different configuration by setting CQs' weights to a large number (10mils) so CQ's `.weightedShare` doesnt change after preemption. This seems to be the core of the issue

**What you expected to happen**:
No infinite preemption cycle

**How to reproduce it (as minimally and precisely as possible)**:
Manifest for queue's hierarchy:

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default-flavor
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: Cohort
metadata:
  name: "top-cohort"
spec:
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 8
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort-cq-a"
spec:
  namespaceSelector: {}
  cohort: "top-cohort"
  fairSharing:
      weight: "0"  #1
  preemption:
    reclaimWithinCohort: Any
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 0
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort-cq-b"
spec:
  namespaceSelector: {}
  cohort: "top-cohort"
  fairSharing:
    weight: "0"  #1
  preemption:
    reclaimWithinCohort: Any
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 0
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "best-effort-lq-a"
spec:
  clusterQueue: "best-effort-cq-a"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "best-effort-lq-b"
spec:
  clusterQueue: "best-effort-cq-b"
```

Job manifest: 
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: best-effort-b-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: best-effort-lq-b
spec:
  parallelism: 1
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: alpine
        command: ["/bin/sleep", "infinity"]
        resources:
          requests:
            cpu: 4
      restartPolicy: Never
```

1. Submit 2 jobs to the CQ-A
2. Submit a job to the CQ-B
3. Observe that only one job from CQ-A is running and there's infinite preemption cycle between the second job from CQ-A and the job from CQ-B 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-12T05:51:08Z

One of the way to solve this issues is to slightly change FairSharing API and prevent setting `0` as `.fairSharing.weight`. Instead user would use `1m` to indicate a CQ/Cohort has the lowest weight possible. I've already discussed it with @gabesaba and agreed on this approach 

Since this would be change that breaks backward compatibility we would need to create a conversion webhook

cc @mimowo @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T06:05:41Z

Are there alternatives which were explored? 

Im not sure this is a role of convertion webhook. I would rather say that if 0 is illegal then we deprecated it as a possible value in 0.14 and drop in v1beta2. Then we could validate against 0 with a proper message. Also, it will allow us to properly support 0 one day if we need to.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T06:29:14Z

Or maybe i misunderstood the proposal, Is it to have a webhook between v1beta1 and v1beta2, converting 0 to 1, and validate against 0 in v1beta2. In v1beta1 we would just deprecated? 

I guess it makes sense, but can we say there are no use cases requiring 0, and we can cover them all with 1? 

Im not clear about it, maybe it is a good topic to ask on wg-batch.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-12T06:39:08Z

> Or maybe i misunderstood the proposal, Is it to have a webhook between v1beta1 and v1beta2, converting 0 to 1, and validate against 0 in v1beta2. In v1beta1 we would just deprecated?

Yes, that's what I meant

> I guess it makes sense, but can we say there are no use cases requiring 0, and we can cover them all with 1?


0 weight was to indicate the lowest priority of a CQ/Cohort, and now users would need to use `1m`. Surely there are some edge cases (e.g. if users previously set `1m` for some CQ/Cohort to distinguish it from `0` weight CQ/Cohort than it doesn't work anymore) but I think those can be resolved by some adjustments by admins
 
> Im not clear about it, maybe it is a good topic to ask on wg-batch.

Sure, I'm happy to discuss this

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T06:53:13Z

Ok, so deprecating and validating against is an option.

The issue reminds me some other similar infinite preemption loops from the past which we solved by using deterministic tie-breaker (timestamps or UIDs). iiuc here, similarly, we need tie-breaking because both CQs get the same DRF=maxInt. 

Could you explain why this approach wouldn't work in this case? I think it would be useful to learn this nuance for better understanding of FS.

### Comment by [@amy](https://github.com/amy) — 2025-09-13T00:13:37Z

Linking this potentially relevant issue. Its not preemption cycling per se. But it is about candidate ordering as well as issues with rounding fractional values up to 1 for large enough clusters: https://github.com/kubernetes-sigs/kueue/issues/6621

So I know that rounding up is what we do today after: https://github.com/kubernetes-sigs/kueue/pull/6617
Just haven't gotten around to quantifying whether this solution is sufficient on our end given the immediate need to fix guarantee reclamation that this PR fixed.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-15T07:29:23Z

Another option is to not allow CQs/Cohorts with 0 weight to issue preemptions. However, I prefer the option of making 0 weight an invalid value, as I think this will result in simpler code and easier to understand API.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T07:33:13Z

My question is if this is solvable easily with a better / deterministic tie-break strategy. If this would work I think the code could remain simple as well. 

Strengthening validation is often hard and requires time for the deprecation process to sink.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-15T08:38:29Z

I've also tested another scenario and hit the same issue: I've set the weights to a large number (e.g. 10mils) and reproduced the same cycle. It seems like the infinite cycle appears whenever the preemption of a Workload doesn't change its CQ's `weightedShare`. Hence I'll rather focus on fixing the core of the issue rather than making `0` weight invalid

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-15T09:31:33Z

I've found the root cause of the problem. What happens is:
1. Two workloads from CQ-A are running
2. Workload from CQ-B comes and preempts one from CQ-A
3. In the next scheduling cycle there are two Workloads, one from CQ-A and one from CQ-B
4. Scheduler runs FS tournament and determines that CQ-A is a winner - this is a problem
5. Then workload from CQ-A is admitted and the cycle repeats

Now, why it happens? This is because of how DRS are calculated in this function: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/fair_sharing_iterator.go#L190-L218

With 0 (or very large) weight, admission of a single Workload doesn't impact DRS value, so
Before admitting second Workload, CQ-A's DRS is `maxInt` (or 1) and it's the same after simulating admission of the second CQ-A's Workload. For CQ-B the result of simulation is the same, DRS is `maxInt` (or 1). Then the ordering fallbacks to creation timestamp where workload from CQ-A wins

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-15T09:33:11Z

So this is related to the discussion @amy started: https://github.com/kubernetes-sigs/kueue/issues/6621
We either need better tie-breaker mechanism or prevent scheduler from leading to tie in the first place (maybe by some artificial change in DRS value if the admission simulation hasn't change it before)

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-15T09:45:52Z

Alternatively, since the impact of the preemption is negligible (the DRS value remains the same) maybe Kueue shouldn't preempt the workload from CQ-A in the first place. This happens because condition of `LessThanOrEqualToFinalShare` strategy are met (the final share is equal) I'm hesitant if we should apply this strategy when preempting. IIUC, the main motivation behind this strategy was to fairly reclaim borrowed quota: if there are two best effort CQs, then high-prio CQ should reclaim quota from those best effort CQs equally. And when it comes to preemption the intended main strategy was `LessThanInitialShare`. 

So my alternative proposal is to create a separation of responsibilities for those two strategies:
- `LessThanOrEqualToFinalShare` should only be used for fair quota reclamation
- `LessThanInitialShare` should only. be used from fair preemption when borrowing quota

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-15T10:47:33Z

> We either need better tie-breaker mechanism or prevent scheduler from leading to tie in the first place (maybe by some artificial change in DRS value if the admission simulation hasn't change it before

We may consider revisiting fractional FS score (https://github.com/kubernetes-sigs/kueue/pull/6617#discussion_r2285066030). This will resolve at least the problem of high weights/rounding. I don't think that the original conclusion of the discussion, that preemption storms will be caused by fractional scores, is correct. In fact, I think it may help prevent preemption storms/unstable preemptions in the case of high weights.

> So my alternative proposal is to create a separation of responsibilities for those two strategies

Maybe, but how to differentiate the cases? I think that this becomes quite complex, especially in conjuction with hierarchical cohorts. And a conceptually complex API for the user. I prefer a solution where these strategies result in a stable state after some number of preemptions. I think that this can be accomplished by implementing several of the options above:

1) prevent 0-weight preemption storm
  a) make 0-weight illegal OR 
  b) prevent 0-weight nodes from issuing preemptions (a simple, hacky way is to return false when preemptorNewShare is MaxInt [here](https://github.com/kubernetes-sigs/kueue/blob/bf2ad4a40a21e50bdd11452ec0ecc1bf7d60080e/pkg/scheduler/preemption/fairsharing/strategy.go#L35-L43))
2) fix tiebreak issue, preferably by getting rid of rounding (see the very first part of this comment)

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-15T11:32:59Z

I agree that a lot of issues come down to lack of precision with the current way of calculating DRS. However, I synced with @mimowo offline and we came up with a way of keeping the same API as now and improving precision. 

Currently when comparing two Workloads we calculate DRS which is:
$DRS_1=\frac{\frac{borrowed_1}{lendable_1}}{weight_1}  \gtreqless  \frac{\frac{borrowed_2}{lendable_2}}{weight_2}  = DRS_2$ 
This comes with two divisions which introduce loss of precision. We could also rewrite those in an equivalent form that eliminates division:
$DRS_1=\frac{\frac{borrowed_1}{lendable_1}}{weight_1} = \frac{borrowed_1}{lendable_1 \cdot weight_1} \gtreqless \frac{borrowed_2}{lendable_2 \cdot weight_2} = DRS_2 <=> borrowed_1 \cdot lendable_2 \cdot weight_2  \gtreqless borrowed_2 \cdot lendable_1 \cdot weight_1$

The results are equivalent but we instead of dividing we now multiply.

Now, there's no a single static value for a candidate, but it dynamically changes while still keeping total order.
(Of course there are edge cases with 0 weight, but those can be easily solved and I would rather show in a PR.)

We still expose the same DRS as previously but the internal calculation differ. This is desirable as we would prefer not to change existing API but the value on its own doesn't determine what happens in case of tie-break. To fully determine what should be the order of candidates a user would need to compare weights, lendable and borrowed quota. This is however not a regression as currently DRS on it's own is non-decisive (by definition) in case of tie-breaks 

/cc @mimowo @gabesaba @amy

### Comment by [@amy](https://github.com/amy) — 2025-09-15T16:44:49Z

I like this: https://github.com/kubernetes-sigs/kueue/issues/6774#issuecomment-3291706679

Regarding super high precision. I remember chatting with @pajakd at the time, and why the value wasn't a float64 in the first place. He mentioned the potential for preemption cycling for super high precision. Want to make sure this wouldn't introduce another kind of cycling. 

@PBundyra after you make the PR, can you assign me as reviewer for a pass? 🙏

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T16:56:29Z

Nice, we also talked with @PBundyra that with that approach we could potentially eliminate this hack: https://github.com/kubernetes-sigs/kueue/pull/6617 (but requires a careful check).

### Comment by [@amy](https://github.com/amy) — 2025-09-15T17:00:03Z

What I mean is, whether its float64 or its borrowed * lendable * weight, both seem like the same category where the end result is a "high precision number".

Will there be preemption cycling for high precision numbers? Where A & B are marginally different, but end up preempting each other? It seemed like that's why you originally had the int "bucketing" solution.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T17:08:51Z

> What I mean is, whether its float64 or its borrowed * lendable * weight, both seem like the same category where the end result is a "high precision number".

It is similar conceptually indeed, but keeping it in the multication form allows us to resolve the cases when weight=0.

> Will there be preemption cycling for high precision numbers? Where A & B are marginally different, but end up preempting each other? It seemed like that's why you originally had the int "bucketing" solution.

I don't think this was ever a "bucketing" solution by design. Probably more of an attempt to avoid surfacing floats in the to the API layer. https://github.com/kubernetes-sigs/kueue/tree/main/keps/1714-fair-sharing. I think it makes sense to assume that user does not need to see the super high resolution, but for Kueue internals, we sometimes use tie-breaks which aren't really surfaced to the user, like for example UIDs.

### Comment by [@amy](https://github.com/amy) — 2025-09-15T17:21:24Z

Mainly want to make sure that `borrowed * lendable * weight` doesn't also result in preemption cycling. If it doesn't, LGTM!

Could there be a situation where there's 2 workloads with marginally different DRS values that end up continuously preempting each other?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T17:33:44Z

That is a valid concern to have about the two interleaving workloads. 

This was actually the problem with buckets, that the tie break continues to resolve the Equal in opposite directions each time.

This comes down to the FinallShare LessOrEqual semantics. because this is FinalShare, then the preemption should not be triggered as long as the Less case (strict inequality) happens.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-16T15:03:26Z

> Could there be a situation where there's 2 workloads with marginally different DRS values that end up continuously preempting each other?

@gabesaba Created a formal proof that this won't happen - we'll put in the documentation soon. However the proof had assumption that for CQ's DRS changes on preemption/admission. While theoretically this is correct, our implementation violated this assumption because of the roundings (and 0 weight but that's a bit different story).

Now let's compare high vs low precision calculation and bucketing ints.
With bucketing ints there are a lot of preemption when using `LessThanOrEqualToFinalShare` strategy because of the `Equal` factor, just as @mimowo mentioned. Bucketing also breaks the formal proof and leads to preemption cycles. We could eliminate that by adding higher precision one way or another (this is an implementation detail). Whenever `LessThanOrEqualToFinalShare` is used this is a desirable solution.

There's also point that @tenzen-y made here: https://github.com/kubernetes-sigs/kueue/pull/6617#discussion_r2286363618 Bucketing ints prevents from `LessThanInitialShare` preemptions that rely on marginal (order of magnitude of rounding error) differences. This is the case only when `LessThanInitialShare` is the only present strategy - if `LessThanOrEqualToFinalShare` is also present the preemption would be issued anyway. Having said that, even with the greater number of `LessThanInitialShare` preemption, there would be no preemption cycles and the algorithm would converge to a stable state.

To sum up, introducing greater precision fixes current bugs that lead to infinite preemption cycles, and it lowers number of preemption whenever `LessThanOrEqualToFinalShare` is present. If `LessThanOrEqualToFinalShare` is not part of a config, higher precision can lead to greater number of preemption, but those preemption converge to a stable state, there is no infinite preemption cycles. Given that by default Kueue uses `LessThanOrEqualToFinalShare` I think we should introduce greater precision.

### Comment by [@amy](https://github.com/amy) — 2025-09-16T18:16:52Z

@PBundyra thanks for the writeup! Interested to check out the proofing writeup. Please tag me to review doc/code changes when relevant. Thank you! 🙏

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-18T11:34:40Z

I've synced with @gabesaba that will take over the implementation
/assign @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T12:12:06Z

I think as a follow up of increasing the resolution we can also drop this one: https://github.com/kubernetes-sigs/kueue/pull/6617
