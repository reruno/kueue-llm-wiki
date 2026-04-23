# Issue #9352: [Flaky E2E] Error pulling image configuration

**Summary**: [Flaky E2E] Error pulling image configuration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9352

**Last updated**: 2026-02-27T17:10:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-19T01:40:37Z
- **Updated**: 2026-02-27T17:10:51Z
- **Closed**: 2026-02-27T17:10:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Error pulling image configuration: download failed after attempts=6: received unexpected HTTP status: 500 Internal Server Error

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/2024217633649332224

**Failure message or logs**:
```
error pulling image configuration: download failed after attempts=6: received unexpected HTTP status: 500 Internal Server Error
error: no context exists with the name: "kind-kind"
ERROR: unknown cluster "kind"
E0218 20:28:55.348847   30895 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.349864   30895 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.351839   30895 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.352659   30895 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.354598   30895 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
E0218 20:28:55.432085   30904 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.433021   30904 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.435178   30904 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.436063   30904 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0218 20:28:55.438115   30904 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
Deleting cluster "kind" ...
make: *** [Makefile-test.mk:180: run-test-e2e-singlecluster-1.34.3] Error 1
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T07:39:57Z

`ERROR: unknown cluster "kind"` nice, in that case it means the cluster is deleted (just with some delay) so we were retrying.

In that case we should stop retrying to delete the cluster, just detect the situation (either by exit code, if dedicated), or message matching

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T17:10:45Z

/close
adderessed by https://github.com/kubernetes-sigs/kueue/pull/9577
We have a sibling issue for the populator: https://github.com/kubernetes-sigs/kueue/issues/9582

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-27T17:10:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9352#issuecomment-3974067038):

>/close
>adderessed by https://github.com/kubernetes-sigs/kueue/pull/9577
>We have a sibling issue for the populator: https://github.com/kubernetes-sigs/kueue/issues/9582


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
