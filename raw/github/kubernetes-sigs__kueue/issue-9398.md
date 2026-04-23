# Issue #9398: [failing test] periodic-kueue-test-e2e-k8s-main-was fails on     statefulsets.apps "prometheus-prometheus" not found

**Summary**: [failing test] periodic-kueue-test-e2e-k8s-main-was fails on     statefulsets.apps "prometheus-prometheus" not found

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9398

**Last updated**: 2026-02-20T20:19:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-20T14:30:52Z
- **Updated**: 2026-02-20T20:19:24Z
- **Closed**: 2026-02-20T17:11:43Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description


**What happened**:
failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-k8s-main-was/2024806519459024896
**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-k8s-main-was/2024806519459024896

```
End To End Suite: k8s-main:latest: [BeforeSuite] expand_less	46s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:672 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc000642500>: 
    statefulsets.apps "prometheus-prometheus" not found
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
            Message: "statefulsets.apps \"prometheus-prometheus\" not found",
            Reason: "NotFound",
            Details: {
                Name: "prometheus-prometheus",
                Group: "apps",
                Kind: "statefulsets",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:672 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc000642500>: 
    statefulsets.apps "prometheus-prometheus" not found
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
            Message: "statefulsets.apps \"prometheus-prometheus\" not found",
            Reason: "NotFound",
            Details: {
                Name: "prometheus-prometheus",
                Group: "apps",
                Kind: "statefulsets",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [BeforeSuite] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/suite_test.go:97 @ 02/20/26 11:37:45.257
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-20T15:12:46Z

cc @IrvingMg ptal

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-20T15:16:32Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-20T20:19:22Z

/kind flake
