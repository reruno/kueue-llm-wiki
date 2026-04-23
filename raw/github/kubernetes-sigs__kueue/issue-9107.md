# Issue #9107: [Flaky E2E] Metrics when workload is admitted should continue to expose metrics after the secret is re-created

**Summary**: [Flaky E2E] Metrics when workload is admitted should continue to expose metrics after the secret is re-created

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9107

**Last updated**: 2026-02-12T08:00:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-11T08:21:27Z
- **Updated**: 2026-02-12T08:00:02Z
- **Closed**: 2026-02-12T08:00:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

End To End Cert Manager Integration Suite: kindest/node:v1.34.3: [It] Metrics when workload is admitted should continue to expose metrics after the secret is re-created 

**First observed in** (PR or commit, if known):

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9103/pull-kueue-test-e2e-certmanager-main/2021494906102484992

**Failure message or logs**:
```
{Timed out after 10.059s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/certmanager/metrics_test.go:254 with:
Unexpected error:
    <exec.CodeExitError>: 
    command terminated with exit code 60
    {
        Err: <*errors.errorString | 0xc0005ba400>{
            s: "command terminated with exit code 60",
        },
        Code: 60,
    }
occurred failed [FAILED] Timed out after 10.059s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/certmanager/metrics_test.go:254 with:
Unexpected error:
    <exec.CodeExitError>: 
    command terminated with exit code 60
    {
        Err: <*errors.errorString | 0xc0005ba400>{
            s: "command terminated with exit code 60",
        },
        Code: 60,
    }
occurred
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/certmanager/metrics_test.go:257 @ 02/11/26 08:15:18.763
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-11T08:22:38Z

/cc @MaysaMacedo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T08:31:21Z

The timeout of 10s seems very small (especially for e2e cert management), should we try increasing that?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T14:09:19Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-certmanager-release-0-15/2021580975758118912

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T16:48:56Z

This is failing pretty often now cc @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-11T17:32:35Z

I think [this](https://github.com/kubernetes-sigs/kueue/pull/9116) should fix the issue.
