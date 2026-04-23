# Issue #541: Consider LimitRanges when calculating Workload usage

**Summary**: Consider LimitRanges when calculating Workload usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/541

**Last updated**: 2023-03-18T06:43:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-02-01T21:50:57Z
- **Updated**: 2023-03-18T06:43:21Z
- **Closed**: 2023-03-17T21:27:18Z
- **Labels**: `kind/feature`
- **Assignees**: [@mcariatm](https://github.com/mcariatm)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Administrators can setup [LimitRanges](https://kubernetes.io/docs/concepts/policy/limit-range/#constraints-on-resource-limits-and-requests) per namespace to set default requests for Pods.

We should consider these defaults when creating a Workload.
It can be done in the Workload webhook so that it applies to any custom job, similar to #316.

Caveat: if a LimitRange is created after the Workload object is created, we will not have an accurate calculation of requests.

This issue is an spinoff from #485

**Why is this needed**:

LimitRanges are a common tool for admins to set defaults for a namespace.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-02-27T14:48:47Z

/assign

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-02-27T14:49:32Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-02-28T15:28:55Z

@alculquicondor  Maybe the workload web-hook is not the best way to add this, since we'll need tho adapt the fix for #590. 
There will a lot easier if:
a.  the  defaulting (both for "limits to requests" and LimitsRanges ) is done in the job web-hook
or
b. the job to workload equality ignores the resources needs of the containers

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-28T15:41:00Z

a. This means that we would have to do the same for every custom job API (mpi, ray, etc), which adds more complexity to integrations.
b. We cannot completely ignore the resources, because that means that we are not calculating the most up-to-date quota.

You can work independently from #590. Whichever PR is ready later will have to rebase.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-14T15:26:17Z

cc @kerthcet 

After some offline discussion, we believe it's better to have a "totalRequests" field in the status. This can be calculated during admission and added in the same API call. This means we don't need to recreate or update the Workloads if LimitRanges or RuntimeClass changes.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-15T11:09:18Z

So we'll only update the totalRequests in admission, and after admission, we'll skip the calculation to avoid querying the limitRange, right? Then we can also solve the bug here https://github.com/kubernetes-sigs/kueue/issues/590

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T14:06:49Z

That is correct, that would solve #590 too. After admission, we would use the calculated requests in the cache.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-18T03:01:54Z

This is solved? What about the field `totalRequests`? Or this is closed by mistake.

### Comment by [@trasc](https://github.com/trasc) — 2023-03-18T06:43:21Z

It is solved. 
This however has two follow-up's #611 and  #612,  In the PR for 611 we'll need to be able to record the requests at the time of admission,  hence we will need some API change for that.
