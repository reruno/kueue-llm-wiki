# Issue #7377: [flaky test] Should update the cluster status to reflect the connection state

**Summary**: [flaky test] Should update the cluster status to reflect the connection state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7377

**Last updated**: 2025-11-12T07:53:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-24T08:32:50Z
- **Updated**: 2025-11-12T07:53:35Z
- **Closed**: 2025-11-12T07:53:34Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description


**What happened**:

Failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7249/pull-kueue-test-e2e-multikueue-main/1981624596008275968

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```

End To End MultiKueue Suite: kindest/node:v1.34.0: [It] MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state expand_less	1m55s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:115 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:115 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:179 @ 10/24/25 07:51:56.672
}
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-07T11:52:21Z

Is it duplicate of https://github.com/kubernetes-sigs/kueue/issues/6573?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:53:28Z

Looks like so by the error, let me close:
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-12T07:53:35Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7377#issuecomment-3520517764):

>Looks like so by the error, let me close:
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
