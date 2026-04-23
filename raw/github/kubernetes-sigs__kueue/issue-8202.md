# Issue #8202: [flaky test] ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload

**Summary**: [flaky test] ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8202

**Last updated**: 2025-12-12T18:19:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-12T10:30:14Z
- **Updated**: 2025-12-12T18:19:46Z
- **Closed**: 2025-12-12T18:19:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

/kind flake 
**What happened**:
failed on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8198/pull-kueue-test-e2e-customconfigs-release-0-15/1999416601295720448
**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End Custom Configs handling Suite: kindest/node:v1.34.0: [It] ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload expand_less	26s
{Expected success, but got an error:
    <*errors.StatusError | 0xc000488f00>: 
    Internal error occurred: failed calling webhook "vresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s": EOF
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
            Message: "Internal error occurred: failed calling webhook \"vresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": EOF",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": EOF",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000488f00>: 
    Internal error occurred: failed calling webhook "vresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s": EOF
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
            Message: "Internal error occurred: failed calling webhook \"vresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": EOF",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": EOF",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:159 @ 12/12/25 10:06:02.101
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T10:30:31Z

cc @sohankunkerkar @mykysha ptal

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-12T13:51:17Z

/assign @sohankunkerkar
