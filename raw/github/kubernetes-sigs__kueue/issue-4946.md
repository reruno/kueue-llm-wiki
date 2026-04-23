# Issue #4946: Security scanner flagging "Command Injection" for kueuectl

**Summary**: Security scanner flagging "Command Injection" for kueuectl

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4946

**Last updated**: 2025-11-23T00:12:23Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-13T16:23:17Z
- **Updated**: 2025-11-23T00:12:23Z
- **Closed**: 2025-11-23T00:12:22Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 14

## Description

If you run `snyk code test` on the kueue code base, the only high vulnerability that occurs from Kueue code:

```
✗ [High] Command Injection 
   Path: cmd/kueuectl/app/passthrough/passthrough.go, line 107 
   Info: Unsanitized input from a CLI argument flows into syscall.Exec, where it is used as a shell command. This may result in a Command Injection vulnerability.
```

Passthrough was added [here](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#pass-through)

Code in question:

https://github.com/kubernetes-sigs/kueue/blob/main/cmd/kueuectl/app/passthrough/passthrough.go#L88

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T06:05:21Z

I think that this is intended behavior. What are your expected fixes?
cc @mbobrovskyi @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T06:10:01Z

Maybe there is a way to sanitize the arguments before passing  further.Maybe k8s exposes some utility function for that, but im not sure. ptal @mbobrovskyi 

EDIT: but if there is nothing exposed, then I would assume we can just rely on the validation inside kubectl.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-14T14:37:34Z

I don't know if it would resolve the warning but I think we have some requirements on the passthrough.

Maybe rather than just pass the entire arguments we can parse it and fail if there is more than 3 elements. I think the shape is 3 elements for all this (kubectl {get/describe/delete/..} {resource} {resourceName}).

Anything else we don't allow?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-14T14:38:32Z


> get workload|wl|clusterqueue|cq|localqueue|lq|resourceflavor|rf
> describe workload|wl|clusterqueue|cq|localqueue|lq|resourceflavor|rf
> edit workload|wl|clusterqueue|cq|localqueue|lq|resourceflavor|rf
> patch workload|wl|clusterqueue|cq|localqueue|lq|resourceflavor|rf
> delete clusterqueue|cq|localqueue|lq|resourceflavor|rf
> 

Maybe patch would be tricky actually?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-21T12:50:38Z

> Maybe there is a way to sanitize the arguments before passing further.Maybe k8s exposes some utility function for that, but im not sure. ptal [@mbobrovskyi](https://github.com/mbobrovskyi)
> 
> EDIT: but if there is nothing exposed, then I would assume we can just rely on the validation inside kubectl.

Good point.
@soltysh any ideas on validation we can do as a pass through to kubectl?

### Comment by [@soltysh](https://github.com/soltysh) — 2025-04-29T12:03:20Z

> [@soltysh](https://github.com/soltysh) any ideas on validation we can do as a pass through to kubectl?

We don't have any logic around that anywhere in kubectl code. What I can suggest is you can use `os/exec#Cmd`, which will work on all platforms. Your current solution limits you to only be usable on linux. When we run plugins [we use exec.Cmd for win, and the rest syscall.Exec](https://github.com/kubernetes/kubernetes/blob/5be79417862d29aecfadb2735cc42da64dff3ba7/staging/src/k8s.io/kubectl/pkg/cmd/cmd.go#L240-L258). The reasoning behind is that the latter will replace the running binary with a new one, but it only works on linux. The former is a workaround for windows. Other than that, [your proposal](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#pass-through) explicitly mentions a set of commands you allow, I'd add a strict validation to only allow those. 

Out of curiosity I found [this article](https://semgrep.dev/docs/cheat-sheets/go-command-injection) specifically discussing the use of `cmd.Exec` but I don't see any sanitation inside there which I could suggest you do, other than just limit the potential commands you allow passing through.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-28T13:02:53Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-27T13:12:29Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-26T13:29:56Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-26T13:30:01Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4946#issuecomment-3338741866):

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-23T23:31:30Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-23T23:31:35Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4946#issuecomment-3439770262):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-23T00:12:18Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-23T00:12:22Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4946#issuecomment-3567180749):

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
