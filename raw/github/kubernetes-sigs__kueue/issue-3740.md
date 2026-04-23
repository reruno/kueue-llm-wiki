# Issue #3740: set nodeSelector for kueue-controller-manager via helm chart

**Summary**: set nodeSelector for kueue-controller-manager via helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3740

**Last updated**: 2025-09-10T08:05:49Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tan-wei-xin-alez](https://github.com/tan-wei-xin-alez)
- **Created**: 2024-12-04T17:12:48Z
- **Updated**: 2025-09-10T08:05:49Z
- **Closed**: 2025-05-03T18:20:54Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
There does not seem to be a way to set the `nodeSelector` for the `controllerManager` in [charts/kueue/values.yaml](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml)

I've also looked in [charts/kueue/templates/manager/manager.yaml](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/manager/manager.yaml) and it's not there either

Right now, I'm doing something like the following in terraform, but it seems like an anti-pattern to patch deployments or anything else after Helm has created them since it also monitors the lifecycle and state of the resources it creates (we don't want to end up with a drift in configuration which can sometimes lead to nasty situations like inability to upgrade the chart later)
```
// limit pods belonging to the following deployments to system nodes
//  - kueue-controller-manager
resource "terraform_data" "patch_kueue_deployments" {
  count = var.enable_kueue ? 1 : 0

  triggers_replace = [
    helm_release.kueue[0].version,
    helm_release.kueue[0].metadata[0].revision,
  ]

  provisioner "local-exec" {
    command = <<-EOT
      kubectl patch deployment kueue-controller-manager --namespace ${helm_release.kueue[0].namespace} --patch '{"spec": {"template": {"spec": {"nodeSelector": {"Type": "system"}}}}}'
    EOT
  }

  depends_on = [
    helm_release.kueue
  ]
}
```

**Why is this needed**:
We scale up some very expensive nodes on our k8s cluster for a certain amount of time and sometimes, the pod belonging to the `kueue-controller-manager` deployment ends up in one of them and no one notices before we get billed a few hundred to a few thousand dollars more because the autoscaler could not scale it down.

So we would like to limit the deployment to specific nodes that do no cost as much.

**Completion requirements**:
If there is an alternative way to set `nodeSelector` for the `controllerManager` in terraform that does not create a drift in configuration over time (so preferably using Helm), then I am all ears.

Otherwise, I'd be willing to open a PR to implement the necessary change myself.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-04T17:41:16Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-03T17:44:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-03T18:20:50Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-03T18:20:54Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3740#issuecomment-2848745711):

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

### Comment by [@tan-wei-xin-alez](https://github.com/tan-wei-xin-alez) — 2025-09-10T08:05:49Z

should be possible now that [helm: support for specifying nodeSelector and tolerations for all Kueue components
](https://github.com/kubernetes-sigs/kueue/pull/5820) has been merged
