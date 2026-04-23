# Issue #9821: integration tests fail to start due to "failed to start the controlplane. retried 5 times: exec: "etcd": executable file not found in $PATH"

**Summary**: integration tests fail to start due to "failed to start the controlplane. retried 5 times: exec: "etcd": executable file not found in $PATH"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9821

**Last updated**: 2026-03-20T20:48:40Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-12T08:20:08Z
- **Updated**: 2026-03-20T20:48:40Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 4

## Description

**Which test is flaking?**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2031910147336441856
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2031910147336441856
**Failure message or logs**:
```
  github.com/onsi/ginkgo/v2/internal.(*Suite).runNode.func3
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/github.com/onsi/ginkgo/v2/internal/suite.go:942
  [FAILED] in [BeforeSuite] - /home/prow/go/src/kubernetes-sigs/kueue/vendor/github.com/onsi/ginkgo/v2/internal/suite.go:338 @ 03/12/26 01:55:37.419
  << Timeline
  [FAILED] Unexpected error:
      <*fmt.wrapError | 0xc0002c06c0>: 
      unable to start control plane itself: failed to start the controlplane. retried 5 times: exec: "etcd": executable file not found in $PATH
      {
          msg: "unable to start control plane itself: failed to start the controlplane. retried 5 times: exec: \"etcd\": executable file not found in $PATH",
          err: <*fmt.wrapError | 0xc0002c06a0>{
              msg: "failed to start the controlplane. retried 5 times: exec: \"etcd\": executable file not found in $PATH",
              err: <*exec.Error | 0xc0002c0640>{
                  Name: "etcd",
                  Err: <*errors.errorString | 0x4d76dc0>{
                      s: "executable file not found in $PATH",
                  },
              },
          },
      }
  occurred
```

**Anything else we need to know?**:

would it help if we increased the number of retries to 10? Maybe we could experiment lowering the number of retries to see if then the error is more common.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T08:20:49Z

Some thought: would it help if we increased the number of retries to 10? Maybe we could experiment lowering the number of retries to see if then the error is more common.

cc @mszadkow who I think was already looking into something similar

cc @mbobrovskyi @sohankunkerkar who may also have some ideas

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-16T17:22:18Z

This looks like this was a transient GitHub issue. `setup-envtest` failed to download `envtest-v1.34.1-linux-amd64.tar.gz`, which left `KUBEBUILDER_ASSETS=""`, so etcd wasn't in PATH. The "retried 5 times" in the error is envtest retrying to start the control plane, not retrying the download. The 4 runs after this one all passed fine.                                                               
              
We could add a guard in the Makefile to fail fast when KUBEBUILDER_ASSETS is empty instead of running all suites just to blow up in BeforeSuite. That'd at least save CI time when this happens again.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T17:35:44Z

> We could add a guard in the Makefile to fail fast when KUBEBUILDER_ASSETS is empty instead of running all suites just to blow up in BeforeSuite. That'd at least save CI time when this happens again.

Good idea, I like fail fast.

On the related topic I think we could do better also retrying connections to external servers which are temporarily unavailable. For example, to repeat fetching from GH with backoff, but this is a separate improvement.

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-03-20T20:48:37Z

/assign @PannagaRao
