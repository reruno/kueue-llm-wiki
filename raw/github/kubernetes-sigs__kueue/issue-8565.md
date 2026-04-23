# Issue #8565: [flaky test] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry when a ProvisioningRequest is in BookingExpired stated, then succeed if the second Provisioning request succeeds [slow]

**Summary**: [flaky test] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry when a ProvisioningRequest is in BookingExpired stated, then succeed if the second Provisioning request succeeds [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8565

**Last updated**: 2026-01-27T08:51:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-13T16:41:58Z
- **Updated**: 2026-01-27T08:51:50Z
- **Closed**: 2026-01-27T08:51:50Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description


**Which test is flaking?**:

Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry when a ProvisioningRequest is in BookingExpired stated, then succeed if the second Provisioning request succeeds [slow] 

**First observed in** (PR or commit, if known):
unknown
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2010705890105102336
**Failure message or logs**:
```

Provisioning admission check suite: [It] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry when a ProvisioningRequest is in BookingExpired stated, then succeed if the second Provisioning request succeeds [slow] expand_less	14s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1149 with:
Expected
    <*v1beta2.RequeueState | 0x0>: nil
not to be nil failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1149 with:
Expected
    <*v1beta2.RequeueState | 0x0>: nil
not to be nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1154 @ 01/12/26 13:39:29.02
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T16:42:18Z

cc @sohankunkerkar @mbobrovskyi any ideas maybe?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-13T18:58:45Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:30:53Z

/priority important-soon
