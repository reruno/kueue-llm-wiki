# Issue #6915: Feature request: Support configuring Kueue to suspend a Job till told otherwise on a per job basis

**Summary**: Feature request: Support configuring Kueue to suspend a Job till told otherwise on a per job basis

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6915

**Last updated**: 2026-03-17T20:15:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@VassilisVassiliadis](https://github.com/VassilisVassiliadis)
- **Created**: 2025-09-18T14:47:27Z
- **Updated**: 2026-03-17T20:15:42Z
- **Closed**: 2026-03-17T20:15:42Z
- **Labels**: `kind/feature`
- **Assignees**: [@VassilisVassiliadis](https://github.com/VassilisVassiliadis)
- **Comments**: 28

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We would like to prevent Kueue from un-suspending any `Job` object (from the supported job types that Kueue can manage) that has some agreed upon label e.g.  `kueue.x-k8s.io/ignore: "true"`

While this label is present and its value is `true`, Kueue should skip the Job - similar to Jobs that implement `JobWithSkip` when they return `Skip()=True`. When the label is removed, or its value is set to `"false"` Kueue, should handle this Job like it normally would.

**Why this is needed**:

We are developing Kubernetes controllers that modify fields in `Jobs` and we'd like our changes to apply before Kueue decides whether to schedule them or not. For example, we're automatically setting the resource requirements of Jobs. To avoid race conditions and ensure correctness, we need a reliable but also lightweight way to prevent Kueue from un-suspending a `Job` while our controllers are still modifying it. The proposed feature will also enable users to reliably keep a Job suspended on demand, since Kueue currently controls `spec.suspend` for Jobs it manages.

This suggestion:

- Eliminates race conditions between our controllers and Kueue’s reconciler
- Has a small surface area and is thus unlikely to cause any problems
- It is completely opt‑in and explicit thereby easy to document

**Alternatives we considered**:

- **Do nothing**
  Our Controllers may modify the Job object several times which will trigger Kueue to process the Job and modify the associated Workload object several times. In the worst case scenario, Kueue will also schedule a Job before our controllers finish updating it and the Job may behave in an unexpected way.

- **Omit `kueue.x-k8s.io/queue-name`**  
  Doesn’t work where a default queue is configured, or where policy enforces that all Jobs must carry a queue name.

- **External AdmissionCheck controller that sets its admission check state to Retry while some label or equivalent is set in the Job object**  
  Heavyweight for this use case, requires spinning up extra Pod and having RBAC to add an AdmissionCheckController to one or more ClusterQueues.

- **Set an invalid queue name first, then swap to the real one**  
  Hacky and error‑prone. Also, to an external observer the Jobs will appear like they are malformed. This could introduce problems in environments where Jobs are expected to have correct names (e.g. namespaces with Kyverno policies or equivalent).

- **Use mutating webhooks instead of controllers to ensure Jobs are updated before Kueue's reconciler sees the object**  
  Guarantees ordering but is not a lightweight approach. This would add latency to the create path and would require additional RBAC to deploy.

- **The external controllers also monitors and updates the associated Workload object by setting `Workload.spec.status.active=false`, then back to `true` after it finishes modifying the Job object**  
  Prevents admission, but requires writing to a Workload owned by Kueue. It also, requires additional RBAC to external controllers. It has a large surface area and is twice as resource hungry as the external controller.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-18T14:56:48Z

IMO the right approach would be to implement https://github.com/kubernetes/kubernetes/issues/121681.

If this was implemented we could set an extra gate for suspend and kueue would only resume if all fields were empty.

With a boolean we are limited in what we can do.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-18T14:58:16Z

I'll leave this to @gabesaba, @mimowo or @tenzen-y if they are open to a workaround though.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-09-18T15:07:56Z

Thank you for your suggestion! You helped me realize that my original description was ambiguous. Basically, I'd like to have a way to temporarily prevent Kueue from acting on any Job type that Kueue supports, not just batchv1/Job, but also custom workloads like PyTorchJob and future types such as TrainJob. I've updated the wording of the issue to reflect that.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T15:45:15Z

Just to verify my understanding: effectively, what we're asking for is the ability for Kueue to **ignore** workloads.

For example, this would be similar in outcome to submitting a Job (e.g., a `batchv1.Job`) with the annotation `kueue.x-k8s.io/queue-name: non-existent-queue`, where the queue name does not correspond to any existing `LocalQueue`. This results in an "Inadmissible" workload, like so:

```yaml
status:
  conditions:
  - lastTransitionTime: "2025-09-18T15:33:59Z"
    message: LocalQueue non-existent-queue doesn't exist
    observedGeneration: 1
    reason: Inadmissible
    status: "False"
    type: QuotaReserved
```

Later, when conditions are right, we could change the label to reference a valid queue name, which would then allow the workload to be admitted:

```bash
kubectl label job my-job 'kueue.x-k8s.io/queue-name=default' --overwrite
```

(or similar).

To be clear, I’m not suggesting this as a workaround, though if it works, great! I’m simply using this example to confirm my understanding of the desired behavior.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-18T16:07:03Z

Correct!

> Set an invalid queue name first, then swap to the real one
Hacky and error‑prone. Also, to an external observer the Jobs will appear like they are malformed. This could introduce problems in environments where Jobs are expected to have correct names (e.g. namespaces with Kyverno policies or equivalent).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T16:11:10Z

What about just deativating the workloads? Setting `.spec.status.active=False`?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T16:16:22Z

> What about just deactivating the workloads, setting `.spec.status.active=false`?

Does Kueue support a Job level configuration, for example an annotation or label, that causes the corresponding Workload to be created in an inactive state, effectively `.spec.status.active=false`?

UPD: to expand on my comment ^

Typically, users don’t interact with Workloads directly, so it could be helpful to provide a signal at the Job level, via an annotation, label, or similar, to create the corresponding Workload in an inactive state.

Alternatively, just thinking out loud, could we configure CQ selectors to exclude certain Jobs? If I understand correctly, today we can already do this for namespaces. Maybe that’s an approach worth considering as well.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-09-19T10:17:16Z

We'd prefer the instructions to temporarily skip a Job to live solely inside the definition of the Job. This way, users will not require any extra RBAC than what they already have (I.e. to create Jobs).

In a way, this is a similar to setting the return value of `JobWithSkip.Skip()` at the granularity of individual jobs but without having to touch Kueue's code.

We also thought about having the external controllers monitor and update the `Workload` objects (bullet 6) but I worry that this might cause issues. For example, cluster admins may be unwilling to let ServiceAccounts have RBAC for patching Workload objects. Also, increasing the objects that our controllers would monitor/patch increases the chances of something going wrong (race conditions, or accidental object updates).

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-19T16:48:41Z

> Alternatively, just thinking out loud, could we configure CQ selectors to exclude certain Jobs? If I understand correctly, today we can already do this for namespaces. Maybe that’s an approach worth considering as well.

To expand on this idea, here is a concrete sketch:
```yaml
kind: ClusterQueue
metadata:
  name: demo
spec:
  namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: my-namespace
  jobSelector:   # Proposed API
    matchExpressions:
      - key: kueue.x-k8s.io/scheduling-hold
        operator: DoesNotExist
```

The `jobSelector` behaves equivalently to `namespaceSelector` and is configured by a Kueue administrator. End users can then add or remove labels on their Job or Workload to control scheduling participation, for example to include it in processing or to exclude, hold it from Kueue’s scheduling cycle. 

**This approach both provides the requested functionality and aligns with Kueue’s established job selection paradigm.**
Granted, this remains a thinking out loud proposal, and we will need to work out edge case safeguards, for example preventing users from marking already processing jobs as ineligible.

WDYT?

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-09-22T09:45:30Z

> This approach both provides the requested functionality and aligns with Kueue’s established job selection paradigm.

Thank you, this could work for us.

>  Granted, this remains a thinking out loud proposal, and we will need to work out edge case safeguards, for example preventing users from marking already processing jobs as ineligible.

I had the same concerns about this new featue. I think the way to go about is to only respect the user instructions if Kueue hasn't already started managing the object. For example, a combination of annotations/labels could help achieve this effect or a perhaps having a rule that Kueue will only respect the user instructions if Kueue hasn't already created a Workload for the object.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-22T15:06:20Z

> For example, a combination of annotations/labels could help achieve this effect or a perhaps having a rule that Kueue will only respect the user instructions if Kueue hasn't already created a Workload for the object.

I was thinking along the same lines initially. Kueue already enforces some well-known “Kueue constants” via webhooks for Kueue-managed Jobs, so using labels/annotations feels natural. But this case is a bit different.

For fixed, well-known keys like `kueue.x-k8s.io/queue-name`, enforcement is straightforward: the Job is the single point of mutation, so the webhook can assert presence and prevent changes. In the proposal here, responsibility is split: the ClusterQueue(CQ) defines a label selector, while the Job sets the label key/value. Those can change independently, possibly by different personas, which makes strict webhook validation much trickier.

The good news is, I don’t think we need heavy validation. Similar to the CQ namespace selector, once a Job has been processed and a corresponding Workload exists, we already have an ownership link between them. That relationship can be tracked regardless of later changes to the CQ selector or the Job’s labels. Conversely, if a Job hasn’t been processed yet, the GenericJob reconciler can simply ignore it when it no longer matches the selector. This seems to require only minor changes and, importantly, stays consistent with established Kueue patterns.

I’d appreciate maintainers’ feedback to confirm we’re not overlooking edge cases. If this direction sounds reasonable, I can put together a small prototype to validate the approach.

WDYT?

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-10-15T10:39:26Z

@mimowo what do you think about @ichekrygin 's suggestion ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T11:12:07Z

I think `kueue.x-k8s.io/ignore: "true"` makes sense, however, I'm wondering if there is a better approach which could also address this issue, basically `kueue.x-k8s.io/active` which could be translated into activation / deactivation of the Job. This would be nice, as it would allow use control the Workload's status.active at the level of Job's API. 

The similar proposal was put forward in this PR https://github.com/kubernetes-sigs/kueue/pull/7199, but I withdraw for now due to some solvable complications, see https://github.com/kubernetes-sigs/kueue/pull/7199#discussion_r2428099620

Please let me know if  `kueue.x-k8s.io/active`  would also resolve your use cases, if so this seems like a more generic approach to me.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-10-15T15:46:58Z

If I understand this correctly then this is exactly what I want !

Could you double check that what I describe below is consistent with what you were thinking ?

---

As a user, I create a Job with the label `kueue.x-k8s.io/active=False` to place it in a "suspended" state. This label is indicating to Kueue that I don't want the Job to be processed yet. In turn, Kueue effectively ignores the Job.

When I'm ready for the Job to be eligible for scheduling, I simply patch the Job object by updating the label `kueue.x-k8s.io/active` to the value `True`. Alternatively, removing the label has the same effect.

After I set the label to True (or just remove it), Kueue detects the change, creates a `Workload`, and begins processing the Job like any other.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T15:51:47Z

Exactly. It is also better capturing the intention I think `kueue.x-k8s.io/ignore`  would suggest "execute the Job bypassing quota checks in Kueue".

With `kueue.x-k8s.io/active=false` the Kueue will create the Workload object in "inactive" state. It will be activated when `kueue.x-k8s.io/active` is removed.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-10-15T15:55:14Z

I think this would work just fine for my use case.

I'm imagining that if I happen to modify my object while it has the `kueue.x-k8s.io/active=false` label (for example to update how many GPUs it requests), Kueue will still propagate those changes to the Workload. However, since the `Workload` is still "inactive" then the job won't be scheduled.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T16:04:13Z

Correct. Still, it would be great to have a small KEP on the Job activation.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T16:04:32Z

cc @tg123

### Comment by [@tg123](https://github.com/tg123) — 2025-10-15T17:26:46Z

we first introduced interface as we did so many other customizations in our crd plugin 
and we don't want to hack any of core components of kueue

label is a good idea 
lets work on kep together

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-10-16T07:44:30Z

Would you like me to put together a draft of a KEP for `kueue.x-k8s.io/active` ?

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-10-16T11:29:51Z

@mimowo @tg123 I wrote a draft for the KEP here: https://github.com/kubernetes-sigs/kueue/pull/7295 let me know what you think!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T06:27:48Z

Added to https://github.com/kubernetes-sigs/kueue/issues/7245 (tentatively)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T07:22:46Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-14T07:38:06Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T18:55:06Z

/remove-lifecycle rotten

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T18:55:10Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-11T18:55:16Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6915#issuecomment-4041436946):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T18:56:01Z

/assign @VassilisVassiliadis
