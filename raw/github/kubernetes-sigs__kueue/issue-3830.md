# Issue #3830: [Flaky test]  Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then succeed if the second Provisioning request succeeds

**Summary**: [Flaky test]  Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then succeed if the second Provisioning request succeeds

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3830

**Last updated**: 2025-05-12T13:16:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-13T07:39:13Z
- **Updated**: 2025-05-12T13:16:49Z
- **Closed**: 2025-05-12T13:16:47Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 12

## Description

/kind flake

**What happened**:

Test failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3729/pull-kueue-test-integration-main/1867281092143222784

**What you expected to happen**:

no random failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat on CI

**Anything else we need to know?**:

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:1640 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:1640 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:1644 @ 12/12/24 18:56:27.215
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T07:39:51Z

cc @mbobrovskyi

@PBundyra (who recently worked on the ProvReq retries)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-13T07:53:03Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-13T09:14:28Z

I think it may be connected with other flakes we currently experience in Kueue, as this test flaked due to workload controller not working properly. This function didn't work as intended
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L208

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-12T09:51:34Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-12T10:32:22Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-12T10:32:27Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3830#issuecomment-2871988974):

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T12:52:06Z

I don't see any resolving PRs.
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-12T12:52:12Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3830#issuecomment-2872444545):

>I don't see any resolving PRs.
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T12:52:16Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-12T13:05:41Z

> I don't see any resolving PRs.

that's right but I would prefer to close issues like this which have no reoccurred for something like 90days. 

First, we lost logs to investigate. Second the issue might have been already fixed by a PR which was not directly attributed to it, for example the increasing of Timeout to 10s. 

We can always reopen when it reoccurs. WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T13:16:42Z

> > I don't see any resolving PRs.
> 
> that's right but I would prefer to close issues like this which have no reoccurred for something like 90days.
> 
> First, we lost logs to investigate. Second the issue might have been already fixed by a PR which was not directly attributed to it, for example the increasing of Timeout to 10s.
> 
> We can always reopen when it reoccurs. WDYT?

SGTM

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-12T13:16:47Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3830#issuecomment-2872541869):

>> > I don't see any resolving PRs.
>> 
>> that's right but I would prefer to close issues like this which have no reoccurred for something like 90days.
>> 
>> First, we lost logs to investigate. Second the issue might have been already fixed by a PR which was not directly attributed to it, for example the increasing of Timeout to 10s.
>> 
>> We can always reopen when it reoccurs. WDYT?
>
>SGTM
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
