# Issue #5265: Release v0.12.0

**Summary**: Release v0.12.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5265

**Last updated**: 2025-05-27T12:14:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-16T06:42:48Z
- **Updated**: 2025-05-27T12:14:30Z
- **Closed**: 2025-05-27T12:14:30Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 13

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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5356
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
      to production: https://github.com/kubernetes/k8s.io/pull/8134
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5367
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
        https://github.com/kubernetes/test-infra/pull/34857
  - [x] Create the presubmits and the periodic jobs for the next patch release:
        https://github.com/kubernetes/test-infra/pull/34858
  - [x] Drop CI Jobs for testing the out-of-support branch:
        https://github.com/kubernetes/test-infra/pull/34858


## Changelog

```markdown
Changes since `v0.11.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- Fix the bug which annotated the Topology CRD as v1beta1 (along with the v1alpha1 version). This resulted in errors when Kueue was installed via Helm, for example, to list the topologies.
  
  The LocalQueue type for the status.flavors[].topology is changed from Topology to TopologyInfo, so if you import Kueue as code in your controller, you may need to adjust the code. (#4866, @mbobrovskyi)
 - Removed `IsManagingObjectsOwner` field from the `IntegrationCallbacks` struct.
  
  If you have implemented the `IsManagingObjectsOwner` field, you will need to remove it manually from your codebase. (#5011, @mbobrovskyi)
 - The API Priority and Fairness configuration for the visibility endpoint is installed by default.
  
  If your cluster is using k8s 1.28 or older, you will need to either update your version of k8s (to 1.29+) or remove the  FlowSchema and PriorityLevelConfiguration from the installation manifests of Kueue. (#5043, @mbobrovskyi)
 
## Changes by Kind

### API Change

- Added optional garbage collector for deactivated workloads. (#5177, @mbobrovskyi)
- Support specifying PodSetUpdates based on ProvisioningClassDetails by the configuration in ProvisioningRequestConfig. (#5204, @mimowo)
- TAS: Support ProvisioningRequests. (#5052, @mimowo)

### Feature

- Add 'kueue.x-k8s.io/podset' label to every admitted Job resource (#5215, @mszadkow)
- Add readOnlyRootFilesystem as default option for kueue deployment. (#5059, @kannon92)
- Added the following optional metrics, when waitForPodsReady is enabled:
  kueue_ready_wait_time_seconds - The time between a workload was created or requeued until ready, per 'cluster_queue'
  kueue_admitted_until_ready_wait_time_seconds - The time between a workload was admitted until ready, per 'cluster_queue'
  kueue_local_queue_ready_wait_time_seconds - The time between a workload was created or requeued until ready, per 'local_queue'
  kueue_local_queue_admitted_until_ready_wait_time_seconds - The time between a workload was admitted until ready, per 'local_queue' (#5136, @mszadkow)
- Allow users to update the priority of a workload from within a job. (#5197, @IrvingMg)
- Cert-manager: allow for external self-signed certificates for the metrics endpoint. (#4800, @sohankunkerkar)
- Evicted_workloads_once_total - counts number of unique workload evictions. (#5259, @mszadkow)
- Helm: Add an option to configure Kueue's mutation webhook with "reinvocationPolicy" (#5063, @yuvalaz99)
- Introduce ObjectRetentionPolicies.FinishedWorkloadRetention flag, which allows to configure a retention policy for Workloads, Workloads will be deleted when their retention period elapses, by default this new behavior is disabled (#2686, @mwysokin)
- Introduce the ProvisioningRequestConfig API which allows to instruct Kueue to create a ProvisioningRequest with a single PodSet with aggregated resources from multiple PodSets in the Workload (eg. PyTorchJob) created by the user. (#5290, @mszadkow)
- Output events to indicate which Worker Cluster was admitted to the Manager Cluster's workload. (#4750, @highpon)
- Promoted LocalQueueDefaulting to Beta and enabled by default. (#5038, @MaysaMacedo)
- Support a new fair sharing alpha feature `Admission Fair Sharing`, along with the new API. It orders workloads based on the recent usage coming from a LocalQueue the workload was submitted to. The recent usage is more important than the priority of workloads (#4687, @PBundyra)
- Support for JAX in the training-operator (#4613, @vladikkuzn)
- TAS: This supports Node replacement for TAS Workloads with an annotation `nodeToReplace`. It updates Workload's TopologyAssignments without requeuing it (#5287, @PBundyra)
- Update AppWrapper to v1.1.1 (#4728, @dgrove-oss)

### Bug or Regression

- Add Necessary RBAC to Update Cohort Status (#4703, @gabesaba)
- Allow one to disable cohorts via a HiearachialCohort feature gate (#4870, @kannon92)
- Fix Kueue crash caused by race condition when deleting ClusterQueue (#5292, @gabesaba)
- Fix LocalQueue's status message to reference LocalQueue, rather than ClusterQueue, when its status is Ready (#4955, @PBundyra)
- Fix RBAC configuration for the Topology API (#5120, @qti-haeyoon)
- Fix RBAC configuration for the Topology API to allow reading and editing by the service accounts using the Kueue Batch Admin role. (#4858, @KPostOffice)
- Fix RayJob webhook validation when `LocalQueueDefaulting` feature is enabled. (#5073, @MaysaMacedo)
- Fix a bug where PropagateResourceRequests would always trigger an API status patch call. (#5110, @alexeldeib)
- Fix a bug which caused Kueue's Scheduler to build invalid SSA patch in some scenarios when  using
  admission checks. This patch would be rejected with the following error message: 
  Workload.kueue.x-k8s.io "job-xxxxxx" is invalid: [admissionChecks[0].lastTransitionTime: Required value (#4935, @alexeldeib)
- Fix bug where Cohorts with FairWeight set to 0 could have workloads running within Nominal Quota preempted (#4962, @gabesaba)
- Fix bug where update to Cohort.FairSharing didn't trigger a reconcile. This bug resulted in the new weight not being used until the Cohort was modified in another way. (#4963, @gabesaba)
- Fix bug which prevented using LeaderWorkerSet with manageJobsWithoutQueueName enabled. In particular, Kueue would create redundant workloads for each Pod, resulting in worker Pods suspended, while the leader Pods could bypass quota checks. (#4808, @mbobrovskyi)
- Fix bug which resulted in under-utilization of the resources in a Cohort.
  Now, when a ClusterQueue is configured with `preemption.reclaimWithinCohort: Any`,
  its resources can be lent out more freely, as we are certain that we can reclaim
  them later. Please see PR for detailed description of scenario. (#4813, @gabesaba)
- Fix classical preemption in the case of hierarchical cohorts. (#4806, @pajakd)
- Fix kueue-viz nil pointer error when defaulting kueue-viz backend/frontend images (#4727, @kannon92)
- Fix panic due to nil ptr exception in scheduler when ClusterQueue is deleted concurrently. (#5138, @sohankunkerkar)
- Fix the bug which prevented running Jobs (with queue-name label) owned by other Jobs for which Kueue does not 
  have the necessary RBAC permissions (for example kserve or CronJob). (#5252, @mimowo)
- Fix the support for pod groups in MutliKueue. (#4854, @mszadkow)
- Fixed a bug that caused Kueue to create redundant workloads for each Job when manageJobsWithoutQueueName was enabled, JobSet integration was disabled, and AppWrapper was used for JobSet. (#4824, @mbobrovskyi)
- Fixed a bug that prevented Kueue from retaining the LeaderWorkerSet workload in deactivation status.
  Fixed a bug that prevented Kueue from automatically deleting the workload when the LeaderWorkerSet was deleted. (#4790, @mbobrovskyi)
- Fixed bug that allow to create Topology without levels. (#5013, @mbobrovskyi)
- Fixed bug that doesn't allow to use WorkloadPriorityClass on LeaderWorkerSet. (#4711, @mbobrovskyi)
- Helm: Fix missing namespace selector on webhook manifest. ManagedJobsNamespaceSelector option was only applied to pods/deployment/statefulset, now it is applied to all kind of jobs.
  Kube-system and Kueue release namespaces are still not excluded automatically by default. (#5323, @mtparet)
- Helm: Fix the default configuration for the metrics service. (#4903, @kannon92)
- Helm: fix ServiceMonitor selecting the wrong service. This previously led to missing Kueue metrics, even with `enablePrometheus` set to `true`. (#5074, @j-vizcaino)
- PodSetTopologyRequests are now configured only when TopologyAwareScheduling feature gate is enabled. (#4742, @mykysha)
- TAS: Add support for Node Selectors. (#4989, @mwysokin)
- TAS: Fix bug where scheduling panics when the workload using TopologyAwareScheduling has container request value specified as zero. (#4971, @qti-haeyoon)
- TAS: Fix the bug where TAS workloads may be admitted after restart of the Kueue controller. (#5276, @mimowo)
- TAS: fix accounting of TAS usage for workloads with multiple PodSets. This bug could prevent admitting workloads which otherwise could fit. (#5325, @lchrzaszcz)
- TAS: fix issues with the initialization of TAS cache in case of errors in event handlers. (#5309, @mimowo)

### Other (Cleanup or Flake)

- ATTENTION: Many renaming changes to prepare KueueViz to be suitable for production:
  - KueueViz is now mentioned KueueViz for its name, label and description
  - Path names and image names are now kueueviz (without hyphen) for consistency and naming restrictions
  - Helm chart values `.Values.kueueViz` remains unchanged as all parameters in helm chart values starts with lower case. (#4753, @akram)
- New kueueviz logo from CNCF design team. (#5247, @akram)
- Remove deprecated AdmissionCheckValidationRules feature gate. (#4995, @mszadkow)
- Remove deprecated InactiveWorkload condition reason. (#5050, @mbobrovskyi)
- Remove deprecated KeepQuotaForProvReqRetry feature gate. (#5030, @mbobrovskyi)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-16T10:11:02Z

LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-16T16:33:54Z

Folks, we have RC0 just released, please test as much as possible: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.0-rc.0. Sanity check:
```
> docker run -it us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.12.0-rc.0
{"level":"info","ts":"2025-05-16T16:32:54.320548515Z","logger":"setup","caller":"kueue/main.go:468","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-05-16T16:32:54.320835106Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v20250516-v0.12.0-rc.0","gitCommit":"cf39c49e72dcf190b062b459e46157ec1fe2cc33"}
```

We already identified issues with @tenzen-y in the release of KueueViz which contains invalid image tags, like `us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueueviz-frontend:main` (instead of the tagged versions). We will work on fixing KueueViz release process on Monday and hopefully will release RC1 then. In the meanwhile please hunt for more issues.

cc @tenzen-y @gabesaba  @mwysokin @mwielgus @dgrove-oss @kannon92 @PBundyra @akram

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-05-16T19:43:29Z

Successful run of AppWrapper CI with kueue 0.12.0-rc.0 deployed: https://github.com/project-codeflare/appwrapper/pull/354

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-19T12:36:59Z

We have rc1, with fixed tagging for KueueViz (or at least I think so): https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.0-rc.1

Please test as much as possible, especially KueueViz as the release process is written from scratch for it. cc @akram @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-19T13:17:13Z

What is the test process for a rc1?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-19T13:21:02Z

> What is the test process for a rc1?

There is no official test process as of now. I think it would be nice if the contributors for specific features (like KueueViz) cover the new features. I'm thinking about KueueViz particularly, because this is totally new in this release.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T13:38:13Z

we will probably move the full release for Friday. Let me know if there are any objections. Until then I will publish new release candidates.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-21T05:33:44Z

We have RC2: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.0-rc.2 with Helm charts published under correct tag (PTAL):
```
> helm pull oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue --version=0.12.0-rc.2 --destination /tmp 
Pulled: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue:0.12.0-rc.2
Digest: sha256:7e6710497e30e7899554167eaad75a358899b103b76ca3ed9588b4850de425a6
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T09:22:10Z

We have [RC3](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.0-rc.3) including https://github.com/kubernetes-sigs/kueue/issues/5266. 

At the moment https://github.com/kubernetes-sigs/kueue/issues/5230 is the last feature I'm aware that would be good to include in the release, plus the bugfix: https://github.com/kubernetes-sigs/kueue/pull/5276

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-23T16:37:01Z

This can go in as a cherry-pick but I think https://github.com/kubernetes-sigs/kueue/pull/5330 should be included in v0.12.0.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T14:22:07Z

Latest diff of release notes: https://www.diffchecker.com/0AVMTrMM/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-26T14:24:25Z

> Latest diff of release notes: https://www.diffchecker.com/0AVMTrMM/

LGTM, thanks

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T18:00:12Z

We have the 0.12.0 release ready, sanity checks:

```
> docker run -it registry.k8s.io/kueue/kueue:v0.12.0
{"level":"info","ts":"2025-05-26T17:55:45.972694909Z","logger":"setup","caller":"kueue/main.go:468","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-05-26T17:55:45.972840189Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v20250526-v0.12.0","gitCommit":"b4306accba45a46b19c1aecc014de269dfeb9e13"}
```
Note that the "GitVersion" reported is "v20250526-v0.12.0", I have opened the issue to investigate and fix: https://github.com/kubernetes-sigs/kueue/issues/5368, but the gitCommit is correct.

```
> helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.0 | grep registry.k8s.io    
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.0
          image: 'registry.k8s.io/kueue/kueue/kueueviz-backend:v0.12.0'
          image: 'registry.k8s.io/kueue/kueue/kueueviz-frontend:v0.12.0'
        image: "registry.k8s.io/kueue/kueue:v0.12.0"
```
