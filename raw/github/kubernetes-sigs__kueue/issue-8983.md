# Issue #8983: [Flaky MultiKueue E2E] ERROR: unknown cluster

**Summary**: [Flaky MultiKueue E2E] ERROR: unknown cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8983

**Last updated**: 2026-03-04T07:00:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-04T14:11:57Z
- **Updated**: 2026-03-04T07:00:22Z
- **Closed**: 2026-03-04T07:00:22Z
- **Labels**: `kind/bug`, `kind/flake`, `area/multikueue`
- **Assignees**: [@TapanManu](https://github.com/TapanManu)
- **Comments**: 5

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

periodic-kueue-test-e2e-multikueue-release-0-15.Overall

**First observed in** (PR or commit, if known):

Periodic multikueue end to end tests.

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2019043147618717696

**Failure message or logs**:
```
ERROR: unknown cluster "kind-worker1"
ERROR: unknown cluster "kind-worker2"
ERROR: unknown cluster "kind-manager"
E0204 13:45:48.646569   29729 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.647444   29729 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.649390   29729 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.650429   29729 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.651226   29729 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.652047   29735 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
E0204 13:45:48.652873   29735 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.654823   29735 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.655587   29735 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.655755   29734 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.656652   29734 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.657437   29735 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
E0204 13:45:48.658617   29734 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.659342   29734 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.661264   29734 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
E0204 13:45:48.720866   29756 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.721947   29756 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.722839   29756 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.724717   29756 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.725077   29761 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.725412   29756 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.725881   29761 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
E0204 13:45:48.727372   29766 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.727745   29761 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.728206   29766 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.728422   29761 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.730089   29766 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.730175   29761 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
The connection to the server localhost:8080 was refused - did you specify the right host or port?
E0204 13:45:48.730819   29766 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
E0204 13:45:48.732669   29766 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp [::1]:8080: connect: connection refused"
```

**Anything else we need to know?**:

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:48:59Z

/area multikueue

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-02-21T08:34:38Z

@mbobrovskyi 

I just ran into this exact same wall of connection refused and unknown cluster errors while running make run-test-multikueue-e2e-1.34.0 locally!

I did some digging into my local logs, and I wanted to share my findings in case it helps track down why this is flaking in CI.

In my case, the root cause was a transient network timeout in Docker while pulling the node image (Client.Timeout exceeded while awaiting headers), which caused kind to fail cluster creation. However, I noticed two secondary issues that made this really hard to debug:

1. **Lack of Fail-Fast:** When kind create cluster failed, the e2e-multikueue-test.sh script did not abort. It continued executing the test suite against non-existent clusters, which generated the massive wall of misleading http://localhost:8080/api connection errors.

2. **Kubeconfig Lock Race Condition:** Because the script attempts to spin up/tear down multiple clusters concurrently, the failure caused a race condition that left a permanent ~/.kube/config.lock file on my machine:
`failed to lock config file: open /Users/.../.kube/config.lock: file exists`

Potential fixes to consider:

1. Should we try Adding a strict check to abort the script immediately if the manager or worker clusters fail to provision.

2. Utilizing isolated, temporary KUBECONFIG files for the E2E test clusters instead of relying on the default ~/.kube/config to avoid the locking race condition.

Happy to help test any script updates for this if needed!

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-21T11:02:11Z

@TapanManu Thank you so much for looking into this and for the deep-dive investigation!

> Happy to help test any script updates for this if needed!

Sure – feel free to create PRs for this.

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-03-01T06:02:35Z

/assign

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-03-01T07:28:51Z

@mbobrovskyi have created a PR for fixing the script, could you review and see if its ok to proceed ?
