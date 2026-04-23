# Issue #6756: Release v0.14.0

**Summary**: Release v0.14.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6756

**Last updated**: 2025-10-01T03:47:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-08T14:34:44Z
- **Updated**: 2025-10-01T03:47:04Z
- **Closed**: 2025-10-01T03:47:03Z
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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7091
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
      to production: https://github.com/kubernetes/k8s.io/pull/8579
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7096
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
        https://github.com/kubernetes/test-infra/pull/35617
  - [x] Create the presubmits and the periodic jobs for the next patch release:
        https://github.com/kubernetes/test-infra/pull/35618
  - [x] Drop CI Jobs for testing the out-of-support branch:
        https://github.com/kubernetes/test-infra/pull/35618


## Changelog

```markdown
Changes since `v0.13.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- ProvisioningRequest: Remove setting deprecated ProvisioningRequest annotations on Kueue-managed Pods:
  - cluster-autoscaler.kubernetes.io/consume-provisioning-request
  - cluster-autoscaler.kubernetes.io/provisioning-class-name
  
  If you are implementing a ProvisioningRequest reconciler used by Kueue you should
  make sure the new annotations are supported:
  - autoscaling.x-k8s.io/consume-provisioning-request
  - autoscaling.x-k8s.io/provisioning-class-name (#6381, @kannon92)
 - Rename kueue-metrics-certs to kueue-metrics-cert cert-manager.io/v1 Certificate name in cert-manager manifests when installing Kueue using the Kustomize configuration.
  
  If you're using cert-manager and have deployed Kueue using the Kustomize configuration, you must delete the existing kueue-metrics-certs cert-manager.io/v1 Certificate before applying the new changes to avoid conflicts. (#6345, @mbobrovskyi)
 - Replace "DeactivatedXYZ" "reason" label values with "Deactivated" and introduce "underlying_cause" label to the following metrics:
  - "pods_ready_to_evicted_time_seconds"
  - "evicted_workloads_total"
  - "local_queue_evicted_workloads_total"
  - "evicted_workloads_once_total"
  
  If you rely on the "DeactivatedXYZ" "reason" label values, you can migrate to the "Deactivated" "reason" label value and the following "underlying_cause" label values:
  - ""
  - "WaitForStart"
  - "WaitForRecovery"
  - "AdmissionCheck"
  - "MaximumExecutionTimeExceeded"
  - "RequeuingLimitExceeded" (#6590, @mykysha)
 - TAS: Enforce a stricter value of the `kueue.x-k8s.io/podset-group-name` annotation in the creation webhook.
  
  Make sure the values of the `kueue.x-k8s.io/podset-group-name` annotation are not numbers.` (#6708, @kshalot)
 
## Upgrading steps

### 1. Back Up Topology Resources (skip if you are not using Topology API):

kubectl get topologies.kueue.x-k8s.io -o yaml > topologies.yaml

### 2. Update apiVersion in Backup File (skip if not using Topology API):
Replace `v1alpha1` with `v1beta1` in topologies.yaml for all resources:

sed -i -e 's/v1alpha1/v1beta1/g' topologies.yaml

### 3. Delete Old CRDs:

kubectl delete crd topologies.kueue.x-k8s.io

### 4. Remove Finalizers from Topologies (skip if you are not using Topology API):

kubectl get topology.kueue.x-k8s.io -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' | while read -r name; do
  kubectl patch topology.kueue.x-k8s.io "$name" -p '{"metadata":{"finalizers":[]}}' --type='merge'
done

### 5. Install Kueue v0.14.0:
Follow the instructions [here](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version) to install.

### 6. Restore Topology Resources (skip if not using Topology API):

kubectl apply -f topologies.yaml

## Changes by Kind

### Deprecation

- Stop serving the QueueVisibility feature, but keep APIs (`.status.pendingWorkloadsStatus`) to avoid breaking changes.
  
  If you rely on the QueueVisibility feature (`.status.pendingWorkloadsStatus` in the ClusterQueue), you must migrate to VisibilityOndDemand 
  (https://kueue.sigs.k8s.io/docs/tasks/manage/monitor_pending_workloads/pending_workloads_on_demand). (#6631, @vladikkuzn)

### API Change

- TAS: Graduated TopologyAwareScheduling to Beta. (#6830, @mbobrovskyi)
- TAS: Support multiple nodes for failure handling by ".status.unhealthyNodes" in Workload. The "alpha.kueue.x-k8s.io/node-to-replace" annotation is no longer used (#6648, @pajakd)

### Feature

- Add an alpha integration for Kubeflow Trainer to Kueue. (#6597, @kaisoz)
- Add an exponential backoff for the TAS scheduler second pass. (#6753, @mykysha)
- Added priority_class label for kueue_local_queue_admitted_workloads_total metric. (#6845, @vladikkuzn)
- Added priority_class label for kueue_local_queue_evicted_workloads_total metric (#6898, @vladikkuzn)
- Added priority_class label for kueue_local_queue_quota_reserved_workloads_total metric. (#6897, @vladikkuzn)
- Added priority_class label for the following metrics:
  - kueue_admitted_workloads_total
  - kueue_evicted_workloads_total
  - kueue_evicted_workloads_once_total
  - kueue_quota_reserved_workloads_total
  - kueue_admission_wait_time_seconds
  - kueue_quota_reserved_wait_time_seconds
  - kueue_admission_checks_wait_time_seconds (#6951, @mbobrovskyi)
- Added priority_class to kueue_local_queue_admission_checks_wait_time_seconds (#6902, @vladikkuzn)
- Added priority_class to kueue_local_queue_admission_wait_time_seconds (#6899, @vladikkuzn)
- Added priority_class to kueue_local_queue_quota_reserved_wait_time_seconds (#6900, @vladikkuzn)
- Added workload_priority_class label for optional metrics (if waitForPodsReady is enabled):
  
  - kueue_ready_wait_time_seconds (Histogram)
  - kueue_admitted_until_ready_wait_time_seconds (Histogram)
  - kueue_local_queue_ready_wait_time_seconds (Histogram)
  - kueue_local_queue_admitted_until_ready_wait_time_seconds (Histogram) (#6944, @IrvingMg)
- DRA: Alpha support for Dynamic Resource Allocation in Kueue. (#5873, @alaypatel07)
- ElasticJobs: Support in-tree RayAutoscaler for RayCluster (#6662, @VassilisVassiliadis)
- KueueViz: Enhancing the following endpoint customizations and optimizations:
  - The frontend and backend ingress no longer have hardcoded NGINX annotations. You can now set your own annotations in Helm’s values.yaml using kueueViz.backend.ingress.annotations and kueueViz.frontend.ingress.annotations
  - The Ingress resources for KueueViz frontend and backend no longer require hardcoded TLS. You can now choose to use HTTP only by not providing kueueViz.backend.ingress.tlsSecretName and kueueViz.frontend.ingress.tlsSecretName
  - You can set environment variables like KUEUEVIZ_ALLOWED_ORIGINS directly from values.yaml using kueueViz.backend.env (#6682, @Smuger)
- MultiKueue: Support external frameworks.
  Introduced a generic MultiKueue adapter to support external, custom Job-like workloads. This allows users to integrate custom Job-like CRDs (e.g., Tekton PipelineRuns) with MultiKueue for resource management across multiple clusters. This feature is guarded by the `MultiKueueGenericJobAdapter` feature gate. (#6760, @khrm)
- Multikueue × ElasticJobs: The elastic `batchv1/Job` supports MultiKueue. (#6445, @ichekrygin)
- ProvisioningRequest: Graduate ProvisioningACC feature to GA (#6382, @kannon92)
- TAS: Graduated to Beta the following feature gates responsible for enabling and default configuration of the Node Hot Swap mechanism: 
  TASFailedNodeReplacement, TASFailedNodeReplacementFailFast, TASReplaceNodeOnPodTermination. (#6890, @mbobrovskyi)
- TAS: Implicit mode schedules consecutive indexes as close as possible (rank-ordering). (#6615, @PBundyra)
- TAS: introduce validation against using PodSet grouping and PodSet slicing for the same PodSet, 
  which is currently not supported. More precisely the `kueue.x-k8s.io/podset-group-name` annotation
  cannot be set along with any of: `kueue.x-k8s.io/podset-slice-size`, `kueue.x-k8s.io/podset-slice-required-topology`. (#7051, @kshalot)
- The following limits for ClusterQueue quota specification have been relaxed:
  - the number of Flavors per ResourceGroup is increased from 16 to 64
  - the number of Resources per Flavor, within a ResourceGroup, is increased from 16 to 64
  
  We also provide the following additional limits:
  - the total number of Flavors across all ResourceGroups is <= 256
  - the total number of Resources across all ResourceGroups is <= 256
  - the total number of (Flavor, Resource) pairs within a ResourceGroup is <= 512 (#6906, @LarsSven)
- Visibility API: Adds support for Securing APIService. (#6798, @MaysaMacedo)
- WorkloadRequestUseMergePatch: allows switching the Status Patch type from Apply to Merge for admission-related patches. (#6765, @mszadkow)

### Bug or Regression

- AFS: Fixed kueue-controller-manager crash when enabled AdmissionFairSharing feature gate without AdmissionFairSharing config. (#6670, @mbobrovskyi)
- ElasticJobs: Fix the bug for the ElasticJobsViaWorkloadSlices feature where in case of Job resize followed by eviction
  of the "old" workload, the newly created workload could get admitted along with the "old" workload.
  The two workloads would overcommit the quota. (#6221, @ichekrygin)
- ElasticJobs: Fix the bug that scheduling of the Pending workloads was not triggered on scale-down of the running 
  elastic Job which could result in admitting one or more of the queued workloads. (#6395, @ichekrygin)
- ElasticJobs: workloads correctly trigger workload preemption in response to a scale-up event. (#6973, @ichekrygin)
- FS: Fix the algorithm bug for identifying preemption candidates, as it could return a different
  set of preemption target workloads (pseudo random) in consecutive attempts in tie-break scenarios,
  resulting in excessive preemptions. (#6764, @PBundyra)
- FS: Fix the following FairSharing bugs:
  - Incorrect DominantResourceShare caused by rounding (large quotas or high FairSharing weight)
  - Preemption loop caused by zero FairSharing weight (#6925, @gabesaba)
- FS: Fixing a bug where a preemptor ClusterQueue was unable to reclaim its nominal quota when the preemptee ClusterQueue can borrow a large number of resources from the parent ClusterQueue / Cohort (#6617, @pajakd)
- FS: Validate FairSharing.Weight against small values which lose precision (0 < value <= 10^-9) (#6986, @gabesaba)
- Fix accounting for the `evicted_workloads_once_total` metric:
  - the metric wasn't incremented for workloads evicted due to stopped LocalQueue (LocalQueueStopped reason)
  - the reason used for the metric was "Deactivated" for workloads deactivated by users and Kueue, now the reason label can have the following values: Deactivated, DeactivatedDueToAdmissionCheck, DeactivatedDueToMaximumExecutionTimeExceeded, DeactivatedDueToRequeuingLimitExceeded. This approach aligns the metric with `evicted_workloads_total`.
  - the metric was incremented during preemption before the preemption request was issued. Thus, it could be incorrectly over-counted in case of the preemption request failure.
  - the metric was not incremented for workload evicted due to NodeFailures (TAS)
  
  The existing and introduced DeactivatedDueToXYZ reason label values will be replaced by the single "Deactivated" reason label value and underlying_cause in the future release. (#6332, @mimowo)
- Fix bug in workload usage removal simulation that results in inaccurate flavor assignment (#7077, @gabesaba)
- Fix support for PodGroup integration used by external controllers, which determine the 
  the target LocalQueue and the group size only later. In that case the hash would not be 
  computed resulting in downstream issues for ProvisioningRequest.
  
  Now such an external controller can indicate the control over the PodGroup by adding
  the `kueue.x-k8s.io/pod-suspending-parent` annotation, and later patch the Pods by setting
  other metadata, like the kueue.x-k8s.io/queue-name label to initiate scheduling of the PodGroup. (#6286, @pawloch00)
- Fix the bug for the StatefulSet integration which would occasionally cause a StatefulSet
  to be stuck without workload after renaming the "queue-name" label. (#7028, @IrvingMg)
- Fix the bug that a workload going repeatedly via the preemption and re-admission cycle would accumulate the
  "Previously" prefix in the condition message, eg: "Previously: Previously: Previously: Preempted to accommodate a workload ...". (#6819, @amy)
- Fix the bug which could occasionally cause workloads evicted by the built-in AdmissionChecks
  (ProvisioningRequest and MultiKueue) to get stuck in the evicted state which didn't allow re-scheduling.
  This could happen when the AdmissionCheck controller would trigger eviction by setting the
  Admission check state to "Retry". (#6283, @mimowo)
- Fix the validation messages when attempting to remove the queue-name label from a Deployment or StatefulSet. (#6715, @Panlq)
- Fixed a bug that prevented adding the kueue- prefix to the secretName field in cert-manager manifests when installing Kueue using the Kustomize configuration. (#6318, @mbobrovskyi)
- HC: When multiple borrowing flavors are available, prefer the flavor which
  results in borrowing more locally (closer to the ClusterQueue, further from the root Cohort).
  
  This fixes the scenario where a flavor would be selected which required borrowing
  from the root Cohort in one flavor, while in a second flavor, quota was
  available from the nearest parent Cohort. (#7024, @gabesaba)
- Helm: Fix a bug where the internal cert manager assumed that the helm installation name is 'kueue'. (#6869, @cmtly)
- Helm: Fixed a bug preventing Kueue from starting after installing via Helm with a release name other than "kueue" (#6799, @mbobrovskyi)
- Helm: Fixed bug where webhook configurations assumed a helm install name as "kueue". (#6918, @cmtly)
- KueueViz: Fix CORS configuration for development environments (#6603, @yankay)
- KueueViz: Fix a bug that only localhost is an executable domain. (#7011, @kincl)
- Pod-integration now correctly handles pods stuck in the Terminating state within pod groups, preventing them from being counted as active and avoiding blocked quota release. (#6872, @ichekrygin)
- ProvisioningRequest: Fix a bug that Kueue didn't recreate the next ProvisioningRequest instance after the
  second (and consecutive) failed attempt. (#6322, @PBundyra)
- Support disabling client-side ratelimiting in Config API clientConnection.qps with a negative value (e.g., -1) (#6300, @tenzen-y)
- TAS: Fix a bug that the node failure controller tries to re-schedule Pods on the failure node even after the Node is recovered and reappears (#6325, @pajakd)
- TAS: Fix a bug where new Workloads starve, caused by inadmissible workloads frequently requeueing due to unrelated Node LastHeartbeatTime update events. (#6570, @utam0k)
- TAS: Fix the scenario when Node Hot Swap cannot find a replacement. In particular, if slices are used
  they could result in generating invalid assignment, resulting in panic from TopologyUngater.
  Now, such a workload is evicted. (#6914, @PBundyra)
- TAS: Node Hot Swap allows replacing a node for workloads using PodSet slices, 
  ie. when the `kueue.x-k8s.io/podset-slice-size` annotation is used. (#6942, @pajakd)
- TAS: fix the bug that Kueue is crashing when PodSet has size 0, eg. no workers in LeaderWorkerSet instance. (#6501, @mimowo)

### Other (Cleanup or Flake)

- Promote ConfigurableResourceTransformations feature gate to stable. (#6599, @mbobrovskyi)
- Support for Kubernetes 1.34 (#6689, @mbobrovskyi)
- TAS: stop setting the "kueue.x-k8s.io/tas" label on Pods. 
  
  In case the implicit TAS mode is used, then the `kueue.x-k8s.io/podset-unconstrained-topology=true` annotation
  is set on Pods. (#6895, @mimowo)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T10:09:32Z

FYI, we have scheduled the tentative release date with @tenzen-y as September 25. 

If we have some very important features we may shift to Sep 30, but don't count on it, and please priorize the ongoing work.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-19T12:30:04Z

I intend to prepare a Release candidate towards the end of the day. It would be great if contributors can engage in manual testing so that we can spot issues. 

I will post again when RC is ready.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-19T17:15:35Z

https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.0-rc.0

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T16:41:49Z

FYI: we moved the release date to 30th September

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T13:48:36Z

We will need to inject into release notes the upgrade procedure related to the graduation of the Topology API: https://github.com/kubernetes-sigs/kueue/issues/3450#issuecomment-3351932973

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T14:44:42Z

I have updated the release notes, including the upgrade procedure

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T14:46:27Z

Could we replace `### 5. Install Kueue v0.14.x:` with `### 5. Install Kueue v0.14.0:`?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T14:46:50Z

Indeed, this release note is for v0.14.0.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T14:47:59Z

done

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T14:49:01Z

> done

SGTM, thanks!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T16:09:34Z

sanity checking:

```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.0 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.0
Digest: sha256:c2eef19fdc9cb51e961453cd5807077b96b7db2ff59b8e660bdb91ecdd9321cc
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.0'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.0'
        image: "registry.k8s.io/kueue/kueue:v0.14.0"
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.14.0
v0.14.0: Pulling from kueue/kueue
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
da8ab0320d02: Pull complete 
Digest: sha256:2b916424b27da0e07c85f02a7b54fde6c054eb94dff1fc0c7c70e36fd64076cc
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.0
{"level":"info","ts":"2025-09-30T16:08:16.255516633Z","logger":"setup","caller":"kueue/main.go:507","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nwaitForPodsReady: {}\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-09-30T16:08:16.255731933Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.0","gitCommit":"431c2e538b87319c838e3a993dfeec2b077f8fa2","buildDate":"2025-09-30T15:24:06Z"}

```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.0
v0.14.0: Pulling from kueue/kueueviz-backend
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
ee70967b0b7d: Pull complete 
Digest: sha256:76e2157f0a4848dd3bda82abe65805e5b2334f1b20d18952b710e49eb4a2a937
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.0
2025/09/30 16:08:52 Starting pprof server on localhost:6060

```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.0
v0.14.0: Pulling from kueue/kueueviz-frontend
d107e437f729: Already exists 
23418204b321: Already exists 
8544b3c3f2fc: Already exists 
ae0081685b50: Already exists 
1ab59cb3b5b2: Already exists 
09930b979d6e: Pull complete 
bc122525fe16: Pull complete 
a64331155033: Pull complete 
b8066afcd568: Pull complete 
4f4fb700ef54: Pull complete 
Digest: sha256:5c0a360ba29361dc41e6208d0ebc1d774231e2e0e322d145a1ccedefb2eec8ad
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.0

```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T03:46:58Z

Closing this issue as all tasks have been completed.
Thank you for all!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-01T03:47:04Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6756#issuecomment-3354611409):

>Closing this issue as all tasks have been completed.
>Thank you for all!
>/close
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
