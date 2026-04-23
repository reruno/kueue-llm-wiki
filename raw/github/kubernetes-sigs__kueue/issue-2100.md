# Issue #2100: Fleky Test: Scheduler Suite: [It] Preemption When most quota is in a shared ClusterQueue in a cohort should allow preempting workloads while borrowing

**Summary**: Fleky Test: Scheduler Suite: [It] Preemption When most quota is in a shared ClusterQueue in a cohort should allow preempting workloads while borrowing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2100

**Last updated**: 2024-04-30T16:38:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-04-29T16:21:51Z
- **Updated**: 2024-04-30T16:38:31Z
- **Closed**: 2024-04-30T16:38:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
Failure on `Scheduler Suite: [It] Preemption When most quota is in a shared ClusterQueue in a cohort should allow preempting workloads while borrowing`.

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2081/pull-kueue-test-integration-release-0-6/1783900768210784256

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc000ef1040>: 
    resourceflavors.kueue.x-k8s.io "one" already exists
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "resourceflavors.kueue.x-k8s.io \"one\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "one",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000ef1040>: 
    resourceflavors.kueue.x-k8s.io "one" already exists
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "resourceflavors.kueue.x-k8s.io \"one\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "one",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/scheduler/preemption_test.go:496 @ 04/26/24 16:55:22.651

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**What you expected to happen**:
No errors happen.

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T16:22:29Z

I observed this at #2081.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-04-30T07:11:47Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-04-30T14:56:35Z

@tenzen-y This issue seems to be caused because we're missing the deletion of the resource flavor after each test. Here we're creating it 
https://github.com/kubernetes-sigs/kueue/blob/8127d46d54febb2d5fd5f5a19ed32e0fc8206099/test/integration/scheduler/preemption_test.go#L417 

but then, in `AfterEach` that object isn't deleted.

https://github.com/kubernetes-sigs/kueue/blob/8127d46d54febb2d5fd5f5a19ed32e0fc8206099/test/integration/scheduler/preemption_test.go#L446 

However, this was fixed already in #1930. Should we cherry pick that commit?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-30T16:14:12Z

> @tenzen-y This issue seems to be caused because we're missing the deletion of the resource flavor after each test. Here we're creating it
> 
> https://github.com/kubernetes-sigs/kueue/blob/8127d46d54febb2d5fd5f5a19ed32e0fc8206099/test/integration/scheduler/preemption_test.go#L417
> 
> but then, in `AfterEach` that object isn't deleted.
> 
> https://github.com/kubernetes-sigs/kueue/blob/8127d46d54febb2d5fd5f5a19ed32e0fc8206099/test/integration/scheduler/preemption_test.go#L446
> 
> However, this was fixed already in #1930. Should we cherry pick that commit?

@IrvingMg Oh, good catch! Thank you for investigating this!
Let me cherry-pick that PR by prow.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-30T16:38:26Z

This would be resolved by #2103 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-30T16:38:30Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2100#issuecomment-2085924108):

>This would be resolved by #2103 
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
