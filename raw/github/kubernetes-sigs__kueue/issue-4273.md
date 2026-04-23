# Issue #4273: [Flaky test] Scheduler when Scheduling workloads on clusterQueues when Hold LocalQueue at startup Should admit workloads according to their priorities

**Summary**: [Flaky test] Scheduler when Scheduling workloads on clusterQueues when Hold LocalQueue at startup Should admit workloads according to their priorities

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4273

**Last updated**: 2026-01-19T07:37:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-17T07:04:42Z
- **Updated**: 2026-01-19T07:37:06Z
- **Closed**: 2026-01-19T07:37:05Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 13

## Description

/kind flake
**What happened**:

Failed test: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1891370482536550400

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

Run CI 

**Anything else we need to know?**:

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:324 with:
Not enough workloads are pending
Expected
    <int>: 2
to equal
    <int>: 3 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:324 with:
Not enough workloads are pending
Expected
    <int>: 2
to equal
    <int>: 3
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/scheduler_test.go:565 @ 02/17/25 06:28:13.731
}
```
**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-17T07:04:54Z

/kind flake

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-02-17T22:57:13Z

```bash
export GINKGO_ARGS='--focus "Scheduler when Scheduling workloads on clusterQueues when Hold LocalQueue at startup Should admit workloads according to their priorities"'
export INTEGRATION_TARGET='test/integration/singlecluster/scheduler'
count=0

while make test-integration ;
do
  count=$[$count + 1]
  echo $count
done
```

ran this trying to reproduce flake ~100 times and have not been able to  reproduce locally

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-18T07:31:32Z

> ran this trying to reproduce flake ~100 times and have not been able to reproduce locally

Thanks for looking at the issue. The other tactics I use for reproducing the issues locally:
- add some stress (./bin/stress --cpu=N)
- add `--race` to `GINKGO_ARGS`
- recompile with instrumentation, here are the steps for k8s tests, but it should be possible to adapt for Kueue:

```sh
# install stress command
go install golang.org/x/tools/cmd/stress@latest

# recompile with race instrumentation
go test ./pkg/controller/job -race -c

# run (it loops and reports failures)
stress ./job.test -test.run TestJobApiBackoffReset
```

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-10T00:29:31Z

There is an error in logs just before the start of the 10s timeout:
```
  2025-02-17T06:28:03.756560364Z	ERROR	scheduler	scheduler/scheduler.go:594	Could not update Workload status	{"schedulingCycle": 43, "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"wl-mid-priority-1\": the object has been modified; please apply your changes to the latest version and try again"}
  sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).requeueAndUpdate
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/scheduler/scheduler.go:594
  sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/scheduler/scheduler.go:292
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:43
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:42
  sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:34
```

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-11T10:44:50Z

I've tried to reproduce locally with --race arg for Ginkgo and also running `/usr/bin/stress --cpu 90`, no failed tests after 100 attempts

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-09T10:50:14Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-09T11:31:46Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-09T11:56:02Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-07T12:49:24Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T13:03:40Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T13:24:12Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T07:37:00Z

/close
1. we no longer have logs to investigate
2. it has not repeated itself for long
3. it is likely fixed by https://github.com/kubernetes-sigs/kueue/pull/7281

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-19T07:37:06Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4273#issuecomment-3766888991):

>/close
>1. we no longer have logs to investigate
>2. it has not repeated itself for long
>3. it is likely fixed by https://github.com/kubernetes-sigs/kueue/pull/7281


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
