# Issue #7577: Compile using Kubeflow Trainer v2.1.0

**Summary**: Compile using Kubeflow Trainer v2.1.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7577

**Last updated**: 2025-11-12T10:00:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-07T08:50:27Z
- **Updated**: 2025-11-12T10:00:58Z
- **Closed**: 2025-11-07T17:16:53Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The Kubeflow Trainer v2.1.0 tag is already published https://github.com/kubeflow/trainer/tree/v2.1.0 

so we should bump our go.mod: https://github.com/kubernetes-sigs/kueue/blob/main/go.mod#L12

**Why is this needed**:

To avoid using RC of Kubeflow in the next release of Kueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T08:50:54Z

cc @IrvingMg @mszadkow @mbobrovskyi

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-07T08:58:46Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-07T14:12:34Z

Do we need to update 0.14 with Trainer 2.1?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T15:31:47Z

Good question. On one hand it could break users who are already using Kueue with Kubeflow 2.0.0, otoh the integration is alpha for now so I think we have freedom to upgrade.

Pragmatically, I think it is unlikely that any users would have already started using for production Kueue 0.14 with Kubeflow 2.0.0, probably mostly experimentation at this point. However, some users may use Kueue 0.14 for prod with Kubeflow 2.1.0 in the coming months.

cc @tenzen-y @andreyvelich any opinion here?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-07T17:19:46Z

cc @astefanutti

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-07T17:22:00Z

> Good question. On one hand it could break users who are already using Kueue with Kubeflow 2.0.0, otoh the integration is alpha for now so I think we have freedom to upgrade.

AFAIK we have never made any distinction about the integration itself being alpha. its not under a feature gate and I believe kueue would support this right?

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-11-08T01:24:14Z

> On one hand it could break users who are already using Kueue with Kubeflow 2.0.0,

@mimowo Could you clarify how that will break existing users, if any ? IIUC, PodSpecOverride and PodTemplateOverride APIs are managed by Kueue controller, so users don't touch it.


I am not sure about adoption of TrainJob in v0.14, since we didn't even publish docs for the previous release.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-08T16:25:22Z

For Openshift AI we are very interested in TrainJob in v0.14. 

I would like to understand what features are limited by Kubeflow 2.0 and what we would gain by including Trainer v2.1.0.

If there is feature work that enables things for Trainer v2.1.0 then I am okay to not cherry-pick 2.1.0 into 0.14.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T16:14:53Z

> > Good question. On one hand it could break users who are already using Kueue with Kubeflow 2.0.0, otoh the integration is alpha for now so I think we have freedom to upgrade.
> 
> AFAIK we have never made any distinction about the integration itself being alpha. its not under a feature gate and I believe kueue would support this right?

The alpha level support is just discretion during development, as we discussed in the issue for Trainer integrations.
So, we do not have any public rule. But, yes. We say the Trainer integration is alpha since the agreement when we introduced Trainer integration.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T16:17:47Z

> For Openshift AI we are very interested in TrainJob in v0.14.
> 
> I would like to understand what features are limited by Kubeflow 2.0 and what we would gain by including Trainer v2.1.0.
> 
> If there is feature work that enables things for Trainer v2.1.0 then I am okay to not cherry-pick 2.1.0 into 0.14.

We evolved the Kueue TrainJob controller to support TAS, which depends on the Trainer v2.1 as a minimum version.
So, even if cherry-pick the Trainer dependency update PR, the released version (v0.14 / v0.13) could not support TAS with TrainJob. And we do not want to cherry-pick TrainJob TAS implementations to released branch.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2025-11-10T19:16:25Z

> For Openshift AI we are very interested in TrainJob in v0.14.

> I would like to understand what features are limited by Kubeflow 2.0 and what we would gain by including Trainer v2.1.0.

There are a couple of changes from Trainer v2.1 that we would want to have like https://github.com/kubeflow/trainer/pull/2802 and also the coupling with the latest version of the SDK to get some changes like https://github.com/kubeflow/sdk/pull/91 that depend on Trainer v2.1.

We don't have specific features needed on the Kueue side, e.g. TAS, but it's not 100% clear whether Kueue 0.14 is "forward' compatible with 2.1 outside of TAS. That may need testing, otherwise cherry-picking the Trainer v2.1 upgrade in 0.14.x would be enough for us.

So I think we fall in the category of users @mimowo mentioned:

> However, some users may use Kueue 0.14 for prod with Kubeflow 2.1.0 in the coming months.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T09:54:55Z

> The alpha level support is just discretion during development, as we discussed in the issue for Trainer integrations.

Indeed, in my mind this is still alpha becuase it is very early, and I don't have any indication of being used on prod yet.

> We evolved the Kueue TrainJob controller to support TAS, which depends on the Trainer v2.1 as a minimum version.
So, even if cherry-pick the Trainer dependency update PR, the released version (v0.14 / v0.13) could not support TAS with TrainJob. And we do not want to cherry-pick TrainJob TAS implementations to released branch.

Supporting TAS in Kueue if we upgrade to 2.1 is very simple, I think this is even the same commit in Kueue: https://github.com/kubernetes-sigs/kueue/pull/7249

So I think it is enough to cherrypick this one and solve conflicts.

> @mimowo Could you clarify how that will break existing users, if any ? IIUC, PodSpecOverride and PodTemplateOverride APIs are managed by Kueue controller, so users don't touch it.

Yes, users don't touch it, but if a user has an already running workload then it is modified. I haven't tested but I think after upgrade `PodTemplateOverride` will be interpreted as nil, and `PodSpecOverride` will not be read by Kueue. As a consequence the eviction for the workload may not work ideal, but this seems a marginal problem TBH.

I would be happy if someone could prepare the PR. We are to maintain 0.14 for long, so maintaining the old version does not seem good, especially as it would not support TAS anyway.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T09:57:31Z

IIUC we need to cherrypick the following PRs:
- https://github.com/kubernetes-sigs/kueue/pull/7249
- https://github.com/kubernetes-sigs/kueue/pull/7586

@IrvingMg can you try to prepare the cherrypick PR, and test manually the upgrade so that we know exactly what happens?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T10:00:58Z

Since this issue is already close I open https://github.com/kubernetes-sigs/kueue/issues/7608  to track the effort and experimentation
