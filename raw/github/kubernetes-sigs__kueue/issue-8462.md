# Issue #8462: Release v0.16.0

**Summary**: Release v0.16.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8462

**Last updated**: 2026-01-27T04:06:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-08T08:02:12Z
- **Updated**: 2026-01-27T04:06:58Z
- **Closed**: 2026-01-27T04:06:57Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 16

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal.
  At least two for minor or major releases. At least one for a patch release.
- [x] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date
  - [ ] Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes.
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""`
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #8792 <!-- example #211 #214 -->
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
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: <!-- example #3007 -->
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/36309
  - [x] Create the presubmits and the periodic jobs for the next patch release: kubernetes/test-infra#36310
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [x] Drop CI Jobs for testing the out-of-support branch: kubernetes/test-infra#36310
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.15.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- Removed FlavorFungibilityImplicitPreferenceDefault feature gate.
  
  Configure flavor selection preference using the ClusterQueue field `spec.flavorFungibility.preference` instead. (#8134, @mbobrovskyi)
- The short name "wl" for workloads has been removed to avoid potential conflicts with the in-tree workload object coming into Kubernetes.
  
  If you rely on "wl" in your "kubectl" command, you need to migrate to other short names ("kwl", "kueueworkload") or a full resource name ("workloads.kueue.x-k8s.io"). (#8472, @kannon92)
 
## Changes by Kind

### API Change

- Add field multiplyBy for ResourceTransformation (#7599, @calvin0327)
- Kueue v0.16 starts using `v1beta2` API version for storage. The new API brings an optimization for the internal representation of TopologyAssignment (in WorkloadStatus) which allows using TAS for larger workloads (under the assumptions described in issue #7220, it allows to increase the maximal workload size from approx. 20k to approx. 60k nodes).
  
  All new Kueue objects created after the upgrade will be stored using `v1beta2`. 
  
  However, existing objects are only auto-converted to the new storage version by Kubernetes during a write request. This means that Kueue API objects that rarely receive updates - such as Topologies, ResourceFlavors, or long-running Workloads - may remain in the older `v1beta1` format indefinitely.
  
  Ensuring all objects are migrated to `v1beta2` is essential for compatibility with future Kueue upgrades. We tentatively plan to discontinue support for `v1beta1` in version 0.18.
  
  To ensure your environment is consistent, we recommend running the following migration script after installing Kueue v0.16 and verifying cluster stability: https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/hack/migrate-to-v1beta2.sh. The script triggers a "no-op" update for all existing Kueue objects, forcing the API server to pass them through conversion webhooks and save them in the `v1beta2` version.
  Migration instructions (including the official script): https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3729056171. (#8020, @mbobrovskyi)
- MultiKueue: Allow up to 20 clusters per MultiKueueConfig. (#8614, @IrvingMg)

### Feature

- CLI: Support "kwl" and "kueueworkload" as a shortname for Kueue Workloads. (#8379, @kannon92)
- ElasticJobs: Support RayJob InTreeAutoscaling by using the ElasticJobsViaWorkloadSlices feature. (#8082, @hiboyang)
- Enable Pod-based integrations by default (#8096, @sohankunkerkar)
- Logs now include `replica-role` field to identify Kueue instance roles (leader/follower/standalone). (#8107, @IrvingMg)
- MultiKueue: Add support for StatefulSet workloads (#8611, @IrvingMg)
- MultiKueue: ClusterQueues with both MultiKueue and ProvisioningRequest admission checks are marked as inactive with reason "MultiKueueWithProvisioningRequest", as this configuration is invalid on manager clusters. (#8451, @IrvingMg)
- MultiKueue: trigger workload eviction on the management cluster when the corresponding workload is evicted
  on the remote worker cluster. In particular this is fixing the issue with workloads using ProvisioningRequests, 
  which could get stuck in a worker cluster which does not have enough capacity to ever admit the workloads. (#8477, @mszadkow)
- Observability: Add more details (the preemptionMode) to the QuotaReserved condition message,
  and the related event, about the skipped flavors which were considered for preemption. 
  Before: "Quota reserved in ClusterQueue preempt-attempts-cq, wait time since queued was 9223372037s; Flavors considered: main: on-demand(Preempt;insufficient unused quota for cpu in flavor on-demand, 1 more needed)"
  After: "Quota reserved in ClusterQueue preempt-attempts-cq, wait time since queued was 9223372037s; Flavors considered: main: on-demand(preemptionMode=Preempt;insufficient unused quota for cpu in flavor on-demand, 1 more needed)" (#8024, @mykysha)
- Observability: Introduce the counter metrics for finished workloads: kueue_finished_workloads_total and kueue_local_queue_finished_workloads_total. (#8694, @mbobrovskyi)
- Observability: Introduce the gauge metrics for finished workloads: kueue_finished_workloads and kueue_local_queue_finished_workloads. (#8724, @mbobrovskyi)
- Security: Support customization (TLSMinVersion and CipherSuites) for TLS used by the Kueue's webhooks server,
  and the visibility server. (#8563, @kannon92)
- TAS: extend the information in condition messages and events about nodes excluded from calculating the
  assignment due to various recognized reasons like: taints, node affinity, node resource constraints. (#8043, @sohankunkerkar)
- WaitForPodsReady.recoveryTimeout now defaults to the value of waitForPodsReady.timeout when not specified. (#8493, @IrvingMg)

### Bug or Regression

- DRA: fix the race condition bug leading to undefined behavior due to concurrent operations
  on the Workload object, manifested by the "WARNING: DATA RACE" in test logs. (#8073, @mbobrovskyi)
- FailureRecovery: Fix Pod Termination Controller's MaxConcurrentReconciles (#8664, @gabesaba)
- Fix ClusterQueue deletion getting stuck when pending workloads are deleted after being assumed by the scheduler. (#8543, @sohankunkerkar)
- Fix EnsureWorkloadSlices to finish old slice when new is admitted as replacement (#8456, @sohankunkerkar)
- Fix `TrainJob` controller not correctly setting the `PodSet` count value based on `numNodes` for the expected number of training nodes. (#8135, @kaisoz)
- Fix a bug that WorkloadPriorityClass value changes do not trigger Workload priority updates. (#8442, @ASverdlov)
- Fix a performance bug as some "read-only" functions would be taking unnecessary "write" lock. (#8181, @ErikJiang)
- Fix the race condition bug where the kueue_pending_workloads metric may not be updated to 0 after the last 
  workload is admitted and there are no new workloads incoming. (#8037, @Singularity23x0)
- Fixed a bug that Kueue's scheduler would re-evaluate and update already finished workloads, significantly
  impacting overall scheduling throughput. This re-evaluation of a finished workload would be triggered when:
  1. Kueue is restarted
  2. There is any event related to LimitRange or RuntimeClass instances referenced by the workload (#8186, @mbobrovskyi)
- Fixed a bug where workloads requesting zero quantity of a resource not defined in the ClusterQueue were incorrectly rejected. (#8241, @IrvingMg)
- Fixed the following bugs for the StatefulSet integration by ensuring the Workload object
  has the ownerReference to the StatefulSet:
  1. Kueue doesn't keep the StatefulSet as deactivated
  2. Kueue marks the Workload as Finished if all StatefulSet's Pods are deleted
  3. changing the "queue-name" label could occasionally result in the StatefulSet getting stuck (#4799, @mbobrovskyi)
- HC: Avoid redundant requeuing of inadmissible workloads when multiple ClusterQueues in the same cohort hierarchy are processed. (#8441, @sohankunkerkar)
- Integrations based on Pods: skip using finalizers on the Pods created and managed by integrations. 
  
  In particular we skip setting finalizers for Pods managed by the built in Serving Workloads  Deployments,
  StatefulSets, and LeaderWorkerSets.
  
  This improves performance of suspending the workloads, and fixes occasional race conditions when a StatefulSet
  could get stuck when deactivating and re-activating in a short interval. (#8530, @mbobrovskyi)
- JobFramework: Fixed a bug that allowed a deactivated workload to be activated. (#8424, @chengjoey)
- Kubeflow TrainJob v2: fix the bug to prevent duplicate pod template overrides when starting the Job is retried. (#8269, @j-skiba)
- LeaderWorkerSet: Fixed a bug that prevented deleting the workload when the LeaderWorkerSet was scaled down. (#8671, @mbobrovskyi)
- LeaderWorkerSet: add missing RBAC configuration for editor and viewer roles to kustomize and helm. (#8513, @kannon92)
- MultiKueue now waits for WorkloadAdmitted (instead of QuotaReserved) before deleting workloads from non-selected worker clusters. To revert to the previous behavior, disable the `MultiKueueWaitForWorkloadAdmitted` feature gate. (#8592, @IrvingMg)
- MultiKueue via ClusterProfile: Fix the panic if the configuration for ClusterProfiles wasn't provided in the configMap. (#8071, @mszadkow)
- MultiKueue: Fix a bug that the priority change by mutating the `kueue.x-k8s.io/priority-class` label on the management cluster is not propagated to the worker clusters. (#8464, @mbobrovskyi)
- MultiKueue: Fixed status sync for CRD-based jobs (JobSet, Kubeflow, Ray, etc.) that was blocked while the local job was suspended. (#8308, @IrvingMg)
- MultiKueue: fix the bug that for Pod integration the AdmissionCheck status would be kept Pending indefinitely,
  even when the Pods are already running.
  
  The analogous fix is also done for the batch/Job when the MultiKueueBatchJobWithManagedBy feature gate  is disabled. (#8189, @IrvingMg)
- MultiKueue: fix the eviction when initiated by the manager cluster (due to eg. Preemption or WaitForPodsReady timeout). (#8151, @mbobrovskyi)
- Observability: Revert the changes in PR https://github.com/kubernetes-sigs/kueue/pull/8599 for transitioning
  the QuotaReserved, Admitted conditions to `False` for Finished workloads. This introduced a regression,
  because users lost the useful information about the timestamp of the last transitioning of these
  conditions to True, without an API replacement to serve the information. (#8599, @mbobrovskyi)
- ProvisioningRequest: Fixed a bug that prevented events from being updated when the AdmissionCheck state changed. (#8394, @mbobrovskyi)
- Scheduling: fix a bug that evictions submitted by scheduler (preemptions and eviction due to TAS NodeHotSwap failing)
  could result in conflict in case of concurrent workload modification by another controller.
  This could lead to indefinite failing requests sent by scheduler in some scenarios when eviction is initiated by
  TAS NodeHotSwap. (#7933, @mbobrovskyi)
- Scheduling: fix the bug that setting (none -> some) a workload priority class label (kueue.x-k8s.io/priority-class) was ignored. (#8480, @andrewseif)
- TAS NodeHotSwap: fixed the bug that allows workload to requeue by scheduler even if already deleted on TAS NodeHotSwap eviction. (#8278, @mbobrovskyi)
- TAS: Fix a bug that MPIJob with runLauncherAsWorker Pod indexes are not correctly evaluated during rank-based ordering assignments. (#8618, @tenzen-y)
- TAS: Fix handling of admission for workloads using the LeastFreeCapacity algorithm when the  "unconstrained"
  mode is used. In that case scheduling would fail if there is at least one node in the cluster which does not have
  enough capacity to accommodate at least one Pod. (#8168, @PBundyra)
- TAS: Fixed an issue where workloads could remain in the second-pass scheduling queue (used for integration
  or TAS with ProvisioningRequests, and for TAS Node Hot Swap) even if they no longer require to be in the queue. (#8431, @skools-here)
- TAS: Fixed handling of the scenario where a Topology instance is re-created (for example, to add a new Topology level).
  Previously, this would cause cache corruption, leading to issues such as:
  1. Scheduling a workload on nodes that are fully occupied by already running workloads.
  2. Scheduling two or more pods of the same workload on the same node (even when the node cannot host both). (#8755, @mimowo)
- TAS: Lower verbosity of expected missing pod index label logs. (#8689, @IrvingMg)
- TAS: fix TAS resource flavor controller to extract only scheduling-relevant node updates to prevent unnecessary reconciliation. (#8452, @Ladicle)
- TAS: fix a performance bug that continues reconciles of TAS ResourceFlavor (and related ClusterQueues) 
  were triggered by updates to Nodes' heartbeat times. (#8342, @PBundyra)
- TAS: fix bug that when TopologyAwareScheduling is disabled, but there is a ResourceFlavor configured with topologyName, then preemptions fail with "workload requires Topology, but there is no TAS cache information". (#8167, @zhifei92)
- TAS: fixed performance issue due to unnecessary (empty) request by TopologyUngater (#8279, @mbobrovskyi)
- TAS: significantly improves scheduling performance by replacing Pod listing with an event-driven
  cache for non-TAS Pods, thereby avoiding expensive DeepCopy operations during each scheduling cycle. (#8484, @gabesaba)

### Other (Cleanup or Flake)

- Fix: Removed outdated comments incorrectly stating that deployment, statefulset, and leaderworkerset integrations require pod integration to be enabled. (#8053, @IrvingMg)
- Improve error messages for validation errors regarding WorkloadPriorityClass changes in workloads. (#8334, @olekzabl)
- MultiKueue: improve the MultiKueueCluster reconciler to skip attempting to reconcile and throw errors
  when the corresponding Secret or ClusterProfile objects don't exist. The reconcile will be triggered on 
  creation of the objects. (#8144, @mszadkow)
- Removes ConfigurableResourceTransformations feature gate. (#8133, @mbobrovskyi)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T08:04:30Z

Referencing the tentative plan: https://github.com/kubernetes-sigs/kueue/issues/8019

The tentative release date is Jan 19th, but it may slip up to two weeks if we decide to wait for some important work nearing completion.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T16:34:49Z

The tentative release date is 22nd Jan

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T14:02:25Z

Folks, as we are approaching v0.16.0 I have prepared the RC0: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.16.0-rc.0

Please give it a round of testing

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-22T14:49:47Z

@mimowo Are we planning to push the release date to next week?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T14:59:52Z

Yes, we are moving the release date for Monday.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-23T03:37:46Z

We probably should update the release notes for v1beta1 deprecation. Based on our discussions in the storage version  issue.

V1beta2: Use v1beta2 as storage version in v0.16
  
 https://github.com/kubernetes-sigs/kueue/issues/8018. (#8020, @mbobrovskyi)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-23T05:33:38Z

> We probably should update the release notes for v1beta1 deprecation. Based on our discussions in the storage version issue.
> 
> V1beta2: Use v1beta2 as storage version in v0.16
> 
> [#8018](https://github.com/kubernetes-sigs/kueue/issues/8018). ([#8020](https://github.com/kubernetes-sigs/kueue/pull/8020), [@mbobrovskyi](https://github.com/mbobrovskyi))

Thank you! Fixed.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-26T12:52:18Z

release lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-26T13:02:53Z

LGTM Releae note

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-26T15:13:13Z


```
.$ ./hack/releasing/wait_for_images.sh -p v0.16.0
Images:

  Checking if "registry.k8s.io/kueue/kueue:v0.16.0" is available.
    ✅ Image "registry.k8s.io/kueue/kueue@sha256:0ecf82777ab2b121dd0f14a63c5547cea7e370378694f41eaffeff81c8800337" is available.
    sha256:0ecf82777ab2b121dd0f14a63c5547cea7e370378694f41eaffeff81c8800337

  Checking if "registry.k8s.io/kueue/kueueviz-backend:v0.16.0" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-backend@sha256:89ea33b386850b9fc2c543743b8ae878c970e5fe38d13f822d9927b73dd76bf4" is available.
    sha256:89ea33b386850b9fc2c543743b8ae878c970e5fe38d13f822d9927b73dd76bf4

  Checking if "registry.k8s.io/kueue/kueueviz-frontend:v0.16.0" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-frontend@sha256:ef4c13f6a63d9f1b5d4845b879f3d832d8f90a77de0ff4db55a44a38ea456a2e" is available.
    sha256:ef4c13f6a63d9f1b5d4845b879f3d832d8f90a77de0ff4db55a44a38ea456a2e

  Checking if "registry.k8s.io/kueue/kueue-populator:v0.16.0" is available.
    ✅ Image "registry.k8s.io/kueue/kueue-populator@sha256:58df9df8512e21e6891f09b0010aa713e84b7087fd1bb89bc226ced9dddad79b" is available.
    sha256:58df9df8512e21e6891f09b0010aa713e84b7087fd1bb89bc226ced9dddad79b

