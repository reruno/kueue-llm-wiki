# Issue #3233: [Flaky integration test] SchedulerWithWaitForPodsReadyNonblockingMode Long PodsReady timeout Should not block admission

**Summary**: [Flaky integration test] SchedulerWithWaitForPodsReadyNonblockingMode Long PodsReady timeout Should not block admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3233

**Last updated**: 2024-10-16T16:16:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-15T06:56:46Z
- **Updated**: 2024-10-16T16:16:22Z
- **Closed**: 2024-10-16T16:16:19Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 8

## Description

/kind flake

**What happened**:

Test failed: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1844256892138819584
testgring link: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main

![image](https://github.com/user-attachments/assets/d6fce02c-d9b5-47ef-a3ab-14819378fe18)


**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build.

**Anything else we need to know?**:

```
{Timed out after 5.001s.
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 5.001s.
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready/scheduler_test.go:635 @ 10/10/24 06:15:45.64
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-15T06:57:30Z

/assign @IrvingMg 
who is also looking at the similarly looking issue: https://github.com/kubernetes-sigs/kueue/issues/3212

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-15T06:59:49Z

/cc @mbobrovskyi 
who may have useful knowledge about the tests

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-16T14:41:08Z

> /assign @IrvingMg who is also looking at the similarly looking issue: #3212

I think it's a duplicate of https://github.com/kubernetes-sigs/kueue/issues/3212.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-16T15:38:31Z

I suspect the same, but I wasn't sure as these are 2 different tests. We can keep both open for now, and close as we fully understand the issue and confirm it is the same root cause.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-16T15:56:58Z

> In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready/scheduler_test.go:635 @ 10/10/24 06:15:45.64


Looks like the error in the same line. So I think it's duplicate.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-16T15:59:33Z

And the test name also the same.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-16T16:16:15Z

Ah, yes my mistake. I thought the names are different
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-16T16:16:20Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3233#issuecomment-2417300459):

>Ah, yes my mistake. I thought the names are different
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
