# Issue #8460: Release v0.15.3

**Summary**: Release v0.15.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8460

**Last updated**: 2026-01-22T14:04:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-08T07:38:45Z
- **Updated**: 2026-01-22T14:04:19Z
- **Closed**: 2026-01-22T14:04:19Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 10

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
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #8700 <!-- example #211 #214 -->
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
      to production: <!-- K8S_IO_PULL --> <!-- example kubernetes/k8s.io#7899 -->
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: <!-- example #3007 -->
  - [ ] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/gbgoxJlnsZg
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
Changes since `v0.15.2`:

## Changes by Kind

### Feature

- CLI: Support "kwl" and "kueueworkload" as a shortname for Kueue Workloads. (#8469, @kannon92)

### Bug or Regression

- Add lws editer and viewer roles to kustomize and helm (#8515, @kannon92)
- FailureRecovery: Fix Pod Termination Controller's MaxConcurrentReconciles (#8665, @gabesaba)
- Fix ClusterQueue deletion getting stuck when pending workloads are deleted after being assumed by the scheduler. (#8548, @sohankunkerkar)
- Fix a bug that WorkloadPriorityClass value changes do not trigger Workload priority updates. (#8499, @ASverdlov)
- HC: Avoid redundant requeuing of inadmissible workloads when multiple ClusterQueues in the same cohort hierarchy are processed. (#8510, @sohankunkerkar)
- Integrations based on Pods: skip using finalizers on the Pods created and managed by integrations. 
  
  In particular we skip setting finalizers for Pods managed by the built in Serving Workloads  Deployments,
  StatefulSets, and LeaderWorkerSets.
  
  This improves performance of suspending the workloads, and fixes occasional race conditions when a StatefulSet
  could get stuck when deactivating and re-activating in a short interval. (#8573, @mbobrovskyi)
- JobFramework: Fixed a bug that allowed a deactivated workload to be activated. (#8438, @chengjoey)
- LeaderWorkerSet: Fixed a bug that prevented deleting the workload when the LeaderWorkerSet was scaled down. (#8673, @mbobrovskyi)
- MultiKueue now waits for WorkloadAdmitted (instead of QuotaReserved) before deleting workloads from non-selected worker clusters. To revert to the previous behavior, disable the `MultiKueueWaitForWorkloadAdmitted` feature gate. (#8600, @IrvingMg)
- MultiKueue: Fix a bug that the priority change by mutating the `kueue.x-k8s.io/priority-class` label on the management cluster is not propagated to the worker clusters. (#8574, @mbobrovskyi)
- MultiKueue: fix the eviction when initiated by the manager cluster (due to eg. Preemption or WairForPodsReady timeout). (#8402, @mbobrovskyi)
- ProvisioningRequest: Fixed a bug that prevented events from being updated when the AdmissionCheck state changed. (#8404, @mbobrovskyi)
- Revert the changes in PR https://github.com/kubernetes-sigs/kueue/pull/8599 for transitioning
  the QuotaReserved, Admitted conditions to `False` for Finished workloads. This introduced a regression,
  because users lost the useful information about the timestamp of the last transitioning of these
  conditions to True, without an API replacement to serve the information. (#8612, @mbobrovskyi)
- Scheduling: fix the bug that setting (none -> some) a workload priority class label (kueue.x-k8s.io/priority-class) was ignored. (#8584, @andrewseif)
- TAS: Fix a bug that MPIJob with runLauncherAsWorker Pod indexes are not correctly evaluated during rank-based ordering assignments. (#8663, @tenzen-y)
- TAS: Fixed an issue where workloads could remain in the second-pass scheduling queue (used for integration
  or TAS with ProvisioningRequests, and for TAS Node Hot Swap) even if they no longer require to be in the queue. (#8431, @skools-here)
- TAS: fix TAS resource flavor controller to extract only scheduling-relevant node updates to prevent unnecessary reconciliation. (#8453, @Ladicle)
- TAS: significantly improves scheduling performance by replacing Pod listing with an event-driven
  cache for non-TAS Pods, thereby avoiding expensive DeepCopy operations during each scheduling cycle. (#8484, @gabesaba)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T07:46:47Z

We tentatively plan next week (Jan 12th+), cc @tenzen-y.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T16:34:30Z

The tentative release date is 15th Jan

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-14T17:51:22Z

Based on offline discussion with @mimowo, we decided to postpone it to 16th Jan because we want to fix a couple of issues before this release.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T10:59:58Z

@tenzen-y @gabesaba  I would like to include https://github.com/kubernetes-sigs/kueue/pull/8484 in the patch release. Since it has still unresolved comments I think it is safer to move the patches to Monday.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T11:25:47Z

> [@tenzen-y](https://github.com/tenzen-y) [@gabesaba](https://github.com/gabesaba) I would like to include [#8484](https://github.com/kubernetes-sigs/kueue/pull/8484) in the patch release. Since it has still unresolved comments I think it is safer to move the patches to Monday.

Agreed

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-20T13:33:33Z

release /lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T13:35:36Z

LGTM, thanks 💯

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T14:01:03Z

Release note lgtm

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-20T15:48:20Z

**Image verification:**

docker run -it registry.k8s.io/kueue/kueue:v0.15.3  2>&1 | grep "Digest"
Digest: sha256:4de0c605f733cd9dd3902d6520068b092a2a0d7a4c371bdd150dd367ad396038

docker run -it registry.k8s.io/kueue/kueueviz-backend:v0.15.3  2>&1 | grep "Digest"
Digest: sha256:556f145c4566e3d258a910b0edd954edb7de1172376cb33018515df67a46a363

docker run -it registry.k8s.io/kueue/kueueviz-frontend:v0.15.3  2>&1 | grep "Digest"
Digest: sha256:ddf7928310aff215223cf49490b281c73bd2cacdc766ce7d787ac59435f7dd96

docker run -it registry.k8s.io/kueue/kueue-populator:v0.15.3  2>&1 | grep "Digest"
Digest: sha256:ba2d99be7462185ed9788ba003fc01e2aaa04d4d61103454b6cf91e7b2098b9f

**Chart verification:**
helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.15.3 2>&1 | grep "Digest"
Digest: sha256:966c6de8d605058135aa911ca0c9aa12dc3659c8714194c97f8eec330a8a9ac3

helm template oci://registry.k8s.io/kueue/charts/kueue-populator --version 0.15.3 2>&1 | grep "Digest"
Digest: sha256:dfe654aed172c0204361fccfd202165e49e8878fbe42d59b746902f7db1745b5

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T14:04:19Z

/close
the release is out
