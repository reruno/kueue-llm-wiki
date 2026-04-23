# Issue #1484: Flaky: Provisioning when A workload is using a provision admission check Should let a running workload to continue after the provisioning request deleted

**Summary**: Flaky: Provisioning when A workload is using a provision admission check Should let a running workload to continue after the provisioning request deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1484

**Last updated**: 2023-12-21T11:17:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-18T15:44:41Z
- **Updated**: 2023-12-21T11:17:07Z
- **Closed**: 2023-12-21T11:17:07Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@B1F030](https://github.com/B1F030)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed "[It] Provisioning when A workload is using a provision admission check Should let a running workload to continue after the provisioning request deleted"

**What you expected to happen**:

No error wouldn't happen.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1468/pull-kueue-test-integration-main/1736772290600767488

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T15:47:11Z

/kind flake

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T16:21:26Z

/assign trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-12-18T17:06:24Z

@alculquicondor where is this  test scenario coming from? What do we actually expect in this case (provisioning request deletion while admitted)?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T17:15:44Z

oh, we added this recently @B1F030

The lifecycle of ProvReq object is independent from the Workload. You can think of a customer having a controller cleaning up ProvReq objects

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T17:15:58Z

/unassign @trasc 
/assing @B1F030

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T18:08:06Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1487/pull-kueue-test-integration-main/1736808350944858112

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T19:02:24Z

/assign @B1F030

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-18T19:02:27Z

@tenzen-y: GitHub didn't allow me to assign the following users: B1F030.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1484#issuecomment-1861354423):

>/assign @B1F030


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-19T03:45:27Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-12-19T05:34:46Z

> The lifecycle of ProvReq object is independent from the Workload. You can think of a customer having a controller cleaning up ProvReq objects

But the admission check controller will recreate the provisioning request, which at lease in the early stages will not be available and the workload will get evicted.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-19T11:25:58Z

> But the admission check controller will recreate the provisioning request, which at lease in the early stages will not be available and the workload will get evicted.

IIUC if the workload is already admitted (running) then we would not be sync the provisioning requests (`syncOwnedProvisionRequest`), because we exit earlier: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/provisioning/controller.go#L138.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-19T15:42:51Z

That's why we added the test. That's the behavior we want and we want to make sure it doesn't regress.
