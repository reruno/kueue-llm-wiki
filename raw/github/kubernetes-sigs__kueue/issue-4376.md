# Issue #4376: Flaky Test: MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted

**Summary**: Flaky Test: MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4376

**Last updated**: 2025-03-19T08:15:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-24T12:47:50Z
- **Updated**: 2025-03-19T08:15:52Z
- **Closed**: 2025-03-19T08:15:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The below E2E test case failed in unrelated PR:

`End To End MultiKueue Suite: kindest/node:v1.31.2: [It] MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted`

```shell
{Expected
    <string>: Internal error occurred: error executing command in container: failed to exec in container: failed to create exec "0c0eab3acc210c78029f12abd60c3ac7a6149ce617809ac123da928f9fffa2b5": task 6ac8586efc6285b09f2d01bb6dfbc669f23b4164cacbdf623aae114fb13f346e not found: not found
to contain substring
    <string>: 137 failed [FAILED] Expected
    <string>: Internal error occurred: error executing command in container: failed to exec in container: failed to create exec "0c0eab3acc210c78029f12abd60c3ac7a6149ce617809ac123da928f9fffa2b5": task 6ac8586efc6285b09f2d01bb6dfbc669f23b4164cacbdf623aae114fb13f346e not found: not found
to contain substring
    <string>: 137
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:609 @ 02/24/25 12:39:23.83
}
```

**What you expected to happen**:
Never errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4375/pull-kueue-test-e2e-multikueue-main/1893999933191622656

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T12:47:57Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T12:48:24Z

cc @dgrove-oss

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-25T07:02:28Z

x-ref with potentially the same underlying bug: https://github.com/kubernetes-sigs/kueue/issues/4378

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:15:46Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:15:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4376#issuecomment-2735682017):

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
