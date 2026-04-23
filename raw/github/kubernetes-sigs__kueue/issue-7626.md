# Issue #7626: Release v0.15.0

**Summary**: Release v0.15.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7626

**Last updated**: 2025-11-28T13:15:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-13T06:49:21Z
- **Updated**: 2025-11-28T13:15:04Z
- **Closed**: 2025-11-28T13:14:53Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 14

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
  - [x] Submit a pull request with the changes: #7987 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8814/
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7988
  - [ ] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/35981
  - [x] Create the presubmits and the periodic jobs for the next patch release: kubernetes/test-infra#35982
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [x] Drop CI Jobs for testing the out-of-support branch: kubernetes/test-infra#35982
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.14.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- MultiKueue: validate remote client kubeconfigs and reject insecure kubeconfigs by default; add feature gate MultiKueueAllowInsecureKubeconfigs to temporarily allow insecure kubeconfigs until v0.17.0.
  
  if you are using MultiKueue kubeconfigs which are not passing the new validation please
  enable the `MultiKueueAllowInsecureKubeconfigs` feature gate and let us know so that we can re-consider
  the deprecation plans for the feature gate. (#7439, @mszadkow)
 - The .status.flavors in LocalQueue is deprecated, which will be removed in the future release.
  
  You can consider migrating from the field usage to VisibilityOnDemand. (#7337, @iomarsayed)
 - Update DRA API used from `v1beta2` to `v1`
  
  in order to use DRA integration by enabling the DynamicResourceAllocation feature gate in Kueue you need to use k8s 1.34+. (#7212, @harche)
 - V1beta2: Expose the v1beta2 API for CRD serving. 
  
  V1beta1 remains supported in this release and used as storage, but please plan for migration.
  
  We would highly recommend preparing the Kueue CustomResources API version upgrade (v1beta1 -> v1beta2)
  since we plan to use v1beta2 for storage in 0.16, and discontinue the support for v1beta1 in 0.17. (#7304, @mimowo)
 
## Changes by Kind

### API Change

- Removed the deprecated workload annotation key "kueue.x-k8s.io/queue-name".
  
  Please ensure you are using the workload label "kueue.x-k8s.io/queue-name" instead. (#7271, @ganczak-commits)
- V1beta2: Delete .enable field from FairSharing API in config (#7583, @mbobrovskyi)
- V1beta2: Delete .enable field from WaitForPodsReady API in config (#7628, @mbobrovskyi)
- V1beta2: FlavorFungibility: introduce `MayStopSearch` in place of `Borrow`/`Preempt`, which are now deprecated in v1beta1. (#7117, @ganczak-commits)
- V1beta2: Graduate Config API to v1beta2. v1beta1 remains supported for this release, but please plan for migration. (#7375, @mbobrovskyi)
- V1beta2: Make .waitForPodsReady.timeout required field in the Config API (#7952, @tenzen-y)
- V1beta2: Make fairSharing.premptionStrategies required field in Config API (#7948, @tenzen-y)
- V1beta2: Remove deprecated PodIntegrationOptions (podOptions field) from v1beta2 Configuration.
  
   If you are using the podOptions in the configMap, you need to migrate to using  managedJobsNamespaceSelector (https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/) before
  the upgrade. (#7406, @nerdeveloper)
- V1beta2: Remove deprecated QueueVisibility in configMap (it was already non-functional). (#7319, @bobsongplus)
- V1beta2: Remove deprecated retryDelayMinutes field from v1beta2 AdmissionCheckSpec (it was already non-functional). (#7407, @nerdeveloper)
- V1beta2: Remove never used .status.fairSharing.admissionFairSharing field from ClusterQueue and Cohort (#7793, @tenzen-y)
- V1beta2: Removed deprecated Preempt/Borrow from FlavorFungibility API (#7527, @mbobrovskyi)
- V1beta2: The internal representation of TopologyAssignment (in WorkloadStatus) has been reorganized to allow using TAS for larger workloads. (More specifically, under the assumptions described in issue #7220, it allows to increase the maximal workload size from approx. 20k to approx. 60k nodes). (#7544, @olekzabl)
- V1beta2: change default for waitForPodsReady.blockAdmission to false (#7687, @mbobrovskyi)
- V1beta2: drop deprecated Flavors field from LocalQueueStatus (#7449, @mbobrovskyi)
- V1beta2: graduate the visibility API (#7411, @mbobrovskyi)
- V1beta2: introduce PriorityClassRef instead of PriorityClassSource and PriorityClassName (#7540, @mbobrovskyi)
- V1beta2: remove deprecated .spec.admissionChecks field from ClusterQueue API in favor of .spec.admissionChecksStrategy. (#7490, @nerdeveloper)
- `ReclaimablePods` feature gate is introduced to enable users switching on and off the reclaimable Pods feature (#7525, @PBundyra)

### Feature

- AdmissionChecks: introduce new optional fields in the workload status for admission checks to control the delay by 
  external and internal admission check controllers:
  - requeueAfterSeconds: specifies minimum wait time before retry
  - retryCount: Tracks retry attempts per admission check (#7620, @sohankunkerkar)
- AdmissionFairSharing: promote the feature to beta (enabled by default). (#7463, @kannon92)
- FailureRecovery: Introduce a mechanism to terminate Pods "stuck" in a terminating state due to node failures.
  The feature is activated by enabling the alpha FailureRecoveryPolicy feature gate (disabled by default).
  Only Pods with the kueue.x-k8s.io/safe-to-forcefully-terminate annotation are handled by the mechanism. (#7312, @kshalot)
- FlavorFungability: introduce the ClusterQueue's API for flavorFungability: `.spec.flavorFungability.preference` to indicate
  the user's preference for borrowing or preemption when there is no flavor which avoids both.
  This new field is a replacement for the alpha feature gate FlavorFungibilityImplicitPreferenceDefault which is considered as deprecated in 0.15 and will be removed in 0.16. (#7316, @vladikkuzn)
- Integrations: the Pod integration is no longer required to be enabled explicitly in the configMap when you are using LeaderWorkerSet, StatefulSet, or Deployment frameworks. (#6736, @IrvingMg)
- JobFramework: Introduce an optional interface for custom Jobs, called JobWithCustomWorkloadActivation, which can be used to deactivate or active a custom CRD workload. (#7199, @tg123)
- KueuePopulator: release of the new experimental sub-project called "kueue-populator". It allows to create the default ClusterQueue, ResourceFlavor and Topology. It also creates default LocalQueues in all namespaces managed by Kueue. (#7940, @mbobrovskyi)
- MultiKueue: Graduate the support for running external jobs to Beta. (#7669, @khrm)
- MultiKueue: It supports Topology Aware Scheduling (TAS) and ProvisioningRequest integration. (#5361, @IrvingMg)
- MultiKueue: Promote MultiKueueBatchJobWithManagedBy to beta which allows to synchronize the Job status periodically during Job execution between the worker and the management cluster for k8s batch Jobs. (#7341, @kannon92)
- MultiKueue: Support for authentication to worker clusters using ClusterProfile API. (#7570, @hdp617)
- Observability: Adjust the `cluster_queue_weighted_share` and `cohort_weighted_share` metrics to report the precise value for the Weighted share, rather than the value rounded to an integer. Also, expand the `cluster_queue_weighted_share` metric with the "cohort" label. (#7338, @j-skiba)
- Observability: Improve the messages presented to the user in scheduling events, by clarifying the reason for "insufficient quota" in case of workloads with multiple PodSets. 
  Before: "insufficient quota for resource-type in flavor example-flavor, request > maximum capacity (24 > 16)"
  After: "insufficient quota for resource-type in flavor example-flavor, previously considered podsets requests (16) + current podset request (8) > maximum capacity (16)" (#7232, @iomarsayed)
- Observability: Summarize the list of flavors considered for admission in the release cycle, but not used eventually for a workload which reserved the quota. 
  The summary is present in the message for the QuotaReserved condition, and in the event.
  Before: "Quota reserved in ClusterQueue tas-main, wait time since queued was 9223372037s"
  After: "Quota reserved in ClusterQueue tas-main, wait time since queued was 9223372037s; Flavors considered: one: default(NoFit;Flavor \"default\" does not support TopologyAwareScheduling)" (#7646, @mykysha)
- Observability: improve the message for the Preempted condition: include preemptor and preemptee object paths to make it easier to locate the objects involved in a preemption.
  Before: "Preempted to accommodate a workload (UID: wl-in, JobUID: job-in) due to reclamation within the cohort"
  After: "Preempted to accommodate a workload (UID: wl-in, JobUID: job-in) due to reclamation within the cohort; preemptor path: /r/c/q; preemptee path: /r/q_borrowing" (#7522, @mszadkow)
- Promote ManagedJobsNamespaceSelectorAlwaysRespected feature to Beta (#7493, @PannagaRao)
- Scheduling: support mutating the "kueue.x-k8s.io/workloadpriorityclass" label for Jobs with reserved quota. (#7289, @mbobrovskyi)
- TAS: It supports the Kubeflow TrainJob (#7249, @kaisoz)
- TAS: The balanced placement is introduced with the TASBalancedPlacement feature gate. (#6851, @pajakd)
- TAS: change the algorithm used in case of "unconstrained" mode (enabled by the kueue.x-k8s.io/podset-unconstrained-topology annotation, or when the "implicit" mode s used) from "BestFit" to "LeastFreeCapacity". 
  
  This allows to optimize the fragmentation for workloads which don't require bin-packing. (#7416, @iomarsayed)
- Transition QuotaReserved to false whenever setting Finished conditions (#7724, @mbobrovskyi)

### Documentation

- V1beta2: Adjust the documentation examples to use v1beta2 consistently. (#7910, @mszadkow)

### Bug or Regression

- AdmissionFairSharing: Fix the bug that occasionally a workload may get admitted from a busy LocalQueue,
  bypassing the entry penalties. (#7780, @IrvingMg)
- Fix a bug that an error during workload preemption could leave the scheduler stuck without retrying. (#7665, @olekzabl)
- Fix a bug that the cohort client-go lib is for a Namespaced resource, even though the cohort is a Cluster-scoped resource. (#7799, @tenzen-y)
- Fix a bug where a workload would not get requeued after eviction due to failed hotswap. (#7376, @pajakd)
- Fix eviction of jobs with memory requests in decimal format (#7430, @brejman)
- Fix existing workloads not being re-evaluated when new clusters are added to MultiKueueConfig. Previously, only newly created workloads would see updated cluster lists. (#6732, @ravisantoshgudimetla)
- Fix handling of RayJobs which specify the spec.clusterSelector and the "queue-name" label for Kueue. These jobs should be ignored by kueue as they are being submitted to a RayCluster which is where the resources are being used and was likely already admitted by kueue. No need to double admit.
  Fix on a panic on kueue managed jobs if spec.rayClusterSpec wasn't specified. (#7218, @laurafitzgerald)
- Fix integration of `manageJobWithoutQueueName` and `managedJobsNamespaceSelector` with JobSet by ensuring that jobSets without a queue are  not managed by Kueue if are not selected by the  `managedJobsNamespaceSelector`. (#7703, @MaysaMacedo)
- Fix invalid annotations path being reported in `JobSet` topology validations. (#7189, @kshalot)
- Fix issue #6711 where an inactive workload could transiently get admitted into a queue. (#7913, @olekzabl)
- Fix malformed annotations paths being reported for `RayJob` and `RayCluster` head group specs. (#7183, @kshalot)
- Fix the bug for the StatefulSet integration that the scale up could get stuck if
  triggered immediately after scale down to zero. (#7479, @IrvingMg)
- Fix the bug that a workload which was deactivated by setting the `spec.active=false` would not have the 
  `wl.Status.RequeueState` cleared. (#7734, @sohankunkerkar)
- Fix the bug that the kubernetes.io/job-name label was not propagated from the k8s Job to the PodTemplate in
  the Workload object, and later to the pod template in the ProvisioningRequest. 
  
  As a consequence the ClusterAutoscaler could not properly resolve pod affinities referring to that label,
  via podAffinity.requiredDuringSchedulingIgnoredDuringExecution.labelSelector. For example, 
  such pod affinities can be used to request ClusterAutoscaler to provision a single node which is large enough
  to accommodate all Pods on a single Node.
  
  We also introduce the PropagateBatchJobLabelsToWorkload feature gate to disable the new behavior in case of 
  complications. (#7613, @yaroslava-serdiuk)
- Fix the kueue-controller-manager startup failures.
  
  This fixed the Kueue CrashLoopBackOff due to the log message: "Unable to setup indexes","error":"could not setup multikueue indexer: setting index on workloads admission checks: indexer conflict. (#7432, @IrvingMg)
- Fix the race condition which could result that the Kueue scheduler occasionally does not record the reason
  for admission failure of a workload if the workload was modified in the meanwhile by another controller. (#7845, @mbobrovskyi)
- Fixed a bug that Kueue would keep sending empty updates to a Workload, along with sending the "UpdatedWorkload" event, even if the Workload didn't change. This would happen for Workloads using any other mechanism for setting
  the priority than the WorkloadPriorityClass, eg. for Workloads for PodGroups. (#7299, @mbobrovskyi)
- Fixed the bug that prevented managing workloads with duplicated environment variable names in containers. This issue manifested when creating the Workload via the API. (#7425, @mbobrovskyi)
- Kueue now properly validates and rejects unsupported DRA (Dynamic Resource Allocation) features with clear error messages instead of silently failing or producing misleading "DeviceClass not mapped" errors. Unsupported features include: AllocationMode 'All', CEL Selectors, Device Constraints, Device Config, FirstAvailable device selection, and AdminAccess. (#7226, @harche)
- MultiKueue x ElasticJobs: fix webhook validation bug which prevented scale up operation when any other
  than the default "AllAtOnce" MultiKueue dispatcher was used. (#7278, @mszadkow)
- MultiKueue: Remove remoteClient from clusterReconciler when kubeconfig is detected as invalid or insecure, preventing workloads from being admitted to misconfigured clusters. (#7486, @mszadkow)
- RBAC: Add rbac for train job for kueue-batch-admin and kueue-batch-user. (#7196, @kannon92)
- Scheduling: With BestEffortFIFO enabled, we will keep attempting to schedule a workload as long as
  it is waiting for preemption targets to complete. This fixes a bugs where an inadmissible
  workload went back to head of queue, in front of the preempting workload, allowing
  preempted workloads to reschedule (#7157, @gabesaba)
- Services: fix the setting of the `app.kubernetes.io/component` label to discriminate between different service components within Kueue as follows:
  - controller-manager-metrics-service for kueue-controller-manager-metrics-service 
  - visibility-service for kueue-visibility-server
  - webhook-service for kueue-webhook-service (#7371, @rphillips)
- TAS: Fix the `requiredDuringSchedulingIgnoredDuringExecution` node affinity setting being ignored in topology-aware scheduling. (#7899, @kshalot)
- TAS: Increase the number of Topology levels limitations for localqueue and workloads to 16 (#7423, @kannon92)
- TAS: Introduce missing validation against using incompatible `PodSet` grouping configuration in `JobSet, `MPIJob`, `LeaderWorkerSet`, `RayJob` and `RayCluster`. 
  
  Now, only groups of two `PodSet`s can be defined and one of the grouped `PodSet`s has to have only a single `Pod`.
  The `PodSet`s within a group must specify the same topology request via one of the `kueue.x-k8s.io/podset-required-topology` and `kueue.x-k8s.io/podset-preferred-topology` annotations. (#7061, @kshalot)
- Visibility API: Fix a bug that the Config clientConnection is not respected in the visibility server. (#7223, @tenzen-y)
- WorkloadRequestUseMergePatch: use "strict" mode for admission patches during scheduling which
  sends the ResourceVersion of the workload being admitted for comparing by kube-apiserver. 
  This fixes the race-condition issue that Workload conditions added concurrently by other controllers
  could be removed during scheduling. (#7246, @mszadkow)

### Other (Cleanup or Flake)

- RBAC: Restrict access to secrets for the Kueue controller manager only to secrets in the Kueue system namespace, ie
  kueue-system by default, or the one specified during installation with Helm. (#7188, @sbgla-sas)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T07:08:50Z

As we are approaching the 0.15 release (planned for 17Nov, but possible 2weeks delay) I prepared the release candidate: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0-rc.0, with the tentative plan for the release: https://github.com/kubernetes-sigs/kueue/issues/7245

Please give it a special round of testing given we introduce v1beta2. Still, we support v1beta1, so no immediate changes should be needed. 

cc @tenzen-y @gabesaba @mwysokin @kannon92 @amy

### Comment by [@khrm](https://github.com/khrm) — 2025-11-14T14:53:12Z

Can we include #7669 as discussed in previous issue? We have done testing for this internally. We can't deploy this to production without it being beta or push it to customer.

It's being used for Distributed CI/CD system using Tekton.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-14T14:58:56Z

> Can we include [#7669](https://github.com/kubernetes-sigs/kueue/pull/7669) as discussed in previous issue? We have done testing for this internally. We can't deploy this to production without it being beta or push it to customer.
> 
> It's being used for Distributed CI/CD system using Tekton.

I'll review this PR but I don't see a reason why this can't be included.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T11:53:21Z

I have synced with @tenzen-y and the new tentative date is 25th November so that we can try to complete the ongoing work, see summary in https://github.com/kubernetes-sigs/kueue/issues/7245#issuecomment-3534085489

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T17:28:23Z

Folks, we have https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0-rc.1 which most notably is fixing the upgrade with https://github.com/kubernetes-sigs/kueue/pull/7772. 

Please give it another round of testing.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T08:28:59Z

We have RC2 https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0-rc.2, most importantly with the bugfix for MultiKueue via ClusterProfiles: https://github.com/kubernetes-sigs/kueue/pull/7863

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T15:33:56Z

We have RC3: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0-rc.3, most importanly it contains the new experimental component: kueue-populator. @j-skiba @mbobrovskyi please check if  the published artifacts look good

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-27T15:44:16Z

```
➜  kueue git:(cleanup/add-kueue-populator-on-releasing) helm install kueue-populator oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue-populator \
  --version 0.15.0-rc.3 \             
  --namespace kueue-system \
  --set kueue.enabled=true \
  --create-namespace \
  --wait
Pulled: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue-populator:0.15.0-rc.3
Digest: sha256:3633725393300a06999ea8ba04f5377c527580811872c149d73fd61abcbd9fcf
W1127 21:12:26.898559   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.898606   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.898565   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.898568   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.898599   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.899750   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.899761   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.901105   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.904219   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.904233   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:27.038874   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:27.038892   23316 warnings.go:70] unrecognized format "int64"
NAME: kueue-populator
LAST DEPLOYED: Thu Nov 27 21:12:25 2025
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
```

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-11-27T16:21:09Z

I confirm, it works.

Scenario with more settings:

```bash
jakubskiba@jakubskiba:~/kueue$ cat topology.yaml 
# populator-config.yaml
kueue:
  enabled: true
kueuePopulator:
  config:
    topology:
      levels:
        - nodeLabel: cloud.google.com/gke-nodepool
    resourceFlavor:
      nodeLabels:
        cloud.google.com/gke-nodepool: "default-pool"
jakubskiba@jakubskiba:~/kueue$ helm install kueue-populator oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue-populator \
  --version 0.15.0-rc.3 \
  --namespace kueue-system \
  --create-namespace \
  --wait \
  -f topology.yaml 
Pulled: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue-populator:0.15.0-rc.3
Digest: sha256:3633725393300a06999ea8ba04f5377c527580811872c149d73fd61abcbd9fcf
I1127 16:16:39.905660 1057055 warnings.go:110] "Warning: unrecognized format \"int32\""
I1127 16:16:39.908820 1057055 warnings.go:110] "Warning: unrecognized format \"int32\""
I1127 16:16:39.914105 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
I1127 16:16:39.918014 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
I1127 16:16:39.918689 1057055 warnings.go:110] "Warning: unrecognized format \"int32\""
I1127 16:16:39.918725 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
I1127 16:16:39.918858 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
I1127 16:16:39.919652 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
I1127 16:16:39.927677 1057055 warnings.go:110] "Warning: unrecognized format \"int32\""
I1127 16:16:39.927698 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
I1127 16:16:40.118635 1057055 warnings.go:110] "Warning: unrecognized format \"int32\""
I1127 16:16:40.118663 1057055 warnings.go:110] "Warning: unrecognized format \"int64\""
NAME: kueue-populator
LAST DEPLOYED: Thu Nov 27 16:16:38 2025
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
jakubskiba@jakubskiba:~/kueue$ kubectl get pods -A
NAMESPACE            NAME                                                  READY   STATUS    RESTARTS   AGE
kube-system          coredns-66bc5c9577-psmw4                              1/1     Running   0          2m18s
kube-system          coredns-66bc5c9577-vjvfz                              1/1     Running   0          2m18s
kube-system          etcd-kind-control-plane                               1/1     Running   0          2m25s
kube-system          kindnet-5szf9                                         1/1     Running   0          2m19s
kube-system          kube-apiserver-kind-control-plane                     1/1     Running   0          2m25s
kube-system          kube-controller-manager-kind-control-plane            1/1     Running   0          2m25s
kube-system          kube-proxy-vzx6m                                      1/1     Running   0          2m19s
kube-system          kube-scheduler-kind-control-plane                     1/1     Running   0          2m25s
kueue-system         kueue-populator-controller-manager-58d54b5fcc-2wlq7   1/1     Running   0          46s
kueue-system         kueue-populator-kueue-populator-7444dfc6c9-6tw6v      1/1     Running   0          46s
local-path-storage   local-path-provisioner-7b8c8ddbd6-4qjd5               1/1     Running   0          2m18s
jakubskiba@jakubskiba:~/kueue$ kubectl get lq
NAME      CLUSTERQUEUE    PENDING WORKLOADS   ADMITTED WORKLOADS
default   cluster-queue   0                   0
jakubskiba@jakubskiba:~/kueue$ kubectl get cq
NAME            COHORT   PENDING WORKLOADS
cluster-queue            0
jakubskiba@jakubskiba:~/kueue$ kubectl get rf
NAME              AGE
tas-gpu-default   29s
jakubskiba@jakubskiba:~/kueue$ kubectl get topologies.kueue.x-k8s.io 
NAME      AGE
default   34s
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T02:26:14Z

LGTM, thank you!

@mbobrovskyi Just curious about the warnings.
Do you know what the following are?

```
Pulled: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue-populator:0.15.0-rc.3
Digest: sha256:3633725393300a06999ea8ba04f5377c527580811872c149d73fd61abcbd9fcf
W1127 21:12:26.898559   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.898606   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.898565   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.898568   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.898599   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.899750   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.899761   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.901105   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:26.904219   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:26.904233   23316 warnings.go:70] unrecognized format "int64"
W1127 21:12:27.038874   23316 warnings.go:70] unrecognized format "int32"
W1127 21:12:27.038892   23316 warnings.go:70] unrecognized format "int64"
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T05:34:27Z

I see the same warnings when installing Kueue with manifests or just running `make install`.

```shell
Warning: unrecognized format "int64"
customresourcedefinition.apiextensions.k8s.io/admissionchecks.kueue.x-k8s.io serverside-applied
Warning: unrecognized format "int32"
customresourcedefinition.apiextensions.k8s.io/clusterqueues.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/cohorts.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/localqueues.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/multikueueclusters.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/multikueueconfigs.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/provisioningrequestconfigs.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/resourceflavors.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/topologies.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/workloadpriorityclasses.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/workloads.kueue.x-k8s.io serverside-applied
```

Probably it should be fixed in the next release: https://github.com/kubernetes/kubernetes/issues/133880.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T06:19:06Z

> I see the same warnings when installing Kueue with manifests or just running `make install`.
> 
> Warning: unrecognized format "int64"
> customresourcedefinition.apiextensions.k8s.io/admissionchecks.kueue.x-k8s.io serverside-applied
> Warning: unrecognized format "int32"
> customresourcedefinition.apiextensions.k8s.io/clusterqueues.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/cohorts.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/localqueues.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/multikueueclusters.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/multikueueconfigs.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/provisioningrequestconfigs.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/resourceflavors.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/topologies.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/workloadpriorityclasses.kueue.x-k8s.io serverside-applied
> customresourcedefinition.apiextensions.k8s.io/workloads.kueue.x-k8s.io serverside-applied
> Probably it should be fixed in the next release: [kubernetes/kubernetes#133880](https://github.com/kubernetes/kubernetes/issues/133880).

I see. Thank you for investigating that 👍

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T09:34:32Z

Release note looks great to me, thank you!

LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T11:23:06Z

sanity checking the promoted artifacts:
```
❯ docker run -it registry.k8s.io/kueue/kueue:v0.15.0
Unable to find image 'registry.k8s.io/kueue/kueue:v0.15.0' locally
v0.15.0: Pulling from kueue/kueue
48e8ffce6d11: Pull complete 
Digest: sha256:15bf4478557991888ac31ce5f6207f236c2125e248ab207d237af3c70996353e
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.15.0
{"level":"info","ts":"2025-11-28T11:19:22.174328413Z","logger":"setup","caller":"kueue/main.go:533","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta2\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-11-28T11:19:22.174559532Z","logger":"setup","caller":"kueue/main.go:162","msg":"Initializing","gitVersion":"v0.15.0","gitCommit":"1929d83062dbc1b3c5ba52fe0ed9d1a8fdad7b91","buildDate":"2025-11-28T10:18:37Z"}
```
```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.15.0 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.15.0
Digest: sha256:c6e7067a6860cc7f0d95a3e37fd84dc4d77afe5430519f9437a5c5476e6bc874
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.15.0'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.15.0'
        image: "registry.k8s.io/kueue/kueue:v0.15.0"
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.15.0
v0.15.0: Pulling from kueue/kueueviz-backend
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
5664b15f108b: Already exists 
045fc1c20da8: Already exists 
4aa0ea1413d3: Already exists 
da7816fa955e: Already exists 
ddf74a63f7d8: Already exists 
776cb14ac130: Pull complete 
Digest: sha256:0aa8e3e65acfd89158e915d58aef86c47e9e6e238b00f4af4c5300faa3df292a
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.15.0
2025/11/28 11:20:48 Starting pprof server on localhost:6060
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.15.0
v0.15.0: Pulling from kueue/kueueviz-frontend
Digest: sha256:1b585c8e884783c2dc120432376fedc4059b1cea34502a1959023d1b23b31d99
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.15.0
```
```
❯ docker run -it registry.k8s.io/kueue/kueue-populator:v0.15.0
Unable to find image 'registry.k8s.io/kueue/kueue-populator:v0.15.0' locally
v0.15.0: Pulling from kueue/kueue-populator
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
5664b15f108b: Already exists 
045fc1c20da8: Already exists 
4aa0ea1413d3: Already exists 
da7816fa955e: Already exists 
ddf74a63f7d8: Already exists 
6bfb1d7b0c20: Pull complete 
Digest: sha256:d97e609a66a11e06fd17012efe18d6121ffde36e49d51f0679d6d95737d8f0d6
Status: Downloaded newer image for registry.k8s.io/kueue/kueue-populator:v0.15.0
```
```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue-populator --version 0.15.0 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue-populator:0.15.0
Digest: sha256:6534f3bc139fb0015a66aa8ec6575a971bb5082e671fd9ec2afa9258bf0bffe2
        image: "registry.k8s.io/kueue/kueue-populator:v0.15.0"
```
