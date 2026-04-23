# Issue #6980: Replace Scheduler stubs with interceptor functions

**Summary**: Replace Scheduler stubs with interceptor functions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6980

**Last updated**: 2025-11-03T18:42:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2025-09-24T08:06:18Z
- **Updated**: 2025-11-03T18:42:08Z
- **Closed**: 2025-11-03T18:42:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

**What would you like to be cleaned**:
As mention here: https://github.com/kubernetes-sigs/kueue/pull/6962#discussion_r2372511842

Investigation a possibility to drop stubs of Scheduler, that could be possibly replaced with proper interceptor functions of FakeClient.

**Why is this needed**:
Scheduler stubs add extra layer of indirection that potentially could be avoided.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-26T09:32:41Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T09:39:43Z

Awesome, thank you for working on that. This stub pattern is legacy

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-02T13:05:49Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-02T13:05:55Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6980#issuecomment-3361150281):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:06:23Z

/close
I think this is completed after https://github.com/kubernetes-sigs/kueue/pull/7153 is merged, along with cherrypicks.

Let me know if I missed something.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-24T06:23:02Z

/reopen

Still need to remove preemption stubs:

https://github.com/kubernetes-sigs/kueue/blob/178155c7eadd36393cecb5da349995c946918b78/pkg/scheduler/preemption/preemption.go#L62-L63

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-24T06:23:08Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6980#issuecomment-3441275192):

>/reopen
>
>Still need to remove preemption stubs:
>
>https://github.com/kubernetes-sigs/kueue/blob/178155c7eadd36393cecb5da349995c946918b78/pkg/scheduler/preemption/preemption.go#L62-L63


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
