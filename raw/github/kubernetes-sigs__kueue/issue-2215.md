# Issue #2215: Make backoffBaseSeconds default consistent with timeout in waitForPodsReady

**Summary**: Make backoffBaseSeconds default consistent with timeout in waitForPodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2215

**Last updated**: 2024-05-21T20:24:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2024-05-17T11:57:48Z
- **Updated**: 2024-05-21T20:24:17Z
- **Closed**: 2024-05-21T20:24:17Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

**What would you like to be cleaned**:

Increase the default for waitForPodsReady to 5-10 minutes. 

**Why is this needed**:

Currently Kueue retries to run a workload almost immediately after it failed to start it for 5 minutes. If the situation was not favorable for the workload for 5 minutes (there was no space in the cluster, cluster autoscaler failed to deliver nodes, the workload is crashing immediately after start etc) it is unlikely to improve just after 10 or 20 seconds. 

cc: @tenzen-y @mimowo

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T13:52:52Z

SGTM
@mwielgus I'm not familiar with ClusterAutoscaler, so could you tell me about how many minutes does cluster-autoscaler prepare a new Node generally take?

### Comment by [@mwielgus](https://github.com/mwielgus) — 2024-05-17T18:44:18Z

This depends on the cloud provider. Usually somewhere between 1-3 minutes. Within 5 minutes the nodes should be up and pods running unless there is limited availability of the requested resources.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T18:47:39Z

I would put it to 1 minute and only for v0.7, where it's configurable.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T08:36:42Z

I agree with both suggestions. 
* 0.6: yes, it is not configurable so keeping a lower base (10s as currently) might be more universal
* 0.7+: I think 1min might be more practical for users and admins who want to observe the timeout in action, say after config change, as waiting 5min in that case might be tedious.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T13:57:10Z

/trasc
EDIT: mistake :)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T13:57:16Z

@trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-21T07:24:11Z

/assign
