# Issue #9009: Release v0.16.1

**Summary**: Release v0.16.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9009

**Last updated**: 2026-02-17T00:24:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-05T15:04:00Z
- **Updated**: 2026-02-17T00:24:02Z
- **Closed**: 2026-02-11T12:57:57Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

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
  - [x] Submit a pull request with the changes: #9105 <!-- example #211 #214 -->
- [x] An OWNER creates a signed tag running
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
      To perform this step, you need [a PGP key registered on github](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys).
- [x] An OWNER pushes the tag with
      `git push upstream $VERSION`
  - Triggers prow to build and publish a staging container image
      `us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:$VERSION`
- [ ] An OWNER [prepares a draft release](https://github.com/kubernetes-sigs/kueue/releases)
  - [x] Create the draft release poiting out to the created tag.
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts in the `artifacts` folder.
  - [x] Upload the files in the `artifacts` folder to the draft release - either
      via UI or `gh release --repo kubernetes-sigs/kueue upload $VERSION artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: <!-- K8S_IO_PULL -->  https://github.com/kubernetes/k8s.io/pull/9102
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.16.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/9112
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
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
Changes since `v0.16.0`:

## Changes by Kind

### Feature

- KueueViz backend and frontend resource requests/limits are now configurable via Helm values (kueueViz.backend.resources and kueueViz.frontend.resources). (#8981, @david-gang)

### Bug or Regression

- Fix Visibility API OpenAPI schema generation to prevent schema resolution errors when visibility v1beta1/v1beta2 APIServices are installed.
  
  The visibility schema issues result in the following error when re-applying the manifest for Kueue 0.16.0:
  `failed to load open api schema while syncing cluster cache: error getting openapi resources: SchemaError(sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkloadsSummary.items): unknown model in reference: "sigs.k8s.io~1kueue~1apis~1visibility~1v1beta1.PendingWorkload"` (#8901, @vladikkuzn)
- Fix a bug where finished or deactivated workloads blocked ClusterQueue deletion and finalizer removal. (#8936, @sohankunkerkar)
- LeaderWorkerSet: Fix the bug where rolling updates with maxSurge could get stuck. (#8886, @PannagaRao)
- LeaderWorkerSet: Fixed bug that doesn't allow to delete Pod after LeaderWorkerSet delete (#8882, @mbobrovskyi)
- Metrics certificate is now reloaded when certificate data is updated. (#9099, @MaysaMacedo)
- MultiKueue & ElasticJobs: fix the bug that the new size of a Job was not reflected on the worker cluster. (#9055, @ichekrygin)
- Observability: Fix Prometheus ServiceMonitor selector and RBAC to enable metrics scraping. (#8980, @IrvingMg)
- Observability: Fixed a bug where workloads that finished before a Kueue restart were not tracked in the gauge metrics for finished workloads. (#8827, @mbobrovskyi)
- Observability: fix the bug that the "replica-role" (leader / follower) log decorator was missing in the log lines output by
  the  webhooks for LeaderWorkerSet and StatefulSet . (#8820, @mszadkow)
- PodIntegration: Fix the bug that Kueue would occasionally remove the custom finalizers when
  removing the `kueue.x-k8s.io/managed` finalizer. (#8903, @mykysha)
- RayJob integration: Make RayJob top level workload managed by Kueue when autoscaling via
  ElasticJobsViaWorkloadSlices is enabled.
  
  If you are an alpha user of the ElasticJobsViaWorkloadSlices feature for RayJobs, then upgrading Kueue may impact running live jobs which have autoscaling / workload slicing enabled. For example, if you upgrade Kueue, before
  scaling-up completes,  the new pods will be stuck in SchedulingGated state. (#9039, @hiboyang)
- TAS: Fix a bug that TAS ignored resources excluded by excludeResourcePrefixes for node placement. (#8990, @sohankunkerkar)
- TAS: Fixed a bug that pending workloads could be stuck, not being considered by the Kueue's scheduler,
  after the restart of Kueue. The workloads would be considered for scheduling again after any update to their 
  ClusterQueue. (#9056, @sohankunkerkar)

### Other (Cleanup or Flake)

- KueueViz: It switches to the v1beta2 API (#8804, @mbobrovskyi)

```

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-05T16:24:48Z

Just a note: we might need https://github.com/kubernetes-sigs/kueue/issues/9005 in this release.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-05T17:15:34Z

> Just a note: we might need [#9005](https://github.com/kubernetes-sigs/kueue/issues/9005) in this release.

I don't want to block patch releases on work that doesn't have a PR yet. 

This work can always go into a new patch release once it is merged.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T17:43:44Z

There is no date yet, but I think mid next week. If the fix can be done and reviewed by then, then we can include. Otherwise, 0.16.2.

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T17:52:33Z

Tentatively planning for Wednesday (11th Feb)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-05T18:43:59Z

> There is no date yet, but I think mid next week. If the fix can be done and reviewed by then, then we can include. Otherwise, 0.16.2.
> 
> cc [@tenzen-y](https://github.com/tenzen-y)

Yes, we will be able to have another round (v0.16.2) after next week if #9005 is not finalized by the next Wed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T08:00:41Z

The release and release notees LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T10:18:01Z

```
❯ ./hack/releasing/wait_for_images.sh --prod $VERSION
Images:

  Checking if "registry.k8s.io/kueue/kueue:v0.16.1" is available.
    ✅ Image "registry.k8s.io/kueue/kueue@sha256:87bdbcb7ab69c5364459710b90b329d51b369c17b21d670f6436fe3f6864a78f" is available.
    sha256:87bdbcb7ab69c5364459710b90b329d51b369c17b21d670f6436fe3f6864a78f

  Checking if "registry.k8s.io/kueue/kueueviz-backend:v0.16.1" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-backend@sha256:26d93e2d0620a3601b81de3339a1f102efd9503055746bd4a2e22c7cb005b7db" is available.
    sha256:26d93e2d0620a3601b81de3339a1f102efd9503055746bd4a2e22c7cb005b7db

  Checking if "registry.k8s.io/kueue/kueueviz-frontend:v0.16.1" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-frontend@sha256:067f9d1a115901bb6731635229059720981b014f1651b1ba628ca4b38341a2d0" is available.
    sha256:067f9d1a115901bb6731635229059720981b014f1651b1ba628ca4b38341a2d0

  Checking if "registry.k8s.io/kueue/kueue-populator:v0.16.1" is available.
    ✅ Image "registry.k8s.io/kueue/kueue-populator@sha256:3f73b9219f91ef9496a32a8ed9ab5bd993a9ac5459813fc3c56cf194beb8e473" is available.
    sha256:3f73b9219f91ef9496a32a8ed9ab5bd993a9ac5459813fc3c56cf194beb8e473

Charts:

  Checking if "registry.k8s.io/kueue/charts/kueue:0.16.1" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue@sha256:46769c995dc7a71cb2ed05797e3f017cea13e440c4ff74d1add35e573f97029d" is available.
    sha256:46769c995dc7a71cb2ed05797e3f017cea13e440c4ff74d1add35e573f97029d

  Checking if "registry.k8s.io/kueue/charts/kueue-populator:0.16.1" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue-populator@sha256:3c5b5fb0c4c1a78b803a2c03e37c4e5e1a3b8480621c914cca665f26996744ee" is available.
    sha256:3c5b5fb0c4c1a78b803a2c03e37c4e5e1a3b8480621c914cca665f26996744ee
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T12:57:53Z

/close
The last pending item is merging of https://github.com/kubernetes-sigs/kueue/pull/9112, I don't expect surprises there.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-11T12:57:59Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9009#issuecomment-3884277452):

>/close
>The last pending item is merging of https://github.com/kubernetes-sigs/kueue/pull/9112, I don't expect surprises there.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@zhanglin2603](https://github.com/zhanglin2603) — 2026-02-17T00:15:41Z

Hey, I went over kubernetes-sigs/kueue#9009 and can take this on.
- My read: this is primarily a authentication task tied to "Release v0.16.1".
- I will focus on these issue-specific points first: release, checklist, not.
- First I will reproduce and confirm expected behavior for the authentication path.
- Then I will implement the fix with targeted tests and keep scope tight (good confidence).
- I will share a working PR update fast (24h for first patch, 48h for final polish) with verification notes.
If this approach works for you, I can start now.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-17T00:24:02Z

@zhanglin2603 I appreciate your enthusiasm but this ticket has to be done by maintainers due to write access to the repo.
