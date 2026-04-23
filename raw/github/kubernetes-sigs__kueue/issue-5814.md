# Issue #5814: Helm: Support for specifying nodeSelector and tolerations for all Kueue components

**Summary**: Helm: Support for specifying nodeSelector and tolerations for all Kueue components

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5814

**Last updated**: 2025-07-03T07:37:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@zmalik](https://github.com/zmalik)
- **Created**: 2025-06-30T12:59:01Z
- **Updated**: 2025-07-03T07:37:26Z
- **Closed**: 2025-07-03T07:37:26Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Support for specifying nodeSelector and tolerations for all Kueue components

**Why is this needed**:
**Dedicated node scheduling**: In many clusters, control‐plane or specialized workloads (e.g. CI/CD, scheduling controllers) must run on nodes marked for system or infra workloads.

**Taint‐based isolation**: Operators often taint dedicated “infra” nodes (e.g. infra=true:NoSchedule) and rely on tolerations to ensure only approved controllers land there. Without tolerations, Kueue pods may be evicted or unschedulable.

**Resource partitioning**: In shared clusters, it’s critical to isolate Kueue’s scheduling engine from user workloads; nodeSelector/tolerations let you pin Kueue to a specific node pool.


This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change, as in helm change or config change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-30T13:07:09Z

Do you assume Kueue Helm chart?

### Comment by [@zmalik](https://github.com/zmalik) — 2025-06-30T13:09:52Z

> Do you assume Kueue Helm chart?

Yes, that enhancement should be scoped to the official Kueue Helm chart. I was looking at the deployment templates under charts/kueue/templates (for example, manager/manager.yaml at https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/manager/manager.yaml),

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-30T13:13:31Z

> > Do you assume Kueue Helm chart?
> 
> Yes, that enhancement should be scoped to the official Kueue Helm chart. I was looking at the deployment templates under charts/kueue/templates (for example, manager/manager.yaml at https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/manager/manager.yaml),

That sounds good to me.
/retitle Helm: Support for specifying nodeSelector and tolerations for all Kueue components

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-30T13:16:28Z

+1, and thank you folks for clarifying this is about helm

### Comment by [@zmalik](https://github.com/zmalik) — 2025-06-30T13:41:28Z

I’d be happy to draft a PR with a possible fix. Would that be helpful?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-30T13:48:11Z

> I’d be happy to draft a PR with a possible fix. Would that be helpful?

Feel free to submit PR. We're happy to review it!
