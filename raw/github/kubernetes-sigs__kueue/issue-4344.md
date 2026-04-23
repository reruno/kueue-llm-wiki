# Issue #4344: Failing Test: MXJob controller when TopologyAwareScheduling enabled should admit workload which fits in a required topology domain

**Summary**: Failing Test: MXJob controller when TopologyAwareScheduling enabled should admit workload which fits in a required topology domain

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4344

**Last updated**: 2025-03-07T18:23:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-21T11:45:46Z
- **Updated**: 2025-03-07T18:23:52Z
- **Closed**: 2025-03-07T18:23:51Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@nasedil](https://github.com/nasedil)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky integration tests: `MXJob Controller Suite: [It] MXJob controller when TopologyAwareScheduling enabled should admit workload which fits in a required topology domain [Redundant]`

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:313 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:313 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/mxjob/mxjob_controller_test.go:446 @ 02/21/25 01:44:58.745
}
```

**What you expected to happen**:
Non errros.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-10/1892750118059249664

<img width="1072" alt="Image" src="https://github.com/user-attachments/assets/eb98ce61-40bb-4056-86eb-c46e583836f8" />

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T11:46:05Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T11:58:33Z

cc @mbobrovskyi @mszadkow PTAL

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-05T14:03:05Z

/retitle Failing Test: MXJob controller when TopologyAwareScheduling enabled should admit workload which fits in a required topology domain

Looks like it has been failing for about two weeks without any success. It is only for 0.10 also.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T15:05:53Z

Indeed it fails consistently: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-release-0-10
since 20th Feb: 

![Image](https://github.com/user-attachments/assets/00e453b5-7260-49d5-bca5-ae13188c6b0c)

https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-10?buildId=1894380878721716224

We need to correlate it with the commit, and find out what went wrong.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T15:06:49Z

cc @nasedil

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T16:34:00Z

/assign

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T17:11:10Z

I ran git bisect and the result is that cb91c2464a7750532e1b24350285f2a41a838a17 is the first bad commit

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T17:15:41Z

Ah, I guess we must have forgotten adding `corev1.ResourcePods:   resource.MustParse("10"),` in this test.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T17:32:01Z

> Ah, I guess we must have forgotten adding `corev1.ResourcePods: resource.MustParse("10"),` in this test.

yes, that fixes the test.  How should I apply the fix?  I realize that in main branch these files are nonexistent

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T17:37:29Z

Open PR directly against release-0.10 branch. When creating the PR you can choose it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T18:23:47Z

/close 
As https://github.com/kubernetes-sigs/kueue/pull/4521 merged

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-07T18:23:52Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4344#issuecomment-2707114272):

>/close 
>As https://github.com/kubernetes-sigs/kueue/pull/4521 merged


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
