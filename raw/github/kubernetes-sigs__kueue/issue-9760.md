# Issue #9760: Release v0.16.3

**Summary**: Release v0.16.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9760

**Last updated**: 2026-03-17T16:23:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-09T15:20:05Z
- **Updated**: 2026-03-17T16:23:41Z
- **Closed**: 2026-03-17T16:23:41Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

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
- [ ] Update the release branch:
  - [x] Ensure there are no unstaged changes in your directory (the script adds everything)
  - [x] Run `./hack/releasing/prepare_pull.sh --target release $VERSION`
  - [x] Wait for this PR to merge #9856 <!-- example #211 #214 -->
- [ ] An OWNER creates a signed tag
  - [x] pull the release branch after PR from previous step merged
  - [x] run
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
      to production: kubernetes/k8s.io#9222 <!-- example kubernetes/k8s.io#7899 -->
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`. May use `./hack/releasing/promote_pull.sh`
  - [x] Wait for the PR to be merged
   - [x] Verify that the image is available `./hack/releasing/wait_for_images.sh --prod $VERSION`
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.16.3
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] for each release:
    - [ ] update the changelog (example #9578)
  - [x] for only the latest release:
    - [x] Run `./hack/releasing/prepare_pull.sh --target main $VERSION`
    - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/9862
    - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.  https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/TgYjvHssetA
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
Changes since `v0.16.2`:

## Changes by Kind

### Feature

- Observability: Add scheduler logs for the scheduling cycle phase boundaries. (#9813, @sohankunkerkar)
- Scheduling: Add the alpha SchedulerLongRequeueInterval feature gate (disabled by default) to increase the 
  inadmissible workload requeue interval from 1s to 10s. This may help to mitigate, on large environments with 
  many pending workloads, issues with frequent re-queues that prevent the scheduler from reaching schedulable 
  workloads deeper in the queue and result in constant re-evaluation of the same top workloads. (#9819, @mbobrovskyi)
- Scheduling: Add the alpha SchedulerTimestampPreemptionBuffer feature gate (disabled by default) to use
  5-minute buffer so that workloads with scheduling timestamps within this buffer don’t preempt each other
  based on LowerOrNewerEqualPriority. (#9837, @mbobrovskyi)

### Bug or Regression

- FailureRecoveryPolicy: forcefully delete stuck pods (without grace period) in addition to transitioning them
  to the `Failed` phase. This fixes a scenario where foreground propagating deletions were blocked by a stuck pod. (#9673, @kshalot)
- Fix a race where updated workload priority could remain stuck in the inadmissible queue and delay rescheduling. (#9678, @sohankunkerkar)
- In fair sharing preemption, bypass DRS strategy gates when the preemptor ClusterQueue is within nominal quota for contested resources, allowing preemption even if the CQ's aggregate DRS is high due to borrowing on other flavors. (#9592, @mukund-wayve)
- Kueueviz: fetch Cohort CRD directly, instead of deriving from ClusterQueues (#9720, @samzong)
- LeaderWorkerSet: fix workload recreation delay during rolling updates by watching for workload deletions. (#9680, @PannagaRao)
- Observability: Fix missing replica_role=leader gauge metrics after HA role transition. (#9794, @IrvingMg)
- Scheduling: Fix a BestEffortFIFO performance issue where many equivalent workloads could
  prevent the scheduler from reaching schedulable workloads deeper in the queue. Kueue now
  skips redundant evaluation by bulk-moving same-hash workloads to inadmissible when one
  representative is categorized as NoFit. (#9698, @sohankunkerkar)
- Scheduling: Fix that the Kueue's scheduler could issue duplicate preemption requests and events for the same workload. (#9627, @sohankunkerkar)
- Scheduling: Fixed a race condition where a workload could simultaneously exist in the scheduler's heap
  and the "inadmissible workloads" list. This fix prevents unnecessary scheduler cycles and prevents temporary 
  double counting for the metric of pending workloads. (#9638, @sohankunkerkar)
- Scheduling: Reduced the maximum sleep time between scheduling cycles from 100ms to 10ms.
  This change fixes a bug where the 100ms delay was excessive on busy systems, in which completed
  workloads can trigger requeue events every second. In such cases, the scheduler could spend up to 10%
  of the time between requeue events sleeping. Reducing the delay allows the scheduler to spend more time
  progressing through the ClusterQueue heap between requeue events. (#9763, @mimowo)
- StatefulSet integration: fix the bug that when using `generateName` the Workload names generated
  for two different StatefulSets would conflict, not allowing to run the second StatefulSet. (#9693, @IrvingMg)
- TAS: Fix performance bug where snapshotting would take very long due to List and DeepCopy
  of all Nodes. Now the cached set of nodes is maintained in event-driven fashion. (#9783, @mbobrovskyi)
- TAS: support ResourceTransformations to define "virtual" resources which allow putting a cap on
  some "virtual" credits across multiple-flavors, see [sharing quotas](https://kueue.sigs.k8s.io/docs/tasks/manage/share_quotas_across_flavors/) for quota-only resources.
  This is considered a bug since there was no validation preventing such configuration before. (#9688, @mbobrovskyi)
- VisibilityOnDemand: Fix the bug that when running Kueue with the custom `--kubeconfig` flag the visibility server
  fails to initialize, because the custom value of the flag is not propagated to it, leading to errors such as:
  "Unable to create and start visibility server","error":"unable to apply VisibilityServerOptions: failed to get delegated authentication kubeconfig:  failed to get delegated authentication kubeconfig: ..." (#9805, @Nilsachy)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T11:47:00Z

Release and changelog look great!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T13:13:15Z

```shell
Images:

  Checking if "registry.k8s.io/kueue/kueue:v0.16.3" is available.
    ✅ Image "registry.k8s.io/kueue/kueue@sha256:0ba76b0019d25f81828f914db0192bc28dcd94af8fb38bac83623c994138e777" is available.
    sha256:0ba76b0019d25f81828f914db0192bc28dcd94af8fb38bac83623c994138e777

  Checking if "registry.k8s.io/kueue/kueueviz-backend:v0.16.3" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-backend@sha256:80370690c14e6ce5ed3e6eef5b008c5b5654ccb295e3227f1d7d745a2eae6915" is available.
    sha256:80370690c14e6ce5ed3e6eef5b008c5b5654ccb295e3227f1d7d745a2eae6915

  Checking if "registry.k8s.io/kueue/kueueviz-frontend:v0.16.3" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-frontend@sha256:8118a8894beacef5db9891d248335b034d177fa5a9ededd7d41ff84f64679427" is available.
    sha256:8118a8894beacef5db9891d248335b034d177fa5a9ededd7d41ff84f64679427

  Checking if "registry.k8s.io/kueue/kueue-populator:v0.16.3" is available.
    ✅ Image "registry.k8s.io/kueue/kueue-populator@sha256:cfeae6eadace96012e6469bc003aa0879b5fb43078aa6b9474eb21004ee99890" is available.
    sha256:cfeae6eadace96012e6469bc003aa0879b5fb43078aa6b9474eb21004ee99890

Charts:

  Checking if "registry.k8s.io/kueue/charts/kueue:0.16.3" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue@sha256:2ddd53da621838fb91f0fc9776c41c3d1e4adb8f86b5005e02b6ee7195decc15" is available.
    sha256:2ddd53da621838fb91f0fc9776c41c3d1e4adb8f86b5005e02b6ee7195decc15

  Checking if "registry.k8s.io/kueue/charts/kueue-populator:0.16.3" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue-populator@sha256:f8c6524d2fde7aac7236991fda0c411a2b32f9e4b0b73435e33eccab7f5bd868" is available.
    sha256:f8c6524d2fde7aac7236991fda0c411a2b32f9e4b0b73435e33eccab7f5bd868
```
