# Issue #1776: A mechanism to list the Workloads that are admitted and not finished

**Summary**: A mechanism to list the Workloads that are admitted and not finished

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1776

**Last updated**: 2024-08-15T07:18:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-27T18:48:38Z
- **Updated**: 2024-08-15T07:18:42Z
- **Closed**: 2024-08-15T07:18:41Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Some way of querying the list of Workloads that are still "running", that is, they are admitted and don't have a Finished condition. Querying by ClusterQueue would be ideal too.

Some options (not necessarily exclusive to each other):
- The kueue CLI
- A visibility endpoint.
- Is there a way to do this just with a kubectl jsonpath?

**Why is this needed**:

For basic diagnostics of the state of the cluster.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change?
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-27T18:52:34Z

Do you expect that we extend the on-demand visibility server or save information on any CustomResource like ClusterQueue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-27T18:53:55Z

I don't think we should save it. This is more for on-demand queries.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-27T18:55:06Z

> I don't think we should save it. This is more for on-demand queries.

It makes sense.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-02-28T08:27:34Z

Tangentially, do you think adding a `running_worloads` metric could be useful too?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-28T08:30:16Z

> Tangentially, do you think adding a `running_worloads` metric could be useful too?

Does it mean Prometheus metric?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-02-28T08:32:09Z

> > Tangentially, do you think adding a `running_worloads` metric could be useful too?
> 
> Does it mean Prometheus metric?

Yes, a Prometheus metric, that would complement the existing `pending_workloads` metric.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-28T14:47:32Z

we already have it https://github.com/kubernetes-sigs/kueue/blob/9afd7e6aadd49e2c44fcafb67b11cf78c5d751ae/pkg/metrics/metrics.go#L120-L126

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-02-28T16:37:04Z

> we already have it
> 
> https://github.com/kubernetes-sigs/kueue/blob/9afd7e6aadd49e2c44fcafb67b11cf78c5d751ae/pkg/metrics/metrics.go#L120-L126

Ah right, this is the one, thanks!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-28T17:18:36Z

Would you like to propose something for this area? Maybe along the lines of a new visibility endpoint?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-02-28T17:59:05Z

Yes. Do you want it to be initially proposed as a KEP?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-28T18:03:31Z

Given that it's an API change, a KEP would be good.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-28T19:25:10Z

Feel free to assign yourself with `/assign`.
Since you joined this org, the command should work well :)

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-04-25T07:28:07Z

If no one working for this, I can help.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-04-25T07:29:44Z

@KunWuLuan I haven't got the chance to work on it. Feel free to assign it to you.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-05-06T03:38:25Z

Do we still need the new endpoints if we already have the KueueCtl?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-06T12:35:52Z

Maybe less so? One slight advantage would be to filter on the server side.

But maybe it would add unnecessary load to the kueue binary?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-04T13:12:55Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-14T16:19:48Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-14T17:23:16Z

This is supported using kueuectl https://kueue.sigs.k8s.io/docs/reference/kubectl-kueue/commands/kueuectl_list/kueuectl_list_workload/

Should we close this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-15T07:18:37Z

> This is supported using kueuectl https://kueue.sigs.k8s.io/docs/reference/kubectl-kueue/commands/kueuectl_list/kueuectl_list_workload/
> 
> Should we close this?

Oh, you're right. Let me close this.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-15T07:18:41Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1776#issuecomment-2290801911):

>> This is supported using kueuectl https://kueue.sigs.k8s.io/docs/reference/kubectl-kueue/commands/kueuectl_list/kueuectl_list_workload/
>> 
>> Should we close this?
>
>Oh, you're right. Let me close this.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
