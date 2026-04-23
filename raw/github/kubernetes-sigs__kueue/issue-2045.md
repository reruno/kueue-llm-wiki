# Issue #2045: [MultiKueue] e2e test fails occassionally

**Summary**: [MultiKueue] e2e test fails occassionally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2045

**Last updated**: 2024-04-24T14:43:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-23T15:27:47Z
- **Updated**: 2024-04-24T14:43:56Z
- **Closed**: 2024-04-24T14:43:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

The `MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state` e2e test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2044/pull-kueue-test-multikueue-e2e-main-1-29/1782781526652489728

The message (for reference, in case the artifacts get cleaned after a while:
```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:411 with:
Expected
    <[]v1.Condition | len:1, cap:4>: [
        {
            Type: "Active",
            Status: "False",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-04-23T14:47:13Z,
            },
            Reason: "ClientConnectionFailed",
            Message: "failed to get API group resources: unable to retrieve the complete list of server APIs: kueue.x-k8s.io/v1beta1: Get \"https://kind-worker1-control-plane:6443/apis/kueue.x-k8s.io/v1beta1\": dial tcp: lookup kind-worker1-control-plane on 10.96.0.10:53: no such host",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000a49cb0>: {
        Expected: <v1.Condition>{
            Type: "Active",
            Status: "True",
            ObservedGeneration: 0,
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Reason: "Active",
            Message: "Connected",
        },
        Options: [
            <*cmp.pathFilter | 0xc000013698>{
                core: {},
                fnc: 0x610cc0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:411 with:
Expected
    <[]v1.Condition | len:1, cap:4>: [
        {
            Type: "Active",
            Status: "False",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-04-23T14:47:13Z,
            },
            Reason: "ClientConnectionFailed",
            Message: "failed to get API group resources: unable to retrieve the complete list of server APIs: kueue.x-k8s.io/v1beta1: Get \"https://kind-worker1-control-plane:6443/apis/kueue.x-k8s.io/v1beta1\": dial tcp: lookup kind-worker1-control-plane on 10.96.0.10:53: no such host",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000a49cb0>: {
        Expected: <v1.Condition>{
            Type: "Active",
            Status: "True",
            ObservedGeneration: 0,
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Reason: "Active",
            Message: "Connected",
        },
        Options: [
            <*cmp.pathFilter | 0xc000013698>{
                core: {},
                fnc: 0x610cc0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:419 @ 04/23/24 14:47:34.263
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-23T15:28:12Z

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-04-24T07:06:46Z

/assign
