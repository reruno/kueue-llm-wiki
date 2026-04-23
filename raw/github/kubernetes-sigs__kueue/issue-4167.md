# Issue #4167: Built-in Tekton PipelineRun Support

**Summary**: Built-in Tekton PipelineRun Support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4167

**Last updated**: 2025-10-24T20:38:36Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@adambkaplan](https://github.com/adambkaplan)
- **Created**: 2025-02-06T20:10:00Z
- **Updated**: 2025-10-24T20:38:36Z
- **Closed**: 2025-10-24T20:38:35Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support [Tekton Pipelines](https://tekton.dev) as a built-in Kueue integration. Tekton `PipelineRun` objects can be potentially supported because it has a "suspended" equivalent through the [Pending PipelineRun](https://tekton.dev/docs/pipelines/pipelineruns/#pending-pipelineruns) feature.

**Why is this needed**:

At scale, Tekton `PipelineRun` objects can overwhelm a Kubernetes cluster due to the chain of objects it creates (child `TaskRun` objects + Pods). Even with pruning mechanisms in place, a cluster that uses webhooks or other mechanisms to launch Tekton `PipelineRuns` can lead to cluster failure.

This is split out from #74, which also includes Argo Workflows. The latter is a different project with an entirely different set of APIs.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-07T02:45:59Z

This sounds great! I wrote up a external integration [here](https://github.com/kubernetes-sigs/kueue/pull/3898) using pod integration.

It would probably be best to have someone from the tekton community to lead this implementation with a KEP. I'm not sure how many folks in the Kueue community are familar with Tekton.

### Comment by [@vdemeester](https://github.com/vdemeester) — 2025-02-11T15:56:34Z

@kannon92 you are right, I think someone from the Tekton Community should definitely help / drive this. This will require a KEP right ?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-11T16:01:48Z

I'm not sure actually. @mimowo @tenzen-y WDYT? Can we add an integration for Tekton without a KEP?

I'd prefer to see some kind of KEP to at least document the plan but I'll leave that decision to @tenzen-y and @mimowo.

It would also be worth seeing how this work would play with https://github.com/kubernetes-sigs/kueue/issues/74 as the hope was to have a general solution for workflows in Kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T16:06:54Z

> Can we add an integration for Tekton without a KEP?

Historically we added some integrations without KEP, but this is always tricky. 

Plus, we don't have much expertise in Tekton so the KEP will be very much appreciated in this case to also describe the higher-level ideas.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T06:11:58Z

I also think that KEP would be better since in case of workflow supporting, it is obviously required to prepare additional mechanism similar to ArgoWorkflow supporting KEP

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-02-13T06:46:04Z

Does the integration with Tekton should be added to kueue''s code base? I think that an external integration would be better.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-13T07:04:02Z

Staring externally is even better as Appswrapper started, or incubate it in kueue under cmd/experimental

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-02-25T18:42:06Z

I created a simple external integration of Kueue and Tekton for supporting PipelineRuns. It's very basic but I think it provide a POC. You can find the code in https://github.com/konflux-ci/tekton-kueue and a short demo in https://www.youtube.com/watch?v=ppXd38CEhoE

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-26T19:01:56Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-27T12:16:51Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-25T12:31:01Z

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

### Comment by [@adambkaplan](https://github.com/adambkaplan) — 2025-08-25T13:27:07Z

@gbenhaim I know on Konflux we have made progress on integrating Kueue with Tekton. Is this a separate "out of tree" implementation, or did we build it into kueue directly?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-25T13:32:31Z

https://github.com/konflux-ci/tekton-kueue

It is done as an external framework for tekton-kueue.

### Comment by [@adambkaplan](https://github.com/adambkaplan) — 2025-08-25T14:17:04Z

I guess it is up to the Kueue maintainers when it comes to which APIs are "included" vs. which ones should be supported by external implementations.

There is a strong argument for current non-core k8s APIs to be moved out of kueue and have external implementations instead (slims down the dependency tree, forces the project to have strong guarantees for the external implementers/frameworks).

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-08-25T18:40:59Z

I think tekton-kueue should stay an external framework thus this issue can be closed. Maybe add a section to the Kueue documentation which links to implementation of external frameworks so users can find them.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-25T18:44:00Z

> I guess it is up to the Kueue maintainers when it comes to which APIs are "included" vs. which ones should be supported by external implementations.

Correct.

> There is a strong argument for current non-core k8s APIs to be moved out of kueue and have external implementations instead (slims down the dependency tree, forces the project to have strong guarantees for the external implementers/frameworks).

This seems to be a bit strong. I don't think we are going to drop in-tree integrations anytime soon.

@tenzen-y @gabesaba @mimowo What kind of policy do we have for in-tree versus external frameworks?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-25T18:45:06Z

> I think tekton-kueue should stay an external framework thus this issue can be closed. Maybe add a section to the Kueue documentation which links to implementation of external frameworks so users can find them.

Is there a way to make this integration general for tekton?

Right now, the integration lives in konflux-ci but its not exactly clear that this solution could be used for generic tekton cd without taking on the konflux dependency?

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-08-25T19:26:05Z

> > I think tekton-kueue should stay an external framework thus this issue can be closed. Maybe add a section to the Kueue documentation which links to implementation of external frameworks so users can find them.
> 
> Is there a way to make this integration general for tekton?
> 
> Right now, the integration lives in konflux-ci but its not exactly clear that this solution could be used for generic tekton cd without taking on the konflux dependency?

The implementation is general to Tekton already. There is no dependency on Konflux. We plan to move it to the openshift-pipelines org or to tektoncd if the community will decide to accept it.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-24T20:15:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-24T20:38:30Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-24T20:38:36Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4167#issuecomment-3444840223):

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
