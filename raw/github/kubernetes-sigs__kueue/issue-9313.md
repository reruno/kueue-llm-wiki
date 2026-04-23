# Issue #9313: [flaky test] MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Summary**: [flaky test] MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9313

**Last updated**: 2026-02-17T17:11:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-17T10:23:15Z
- **Updated**: 2026-02-17T17:11:40Z
- **Closed**: 2026-02-17T17:11:40Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 9

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9309/pull-kueue-test-e2e-multikueue-release-0-15/2023697194514649088
**Failure message or logs**:
```
End To End MultiKueue Suite: kindest/node:v1.35.0: [It] MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state expand_less	1m39s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:258 with:
Expected
    <v1.Time>: {
        Time: 2026-02-17T10:03:26Z,
    }
not to equal
    <v1.Time>: {
        Time: 2026-02-17T10:03:26Z,
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:258 with:
Expected
    <v1.Time>: {
        Time: 2026-02-17T10:03:26Z,
    }
not to equal
    <v1.Time>: {
        Time: 2026-02-17T10:03:26Z,
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:1407 @ 02/17/26 10:11:06.447

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**Anything else we need to know?**:

I think this is likely a new problem related to https://github.com/kubernetes-sigs/kueue/pull/9275. 

Maybe we should just give it more time than 10s?

Or maybe the rollout started to progress in exactly the same second? In that case maybe instead of checking time we should check the `ObservedGeneration` for status

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T10:23:24Z

cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T10:24:59Z

Or maybe the rollout started to progress in exactly the same second? In that case maybe instead of checking time we should check the ObservedGeneration for status. 

I would check for bump in ObservedGeneration rather than time, and give it LongTimeout to ensure there is no issues with timing. 

Wdyt @mbobrovskyi ?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-17T11:23:30Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-17T11:28:30Z

> I would check for bump in ObservedGeneration rather than time

Deployment condition still doesn't have ObservedGeneration.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T11:37:40Z

I'm talking about the observedGeneration for the entire status, here is an example status I can see for my deployment of Kueue:

```yaml
  status:
    availableReplicas: 1
    conditions:
    - lastTransitionTime: "2026-02-10T18:11:25Z"
      lastUpdateTime: "2026-02-10T18:11:25Z"
      message: Deployment has minimum availability.
      reason: MinimumReplicasAvailable
      status: "True"
      type: Available
    - lastTransitionTime: "2026-02-10T18:11:11Z"
      lastUpdateTime: "2026-02-10T19:11:10Z"
      message: ReplicaSet "kueue-controller-manager-d9f9f7b" has successfully progressed.
      reason: NewReplicaSetAvailable
      status: "True"
      type: Progressing
    observedGeneration: 10
    readyReplicas: 1
    replicas: 1
    updatedReplicas: 1
```
So I think instead of checking the `lastUpdateTime` we could check if the generation for the status was bumped.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-17T11:45:31Z

> I'm talking about the observedGeneration for the entire status, here is an example status I can see for my deployment of Kueue:

Ah, I see what you mean – yes, that makes sense. However, I wouldn’t consider this safe. What if the Deployment updates other fields? I’d prefer to keep both checks.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T11:58:56Z

>  I’d prefer to keep both checks.

Maybe but what if the update happens within the same second? The timestamp fields have only 1s resolution lastUpdateTime. I'm not sure this was the reason for the failure -would need to check logs, but this seems like a possiibility.,

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T12:02:31Z

I think this is correct:
1. remember the previous lastUpdateTime
2. use waiting to cross the second boundary
3. trigger deployment update
4. verify the new lastUpdateTime

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T12:44:39Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9311/pull-kueue-test-e2e-multikueue-main/2023734161025536000
