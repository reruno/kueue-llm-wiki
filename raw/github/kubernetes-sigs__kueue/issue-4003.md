# Issue #4003: Flaky Test: Multikueue no GC Should remove the worker's workload when AC is rejected (from ready)

**Summary**: Flaky Test: Multikueue no GC Should remove the worker's workload when AC is rejected (from ready)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4003

**Last updated**: 2025-01-20T07:31:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-01-20T05:54:15Z
- **Updated**: 2025-01-20T07:31:22Z
- **Closed**: 2025-01-20T06:36:47Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failure on "Multikueue Suite: [It] Multikueue no GC Should remove the worker's workload when AC is rejected (from ready) [slow]".

```shell
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/multikueue_test.go:1754 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/multikueue_test.go:1754 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/multikueue_test.go:1755 @ 01/17/25 18:25:51.581
}
```

**What you expected to happen**:
Always succeeded

**How to reproduce it (as minimally and precisely as possible)**:

- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1880316928468193280
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1881041710994165760

<img width="1469" alt="Image" src="https://github.com/user-attachments/assets/f252f29c-c031-49e4-865f-048dd9b32b9f" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-20T05:57:46Z

This case was added in https://github.com/kubernetes-sigs/kueue/pull/3938.
@mszadkow Could you investigate this?

This might affect on today's release schedule.
cc: @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-20T05:57:55Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-20T06:25:46Z

This is a new test failing added recently https://github.com/kubernetes-sigs/kueue/pull/3938 and it has not been cherry-picked yet, so should not interfer with the release branches.

As for the main I think the flake demonstrates that actually the issue https://github.com/kubernetes-sigs/kueue/issues/3841 exists. I want to reopen the issue and rollback the PR adding the test.

Rollback of the PR will fix the flake and we will re add the test once the underlying issue is fixed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-20T06:36:43Z

> This is a new test failing added recently [#3938](https://github.com/kubernetes-sigs/kueue/pull/3938) and it has not been cherry-picked yet, so should not interfer with the release branches.
> 
> As for the main I think the flake demonstrates that actually the issue [#3841](https://github.com/kubernetes-sigs/kueue/issues/3841) exists. I want to reopen the issue and rollback the PR adding the test.
> 
> Rollback of the PR will fix the flake and we will re add the test once the underlying issue is fixed.

That sounds great to me. Let me close this for now.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-20T06:36:48Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4003#issuecomment-2601482454):

>> This is a new test failing added recently [#3938](https://github.com/kubernetes-sigs/kueue/pull/3938) and it has not been cherry-picked yet, so should not interfer with the release branches.
>> 
>> As for the main I think the flake demonstrates that actually the issue [#3841](https://github.com/kubernetes-sigs/kueue/issues/3841) exists. I want to reopen the issue and rollback the PR adding the test.
>> 
>> Rollback of the PR will fix the flake and we will re add the test once the underlying issue is fixed.
>
>That sounds great to me. Let me close this for now.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-20T07:31:21Z

Revert PR
https://github.com/kubernetes-sigs/kueue/pull/4005
