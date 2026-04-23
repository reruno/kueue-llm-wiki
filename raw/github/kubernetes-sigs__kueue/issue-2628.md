# Issue #2628: Release v0.8.0

**Summary**: Release v0.8.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2628

**Last updated**: 2024-07-25T08:40:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-07-16T16:32:59Z
- **Updated**: 2024-07-25T08:40:47Z
- **Closed**: 2024-07-23T09:53:22Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

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
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #2649
- [x] An OWNER [prepares a draft release](https://github.com/kubernetes-sigs/kueue/releases)
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts and upload the files in the `artifacts` folder
      to the draft release.
- [x] An OWNER creates a signed tag running
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
      To perform this step, you need [a PGP key registered on github](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys).
- [x] An OWNER pushes the tag with
      `git push $VERSION`
  - Triggers prow to build and publish a staging container image
      `gcr.io/k8s-staging-kueue/kueue:$VERSION`
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7032
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] Update the below files with respective values in `main` branch : #2651
  - Latest version in `README.md`
  - Release notes in the `CHANGELOG`
  - `version` in `site/config.toml`
  - `appVersion` in `charts/kueue/Chart.yaml`
  - `last-updated`, `last-reviewed`, `commit-hash`, `project-release`, `distribution-points` and `sbom-file` in `SECURITY-INSIGHTS.yaml`
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/33033


## Changelog

