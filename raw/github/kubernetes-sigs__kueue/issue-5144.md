# Issue #5144: [release-0.11] Flaky Test: End To End Custom Configs handling Suite for ManageJobsWithoutQueueName

**Summary**: [release-0.11] Flaky Test: End To End Custom Configs handling Suite for ManageJobsWithoutQueueName

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5144

**Last updated**: 2025-08-26T15:31:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-04-30T07:49:59Z
- **Updated**: 2025-08-26T15:31:48Z
- **Closed**: 2025-08-08T06:18:19Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

In the release-0.11 periodic CI jobs, we have seen the following unexpected errors:

- `ManageJobsWithoutQueueName without JobSet integration when manageJobsWithoutQueueName=true should create only one workload for parent job`

```shell
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:858 with:
Expected
    <string>: 
to equal
    <string>: Completed failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:858 with:
Expected
    <string>: 
to equal
    <string>: Completed
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:859 @ 04/30/25 00:59:13.519
}
```

- `End To End Custom Configs handling Suite: kindest/node:v1.32.3: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not suspend child jobs of admitted jobs`

```shell
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:183 with:
Expected
    <v1beta2.AppWrapperPhase>: Running
to equal
    <v1beta2.AppWrapperPhase>: Succeeded failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:183 with:
Expected
    <v1beta2.AppWrapperPhase>: Running
to equal
    <v1beta2.AppWrapperPhase>: Succeeded
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:184 @ 04/30/25 01:00:26.832
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-11/1917380563962957824

<img width="1456" alt="Image" src="https://github.com/user-attachments/assets/5d7ad4fe-0408-4977-98bb-3f28c5e8adcd" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-30T07:50:30Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-30T07:56:30Z

cc @kaisoz has knowledge for these cases since @kaisoz implemented these tests, IIUC

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-04-30T13:01:43Z

/assign
thanks @tenzen-y I'll have a look 😊

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-29T13:10:10Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T13:12:17Z

/remove-lifecycle stale

@kaisoz Any updates?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T06:18:15Z

/close 
We no longer maintain 0.11. I think this issue might have got resoled by now by https://github.com/kubernetes/test-infra/pull/35257

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-08T06:18:20Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5144#issuecomment-3166702752):

>/close 
>We no longer maintain 0.11. I think this issue might have got resoled by now by https://github.com/kubernetes/test-infra/pull/35257


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-08-26T12:59:03Z

Thx @mimowo for taking care of this! 

@tenzen-y sorry I didn't answer your question earlier, I missed this. I started working on it but I couldn't reproduce it, then something came in between and had to put it on hold

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T15:31:48Z

> Thx [@mimowo](https://github.com/mimowo) for taking care of this!
> 
> [@tenzen-y](https://github.com/tenzen-y) sorry I didn't answer your question earlier, I missed this. I started working on it but I couldn't reproduce it, then something came in between and had to put it on hold

No worries, thank you for investigating that!
