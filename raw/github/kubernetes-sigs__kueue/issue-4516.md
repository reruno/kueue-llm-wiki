# Issue #4516: Flaky Test (0.10): TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering

**Summary**: Flaky Test (0.10): TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4516

**Last updated**: 2025-03-19T08:13:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-06T22:57:21Z
- **Updated**: 2025-03-19T08:13:35Z
- **Closed**: 2025-03-19T08:13:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@nasedil](https://github.com/nasedil)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The `End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering` failed on periodic CI

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/statefulset_test.go:94 with:
Expected
    <int32>: 1
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/statefulset_test.go:94 with:
Expected
    <int32>: 1
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/statefulset_test.go:95 @ 03/06/25 22:39:21.027
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-tas-release-0-10/1897774917185703936

<img width="1395" alt="Image" src="https://github.com/user-attachments/assets/bcc13e50-c9ce-4edb-8d43-de5e2c11a6f9" />

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T07:36:32Z

cc @nasedil PTAL as you chase down some of the TAS-related flakes

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T17:34:15Z

/assign nasedil

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-10T07:51:33Z

git bisect suggests that the first bad commit is ab51b3e01a53431d77228cc25a4d076ac481a582, but to me it does not look suspicious.  I will re-test.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T08:12:07Z

Yeah, it does not seem related. Since this is a flake you may need to repeat the runs when bisecting.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-10T11:44:28Z

I reran bisect, looks like the flake was introduced here 4f9c31ba0cc56f8d3a22d7a6051c8043d6d4c9c7

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T12:19:14Z

This sounds reasonable, maybe some intersection between introduction of agnhost and StatefulSets. 

Before we moved to agnhost this test was rather stable (I don't remember flakes here). Once we moved to agnhost it remained stable, because we didn't really do any upgrade. Now, as we moved to agnhost and do upgrade there is an issue.

Since the test was stable before agnhost image I believe the StatefulSet logic is ok, and we are likely hitting a test code issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T12:25:44Z

Actually, https://github.com/kubernetes-sigs/kueue/commit/4f9c31ba0cc56f8d3a22d7a6051c8043d6d4c9c7 wouldn't explain the failures in `e2e/tas/statefulset_test.go:95`. I was thinking it might be explaining the failures https://github.com/kubernetes-sigs/kueue/issues/4520. In any case more investigation is needed.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:13:30Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:13:34Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4516#issuecomment-2735676988):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
