# Issue #2738: [Flaky test] e2e tests occasionally fail when deleting kind cluster

**Summary**: [Flaky test] e2e tests occasionally fail when deleting kind cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2738

**Last updated**: 2025-04-17T17:01:44Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-01T09:23:11Z
- **Updated**: 2025-04-17T17:01:44Z
- **Closed**: 2025-04-17T17:01:43Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/rotten`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 19

## Description


**What happened**:

The period e2e test failed on deleting kind cluster: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-multikueue-e2e-main/1818706058688860160.

This may happen when the entire test suite is green.

It looks like a rare flake (https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-multikueue-e2e-main): 
![image](https://github.com/user-attachments/assets/ac6390d4-4b2e-4b79-803e-1bf6e2c4cfe9)


**What you expected to happen**:

No random failures.

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build, it happened on periodic build.

**Anything else we need to know?**:

The logs from the failure:
```
Ginkgo ran 1 suite in 3m16.816345076s
Test Suite Passed
Switched to context "kind-kind-manager".
Exporting logs for cluster "kind-manager" to:
/logs/artifacts/run-test-multikueue-e2e-1.30.0
No resources found in default namespace.
Deleting cluster "kind-manager" ...
ERROR: failed to delete cluster "kind-manager": failed to delete nodes: command "docker rm -f -v kind-manager-control-plane" failed with error: exit status 1

Command Output: Error response from daemon: cannot remove container "/kind-manager-control-plane": could not kill: tried to kill container, but did not receive an exit event
make: *** [Makefile-test.mk:100: run-test-multikueue-e2e-1.30.0] Error 1
+ EXIT_VALUE=2
+ set +o xtrace
Cleaning up after docker in docker.
================================================================================
Waiting 30 seconds for pods stopped with terminationGracePeriod:30
Cleaning up after docker
ed68da3fb667
6beb571d417e
bf442dfcffc1
Waiting for docker to stop for 30 seconds
Stopping Docker: dockerProgram process in pidfile '/var/run/docker-ssd.pid', 1 process(es), refused to die.
```
It looks like we give 30s to teardown a kind cluster. I'm wondering if increasing the timeout to 45s could help.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-01T09:23:30Z

/cc @mbobrovskyi @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-01T09:23:38Z

/kind flake

### Comment by [@trasc](https://github.com/trasc) — 2024-08-01T09:29:40Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-08-01T12:40:21Z

> It looks like we give 30s to teardown a kind cluster. I'm wondering if increasing the timeout to 45s could help.

That timeout is part of the test image and the failure at that point is already ignored.

The issue is indeed related to `kind delete` however since is very little we ca do about it and it has nothing to do with the e2e suites we should just ignore it as we do wit other cleanup steps.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2024-08-02T17:20:04Z

This shouldn't be happening and as far as I know isn't in Kubernetes's e2e tests.

In the future when you see issues like this please go ahead and reach out to the kind project.

cc @aojea 

I'm fairly occupied today but can probably dig into this by sometime Monday.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-02T17:23:57Z

> This shouldn't be happening and as far as I know isn't in Kubernetes's e2e tests.

Right, I've never seen this in the code k8s, but this is the first time I see it in Kueue too, so maybe this is some very rare one-off.

### Comment by [@aojea](https://github.com/aojea) — 2024-08-02T17:43:16Z

> refused to die.

😮‍💨 

https://storage.googleapis.com/kubernetes-jenkins/logs/periodic-kueue-test-multikueue-e2e-main/1818706058688860160/build-log.txt

> ERROR: failed to delete cluster "kind-manager": failed to delete nodes: command "docker rm -f -v kind-manager-control-plane" failed with error: exit status 1
> Command Output: Error response from daemon: cannot remove container "/kind-manager-control-plane": could not kill: tried to kill container, but did not receive an exit event


what are these e2e doing with the network @mimowo ?

```
[38;5;243m/home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:463[0m
  [1mSTEP:[0m wait for check active [38;5;243m@ 07/31/24 18:01:33.731[0m
  [1mSTEP:[0m Disconnecting worker1 container from the kind network [38;5;243m@ 07/31/24 18:01:34.06[0m
  [1mSTEP:[0m Waiting for the cluster to become inactive [38;5;243m@ 07/31/24 18:01:34.54[0m
  [1mSTEP:[0m Reconnecting worker1 container to the kind network [38;5;243m@ 07/31/24 18:02:19.212[0m
  [1mSTEP:[0m Waiting for the cluster do become active [38;5;243m@ 07/31/24 18:02:49.147[0m
[38;5;10m• [77.390 seconds][0m
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-05T07:19:59Z

> > refused to die.
> 
> 😮‍💨

This is something that we observe on every built - also successful, but I see it also on JobSet e2e tests and core k8s e2e tests, example [link](https://storage.googleapis.com/kubernetes-jenkins/pr-logs/pull/126534/pull-kubernetes-e2e-kind/1820084932546924544/build-log.txt).

> what are these e2e doing with the network @mimowo ?

These are tests for MultiKueue. We run 3 Kind clusters (one manager and 2 workers). We disconnect the network between the manager and a worker using that command: `docker network disconnect kind kind-worker1-control-plane`. Later we re-connect the clusters.

It is done to simulate transient connectivity issues between the clusters.

### Comment by [@aojea](https://github.com/aojea) — 2024-08-05T12:11:51Z

seems the other bug reported https://github.com/kubernetes/kubernetes/issues/123313 with the same symptom was fixed by https://github.com/kubernetes/test-infra/pull/32245

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2024-08-05T20:13:35Z

> This is something that we observe on every built - also successful, but I see it also on JobSet e2e tests and core k8s e2e tests, example [link](https://storage.googleapis.com/kubernetes-jenkins/pr-logs/pull/126534/pull-kubernetes-e2e-kind/1820084932546924544/build-log.txt).

Yeah, that's different, the process cleanup of the docker daemon is less concerning when we're succesfully deleting the node containers (which we did in that link, prior to the issue turning down the docker daemon), I don't think that's related but should also be tracked (https://github.com/kubernetes/test-infra/issues/33227).

In that link we can see `kind delete cluster` successfully deleting the nodes without timeout issues.

> so maybe this is some very rare one-off.

I think they may also run on different clusters (k8s-infra-prow-build vs the k8s infra EKS cluster) with different OS, machine type, etc. There may be some different quirk with the environment between them.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-03T20:31:56Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-03T21:25:17Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T09:58:38Z

/close
I haven't seen a single failure like that in the last couple of months. Let's close for now and re-consider options when this happens again.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-12T09:58:42Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2738#issuecomment-2538418306):

>/close
>I haven't seen a single failure like that in the last couple of months. Let's close for now and re-consider options when this happens again.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-18T16:48:34Z

This issue happens again https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4606/pull-kueue-test-e2e-customconfigs-main/1902033866957262848.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-18T16:49:09Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-18T16:49:13Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2738#issuecomment-2733998011):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-17T17:01:38Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-17T17:01:43Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2738#issuecomment-2813564575):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
