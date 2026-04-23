# Issue #7457: [flaky test] The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Summary**: [flaky test] The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7457

**Last updated**: 2025-11-14T18:23:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-30T14:54:46Z
- **Updated**: 2025-11-14T18:23:38Z
- **Closed**: 2025-11-14T18:23:38Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

/kind flake


**What happened**:

failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7448/pull-kueue-test-e2e-multikueue-main/1983905265296084992

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
MultiKueue when The connection to a worker cluster is unreliable [It] Should update the cluster status to reflect the connection state
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:978
  [FAILED] Expected success, but got an error:
      <*errors.StatusError | 0xc000bb8820>: 
      conversion webhook for kueue.x-k8s.io/v1beta1, Kind=ClusterQueue failed: Post "[https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s](https://kueue-webhook-service.kueue-system.svc/convert?timeout=30s)": dial tcp 10.244.1.9:9443: connect: connection refused
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
              Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=ClusterQueue failed: Post \"[https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s](https://kueue-webhook-service.kueue-system.svc/convert?timeout=30s)\": dial tcp 10.244.1.9:9443: connect: connection refused",
              Reason: "",
              Details: nil,
              Code: 500,
          },
      }
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:1040 @ 10/30/25 14:50:02.347
  There were additional failures detected.  To view them in detail run ginkgo -vv
------------------------------
```

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-05T08:00:17Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T15:00:54Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/1986747963547848704

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-14T04:11:01Z

Is it duplicate of https://github.com/kubernetes-sigs/kueue/issues/6573?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T07:37:34Z

Well hard to tell until we know the root cause for the issues, because the asserts are a bit different, but maybe the cause is the same. Lets investigate under the repro which @IrvingMg has. Once we understand that issue we will be in a better position to tell if this is the same or not
