# Issue #8654: Support for Temporary Quota Overrides in ClusterQueue

**Summary**: Support for Temporary Quota Overrides in ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8654

**Last updated**: 2026-02-18T09:00:56Z

---

## Metadata

- **State**: open
- **Author**: [@saza-ku](https://github.com/saza-ku)
- **Created**: 2026-01-19T10:01:13Z
- **Updated**: 2026-02-18T09:00:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 14

## Description

**What would you like to be added**:

I would like to have a mechanism to temporarily override resource quotas within a ClusterQueue. This feature would allow users to define a specific time window during which the nominal quota, borrowingLimit and lendingLimit are adjusted (increased or decreased).

Specifically, I am envisioning a functionality similar to TemporaryThresholdOverrides in[ kube-throttler](https://github.com/pfnet/kube-throttler?tab=readme-ov-file#temporary-threshold-overrides).

Regarding the design, I am considering two potential approaches:
- Adding a field to ClusterQueue.spec
  - Introduce a field that includes the list of desired quota, start time, and end time.
  - Similar to kube-throttler.
- Introducing a new CRD
  - Create a separate CRD (e.g., TemporaryQuotaOverride) that targets a specific ClusterQueue.

If we adopt a new CRD, the spec would be like this. (This is not an actual proposal, but rather an example of what a proposal might look like.)

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: TemporaryQuotaOverride
metadata:
  name: org-a-2026-01
spec:
  queueName: org-a-queue
  overrides:
  - flavorName: high-performance
    resources:
    - name: cpu
      borrowingLimit: 27
    - name: memory
      borrowingLimit: 241Gi
  begin: 2026-01-01T00:00:00:+9:00
  end: 2026-02-01T00:00:00+09:00
```

**Why is this needed**:
In our cluster, there are frequent requirements to temporarily increase a team's quota. Currently, these operations often require manual updates to the ClusterQueue. To automate this task, we need a native or structured way to handle temporary overrides.

This requirement is already a standard in traditional HPC schedulers. For example, Slurm's [Resource Reservation](https://slurm.schedmd.com/reservations.html) allocates specific resources for a specific set of users during a defined time window. Providing an equivalent native capability might help migrate more workloads from traditional HPC environments to Kubernetes.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T10:03:12Z

cc @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:24:02Z

/priority important-longterm

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-20T14:54:07Z

Interesting use case! thanks for sharing. I have a few questions to better understand the intent:

- What happens when an override expires while workloads are still running? Do they get preempted, or does the change only affect new admissions?

- How does this interact with fair sharing?

- Have you considered whether similar behavior could be achieved using cohort borrowing semantics combined with scheduled GitOps changes?

I’m also curious about the overall design direction here like are you leaning toward an inline ClusterQueue field or introducing a new CRD?

### Comment by [@utam0k](https://github.com/utam0k) — 2026-01-20T22:42:18Z

Hi, I'm working on this with him. Thanks for your comment!

> What happens when an override expires while workloads are still running? Do they get preempted, or does the change only affect new admissions?

We haven't fully ironed out the details yet. For our specific use case, either way is fine. That said, since ClusterQueue updates don't trigger preemption as of now, it's probably simplest to just stick with that behavior for the implementation.

> How does this interact with fair sharing?

To be honest, that wasn't really on my radar. The easiest path would be to just make them mutually exclusive, but do you have any better ideas? I don't have much experience with fair sharing, so I'm a bit stuck on the best way to handle it.

> Have you considered whether similar behavior could be achieved using cohort borrowing semantics combined with scheduled GitOps changes?

I actually looked into that first. The problem is that when you're using GitOps, you run into field ownership issues—the system constantly tries to revert any temporary manual tweaks back to the source-of-truth manifest. Managing that drift is pretty tricky.

> I’m also curious about the overall design direction here like are you leaning toward an inline ClusterQueue field or introducing a new CRD?

I'm leaning toward a new CRD, but I'm open to suggestions. I'd like to nail down the exact requirements first and then go with whatever option makes the most sense.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-22T02:25:04Z

>We haven't fully ironed out the details yet. For our specific use case, either way is fine. That said, since ClusterQueue updates don't trigger preemption as of now, it's probably simplest to just stick with that behavior for the implementation.

Sticking with current behavior (no preemption on CQ updates) makes sense as a starting point.

>To be honest, that wasn't really on my radar. The easiest path would be to just make them mutually exclusive, but do you have any better ideas? I don't have much experience with fair sharing, so I'm a bit stuck on the best way to handle it.

IIUC, the DRS calculation adapts correctly whether you're overriding `borrowingLimit`, `lendingLimit`, or `nominalQuota`. No need to make them mutually exclusive. One design clarification worth clarifying: what does "temporarily increase quota" mean operationally?

### Comment by [@utam0k](https://github.com/utam0k) — 2026-01-22T12:07:16Z

@sohankunkerkar Thanks for the comment.

> what does "temporarily increase quota" mean operationally?

I believe the details should be discussed further in the KEP. Currently, my assumption is that when a `TemporaryQuotaOverride` is created, the actual applied value (the override) will be reflected in the status of the target `ClusterQueue`. Of course, other approaches could be considered if we introduce a new CR.

To give you a use case, imagine a multi-tenant Kubernetes cluster. A tenant might need to temporarily occupy a large amount of resources for a specific period, such as for a paper submission deadline. In this scenario, the tenant admin would create a PR with the `TemporaryQuotaOverride` manifest in a GitOps repository. The cluster admin then approves and merges the PR to apply the changes to production.

### Comment by [@saza-ku](https://github.com/saza-ku) — 2026-01-26T03:01:22Z

@sohankunkerkar Thanks for your comments!

If this feature seems worth thoroughly discussing, I'd like to propose it as a KEP for more detailed discussion. Or should we first refine the more detailed requirements before proceeding?

### Comment by [@saza-ku](https://github.com/saza-ku) — 2026-01-26T05:42:43Z

@mwielgus @mimowo
Would it be fine to start drafting a KEP for this proposal? We'd like to formalize the discussion and gather feedback on the design through the KEP process.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T08:03:22Z

Thank you for the discussion / proposal. I think this is quite interesting and certainly important. One use-case we know is running "hero". They are run rarely, and it is tricky to set quota in such a way that it fits both small BAU workloads, and the hero workloads.

One idea we've been discussing is that the "hero CQ" can temporarily preempt workloads from other CQs (even if they are below NominalQuota, so temporarily lowering the "Effective Nominal Quota" of other ClusterQueues) when a hero workload is scheduled in the hero CQ.

Wdyt? Is running "hero" workloads your use case too? Or more generally, would such an alternative proposal cover your use-case for introducing the TemporaryQuotaOverrides?

cc @gabesaba @tenzen-y @mwysokin

### Comment by [@utam0k](https://github.com/utam0k) — 2026-01-27T12:18:12Z

@mimowo Thanks for your comment. Interesting. I'm not sure about the "hero" you suggested, but what if 100 (or more) tenants need a temporary quota? Will all tenants use the same hero?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T15:27:17Z

I opened the dedicated issue for the "hero" workload issue: https://github.com/kubernetes-sigs/kueue/issues/8826

> I'm not sure about the "hero" you suggested, but what if 100 (or more) tenants need a temporary quota? Will all tenants use the same hero?

Yeah, "hero" ClusterQueue may not be best fit here, it just sounded to me similar, because in case of the "hero" ClusterQueue, what we need is a temporary decrease of "nominal quota".

What is the main use case for the `TemporaryQuotaOverrides`?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-27T17:48:03Z

> I opened the dedicated issue for the "hero" workload issue: [#8826](https://github.com/kubernetes-sigs/kueue/issues/8826)
> 
> > I'm not sure about the "hero" you suggested, but what if 100 (or more) tenants need a temporary quota? Will all tenants use the same hero?
> 
> Yeah, "hero" ClusterQueue may not be best fit here, it just sounded to me similar, because in case of the "hero" ClusterQueue, what we need is a temporary decrease of "nominal quota".
> 
> What is the main use case for the `TemporaryQuotaOverrides`?

I'm with @mimowo. This enhancement request has a couple of enhancements, as I can see in the following:

1. They want to define limited quotas within a specific time scope.
2. They want to drastically relax quota restrictions only for specific tenants (x number of namespaces).

At least, we should decouple those requests to 2 enhancement request, and (1 has already tracked by https://github.com/kubernetes-sigs/kueue/issues/8522, IIUC. (Please correct me if it doesn't match with this story)

For (2), I imagine the situation where cluster admins have a cluster-wide global (shared) clusterqueue which is used by almost tenents, and at some points, they want to relax the quota only in a specific tenant and a specific time scope.

If my understanding is correct, I'm curious about the reason why @saza-ku and @utam0k don't want to have a Hierarchical Cohort. In my assumption, the cluster admins can have (a) a single global (shared) Cohort that has almost all the compute units available in the cluster, and (b) some of the children ClusterQueues or Cohorts for highly prioritized business units or projects.

The Jobs came from highly prioritized projects (tenants), which are accommodated by (b), and if they want to oversubscribe the (b) quotas, they can borrow quotas from (a) automatically. Once the highly prioritized projects are finished, the cluster admins will remove nominal quotas from (b), then users always borrow from (a).

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-29T15:27:04Z

Thank you for mentioning in #8869!
Let me share a bit more context.

We have a hierarchical cohort with a total capacity of 100, where the child CQs:
- project-A: nominal quota 30
- project-B: nominal quota 40
- shared-priority-low: nominal quota 0

Sometimes, we need to temporarily increase `project-B`'s quota (e.g., from 40 to 60). In that situations, we'd like to keep `project-A`'s quota as is and reserve the extra capacity from the remaining resources in the cohort.
If `ResourceQuotaLease` could allow us to temporarily assign available resources to a specific CQ, it would be a work for us.

> At least, we should decouple those requests to 2 enhancement request, and (1 has already tracked by https://github.com/kubernetes-sigs/kueue/issues/8522, IIUC. (Please correct me if it doesn't match with this story)

Regarding https://github.com/kubernetes-sigs/kueue/issues/8522, this aims to ensure fairness for the `shared` CQ. In contrast, this proposal targets projects that occasionally need a temporary "high-priority" status.

### Comment by [@saza-ku](https://github.com/saza-ku) — 2026-02-18T09:00:56Z

Let me clarify the background context and the specific use case we are addressing.

As shown in the Figure 1, we manage resources under a parent Cohort with two types of CQs. The parent Cohort has all nominalQuota. Each CQ has borrowingLimit, but nominalQuota is set to 0 (in Figure 2). Workload priorities are enforced on each CQ via Validation Admission Policy (in Figure 3).

1. Project CQs: They only accept high-priority workload, but borrowingLimit is limited.
2. Shared CQ: This only accepts low-priority workload, but it can borrow unlimited resources from the parent Cohort.

We strictly limit the Project CQs' borrowing capabilities during normal operations. However, we frequently face scenarios where a specific project requires additional resources temporarily. For instance, as illustrated in the Figure 4, we might need to increase Project A's borrowingLimit from 30 to 50 specifically for the duration of 3/1 to 3/31, and revert from 50 to 30 once the period ends.

I believe this new mechanism is necessary because other concepts, such as Uber Cluster Queues (https://github.com/kubernetes-sigs/kueue/pull/8864) or ResourceQuotaLease (https://github.com/kubernetes-sigs/kueue/issues/8869), address different problems and do not meet our specific requirements.


| | |
| :---: | :---: |
|<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/32262a34-1155-4a6b-9508-66730663dd60" />|<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/d7eb42ba-d1fc-462e-939c-d551ae4a47be" />|
|<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/05b6e01c-bd24-4774-8b92-68de9a4e4484" />|<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/c35f326b-9a87-496a-a060-982a54572baa" />|
