# Issue #6695: Flaky End To End Suite: Pod groups when Single CQ Unscheduled Pod which is deleted can be replaced in group

**Summary**: Flaky End To End Suite: Pod groups when Single CQ Unscheduled Pod which is deleted can be replaced in group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6695

**Last updated**: 2025-09-01T12:26:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-29T09:04:33Z
- **Updated**: 2025-09-01T12:26:34Z
- **Closed**: 2025-09-01T12:26:33Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

`End To End Suite: kindest/node:v1.34.0: [It] Pod groups when Single CQ Unscheduled Pod which is deleted can be replaced in group` failed in periodic Job.

```shell
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:332 with:
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
                Time: 2025-08-28T16:11:22Z,
            },
            Reason: "Unschedulable",
            Message: "0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) didn't match Pod's node affinity/selector. no new claims to deallocate, preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc0008a2c00>: {
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
            <*cmp.pathFilter | 0xc000a029d8>{
                core: {},
                fnc: 0x187efa0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:332 with:
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
                Time: 2025-08-28T16:11:22Z,
            },
            Reason: "Unschedulable",
            Message: "0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) didn't match Pod's node affinity/selector. no new claims to deallocate, preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc0008a2c00>: {
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
            <*cmp.pathFilter | 0xc000a029d8>{
                core: {},
                fnc: 0x187efa0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:337 @ 08/28/25 16:11:34.887
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/1961095791665745920

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-29T09:05:09Z

@mbobrovskyi After we enable the v1.34 E2E, we face this error. Could you check that?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-29T09:05:19Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-01T08:13:31Z

Ah, I got it. We only ignore `.status.conditions[*].observedGeneration`. But, I guess we need to ignore `.status.observedGeneratio` as well.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-01T08:17:28Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-01T11:04:46Z

I think this error happens before https://github.com/kubernetes-sigs/kueue/pull/6694 fixes.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-01T11:23:56Z

@tenzen-y can we close it?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-01T11:56:33Z

> I think this error happens before [#6694](https://github.com/kubernetes-sigs/kueue/pull/6694) fixes.

Uhm, that's sounds interesting since I observed this failure after #6694 is merged.
Can't you repro this case?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-01T12:21:51Z

The test failed on 08/28/25, but the PR was merged on 08/29/25.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-01T12:26:28Z

> The test failed on 08/28/25, but the PR was merged on 08/29/25.

Oh, I see. In that case, the notification seems to be outdated.
Thank you for checking that!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-01T12:26:34Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6695#issuecomment-3242170188):

>> The test failed on 08/28/25, but the PR was merged on 08/29/25.
>
>Oh, I see. In that case, the notification seems to be outdated.
>Thank you for checking that!
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
