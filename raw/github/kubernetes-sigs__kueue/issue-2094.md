# Issue #2094: kueue controller lacks permission for configmaps.

**Summary**: kueue controller lacks permission for configmaps.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2094

**Last updated**: 2025-05-24T01:09:00Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2024-04-29T10:08:06Z
- **Updated**: 2025-05-24T01:09:00Z
- **Closed**: 2025-05-24T01:08:58Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

kueue controller lacks permission for configmaps.

![image](https://github.com/kubernetes-sigs/kueue/assets/30817980/626ab068-f0e5-466a-9b1c-cd4dfd28b63b)

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

I built the image based on commit 9890f41dfbdae.

Install kueue by:

kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/manifests.yaml

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.28.3
- Kueue version (use `git describe --tags --dirty --always`): v0.6.2
- Cloud provider or hardware configuration: 
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T10:19:17Z

@KunWuLuan This is curious. Could you investigate which operations we depend on the ConfigMap?
After that could you submit a PR?

Note that we manage the permissions by the kubebuilder markers like this:

https://github.com/kubernetes-sigs/kueue/blob/37c0943ab03c141d2d559decd44f29a98e76ce6d/pkg/controller/core/clusterqueue_controller.go#L144-L148

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:42:50Z

/assign @mszadkow
could you investigate this?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:42:52Z

@alculquicondor: GitHub didn't allow me to assign the following users: mszadkow.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2094#issuecomment-2189933742):

>/assign @mszadkow
>could you investigate this?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-23T21:14:23Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-24T13:17:47Z

/assign @mszadkow

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-24T13:17:55Z

/remove-lifecycle stale

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-01T08:29:30Z

@KunWuLuan could you provide more information on how to reproduce it?
Maybe what was the setup and installed packages?

### Comment by [@ukclivecox](https://github.com/ukclivecox) — 2024-12-11T10:45:46Z

I had this issue when the namespace for the rolebinding for `kueue-visibility-server-auth-reader` was overwritten by kustomize to be `kueue-system` rather than `kube-system` as this is the one resource in the manifest which is not meant to be in the `kueue-system` namespace.

### Comment by [@botanical6748](https://github.com/botanical6748) — 2024-12-19T23:31:12Z

> I had this issue when the namespace for the rolebinding for `kueue-visibility-server-auth-reader` was overwritten by kustomize to be `kueue-system` rather than `kube-system` as this is the one resource in the manifest which is not meant to be in the `kueue-system` namespace.

I'm curious how you resolved this? I'm running into the same issue and am wondering if there is an update the default config that will prevent Kustomize from overwriting the namespace.

### Comment by [@ukclivecox](https://github.com/ukclivecox) — 2024-12-24T08:21:38Z

I needed to add a patch to my kustomize

```
patchesJson6902:
  - target:
      group: ""
      version: v1
      kind: RoleBinding
      name: 'kueue-visibility-server-auth-reader'
    patch: |-
      - op: replace
        path: /metadata/namespace                                                                                      
        value: kube-system                                                                                             
      - op: replace                                                                                                    
        path: /subjects/0/namespace                                                                                    
        value: kueue-system                          
```

### Comment by [@botanical6748](https://github.com/botanical6748) — 2024-12-24T22:53:38Z

> I needed to add a patch to my kustomize
> 
> 
> 
> ```
> 
> patchesJson6902:
> 
>   - target:
> 
>       group: ""
> 
>       version: v1
> 
>       kind: RoleBinding
> 
>       name: 'kueue-visibility-server-auth-reader'
> 
>     patch: |-
> 
>       - op: replace
> 
>         path: /metadata/namespace                                                                                      
> 
>         value: kube-system                                                                                             
> 
>       - op: replace                                                                                                    
> 
>         path: /subjects/0/namespace                                                                                    
> 
>         value: kueue-system                          
> 
> ```

Awesome thanks so much for the reply!

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-24T23:39:10Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-24T00:19:26Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-24T01:08:54Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-24T01:08:59Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2094#issuecomment-2906243243):

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