```markdown
Changes since `v0.7.0`:
### Urgent Upgrade Notes 

#### (No, really, you MUST read this before you upgrade)

- Use a single rate limiter for all API types clients.
  
  Consider adjusting `clientConnection.qps` and `clientConnection.burst` if you observe any performance degradation. (#2462, @trasc)
 
### Feature

- Add a column to workload indicating if it is finished (#2615, @highpon)
- Add preempted_workloads_total metric that tracks the number of preemptions issued by a ClusterQueue) (#2538, @vladikkuzn)
- Add the following events for eviction on the workload indicating the reason for eviction:
  - "EvictedDueToPodsReadyTimeout"
  - "EvictedDueToAdmissionCheck"
  - "EvictedDueToClusterQueueStopped"
  - "EvictedDueToInactiveWorkload" (renamed from InactiveWorkload)
  
  If you were watching for the typed Normal event with `InactiveWorkload` reason, use `EvictedDueToInactiveWorkload` reason one instead. (#2376, @mbobrovskyi)
- AdmissionChecks: A workload with a Rejected AdmissionCheck gets deactivated (#2363, @PBundyra)
- Allow stoping admission from a specific LocalQueue. (#2173, @mbobrovskyi)
- Allow usage of the pod integration for pods belonging to jobs that Kueue supports, if the support for the job type is explicitly disabled (#2493, @trasc)
- CLI: Add stop/resume localqueue commands (#2415, @rainfd)
- CLI: Added Node Labels column on resource flavor list. (#2557, @mbobrovskyi)
- CLI: Added create resourceflavor command. (#2517, @mbobrovskyi)
- CLI: Added list resourceflavor command. (#2525, @mbobrovskyi)
- CLI: Added resourceflavor to pass-through commands. (#2518, @mbobrovskyi)
- CLI: Added version command. (#2346, @mbobrovskyi)
- CLI: Adds `for` filter to list workloads. (#2238, @IrvingMg)
- CLI: Adds create clusterqueue command. (#2201, @IrvingMg)
- CLI: Support autocompletion (#2314, @mbobrovskyi)
- CLI: Support paging on kueue CLI list commands. (#2313, @mbobrovskyi)
- CLI: kubectl-kueue tar.gz archives is part of the release artifacts. (#2513, @mbobrovskyi)
- Do not start Kueue when the visibility server cannot be started, but is requested. (#2636, @mbobrovskyi)
- Experimental support for helm charts in the gcr.io/k8s-staging-kueue/charts/kueue repository (#2377, @IrvingMg)
- Improved logging for scheduling and preemption in levels 4 and 5 (#2504, @alculquicondor)
- Introduce the MultiplePreemptions flag, which allows more than one
  preemption to occur in the same scheduling cycle, even with overlapping
  FlavorResources (#2641, @gabesaba)
- More granular Preemption condition reasons: PriorityReclamation, InCohortReclamation, InCohortFairSharing, InCohortReclaimWhileBorrowing (#2411, @vladikkuzn)
- MultiKueue: Allow for defaulting of the spec.managedBy field for Jobs managed by MultiKueue.
  The defaulting is enabled by the MultiKueueBatchJobWithManagedBy feature-gate. (#2401, @vladikkuzn)
- MultiKueue: Remove remote objects synchronously when the worker cluster is reachable. (#2347, @trasc)
- MultiKueue: Use batch/Job `spec.managedBy` field (#2331, @trasc)
- Multikueue: Batch reconcile events for remote workloads. (#2380, @trasc)
- ProvisioningRequest: Support for ProvisioningRequest's condition `BookingExpired` (#2445, @PBundyra)
- ProvisioningRequets: Support for ProvisioningRequest's condition `CapacityRevoked`. ProvisioningRequests objects persist until the corresponding Job or the Workload is deleted (#2196, @PBundyra)

### Documentation

- Added details documentation for kubectl-kueue plugin. (#2613, @mbobrovskyi)
- Improve the documentation for the waitForPodsReady (#2541, @mimowo)

### Bug or Regression

- Added raycluster roles to manifests.yaml (#2618, @mbobrovskyi)
- CLI: Fixed no Auth Provider found for name "oidc" error. (#2602, @Kavinraja-G)
- Fix check that prevents preemptions when a workload requests 0 for a resource that is at nominal or over it. (#2520, @alculquicondor)
- Fix for the scenario when a workload doesn't match some resource flavors due to affinity or taints
  could cause the workload to be continuously retried. (#2407, @KunWuLuan)
- Fix missing fairSharingStatus in ClusterQueue (#2424, @mbobrovskyi)
- Fix missing metric cluster_queue_status (#2474, @mbobrovskyi)
- Fix panic that could occur when a ClusterQueue is deleted while Kueue was updating the ClusterQueue status. (#2461, @mbobrovskyi)
- Fix panic when there is not enough quota to assign flavors to a Workload in the cohort, when FairSharing is enabled. (#2439, @mbobrovskyi)
- Fix performance issue in logging when processing LocalQueues. (#2485, @alexandear)
- Fix race condition on delete workload from queue manager. (#2460, @mbobrovskyi)
- Fix race condition on requeue workload. (#2509, @mbobrovskyi)
- Fix race condition on run garbage collection in multikueuecluster reconciler. (#2479, @mbobrovskyi)
- Fix the validation messages, to report the new value rather than old, for the following immutable labels: `kueue.x-k8s.io/queue-name`, `kueue.x-k8s.io/prebuilt-workload-name`, and `kueue.x-k8s.io/priority-class`. (#2544, @xuxianzhang)
- Fixed issue that prevented restoring the startTime and pod template when evicting a batch/v1 Job, if any API errors happened in the process (#2567, @mbobrovskyi)
- MultiKueue: Do not reject a JobSet if the corresponding cluster queue doesn't exist (#2425, @vladikkuzn)
- MultiKueue: Skip garbage collection for disconnected clients which could occasionally result in panic. (#2369, @trasc)
- Show weightedShare in ClusterQueue status.fairSharing even if the value is zero (#2521, @alculquicondor)
- Skip duplicate Tolerations when an admission check introduces a toleration that the job also set. (#2498, @trasc)

### Other (Cleanup or Flake)

- Importer: corrects the field name `observedFirstIn` in logs. (#2500, @alexandear)
- Use Patch instead of Update on jobframework multikueue adapters to prevent the risk of dropping fields. (#2590, @mbobrovskyi)
- Use Patch instead of Update on jobframework to prevent the risk of dropping fields. (#2553, @mbobrovskyi)
```

```[tasklist]
### Pending PRs/issues
- [ ] #2538
- [ ] #2596
- [ ] #2572
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-16T16:34:01Z

LGTM

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-18T20:57:53Z

Added release notes (except for #2596, which is in review).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-23T09:53:18Z

Completed.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-23T09:53:23Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2628#issuecomment-2244764937):

>Completed.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
