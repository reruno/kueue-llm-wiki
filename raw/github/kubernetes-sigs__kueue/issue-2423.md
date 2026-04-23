# Issue #2423: ClientConnection.QPS applies to individual API types

**Summary**: ClientConnection.QPS applies to individual API types

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2423

**Last updated**: 2024-06-25T15:09:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-06-17T11:34:10Z
- **Updated**: 2024-06-25T15:09:39Z
- **Closed**: 2024-06-25T15:09:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 6

## Description

**What happened**:
When setting [ClientConnection.QPS](https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/apis/config/v1beta1/configuration_types.go#L301), the limit applies to each type (e.g. pod, workload, status, clusterqueue, etc)

**What you expected to happen**:
This should be a global limit. Otherwise, it is hard for administrators to know exactly how many queries per second Kueue will be making to the API Server.

**How to reproduce it (as minimally and precisely as possible)**:
Set to a very low limit (e.g. 1), with burst set to same as the limit. Observe that Kueue is making more than 1 call per second to the API Server.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-06-17T13:35:14Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-06-20T10:40:23Z

> Set to a very low limit (e.g. 1), with burst set to same as the limit. Observe that Kueue is making more than 1 call per second to the API Server.

@gabesaba How many calls do you observe?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-06-20T11:27:21Z

> > Set to a very low limit (e.g. 1), with burst set to same as the limit. Observe that Kueue is making more than 1 call per second to the API Server.
> 
> @gabesaba How many calls do you observe?

it should be on the O(#API types). I didn't check if this was multiplied by namespaces, for namespaced types. So in the case of 1qps, at least CQ, LQ, Workload, Pod, Event (and others I may be missing) = 5qps.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-20T11:41:49Z

> > > Set to a very low limit (e.g. 1), with burst set to same as the limit. Observe that Kueue is making more than 1 call per second to the API Server.
> > 
> > 
> > @gabesaba How many calls do you observe?
> 
> it should be on the O(#API types). I didn't check if this was multiplied by namespaces, for namespaced types. So in the case of 1qps, at least CQ, LQ, Workload, Pod, Event (and others I may be missing) = 5qps.

How do you "mesure" this?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-06-20T12:14:42Z

I'm not sure what development environment you're using, but generally: 

- access k8 apiserver logs
- filter requests from Kueue
- add some load to Kueue so that it's making enough API calls
- group by time observe that in a given window (e.g. 60 seconds), there are more than 60 calls (if qps=1)
- additionally, group by API type (Workload/Pod/CQ) - observe that qps is at most the limit you set

### Comment by [@trasc](https://github.com/trasc) — 2024-06-21T11:12:35Z

@gabesaba It took some time but I found the cause, #2462 should fix it, please let me know if you can confirm the fix on your side as well.
