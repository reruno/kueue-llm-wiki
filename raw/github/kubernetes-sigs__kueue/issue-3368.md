# Issue #3368: Flaky E2E Test: Pod groups when Single CQ should admit group that fits

**Summary**: Flaky E2E Test: Pod groups when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3368

**Last updated**: 2024-10-31T08:09:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-10-30T05:24:23Z
- **Updated**: 2024-10-31T08:09:07Z
- **Closed**: 2024-10-31T08:09:05Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
Failed End To End Suite: kindest/node:v1.29.4: [It] Pod groups when Single CQ should admit group that fits.

```
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:685 with:
Expected workload to be finalized
Expected
    <[]string | len:1, cap:4>: [
        "kueue.x-k8s.io/resource-in-use",
    ]
to be empty failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:685 with:
Expected workload to be finalized
Expected
    <[]string | len:1, cap:4>: [
        "kueue.x-k8s.io/resource-in-use",
    ]
to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:130 @ 10/30/24 05:16:41.103
}
```

**What you expected to happen**:
No errors happened

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3367/pull-kueue-test-e2e-main-1-29/1851491513939267584

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-30T07:15:49Z

/reopen

Due to https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3367/pull-kueue-test-e2e-main-1-29/1851518472048087040 and https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3367/pull-kueue-test-e2e-main-1-30/1851518474547892224.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-30T07:15:53Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3368#issuecomment-2446044793):

>/reopen
>
>Due to https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3367/pull-kueue-test-e2e-main-1-29/1851518472048087040.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-31T08:03:46Z

Isn't this reoccurring, right?
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-31T08:03:50Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3368#issuecomment-2449267177):

>Isn't this reoccurring, right?
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-31T08:05:58Z

> Isn't this reoccurring, right? /reopen

You mean here https://github.com/kubernetes-sigs/kueue/pull/3384? No, it happens before. 

https://github.com/kubernetes-sigs/kueue/pull/3383 should fix it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-31T08:09:01Z

> You mean here #3384? No, it happens before.

Oh, I see. Thank you for letting me know.
I was missed the PR.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-31T08:09:06Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3368#issuecomment-2449275795):

>> You mean here #3384? No, it happens before.
>
>Oh, I see. Thank you for letting me know.
>I was missed the PR.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
