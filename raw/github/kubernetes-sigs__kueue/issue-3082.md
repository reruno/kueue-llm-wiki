# Issue #3082: After the Jobs are stopped, Job PodTemplate Labels are not restored only during unit testing

**Summary**: After the Jobs are stopped, Job PodTemplate Labels are not restored only during unit testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3082

**Last updated**: 2024-10-02T15:19:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-09-17T19:03:29Z
- **Updated**: 2024-10-02T15:19:51Z
- **Closed**: 2024-10-02T15:19:32Z
- **Labels**: `kind/support`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Only during unit testing, the Job PodTemplate Labels (`.spec.template.labels`) are not restored. 
But, during integration testing and actual cluster running, they are restored after the Jobs are suspended.

**What you expected to happen**:
The Job PodTemplate Labels are always restored after the Jobs are stopped.

**How to reproduce it (as minimally and precisely as possible)**:
We can see the reproduced PR and CI logs there:

- https://github.com/kubernetes-sigs/kueue/pull/3081
- https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3081/pull-kueue-test-unit-main/1836114474063368192

**Anything else we need to know?**:
We verify if those labels (.spec.template.labels) are restored only during the integration testing, and the testing always successful: https://github.com/kubernetes-sigs/kueue/blob/e812a0682a4d96b4a4a82f654202ce3d50d52541/test/integration/controller/jobs/job/job_controller_test.go#L756-L767

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-09-18T09:04:26Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-09-19T10:46:23Z

@tenzen-y please have a look at my explanation here: https://github.com/kubernetes-sigs/kueue/pull/3081/files#r1766613892

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-02T15:19:27Z

> @tenzen-y please have a look at my explanation here: https://github.com/kubernetes-sigs/kueue/pull/3081/files#r1766613892

As I commented the above PR, this is my misunderstanding. 
@mszadkow Thank you for the investigation, again!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-02T15:19:33Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3082#issuecomment-2388954127):

>> @tenzen-y please have a look at my explanation here: https://github.com/kubernetes-sigs/kueue/pull/3081/files#r1766613892
>
>As I commented the above PR, this is my misunderstanding. 
>@mszadkow Thank you for the investigation, again!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-02T15:19:46Z

/remove-kind bug
/kind support
