# Issue #5480: [flaky test] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then succeed if the second Provisioning request succeeds

**Summary**: [flaky test] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then succeed if the second Provisioning request succeeds

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5480

**Last updated**: 2025-07-30T16:52:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-03T15:24:02Z
- **Updated**: 2025-07-30T16:52:29Z
- **Closed**: 2025-07-30T16:52:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description


**What happened**:

failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5479/pull-kueue-test-integration-baseline-release-0-12/1929919449490526208

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:959 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:959 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:963 @ 06/03/25 15:19:32.596
}
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T15:24:11Z

cc @mszadkow @mbobrovskyi ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T15:24:18Z

/kind flake

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-07-16T10:00:11Z

It appears to happened once in the history so far.
I run stress tests over 270 times and for 30 minutes and got no reproduction.

However I see that test says:
`"Checking the AdmissionCheck is set to Retry, and the workload has requeueState set"`
but it only checks the `requeueState`.

Investigating further

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-07-16T12:38:26Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T15:21:15Z

It repeated again: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6211/pull-kueue-test-integration-baseline-release-0-11/1949850646760919040

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T06:59:08Z

@mszadkow I think the underlying issue is https://github.com/kubernetes-sigs/kueue/issues/5129, I can take that as I'm working on the other issue.
