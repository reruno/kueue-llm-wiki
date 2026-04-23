# Issue #5897: Evaluate the "WorkloadResize" approach to DynamicallySized Jobs (ResizeRequests)

**Summary**: Evaluate the "WorkloadResize" approach to DynamicallySized Jobs (ResizeRequests)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5897

**Last updated**: 2026-04-09T09:27:37Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-08T06:41:57Z
- **Updated**: 2026-04-09T09:27:37Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 14

## Description

**What would you like to be added**:

I would like to evaluate the "WorkloadResize" as an alternative to Dynamically Sized Jobs. I'm ok exploring both options for the time being so that we have more context. See [WorkloadSlice](https://github.com/kubernetes-sigs/kueue/pull/5648) approach currently attempted.

Outline of the approach:
- we only have one workload and maintain one-to-one correspondence with the Job
- when a user modifies the Job and we detect it is not equivalent to the workload only by the size, then instead of deleting and re-creating the workload we update the Workload with the following structure. 
```yaml
spec:
   resizeRequest:
    podsets:
    - name: "main"
      count: 10
```
I think this could be done in Job reconciler's `ensureOneWorkload`.

- once the workload controller sees the `spec.resizeRequests` it adds the workload again into the queues (even though it already has QuotaReservation), so some checks will need to be relaxed.
- the new "WorkloadResizeRequest` when searching for quota always subtracts the quota coming from the already admitted copy of the workload
- once there is enough quota for the WorkloadResizeRequest, then the scheduler assumes the new version of the workload, and sends the workload Update request, updating the "status.admission" field
- the mechanics related to gating / ungating new Pods would be similar as in the WorkloadSlice approach

**Why is this needed**:

The one-to-one correspondence has some advantages which are tricky in the workload slices approach:
- Metrics are properly counting the workloads
- MultiKueue support is simplified
- Workload object validation can be very specific
- ensuring the new assignment lands on the same ResourceFlavor is simple

Maybe the API would also be flexible to accommodate "in-place" pod scale ups, but we can keep it out of scope.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Prototype
- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T06:42:12Z

cc @ichekrygin @tenzen-y

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-06T07:38:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T07:40:24Z

/remove-lifecycle

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T07:40:40Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:27:08Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T09:57:39Z

cc @yaroslava-serdiuk

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-05T16:35:08Z

+1 this will simplify Dynamically Sized jobs. We hit issue that current two steps (finishing old workload slice then admitting new workload slice) are not within a single atomic transaction, which has a time gap in the middle that there is no admitted workload for the job.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-05T18:05:24Z

> +1 this will simplify Dynamically Sized jobs. We hit issue that current two steps (finishing old workload slice then admitting new workload slice) are not within a single atomic transaction, which has a time gap in the middle that there is no admitted workload for the job.

I’d be very interested to hear more details about this case as well. I’m not sure this thread is the best place to fully unpack it, but could you share a bit more context, specifically around what you mean by the “gap”?

In particular:

* Is this gap something you’ve observed in practice, or is it primarily a theoretical concern based on the current two-step flow?
* Did you encounter situations where the old slice was evicted or finished, but the new slice failed to get admitted?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T18:35:24Z

@hiboyang has a particular issue in PR : https://github.com/kubernetes-sigs/kueue/pull/8341#discussion_r2762655778. We can discuss more there.

Aside from this particular issue, the current design has the problem with the "quota violation", due to the gap between the old Workload getting Finished, and the getting Admitted, but Pods are running during this gap and occupy resources (topology domains / nodes).

This gap is usually small, but might be arbitrarily large.  This can happen if the request to Admit the new workload fails (for whatever reason), and in the next scheduling cycle picks up a high priority workload.

This quota violation may also be a problem for the coming TAS + ElasticWorklaods that @sohankunkerkar is doing, as Kueue TAS scheduler may wrongly put Pods on the occupied domains.

I think if we aim to build a reliable solution we need to make the process transactional and guarantee "stickiness" - that even a high priority workload cannot "slip in" when the replacement getting Admitted. Another alternative is the WorklaodResize approach to make the process atomic.

On top of that the integration with MultiKueue is much harder than if this was a single Workload.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-02-05T18:56:09Z

> > +1 this will simplify Dynamically Sized jobs. We hit issue that current two steps (finishing old workload slice then admitting new workload slice) are not within a single atomic transaction, which has a time gap in the middle that there is no admitted workload for the job.
> 
> I’d be very interested to hear more details about this case as well. I’m not sure this thread is the best place to fully unpack it, but could you share a bit more context, specifically around what you mean by the “gap”?
> 
> In particular:
> 
> * Is this gap something you’ve observed in practice, or is it primarily a theoretical concern based on the current two-step flow?
> * Did you encounter situations where the old slice was evicted or finished, but the new slice failed to get admitted?

I had the issue when one workload is finished and another is not admitted when tested ProvisioningRequest support for Elastic Workloads. The gap there is the time for ProvisioningRequest to be Provisioned, which could be a lot.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-05T20:42:57Z

> This gap is usually small, but might be arbitrarily large. This can happen if the request to admit the new workload fails (for whatever reason), and in the next scheduling cycle a higher-priority workload is picked up.

Use case: during scale-up, the old workload slice is evicted, but the new workload slice is not admitted.

First, old workload-slice eviction does not follow or rely on the workload preemption paradigm, where evicted workloads do not guarantee preemptor admission and where a scheduling gap between preemption and admission is expected. In contrast, old workload-slice eviction here is an explicit call that immediately precedes new workload-slice admission. That said, I agree there is a class of transient failures, for example API or network errors, that could cause the new workload-slice admission request to fail, resulting in eviction of the old slice without successful admission of the new one. I want to explicitly call out this class of errors as the relevant risk.

Second, in such cases, when a job ends up with a new but unadmitted slice, the job should be suspended and capacity accounting restored. If this does not happen, that would be a bug rather than an intended behavior.

This is precisely why I am keen to get as much detail as possible about the reported scenario. Ideally, this would be captured as a GitHub issue with concrete reproduction steps, logs, and any other supporting details, so we can investigate it properly.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-05T20:44:09Z

> I had the issue when one workload is finished and another is not admitted when tested ProvisioningRequest support for Elastic Workloads. The gap there is the time for ProvisioningRequest to be Provisioned, which could be a lot.

@yaroslava-serdiuk, would it be possible to report this as a GitHub issue and provide supporting repro details?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-05T20:49:19Z

I went ahead and reported this as an issue: [https://github.com/kubernetes-sigs/kueue/issues/9015](https://github.com/kubernetes-sigs/kueue/issues/9015)

@yaroslava-serdiuk and @hiboyang, if you’re able to, it would be great to collaborate on this. Any details you can share, such as setup, reproduction steps, logs, or observations, would be really helpful in understanding and addressing the issue.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-04-09T09:27:34Z

/assign
