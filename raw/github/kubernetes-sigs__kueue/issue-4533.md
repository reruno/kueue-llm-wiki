# Issue #4533: Release v0.11.0

**Summary**: Release v0.11.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4533

**Last updated**: 2025-03-20T14:58:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-10T08:33:16Z
- **Updated**: 2025-03-20T14:58:34Z
- **Closed**: 2025-03-20T14:58:32Z
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
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4698
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
      via UI or `gh release --repo kubernetes-sigs/kueue upload <tag> artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to 
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: kubernetes/k8s.io#7900
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.11.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4707
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/34559
  - [x] Create the presubmits and the periodic jobs for the next patch release: https://github.com/kubernetes/test-infra/pull/34561


## Changelog

```markdown
Changes since `0.10.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- If you implement the GenericJob interface for a custom Job CRD you need to update the
  implementation of the PodSets function as its signature is extended to return potential errors. (#4002, @Horiodino)
 - If you implement the GenericJob interface you need to update the implementation as
  the PodSet.Name field has changed its type from string to PodSetReference. (#4417, @vladikkuzn)
 - The configuration field `integrations.podOptions` is deprecated. 
  
  Users who set the `Integrations.PodOptions` namespace selector to a non-default
  value should plan for migrating to use `managedJobsNamespaceSelector` instead, as the PodOptions
  selector is going to be removed in a future release. (#4256, @dgrove-oss)
 
## Changes by Kind

### Feature

- Add a column to multikueue indicating if it is connected to worker cluster (#4335, @highpon)
- Add an integration for AppWrappers to Kueue. (#3953, @dgrove-oss)
- Add integration for LeaderWorkerSet where Pods are managed by the pod-group integration. (#3515, @vladikkuzn)
- Add the full name of the preempting workload to applicable log lines to make debugging preemption easier. (#4398, @KPostOffice)
- Adds kueue-viz helm charts allowing installation of kueue-viz using helm (#3852, @akram)
- Adds the JobUID to preemption condition messages.  This makes it easy to get the preempting workload using `kubectl get workloads --selector=kueue.x-k8s.io/job-uid=<JobUID>` (#4524, @avrittrohwer)
- Allow mutating queue-name label in StatefulSet Webhook when ReadyReplicas equals zero. (#3520, @mbobrovskyi)
- Allow one to configure certificates for metrics (#4385, @kannon92)
- Expose the TopologyName in LocalQueue status (#4543, @mbobrovskyi)
- Helm: Adds kueueViz parameters `enableKueueViz`, `kueueViz.backend.image` and `kueueViz.frontend.image` (#4410, @akram)
- Improve error messages when the ProvisioningRequest Admission Check is not initialized due to a missing or unsupported version of the ProvisioningRequest CRD. (#4131, @Horiodino)
- Kueue exposes a new recovery mechanism as part of the WaitForPodsReady API. This evicts jobs which surpasses configured threshold for pod's recovery during runtime (#4301, @PBundyra)
- Kueue exposes a new recovery mechanism as part of the WaitForPodsReady API. This evicts jobs which surpasses configured threshold for pod's recovery during runtime (#4302, @PBundyra)
- Kueue-viz: allow to configure the application port by the KUEUE_VIZ_PORT env. variable. (#4178, @lekaf974)
- MultiKueue: Add support for Kubeflow Training-Operator Jobs  `spec.runPolicy.managedBy` field (#4116, @mszadkow)
- Support KubeRay integrations (RayJob and RayCluster) for MultiKueue via the managedBy mechanism. 
  This allows for the installation of the Ray operator on the management cluster. (#4677, @mszadkow)
- Support Pod integration in MultiKueue. (#4034, @Bobbins228)
- Support RayCluster in MultiKueue, assuming only Ray CRDs are installed on the management cluster. (#3959, @mszadkow)
- Support RayJob in MultiKueue, assuming only Ray CRDs are installed on the management cluster. (#3892, @mszadkow)
- TAS: Add a new default algorithm to minimize resource fragmentation. The old algorithm is gated behind the `TASLargestFit` feature gate. (#4228, @PBundyra)
- TAS: Support cohorts and preemption within them. (#4418, @mimowo)
- TAS: Support preemption within ClusterQueue (#4171, @mimowo)
- TopologyAwareScheduling can now be used with `kueue.x-k8s.io/podset-unconstrained-topology` annotation (#4567, @PBundyra)
- TopologyAwareScheduling can now be used with profiles based on feature gates. TopologyAwareScheduling has now a new algorithm LeastFreeCapacityFit (#4576, @PBundyra)
- Upgrade Kuberay to v1.3.1. (#4568, @mszadkow)
- Use TAS for workloads implicitly (without TAS annotations) when the target CQ is TAS-only, meaning
  all the resource flavors have spec.topologyName specified. (#4519, @mimowo)
- WaitForPodsReady countdown is now measured since the admission of the workload instead of setting `PodsReady` condition to `False` (#4287, @PBundyra)
- [FSxHC] Add Cohort Fair Sharing Status and Metrics (#4561, @mbobrovskyi)
- [FSxHC] Extend Cohort API with Fair Sharing Configuration (#4288, @gabesaba)
- [FSxHC] Make Fair Sharing compatible with Hierarchical Cohorts during preemption (#4572, @gabesaba)
- [FSxHC] Make Fair Sharing compatible with Hierarchical Cohorts during scheduling (#4503, @gabesaba)

### Bug or Regression

- Add missing external types to apply configurations (#4191, @astefanutti)
- Align default value for `managedJobsNamespaceSelector` in helm chart and kustomize files. (#4262, @dgrove-oss)
- Disable the StatefulSet webhook in the kube-system and kueue-system namespaces by default. 
  This aligns the default StatefulSet webhook configuration with the Pod and Deployment configurations. (#4121, @kannon92)
- Fix a bug is incorrect field path in inadmissible reasons and messages when Pod resources requests do not satisfy LimitRange constraints. (#4267, @tenzen-y)
- Fix a bug is incorrect field path in inadmissible reasons and messages when container requests exceed limits (#4216, @tenzen-y)
- Fix a bug that allowed unsupported changes to some PodSpec fields which were resulting in the StatefulSet getting stuck on Pods with schedulingGates. 
  
  The validation blocks mutating the following Pod spec fields: `nodeSelector`, `affinity`, `tolerations`, `runtimeClassName`, `priority`, `topologySpreadConstraints`, `overhead`, `resourceClaims`, plus container (and init container) fields: `ports` and `resources.requests`. 
  
  Mutating other fields, such as container image, command or args, remains allowed and supported. (#4081, @mbobrovskyi)
- Fix a bug that doesn't allow Kueue to delete Pods after a StatefulSet is deleted. (#4150, @mbobrovskyi)
- Fix a bug that occurs when a PodTemplate has not been created yet, but the Cluster Autoscaler attempts to process the ProvisioningRequest and marks it as failed. (#4086, @mbobrovskyi)
- Fix a bug that prevented tracking some of the controller-runtime metrics in Prometheus. (#4217, @tenzen-y)
- Fix a bug truncating AdmissionCheck condition message at `1024` characters when creation of the associated ProvisioningRequest or PodTemplate fails. 
  Instead, use the `32*1024` characters limit as for condition messages. (#4190, @mbobrovskyi)
- Fix building TAS assignments for workloads with multiple PodSets (eg. JobSet or kubeflow Jobs). The assignment was computed independently for the PodSets which could result in conflicts rendering the pods unschedulable by the kube-scheduler. (#3937, @kerthcet)
- Fix populating the LocalQueue metrics: `kueue_local_queue_resource_usage` and `kueue_local_queue_resource_reservation`. (#3988, @mykysha)
- Fix the bug that prevented Kueue from updating the AdmissionCheck state in the Workload status on a ProvisioningRequest creation error. (#4114, @mbobrovskyi)
- Fix the bug that prevented scaling StatefulSets which aren't managed by Kueue when the "statefulset" integration is enabled. (#3991, @mbobrovskyi)
- Fix the permission bug which prevented adding the `kueue.x-k8s.io/resource-in-use` finalizer to the Topology objects, resulting in repeatedly logged errors. (#3910, @kerthcet)
- Fixes a bug in 0.10.0 which resulted in the kueue manager configuration not being logged. (#3876, @dgrove-oss)
- Fixes a bug that would result in default values not being properly set on creation for enabled integrations whose API was not available when the Kueue controller started. (#4547, @dgrove-oss)
- Helm: Fix the unspecified LeaderElection Role and Rolebinding namespaces (#4383, @eric-higgins-ai)
- Helm: Fixed a bug that prometheus namespace is enforced with namespace the same as kueue-controller-manager (#4484, @kannon92)
- Improve error message in the event when scheduling for TAS workload fails due to unassigned flavors. (#4204, @mimowo)
- Propagate the top-level setting of the `kueue.x-k8s.io/priority-class` label to the PodTemplate for
  Deployments and StatefulSets. This way the Workload Priority class is no longer ignored by the workloads. (#3980, @Abirdcfly)
- TAS: Do not ignore the TAS annotation if set on the template for the Ray submitter Job. (#4341, @mszadkow)
- TAS: Fix a bug that TopolologyUngator cound not be triggered the leader change when enabled HA mode (#4653, @tenzen-y)
- TAS: Fix a bug that incorrect topologies are assigned to Workloads when topology has insufficient allocatable Pods count (#4271, @tenzen-y)
- TAS: Fix a bug that unschedulable nodes (".spec.unschedulable=true") are counted as allocatable capacities (#4181, @tenzen-y)
- TAS: Fixed a bug that allows to create a JobSet with both kueue.x-k8s.io/podset-required-topology and kueue.x-k8s.io/podset-preferred-topology annotations set on the PodTemplate. (#4130, @mbobrovskyi)
- Update FairSharing to be incompatible with ClusterQueue.Preemption.BorrowWithinCohort. Using these parameters together is a no-op, and will be validated against in future releases. This change fixes an edge case which triggered an infinite preemption loop when these two parameters were combined. (#4165, @gabesaba)

### Other (Cleanup or Flake)

- MultiKueue: Do not update the status of the Job on the management cluster while the Job is suspended. This is updated  for jobs represented by JobSet, Kubeflow Jobs and MPIJob. (#4070, @IrvingMg)
- Promote WorkloadResourceRequestsSummary feature gate to stable (#4166, @dgrove-oss)
- Publish helm charts to the Kueue staging repository `http://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts`, 
  so that they can be promoted to the permanent location under `registry.k8s.io/kueue/charts`. (#4680, @mimowo)
- Remove the support for Kubeflow MXJob. (#4077, @mszadkow)
- Renamed Log key from "attemptCount" to "schedulingCycleCount". This key tracks how many scheduling cycles we have done since starting Kueue. (#4108, @gabesaba)
- Support for Kubernetes 1.32 (#3820, @mbobrovskyi)
- The APF configuration, using v1beta3 API dedicated for Kubernetes 1.28 (or older), for the visibility server is no longer part of the release artifacts of Kueue. (#3983, @mbobrovskyi)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T09:02:25Z

cc @tenzen-y @dgrove-oss @kannon92 @mwielgus @mwysokin @PBundyra @gabesaba 

We are aiming for the release March 18th. 

Prior to that, this week (probably Thursday or Friday), I would like to have RC1.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-10T13:23:57Z

Is there any chance of a slightly earlier RC1 (eg Wed)?

The AppWrapper 1.0.x release line supports both Kueue 0.10 (as an external framework) and Kueue main (as a built-in framework).   I'd like to make an AppWrapper 1.1.x release line that would only support Kueue 0.11, because it makes the AppWrapper controller simpler and easier to configure/deploy (I get to remove all the external framework implementation).   I need a KueueRC (with images I can reliably pull in the AppWrapper CI) before I can make the AppWrapper 1.1.0 release and then do a PR to update Kueue from AppWrapper 1.0.6 to 1.1.0.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T13:29:43Z

Wednesday sgtm, wdyt @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-10T13:44:48Z

I'm also fine on Wed

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-12T07:35:37Z

The release note differences for RC release: https://www.diffchecker.com/4JqW3gRp/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T07:46:54Z

The diff of notes lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-12T07:58:57Z

First RC version has been released: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.11.0-rc.0

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T10:15:40Z

Folks, we are considering moving the release date from 18th to 20th (or 21st) to make it easier for me and @tenzen-y to find a common slot. Let me know if you have some preference, otherwise we will assume the 20th and 21st are equally good.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T10:42:12Z

FYI: the new tentative date is 20th of March.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T08:23:32Z

Diff of release notes since https://github.com/kubernetes-sigs/kueue/issues/4533#issuecomment-2716902178: https://www.diffchecker.com/xAJ59uBp/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-20T08:25:51Z

> https://www.diffchecker.com/xAJ59uBp/

SGTM, thank you

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T14:58:26Z

/close
All steps are done. Enjoy 🥳

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-20T14:58:33Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4533#issuecomment-2740757679):

>/close
>All steps are done. Enjoy 🥳 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
