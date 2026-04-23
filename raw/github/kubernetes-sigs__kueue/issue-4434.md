# Issue #4434: Flaky Test: Pod groups when Single CQ should allow to preempt the lower priority group

**Summary**: Flaky Test: Pod groups when Single CQ should allow to preempt the lower priority group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4434

**Last updated**: 2025-03-18T09:31:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-27T17:34:55Z
- **Updated**: 2025-03-18T09:31:51Z
- **Closed**: 2025-03-18T09:31:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The below E2E test failed.

```
End To End Suite: kindest/node:v1.30.0: [It] Pod groups when Single CQ should allow to preempt the lower priority group
```

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:483 with:
Expected
    <v1.PodPhase>: Succeeded
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:483 with:
Expected
    <v1.PodPhase>: Succeeded
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:485 @ 02/27/25 01:48:44.842
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-10-1-30/1894925220897099776

<img width="1407" alt="Image" src="https://github.com/user-attachments/assets/290cd7bf-ef6f-4bc9-9ecf-1e962c79c977" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-27T17:35:06Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-27T17:43:06Z

/assign @mszadkow 
I believe this is after the recent changes, as we use BehaviorExitFast. The Pod succeeds if it has enough time to complete, it fails if the Delete request is faster. I think we should use WaitForDeletion, and just let the pod to be deleted and failed. We may just need to use Pod's `spec.terminationgraceperiodseconds`=1 to make it fast. ~Alternatively trigger /exit 1 instead of exit 1 to let it fail.~ - this will not work becuase the Pod is deleted due to preemption.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-28T09:49:27Z

Got it, will try with suggested solution.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-04T09:58:34Z

/reopen
it failed in the exactly same place after the "fix" was merged: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4418/pull-kueue-test-e2e-main-1-29/1896856206312476672. So, I think it didn't help in the end.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-04T09:58:39Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4434#issuecomment-2696894350):

>/reopen
>it failed in the exactly same place after the "fix" was merged: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4418/pull-kueue-test-e2e-main-1-29/1896856206312476672. So, I think it didn't help in the end.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T08:34:32Z

I think the  other problem might be that WaitForActivePodsAndTerminate captures all pods in the  namespace currently, and in this test there are two groups with potentially active pods at the same time. I think we should strenghten the labels selector in this  case. Maybe the function could accept an extra labels selector which will allow to target pods for specific groups. 

cc @mszadkow @dgrove-oss (in case this might be also related to appwrapper flakes)

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-05T08:40:06Z

> I think the other problem might be that WaitForActivePodsAndTerminate captures all pods in the namespace currently, and in this test there are two groups with potentially active pods at the same time. I think we should strenghten the labels selector in this case. Maybe the function could accept an extra labels selector which will allow to target pods for specific groups.
> 
> cc [@mszadkow](https://github.com/mszadkow) [@dgrove-oss](https://github.com/dgrove-oss) (in case this might be also related to appwrapper flakes)

That's something I missed there, yes, we definitively need more filtering on pods termination.

However for this issue there another thing (a reason to flake), that sometimes preemption results in pod success, although it was programmed to `exit 1`.
```
g.Expect(p.Status.Phase).To(gomega.Equal(corev1.PodFailed)) <- line 483
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T09:25:56Z

> However for this issue there another thing (a reason to flake), that sometimes preemption results in pod success, although it was programmed to exit 1.

Right, but maybe WaitForActivePodsAndTerminate catches some other pods in the namespace, not sure, but since the selector is not targeting specific group it is hard to tell imo. 

For better debuggability we may start with outputting the names of the pods which are being terminated in WaitForActivePodsAndTerminate. Then, also make this line `g.Expect(p.Status.Phase).To(gomega.Equal(corev1.PodFailed))` output the name of the asserted pod. There is some syntax like `Should(gomega.HaveField("Status.Phase", gomega.Equal(corev1.PodFailed))`, ptal: https://github.com/kubernetes/kubernetes/blob/9d9e1afdf78bce0a517cc22557457f942040ca19/test/e2e/apps/job.go#L1324-L1326. IIUC in case of failure it would return the entire pod object (including its name).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T08:49:06Z

This seems to remain an issue as it failed here: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4503/pull-kueue-test-e2e-main-1-30/1897308527806910464

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T10:13:22Z

This test also failed once when I ran e2e tests locally

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T17:08:49Z

It just happened on an unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4562/pull-kueue-test-e2e-main-1-31/1900226809132224512

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T17:10:41Z

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:206 with:
Expected
    <v1.PodPhase>: Pending
to equal
    <v1.PodPhase>: Running failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:206 with:
Expected
    <v1.PodPhase>: Pending
to equal
    <v1.PodPhase>: Running
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:207 @ 03/13/25 17:01:21.384

There were additional failures detected after the initial failure. These are visible in the timeline
```
or maybe this is yet another issue, but just in the same file