Charts:

  Checking if "registry.k8s.io/kueue/charts/kueue:0.16.0" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue@sha256:5026ff4ef7335e0341f88b709951d2adb9a53db28684baefb1577f481d7fff3f" is available.
    sha256:5026ff4ef7335e0341f88b709951d2adb9a53db28684baefb1577f481d7fff3f

  Checking if "registry.k8s.io/kueue/charts/kueue-populator:0.16.0" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue-populator@sha256:c2a20e63549f6e0a2b65ea9fea2ac100068fa0d0aed41d2690253b117c018263" is available.
    sha256:c2a20e63549f6e0a2b65ea9fea2ac100068fa0d0aed41d2690253b117c018263
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T16:07:45Z

Highlights:
* **API Version Graduation** :up:  The v1beta2 API is now used for CRD serving and storage. While v1beta1 remains supported for now, we plan to discontinue it in version 0.18. The migration script is provided to help you smoothly transition existing objects. This is a major milestone towards v1!
* **Topology-Aware Scheduling (TAS)** :jigsaw: with the optimized representation of Workloads in v1beta2 for Topology-Aware Scheduling supports workloads spanning up to 60k nodes.
* **MultiKueue**  :globe_with_meridians: now supports StatefulSets. We also improved the support for preemptions and autoscaling via ProvisioningRequests.
* **Serving Workload Integrations**:electric_plug: based on StatefulSet and LeaderWorkerSet are now enabled by default. The Pod integration is also now enabled by default.
* **Enhanced Observability** :hammer_and_wrench: TAS event messages we now include information about nodes excluded from scheduling. Additionally, logs and metrics with the replica-role (leader / follower).

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-26T16:09:02Z

> Highlights:

Thank you, @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-26T16:59:08Z

After this has been finalized, we should add the following PRs to the v0.17 milestone with `/milestone v0.17`:
- https://github.com/kubernetes-sigs/kueue/pull/8789

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T17:16:57Z

Just Created the 0.17 milestone in kueue, and tagged the PR. We also have the pending PR for the automation in test-infra: https://github.com/kubernetes/test-infra/pull/36309

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-27T04:06:52Z

> Just Created the 0.17 milestone in kueue, and tagged the PR. We also have the pending PR for the automation in test-infra: https://github.com/kubernetes/test-infra/pull/36309

Thank you, I think that all tasks has been completed.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-27T04:06:58Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8462#issuecomment-3802979939):

>> Just Created the 0.17 milestone in kueue, and tagged the PR. We also have the pending PR for the automation in test-infra: https://github.com/kubernetes/test-infra/pull/36309
>
>Thank you, I think that all tasks has been completed.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
