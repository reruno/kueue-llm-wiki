# Issue #5941: [flaky test] Topology Aware Scheduling when Delete Topology when ResourceFlavor exists should not allow to delete topology

**Summary**: [flaky test] Topology Aware Scheduling when Delete Topology when ResourceFlavor exists should not allow to delete topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5941

**Last updated**: 2025-07-11T14:09:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-11T08:37:06Z
- **Updated**: 2025-07-11T14:09:33Z
- **Closed**: 2025-07-11T14:09:33Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

/kind flake


**What happened**:

failure: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-12/1943390196502368256

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Delete Topology when ResourceFlavor exists should not allow to delete topology expand_less	2s
{Failed after 0.258s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:122 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0006dafa0>: 
    topologies.kueue.x-k8s.io "topology" not found
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "topologies.kueue.x-k8s.io \"topology\" not found",
            Reason: "NotFound",
            Details: {
                Name: "topology",
                Group: "kueue.x-k8s.io",
                Kind: "topologies",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Failed after 0.258s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:122 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0006dafa0>: 
    topologies.kueue.x-k8s.io "topology" not found
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "topologies.kueue.x-k8s.io \"topology\" not found",
            Reason: "NotFound",
            Details: {
                Name: "topology",
                Group: "kueue.x-k8s.io",
                Kind: "topologies",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:124 @ 07/10/25 19:37:26.128
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-11T10:37:47Z

```
  [38;5;243mTimeline >>[0m
  "level"=0 "msg"="Created namespace" "namespace"="tas-t2qhs"
  2025-07-10T19:37:25.60570738Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"topology"}}
  [1mSTEP:[0m check topology has finalizer [38;5;243m@ 07/10/25 19:37:25.605[0m
  2025-07-10T19:37:25.606173236Z	LEVEL(-2)	tas/topology_controller.go:100	Reconcile Topology	{"controller": "tas_topology_controller", "namespace": "", "name": "topology", "reconcileID": "fe4e3294-3aa5-4f91-b887-72997fe28809"}
  2025-07-10T19:37:25.612252664Z	LEVEL(-2)	tas/topology_controller.go:100	Reconcile Topology	{"controller": "tas_topology_controller", "namespace": "", "name": "topology", "reconcileID": "6c85a0f9-29d3-4c80-90dc-f7233ca5576a"}
  [1mSTEP:[0m delete topology [38;5;243m@ 07/10/25 19:37:25.864[0m
  [1mSTEP:[0m check topology still present [38;5;243m@ 07/10/25 19:37:25.869[0m
  2025-07-10T19:37:25.869753804Z	LEVEL(-2)	tas/topology_controller.go:100	Reconcile Topology	{"controller": "tas_topology_controller", "namespace": "", "name": "topology", "reconcileID": "be8e82fb-da82-4dbd-87ab-075a40cc2a6c"}
  2025-07-10T19:37:25.877327343Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:149	Topology delete event	{"topology": {"name":"topology"}}
  [38;5;9m[FAILED][0m in [It] - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:124 [38;5;243m@ 07/10/25 19:37:26.128[0m
  2025-07-10T19:37:26.150097984Z	LEVEL(-2)	tas-resource-flavor-controller	tas/resource_flavor.go:165	Topology TAS ResourceFlavor event	{"flavor": "tas-flavor"}
  2025-07-10T19:37:26.150127045Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:133	ResourceFlavor create event	{"resourceFlavor": {"name":"tas-flavor"}}
```
From this log we can see that the culprit is that the ResourceFlavor event was propagated already after the test was marked as failed.
- `2025-07-10T19:37:26.150097984Z` - the ResourceFlavor event was received and the cache was updated
- `2025-07-10T19:37:25.869753804Z` - was the Topology reconcile which deleted the finalizer, leading to the test failing

This is completely normal in k8s, events may be delivered with delay, even if we call Create for ResourceFlavor, before Create for Topology.

To address this issue I see two possibilities to somehow ensure ResourceFlavor is already visible in cache:
1. create CQ and await until it is Active. It only gets active if the ResourceFlavor is in cache
2. add custom sleep, in this case 300ms would be enough, but we could use something like 500ms for some buffer

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-11T10:42:06Z

cc @mbobrovskyi @tenzen-y any preferences or other ideas? I don't have a strong preference, and I'm perfectly fine with both. We applied the custom delay strategy [here](https://github.com/kubernetes-sigs/kueue/blob/edd0a329e1b90c66c4d567775a883ab1e590baa6/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L610), and so far the failure haven't returned. OTOH, the CQ approach seems more reliable, so we could start here.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-11T13:10:47Z

> create CQ and await until it is Active. It only gets active if the ResourceFlavor is in cache

I like this idea.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-11T13:15:50Z

/assign
