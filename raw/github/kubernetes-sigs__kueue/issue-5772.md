# Issue #5772: Flaky e2e TAS test due to concurrent node changes

**Summary**: Flaky e2e TAS test due to concurrent node changes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5772

**Last updated**: 2025-07-16T06:40:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-25T13:40:50Z
- **Updated**: 2025-07-16T06:40:25Z
- **Closed**: 2025-07-16T06:40:25Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

/kind flake
**What happened**:

failure on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5767/pull-kueue-test-e2e-tas-main/1937863350411071488

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
run ci

**Anything else we need to know?**:

```
End To End TAS Suite: kindest/node:v1.33.1: [BeforeSuite] expand_less	0s
{Unexpected error:
    <*errors.StatusError | 0xc00068a780>: 
    Operation cannot be fulfilled on nodes "kind-worker8": the object has been modified; please apply your changes to the latest version and try again
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
            Message: "Operation cannot be fulfilled on nodes \"kind-worker8\": the object has been modified; please apply your changes to the latest version and try again",
            Reason: "Conflict",
            Details: {Name: "kind-worker8", Group: "", Kind: "nodes", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 409,
        },
    }
occurred failed [FAILED] Unexpected error:
    <*errors.StatusError | 0xc00068a780>: 
    Operation cannot be fulfilled on nodes "kind-worker8": the object has been modified; please apply your changes to the latest version and try again
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
            Message: "Operation cannot be fulfilled on nodes \"kind-worker8\": the object has been modified; please apply your changes to the latest version and try again",
            Reason: "Conflict",
            Details: {Name: "kind-worker8", Group: "", Kind: "nodes", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 409,
        },
    }
occurred
In [BeforeSuite] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/suite_test.go:83 @ 06/25/25 13:32:12.835
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-25T13:40:57Z

cc @mbobrovskyi

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-07-15T13:07:23Z

API server audit logs reveal very close node patches:
```
2025-06-25T13:32:12.795286855Z stderr F I0625 13:32:12.794864       1 httplog.go:134] "HTTP" verb="PATCH" URI="/api/v1/nodes/kind-worker8/status?timeout=10s" latency="6.487576ms" userAgent="kubelet/v1.33.1 (linux/amd64) kubernetes/8adc0f0" audit-ID="a28a438b-e11f-4e2c-84ae-189a234d6168" srcIP="172.18.0.5:39086" apf_pl="node-high" apf_fs="system-node-high" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="5.956469ms" resp=200

2025-06-25T13:32:12.83516522Z stderr F I0625 13:32:12.834954       1 httplog.go:134] "HTTP" verb="PATCH" URI="/api/v1/nodes/kind-worker8/status" latency="5.126668ms" userAgent="tas.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="c02c5898-1b6e-4b34-89ea-97777b1e6cb4" srcIP="172.18.0.1:57328" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="4.692373ms" resp=409
```

The one sent by our test has `global-default` priority level, so even if they were happening at the exact time would not be picked.
What I think will work here is to retry the call with `Eventually`.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-07-15T13:07:52Z

/assign
