# Issue #3822: Support KubeRay in MultiKueue via managedBy

**Summary**: Support KubeRay in MultiKueue via managedBy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3822

**Last updated**: 2025-04-16T11:48:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-12T09:15:26Z
- **Updated**: 2025-04-16T11:48:32Z
- **Closed**: 2025-04-16T11:48:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 27

## Description

**What would you like to be added**:

Support for KubeRay via managedBy in MultiKueue.

The relevant support for the managedBy field has been recently merged in KubeRay, see https://github.com/ray-project/kuberay/issues/2544, and will be released most likely in 1.3.
Until then we can use the main branch of kuberay in Kueue to test it all works. Once KubeRay is released we can switch to the released version and merge to Kueue.

**Why is this needed**:

Support of KubeRay via managedBy in MultiKueue, allowing for:
- ease of setup where full KubeRay can be installed on the management cluster (not just CRDs)
- hybrid deployments, where some RayJobs are executed via MultiKueue and some locally on the management cluster

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T09:15:58Z

/assign @mszadkow 

cc @mbobrovskyi @andrewsykim @mwielgus @mwysokin

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-13T10:06:52Z

This ticket requires to first provide RayJob and RayCluster Multikueue adapter and setup e2e tests,
as we don't have them yet.
First PR will be about adapter and multikueue e2e tests with ray-operator v1.2.2- no managedBy yet, as this requires `latest`.
Second PR will be the attempt to work with ray-operator `latest` and use of managedBy.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T10:18:16Z

sgtm, we can start with tests using 1.2.2 but without managedBy field and merge it as a starter. Or alternatively already use latest (main) of KubeRay just for testing purposes - we will merge once KubeRay is released.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-18T12:37:18Z

Another problem that I have right now is that Kuberay clusters startup time is huge for e2e tests.
It's about 5 minutes, maybe it's due to requirement to use rayproject image, but setting anything else as image results in job to stall at initialisation.
Normally we use `sleep` image just to call anything, but it won't work with ray cluster.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T12:55:08Z

Ok, in that case we may need to have a separate CI for Ray. 

However, let me first understand what you exactly mean by "cluster startup time" - is this the installation of the KubeRay, or time to run the first RayJob? Does it also take long to run follow-up Jobs?

Also, please make sure you are rebased against the main branch, because recently we increased CPU limits for Kueue to 2000m which might be relevant here too.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-12-18T15:08:07Z

> Normally we use sleep image just to call anything, but it won't work with ray cluster.

It may be possible to construct a dummy RayCluster that just calls `sleep` with a lighter image, but I haven't tried this myself. Assuming the start-up time issue is due to pulling the default Ray images

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T15:19:18Z

thank you @andrewsykim for the suggestion. @mszadkow can we try that? maybe you already did and hit some complications?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-19T07:40:15Z

Well I have tried to load the image up-front to the test cluster (kind), but then I had space limitation issues, at least locally.
Will have to verify what happens in CI.
@andrewsykim did you mean I could build lighter version of `rayproject/ray` ?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-12-20T02:25:06Z

> @andrewsykim did you mean I could build lighter version of rayproject/ray ?

No, when you constuct a RayJob or RayCluster, you can pass arbitrary images for the Head and Worker pods. So you can try using much smaller images used in other tests that just need to run `sleep`.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-23T15:26:59Z

I found a way to run other type of image, just with bash and calling sleep.
However it seems that kuberay overrides KUBERAY_GEN_RAY_START_CMD and never mind what I put there it's ` ray start --head  --dashboard-host=0.0.0.0  --metrics-export-port=8080  --block  --dashboard-agent-listen-port=52365`.
Then I would have to install ray to the docker...
Let's first go with `rayproject` image

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-05T12:05:23Z

I think, I will start early integration of v1.3.0-rc.0 within days
https://github.com/ray-project/kuberay/releases/tag/v1.3.0-rc.0
quay.io/kuberay/operator:v1.3.0-rc.0

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-07T09:14:28Z

@andrewsykim @mimowo 
I have encountered an issue with kuberay v1.3.0-rc.0 upgrade.

Kuberay has [k8s.io/component-base](http://k8s.io/component-base) v0.29.6
Kueue has [k8s.io/component-base](http://k8s.io/component-base) v0.32.1

There is a small change that affect us https://github.com/kubernetes/component-base/blob/264c1fd30132a3b36b7588e50ac54eb0ff75f26a/featuregate/testing/feature_gate.go#L47
this function now returns nothing, while before it returned a cleanup function.

This result in:
vendor/github.com/ray-project/kuberay/ray-operator/pkg/features/features.go:40:9: featuregatetesting.SetFeatureGateDuringTest(tb, utilfeature.DefaultFeatureGate, f, value) (no value) used as value
make: *** [build] Error 1

Question remains if it's ok to upgrade Kuberay's component base to v0.32.1 for 1.3.0 release?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-02-07T16:32:03Z

No objections to upgrade component base to v0.32.1 -- do you mind opening a PR for that?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-07T22:43:32Z

I am in the process of doing that, though I am afraid it won't just this package.
But let's see the results first ;)

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-17T10:57:29Z

@andrewsykim @mimowo 
After lengthy battle here is the PR: https://github.com/ray-project/kuberay/pull/3004

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-17T14:37:16Z

@andrewsykim is there any slack channel on `kubernetes.slack.com` dedicated to kuberay?
I only found dedicated workspace: https://github.com/ray-project/kuberay/issues/1059

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T20:31:55Z

> [@andrewsykim](https://github.com/andrewsykim) is there any slack channel on `kubernetes.slack.com` dedicated to kuberay? I only found dedicated workspace: [ray-project/kuberay#1059](https://github.com/ray-project/kuberay/issues/1059)

IIUC, Ray slack is only ray.slack.com

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-12T13:28:21Z

@mimowo @tenzen-y @andrewsykim 
I have tested locally that [kuberay release-1.3 with backport](https://github.com/ray-project/kuberay/pull/3163) works with Kueue.
I even run MultiKueue e2e tests with managedBy and kuberay-operator running on manager cluster and it passes, thus I think it is safe to proceed whenever Kuberay releases next 1.3.X version.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-12T22:21:04Z

> [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y) [@andrewsykim](https://github.com/andrewsykim) I have tested locally that [kuberay release-1.3 with backport](https://github.com/ray-project/kuberay/pull/3163) works with Kueue. I even run MultiKueue e2e tests with managedBy and kuberay-operator running on manager cluster and it passes, thus I think it is safe to proceed whenever Kuberay releases next 1.3.X version.

Thank you for your effort!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T14:12:02Z

/reopen
this is not done yet, only KubeRay is bumped so far. which is the prerequisite

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-18T14:12:09Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3822#issuecomment-2733406446):

>/reopen
>this is not done yet, only KubeRay is bumped so far. which is the prerequisite


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-18T15:51:02Z

This https://github.com/kubernetes-sigs/kueue/pull/4677 should conclude the task.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T15:58:28Z

We ahould also follow up with docs update. but this can be post release

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T10:31:49Z

/release-note-edit
```release-note
Support KubeRay (RayJob and RayCluster integrations) in MultiKueue via managedBy. 
This allows using the integrations and installing the KubeRay operator on the management cluster.
```

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-03T11:38:56Z

@mimowo Docs have beed updated - https://github.com/kubernetes-sigs/kueue/pull/4686.
Are there any other places to be updated or we could close this one?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T11:48:25Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-16T11:48:31Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3822#issuecomment-2809330402):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
