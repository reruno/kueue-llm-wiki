# Issue #6691: Take into account Pod observedGeneration in E2E test for v1.34

**Summary**: Take into account Pod observedGeneration in E2E test for v1.34

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6691

**Last updated**: 2025-08-29T07:41:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-28T16:30:23Z
- **Updated**: 2025-08-29T07:41:10Z
- **Closed**: 2025-08-29T07:41:10Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We should refine the E2E test to support Pod `.status.observedGeneration`.

**Why is this needed**:

Since Kubernetes v1.34, the PodObservedGenerationTracking FG is enabled by default.

https://kubernetes.io/docs/concepts/workloads/pods/#pod-generation

So, our E2E tests always fail: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6686/pull-kueue-test-e2e-main-1-34/1961095983311884288

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:332 with:
Expected
    <[]v1.PodCondition | len:1, cap:1>: [
        {
            Type: "PodScheduled",
            ObservedGeneration: 2,
            Status: "False",
            LastProbeTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            LastTransitionTime: {
                Time: 2025-08-28T16:09:20Z,
            },
            Reason: "Unschedulable",
            Message: "0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) didn't match Pod's node affinity/selector. no new claims to deallocate, preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000738840>: {
        Expected: <v1.PodCondition>{
            Type: "PodScheduled",
            ObservedGeneration: 0,
            Status: "False",
            LastProbeTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Reason: "Unschedulable",
            Message: "",
        },
        Options: [
            <*cmp.pathFilter | 0xc0002a97b8>{
                core: {},
                fnc: 0x187efa0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:332 with:
Expected
    <[]v1.PodCondition | len:1, cap:1>: [
        {
            Type: "PodScheduled",
            ObservedGeneration: 2,
            Status: "False",
            LastProbeTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            LastTransitionTime: {
                Time: 2025-08-28T16:09:20Z,
            },
            Reason: "Unschedulable",
            Message: "0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) didn't match Pod's node affinity/selector. no new claims to deallocate, preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000738840>: {
        Expected: <v1.PodCondition>{
            Type: "PodScheduled",
            ObservedGeneration: 0,
            Status: "False",
            LastProbeTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Reason: "Unschedulable",
            Message: "",
        },
        Options: [
            <*cmp.pathFilter | 0xc0002a97b8>{
                core: {},
                fnc: 0x187efa0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:337 @ 08/28/25 16:09:33.263
}
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-28T16:53:10Z

We must implement this mechanism alongside to add 1.34 to CI.

### Comment by [@haardikdharma10](https://github.com/haardikdharma10) — 2025-08-28T22:13:55Z

@tenzen-y - In the test, should the `observedgeneration` field be compared with pod's `.metadata.generation` or be included in the ignored fields?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-29T06:10:13Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-29T06:25:28Z

We can just ignore that the same as the other resources: https://github.com/kubernetes-sigs/kueue/blob/main/test/util/constants.go
