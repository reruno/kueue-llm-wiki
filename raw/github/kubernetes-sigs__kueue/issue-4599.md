# Issue #4599: Flaky E2E Test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend a job

**Summary**: Flaky E2E Test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend a job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4599

**Last updated**: 2025-03-20T14:44:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-14T05:56:18Z
- **Updated**: 2025-03-20T14:44:40Z
- **Closed**: 2025-03-20T14:44:40Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

We observed the following test case failure on the periodic Job:

`End To End Custom Configs handling Suite: kindest/node:v1.31.1: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend a job`

```shell
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:116 with:
Expected
    <bool>: true
to be false failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:116 with:
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:117 @ 03/13/25 22:35:22.801
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-main/1900311656727056384

<img width="1448" alt="Image" src="https://github.com/user-attachments/assets/8bb5d4ee-1526-4ccd-8364-b56730920c73" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T05:56:27Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:12:18Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:12:23Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4599#issuecomment-2735673714):

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T08:28:55Z

/reopen
Actually, this would not be affected by the changes to resources, because it is a different suite.

So, to fix it, we need to either bump resources aligning with other e2e tests, or the timeout. We still have a room to increase timeout here, as only 10s was used so far. So, in this case I suggest starting with timeout. Also, in this suite we don't install yet the heavy RayOperator or KubeflowTrainingOperator. I suggest we increase the resources when we decide to install the operators.

cc @mszadkow could you open a PR to bump the timeout?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-20T08:29:00Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4599#issuecomment-2739565981):

>/reopen
>Actually, this would not be affected by the changes to resources, because it is a different suite.
>
>So, to fix it, we need to either bump resources aligning with other e2e tests, or the timeout. We still have a room to increase timeout here, as only 10s was used so far. So, in this case I suggest starting with timeout. Also, in this suite we don't install yet the heavy RayOperator or KubeflowTrainingOperator. I suggest we increase the resources when we decide to install the operators.
>
>cc @mszadkow could you open a PR to bump the timeout?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T08:49:47Z

/assign @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-20T09:53:01Z

I have checked and that lack of proper image does not affect the test, bc what we care here is if there is an admission.
However the job events show this:
```
│   Normal   Scheduled  8s    default-scheduler  Successfully assigned e2e-whqn2/test-job-htfbm to kind-worker2                                        │
│   Normal   Pulling    8s    kubelet            Pulling image "pause"                                                                                 │
│   Warning  Failed     7s    kubelet            Failed to pull image "pause": failed to pull and unpack image "docker.io/library/pause:latest": faile │
│ d to resolve reference "docker.io/library/pause:latest": pull access denied, repository does not exist or may require authorization: server message: │
│  insufficient_scope: authorization failed                                                                                                            │
│   Warning  Failed     7s    kubelet            Error: ErrImagePull                                                                                   │
│   Normal   BackOff    6s    kubelet            Back-off pulling image "pause"                                                                        │
│   Warning  Failed     6s    kubelet            Error: ImagePullBackOff
```
wdyt should we care about all e2e tests have proper container image?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T09:59:35Z

Yes, let's fix the images for all tests. However, this could be a follow up to increasing timeout here.

Alternatively, in this PR we increase timeout, and scope image fixing to customconfigs, wdyt?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-20T10:07:22Z

Can be done in the same one IMO
