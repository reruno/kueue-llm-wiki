# Issue #4139: [Flaky test] Metrics-related e2e tests fail occasionally

**Summary**: [Flaky test] Metrics-related e2e tests fail occasionally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4139

**Last updated**: 2025-02-17T08:54:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-03T16:07:32Z
- **Updated**: 2025-02-17T08:54:25Z
- **Closed**: 2025-02-17T08:54:25Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 2

## Description

/kind flake

**What happened**:

metrics related e2e tests failed in runs of an unrelated branch
- "Metrics when workload is admitted should ensure the default metrics are available" https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-32/1886439313932029952
- "Metrics when workload is admitted with eviction and preemption should ensure the eviction and preemption metrics are available" https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat on CI

**Anything else we need to know?**:

```
{Timed out after 10.143s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/metrics_test.go:623 with:
Metric kueue_local_queue_quota_reserved_workloads_total was found in output # HELP certwatcher_read_certificate_errors_total Total number of certificate read errors
# TYPE certwatcher_read_certificate_errors_total counter
certwatcher_read_certificate_errors_total 0
# HELP certwatcher_read_certificate_total Total number of certificate reads
# TYPE certwatcher_read_certificate_total counter
certwatcher_read_certificate_total 23
# HELP controller_runtime_active_workers Number of currently used workers per controller
# TYPE controller_runtime_active_workers gauge
controller_runtime_active_workers{controller="admissioncheck"} 0
controller_runtime_active_workers{controller="appwrapper"} 0
controller_runtime_active_workers{controller="cert-rotator"} 0
controller_runtime_active_workers{controller="clusterqueue"} 0
controller_runtime_active_workers{controller="cohort"} 0
controller_runtime_active_workers{controller="job"} 0
controller_runtime_active_workers{controller="jobset"} 0
controller_runtime_active_workers{controller="leaderworkerset"} 0
controller_runtime_active_workers{controller="leaderworkerset-pod"} 0
controller_runtime_active_workers{controller="localqueue"} 0
controller_runtime_active_workers{controller="multikueue-admissioncheck"} 0
controller_runtime_active_workers{controller="multikueue-workload"} 0
controller_runtime_active_workers{controller="multikueuecluster"} 0
controller_runtime_active_workers{controller="provisioning-admissioncheck"} 0
controller_runtime_active_workers{controller="provisioning-workload"} 0

...

leader_election_master_status{name="c1f6bfd2.kueue.x-k8s.io"} 1
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 9.36
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.073741816e+09
# HELP process_network_receive_bytes_total Number of bytes received by the process over the network.
# TYPE process_network_receive_bytes_total counter
process_network_receive_bytes_total 1.072063e+07
# HELP process_network_transmit_bytes_total Number of bytes sent by the process over the network.
# TYPE process_network_transmit_bytes_total counter
process_network_transmit_bytes_total 8.970838e+06
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 32
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 9.8254848e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.73859753992e+09
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.336942592e+09
# HELP process_virtual_memory_max_bytes Maximum amount of virtual memory available in bytes.
# TYPE process_virtual_memory_max_bytes gauge
process_virtual_memory_max_bytes 1.8446744073709552e+19

Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/metrics_test.go:625 @ 02/03/25 15:49:24.579
}
```
Does not seem to provide useful info for debugging. It would be great to see exactly which metric is missing.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-03T16:07:45Z

cc @mbobrovskyi @mykysha PTAL

### Comment by [@mykysha](https://github.com/mykysha) — 2025-02-03T16:11:11Z

/assign
