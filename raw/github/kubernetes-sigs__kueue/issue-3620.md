# Issue #3620: [TAS Flaky test] TopologyAwareScheduling for Job when Creating a Job Should allow to run a Job with parallelism < completions

**Summary**: [TAS Flaky test] TopologyAwareScheduling for Job when Creating a Job Should allow to run a Job with parallelism < completions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3620

**Last updated**: 2024-11-25T13:12:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-25T09:38:13Z
- **Updated**: 2024-11-25T13:12:59Z
- **Closed**: 2024-11-25T13:12:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

The test flaked on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3528/pull-kueue-test-tas-e2e-main/1860964874574630912

**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat on CI

**Anything else we need to know?**:

```
TopologyAwareScheduling for Job when Creating a Job Should allow to run a Job with parallelism < completions
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/job_test.go:228
  STEP: verify the workload "e2e-tas-job-nwd4c/job-test-job-3ba63" gets TopologyAssignment becomes finished @ 11/25/24 08:42:28.731
  [PANICKED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/gomega/internal/async_assertion.go:321 @ 11/25/24 08:42:28.783
• [PANICKED] [1.464 seconds]
TopologyAwareScheduling for Job when Creating a Job [It] Should allow to run a Job with parallelism < completions
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/job_test.go:228
  [PANICKED] Test Panicked
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/gomega/internal/async_assertion.go:321 @ 11/25/24 08:42:28.783
  runtime error: invalid memory address or nil pointer dereference
  Full Stack Trace
    github.com/onsi/gomega/internal.(*AsyncAssertion).buildActualPoller.func3.1()
    	/home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/gomega/internal/async_assertion.go:321 +0x186
    panic({0x18d6140?, 0x2bfe7f0?})
    	/usr/local/go/src/runtime/panic.go:785 +0x132
    sigs.k8s.io/kueue/test/e2e/tas.init.func1.3.6.1.1({0x1df0de0, 0xc000467c40})
    	/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/job_test.go:248 +0xcf
    reflect.Value.call({0x1829e00?, 0xc0006125d0?, 0xc0001a5738?}, {0x1b06e7c, 0x4}, {0xc000012f78, 0x1, 0x0?})
    	/usr/local/go/src/reflect/value.go:581 +0xca6
    reflect.Value.Call({0x1829e00?, 0xc0006125d0?, 0xc000467c40?}, {0xc000012f78?, 0xc0006125d0?, 0x1829e00?})
    	/usr/local/go/src/reflect/value.go:365 +0xb9
    github.com/onsi/gomega/internal.(*AsyncAssertion).buildActualPoller.func3()
    	/home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/gomega/internal/async_assertion.go:325 +0x11f
    github.com/onsi/gomega/internal.(*AsyncAssertion).match(0xc0002[610](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3528/pull-kueue-test-tas-e2e-main/1860964874574630912#1:build-log.txt%3A610)a0, {0x1dd6f90, 0x2c6dd20}, 0x1, {0x0, 0x0, 0x0})
    	/home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/gomega/internal/async_assertion.go:398 +0x179
    github.com/onsi/gomega/internal.(*AsyncAssertion).Should(0xc0002610a0, {0x1dd6f90, 0x2c6dd20}, {0x0, 0x0, 0x0})
    	/home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/gomega/internal/async_assertion.go:145 +0x86
    sigs.k8s.io/kueue/test/e2e/tas.init.func1.3.6.1()
    	/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/job_test.go:250 +0x11f
    sigs.k8s.io/kueue/test/e2e/tas.init.func1.3.6()
    	/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/job_test.go:245 +0x991
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-25T09:38:24Z

/kind flake
/assign
