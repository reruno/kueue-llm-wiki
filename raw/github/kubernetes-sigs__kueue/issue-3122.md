# Issue #3122: Expose Flavors in LocalQueue Status

**Summary**: Expose Flavors in LocalQueue Status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3122

**Last updated**: 2025-09-26T08:32:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@KPostOffice](https://github.com/KPostOffice)
- **Created**: 2024-09-23T18:44:15Z
- **Updated**: 2025-09-26T08:32:36Z
- **Closed**: 2024-10-18T15:29:05Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add a status field to LocalQueue which lists out available flavors

**Why is this needed**:
I would like to be able to see the resource flavors available in each LocalQueue that I have access to

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-24T09:50:20Z

Updating the flavors in status will eat QPS to update the information which is just one step away so I would prefer to understand what is the use-case.

Would it work for you composing these queries:
```sh
CQ_NAME=$(kubectl get lq/user-queue -ojson | jq -r .spec.clusterQueue)
kubectl get cq/$CQ_NAME -ojson | jq .spec.resourceGroups\[\].flavors\[\].name
```
If this works, maybe just need a docs update for "common tasks", or extend kueuectl?

/cc @mwielgus @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-24T12:17:19Z

> Updating the flavors in status will eat QPS to update the information which is just one step away so I would prefer to understand what is the use-case.

We already have API calls to populate the usage, so this wouldn't add additional calls.

> Would it work for you composing these queries

This might not work, depending on the RBAC rules, as users might not have read access to ClusterQueues.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-24T12:21:48Z

I see, sounds good

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-24T14:43:04Z

> > Would it work for you composing these queries
> 
> This might not work, depending on the RBAC rules, as users might not have read access to ClusterQueues.

The RBAC permission deeply depends on the organization's policies. So, it might be better to add troubleshooting guide or any dedicated task document how to obtain the tied resourceFlavors.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-09-24T16:05:48Z

> This might not work, depending on the RBAC rules, as users might not have read access to ClusterQueues.

This is exactly the issue we are facing. Letting the users know the flavors is useful since it can give an idea of the capabilities provided by a LocalQueue. (i.e. one flavor may have newer GPUs)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-26T08:15:31Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T09:48:20Z

A small follow up for TAS: https://github.com/kubernetes-sigs/kueue/issues/4534

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T08:32:36Z

cc @varshaprasad96 @KPostOffice this feature was introduced before we had the visibility API, which can expose some visibility information "on-demand" without duplicating the information (as currently the feature requires duplication of information). Thus, we are considering to deprecate and eventually drop this feature: https://github.com/kubernetes-sigs/kueue/issues/6777

Let us know if you still find this feature useful, or would like to work on replacing the feature as visibility on-demand endpoint.
