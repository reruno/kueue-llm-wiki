# Issue #9008: Release v0.15.4

**Summary**: Release v0.15.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9008

**Last updated**: 2026-02-11T11:42:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-05T15:03:47Z
- **Updated**: 2026-02-11T11:42:05Z
- **Closed**: 2026-02-11T11:42:03Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 7

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal.
  At least two for minor or major releases. At least one for a patch release.
- [x] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date
  - [x] Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes.
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""`
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #9106 <!-- example #211 #214 -->
- [x] An OWNER creates a signed tag running
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
      To perform this step, you need [a PGP key registered on github](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys).
- [x] An OWNER pushes the tag with
      `git push upstream $VERSION`
  - Triggers prow to build and publish a staging container image
      `us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:$VERSION`
- [x] An OWNER [prepares a draft release](https://github.com/kubernetes-sigs/kueue/releases)
  - [x] Create the draft release poiting out to the created tag.
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts in the `artifacts` folder.
  - [x] Upload the files in the `artifacts` folder to the draft release - either
      via UI or `gh release --repo kubernetes-sigs/kueue upload $VERSION artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: <!-- K8S_IO_PULL --> https://github.com/kubernetes/k8s.io/pull/9103
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.4
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [ ] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/9113
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/lGGHrgFIJ1c
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.15.3`:

## Changes by Kind

### Feature

- KueueViz backend and frontend resource requests/limits are now configurable via Helm values (kueueViz.backend.resources and kueueViz.frontend.resources). (#8982, @david-gang)

### Bug or Regression

- Fix a bug where finished or deactivated workloads blocked ClusterQueue deletion and finalizer removal. (#8940, @sohankunkerkar)
- LeaderWorkerSet: Fix the bug where rolling updates with maxSurge could get stuck. (#8887, @PannagaRao)
- LeaderWorkerSet: Fixed bug that doesn't allow to delete Pod after LeaderWorkerSet delete (#8883, @mbobrovskyi)
- Metrics certificate is now reloaded when certificate data is updated. (#9100, @MaysaMacedo)
- MultiKueue & ElasticJobs: fix the bug that the new size of a Job was not reflected on the worker cluster. (#9044, @ichekrygin)
- Observability: Fix Prometheus ServiceMonitor selector and RBAC to enable metrics scraping. (#8979, @IrvingMg)
- PodIntegration: Fix the bug that Kueue would occasionally remove the custom finalizers when
  removing the `kueue.x-k8s.io/managed` finalizer. (#8905, @mykysha)
- RayJob integration: Make RayJob top level workload managed by Kueue when autoscaling via
  ElasticJobsViaWorkloadSlices is enabled.
  
  If you are an alpha user of the ElasticJobsViaWorkloadSlices feature for RayJobs, then upgrading Kueue may impact running live jobs which have autoscaling / workload slicing enabled. For example, if you upgrade Kueue, before
  scaling-up completes,  the new pods will be stuck in SchedulingGated state. After Kueue version update, cluster admins probably should migrate from the old RayJob with ElasticJobsViaWorkloadSlices to the new one (recreating). (#9070, @mimowo)
- TAS: Fix a bug that TAS ignored resources excluded by excludeResourcePrefixes for node placement. (#8991, @sohankunkerkar)
- TAS: Fixed a bug that pending workloads could be stuck, not being considered by the Kueue's scheduler,
  after the restart of Kueue. The workloads would be considered for scheduling again after any update to their 
  ClusterQueue. (#9057, @sohankunkerkar)
- TAS: Fixed handling of the scenario where a Topology instance is re-created (for example, to add a new Topology level).
  Previously, this would cause cache corruption, leading to issues such as:
  1. Scheduling a workload on nodes that are fully occupied by already running workloads.
  2. Scheduling two or more pods of the same workload on the same node (even when the node cannot host both). (#8765, @mimowo)
- TAS: Lower verbosity of expected missing pod index label logs. (#8702, @IrvingMg)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T07:10:42Z

Given the number of changes to the RayJob support for ElasticWorklaods is would be good to do manual testing before the release: https://github.com/kubernetes-sigs/kueue/pull/9068#issuecomment-3875764059

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T19:26:06Z

@tenzen-y I have conducted testing of the upgrade from 0.15.3 to release-0.15 images twice.

I basically started the RayJob, and after a while triggered the upgrade, maybe 15s-30s. Once the upgrade was smooth and the RayJob continued, once it corrupted (Running state, but the Pods were failed). 

So, yes, the Elastic RayJob may fail on Kueue upgrade, but I think it is ok since the ElasticJobs are Alpha still. Also, it wasn't "catastrophic" - the issue was limited to the RayJob. Deleting the RayJob helped.

I also tested manually scaling of the batch/Job and didn't spot issues.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T08:14:00Z

> [@tenzen-y](https://github.com/tenzen-y) I have conducted testing of the upgrade from 0.15.3 to release-0.15 images twice.
> 
> I basically started the RayJob, and after a while triggered the upgrade, maybe 15s-30s. Once the upgrade was smooth and the RayJob continued, once it corrupted (Running state, but the Pods were failed).
> 
> So, yes, the Elastic RayJob may fail on Kueue upgrade, but I think it is ok since the ElasticJobs are Alpha still. Also, it wasn't "catastrophic" - the issue was limited to the RayJob. Deleting the RayJob helped.
> 
> I also tested manually scaling of the batch/Job and didn't spot issues.

Thank you for carefully verifying the upgrade behavior. Yes, that is our expectation as we discussed in the cherry-pick PR.
As we discussed offline, we just had a break in the release note (NOT action required) since ElasticJobsViaWorkloadSlices is still in an alpha stage.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T08:14:09Z

release and release note LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T10:29:09Z

I verified the published images:

```shell
docker run -it registry.k8s.io/kueue/kueue:v0.15.4 2>&1 | grep "Digest"
Digest: sha256:c4c0856b5f60fa83c6f70b34dca0f81c22b7e184f610647092fccaac1dafd001

docker run -it registry.k8s.io/kueue/kueueviz-backend:v0.15.4 2>&1 | grep "Digest"
Digest: sha256:b776fef93e0c0d2cbab5b3e12ba882856abe52c49b5dab4863166df387072fb7

docker run -it registry.k8s.io/kueue/kueueviz-frontend:v0.15.4 2>&1 | grep "Digest"
Digest: sha256:8a992d27c94d34ea23f22f773d2818267880b8834e1a77378cb350880630d60a

docker run -it registry.k8s.io/kueue/kueue-populator:v0.15.4 2>&1 | grep "Digest"
Digest: sha256:48dacd4e6dace9afa0aa34e01a84fc9e3c92682e52350fba9bdf075f66e10ad0

helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.15.4 2>&1 | grep "Digest"
Digest: sha256:b0976a037c1ef777acd1bc4ed1f3f1e4258281921f52f596aaed769bf7c4fba5

helm template oci://registry.k8s.io/kueue/charts/kueue-populator --version 0.15.4 2>&1 | grep "Digest"
Digest: sha256:d36803535379a64296da18da2f41f71b4ec6bff9b239415e9cbc3b33f36e4896
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T11:41:58Z

done.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-11T11:42:04Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9008#issuecomment-3883904082):

>done.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
