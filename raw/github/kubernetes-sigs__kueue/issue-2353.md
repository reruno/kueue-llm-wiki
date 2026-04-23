# Issue #2353: Flaky integration test: Should print workloads list with paging

**Summary**: Flaky integration test: Should print workloads list with paging

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2353

**Last updated**: 2024-06-11T15:46:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-06-04T17:45:12Z
- **Updated**: 2024-06-11T15:46:08Z
- **Closed**: 2024-06-11T15:46:08Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

Integration test failed: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2314/pull-kueue-test-integration-main/1798039851593895936

**What you expected to happen**:

No flake

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build.

**Anything else we need to know?**:

```
  [FAILED] Expected
      <string>: "...     1s
      "
  to equal               |
      <string>: "...     0s
      "
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/list_test.go:206 @ 06/04/24 17:19:10.001
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-04T19:04:30Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-05T12:07:36Z

As discussed [here](https://github.com/kubernetes-sigs/kueue/pull/2354#discussion_r1627577356) need to fix tests using fake clock.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-06T06:43:50Z

It seems the fake clock is WIP here: https://github.com/kubernetes-sigs/kueue/pull/2364

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-10T15:30:13Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-10T15:30:18Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2353#issuecomment-2158666004):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-10T15:31:38Z

Still have issue https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2392/pull-kueue-test-integration-main/1800186041294917632.

```
{Expected
    <string>: "...     0s
    wl1..."
to equal               |
    <string>: "...     1s
    wl1..." failed [FAILED] Expected
    <string>: "...     0s
    wl1..."
to equal               |
    <string>: "...     1s
    wl1..."
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/list_test.go:227 @ 06/10/24 15:26:45.03
}
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-11T06:28:40Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2346/pull-kueue-test-integration-main/1800200554622750720

```
{Expected
    <string>: "...     true  ..."
to equal               |
    <string>: "...     false ..." failed [FAILED] Expected
    <string>: "...     true  ..."
to equal               |
    <string>: "...     false ..."
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/list_test.go:168 @ 06/10/24 16:24:51.58
}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-11T15:37:56Z

/reopen 
For the https://github.com/kubernetes-sigs/kueue/pull/2399 fix.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-11T15:38:01Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2353#issuecomment-2161071423):

>/reopen 
>For the https://github.com/kubernetes-sigs/kueue/pull/2399 fix.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
