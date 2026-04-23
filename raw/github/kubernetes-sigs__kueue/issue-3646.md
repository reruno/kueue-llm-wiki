# Issue #3646: Release v0.10.0

**Summary**: Release v0.10.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3646

**Last updated**: 2025-01-08T15:06:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-26T08:27:08Z
- **Updated**: 2025-01-08T15:06:06Z
- **Closed**: 2025-01-08T15:06:03Z
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
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #3861
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
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: kubernetes/k8s.io#7613
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: #3863
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/33960
  - [x] Create the presubmits and the periodic jobs for the next patch release:
        https://github.com/kubernetes/test-infra/pull/33961


## Changelog

```markdown
Changes since `v0.9.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- PodSets for RayJobs now account for submitter Job when spec.submissionMode=k8sJob is used.
  
  if you used the RayJob integration you may need to revisit your quota settings, 
  because now Kueue accounts for the resources required by the KubeRay submitter Job
  when the spec.submissionMode=k8sJob (by default 500m CPU and 200Mi memory) (#3729, @andrewsykim)
 - Removed the v1alpha1 Visibility API.
  
  The v1alpha1 Visibility API is deprecated. Please use v1beta1 instead. (#3499, @mbobrovskyi)
 - The InactiveWorkload reason for the Evicted condition is renamed to Deactivated. 
  Also, the reasons for more detailed situations are renamed:
    - InactiveWorkloadAdmissionCheck -> DeactivatedDueToAdmissionCheck
    - InactiveWorkloadRequeuingLimitExceeded -> DeactivatedDueToRequeuingLimitExceeded
  
  If you were watching for the "InactiveWorkload" reason in the "Evicted" condition, you need
  to start watching for the "Deactivated" reason. (#3593, @mbobrovskyi)
 
## Changes by Kind

### Feature

- Adds a managedJobsNamespaceSelector to the Kueue configuration that enables namespace-based control of whether Jobs submitted without a `kueue.x-k8s.io/queue-name` label are managed by Kueue for all supported Job Kinds. (#3712, @dgrove-oss)
- Allow mutating the queue-name label for non-running Deployments. (#3528, @mbobrovskyi)
- Allowed StatefulSet scaling down to zero and scale up from zero. (#3487, @mbobrovskyi)
- Extend the GenericJob interface to allow implementations of custom Job CRDs to use
  Topology-Aware Scheduling with rank-based ordering. (#3704, @PBundyra)
- Introduce alpha feature, behind the LocalQueueMetrics feature gate, which allows users to get the prometheus LocalQueues metrics:
  local_queue_pending_workloads
  local_queue_quota_reserved_workloads_total
  local_queue_quota_reserved_wait_time_seconds
  local_queue_admitted_workloads_total
  local_queue_admission_wait_time_seconds
  local_queue_admission_checks_wait_time_seconds
  local_queue_evicted_workloads_total
  local_queue_reserving_active_workloads
  local_queue_admitted_active_workloads
  local_queue_status
  local_queue_resource_reservation
  local_queue_resource_usage (#3673, @KPostOffice)
- Introduce the LocalQueue defaulting, enabled by the LocalQueueDefaulting feature gate. 
  When a new workload is created without the "queue-name" label,  and the LocalQueue
  with name "default" name exists in the workload's namespace, then the value of the
  "queue-name" is defaulted to "default". (#3610, @yaroslava-serdiuk)
- Kueue-viz: A Dashboard for kueue (#3727, @akram)
- Optimize the size of the Workload object when Topology-Aware Scheduling is used, and the 
  `kubernetes.io/hostname` is defined as the lowest Topology level. In that case the `TopologyAssignment`
  in the Workload's Status contains value only for this label, rather than for all levels defined. (#3677, @PBundyra)
- Promote MultiplePreemptions feature gate to stable, and drop the legacy preemption logic. (#3602, @gabesaba)
- Promoted ConfigurableResourceTransformations and WorkloadResourceRequestsSummary to Beta and enabled by default. (#3616, @dgrove-oss)
- ResourceFlavorSpec that defines topologyName is not immutable (#3738, @PBundyra)
- Respect node taints in Topology-Aware Scheduling when the lowest topology level is kubernetes.io/hostname. (#3678, @mimowo)
- Support `.featureGates` field in the configuration API to enable and disable the Kueue features (#3805, @kannon92)
- Support rank-based ordering of Pods with Topology-Aware Scheduling. 
  The Pod indexes are determined based on the "kueue.x-k8s.io/pod-group-index" label which
  can be set by an external controller managing the group. (#3649, @PBundyra)
- TAS: Support rank-based ordering for StatefulSet. (#3751, @mbobrovskyi)
- TAS: The CQ referencing a Topology is deactivated if the topology does not exist. (#3770, @mimowo)
- TAS: support rank-based ordering for JobSet (#3591, @mimowo)
- TAS: support rank-based ordering for Kubeflow (#3604, @mbobrovskyi)
- TAS: support rank-ordering of Pods for the Kubernetes batch Job. (#3539, @mimowo)
- TAS: validate that kubernetes.io/hostname can only be at the lowest level (#3714, @mbobrovskyi)

### Bug or Regression

- Added validation for Deployment queue-name to fail fast (#3555, @mbobrovskyi)
- Added validation for StatefulSet queue-name to fail fast. (#3575, @mbobrovskyi)
- Change, and in some scenarios fix, the status message displayed to user when a workload doesn't fit in available capacity. (#3536, @gabesaba)
- Determine borrowing more accurately, allowing preempting workloads which fit in nominal quota to schedule faster (#3547, @gabesaba)
- Fix Kueue crashing when the node for an admitted workload is deleted. (#3715, @mimowo)
- Fix a bug which occasionally prevented updates to the PodTemplate of the Job on the management cluster
  when starting a Job (e.g. updating nodeSelectors), when using `MultiKueueBatchJobWithManagedBy` enabled. (#3685, @IrvingMg)
- Fix accounting for usage coming from TAS workloads using multiple resources. The usage was multiplied
  by the number of resources requested by a workload, which could result in under-utilization of the cluster.
  It also manifested itself in the message in the workload status which could contain negative numbers. (#3490, @mimowo)
- Fix computing the topology assignment for workloads using multiple PodSets requesting the same
  topology. In particular, it was possible for the set of topology domains in the assignment to be empty,
  and as a consequence the pods would remain gated forever as the TopologyUngater would not have
  topology assignment information. (#3514, @mimowo)
- Fix dropping of reconcile requests for non-leading replica, which was resulting in workloads
  getting stuck pending after the rolling restart of Kueue. (#3612, @mimowo)
- Fix memory leak due to workload entries left in MultiKueue cache. The leak affects the 0.9.0 and 0.9.1 
  releases which enable MultiKueue by default, even if MultiKueue is not explicitly used on the cluster. (#3835, @mimowo)
- Fix misleading log messages from workload_controller indicating not existing LocalQueue or
  Cluster Queue. For example "LocalQueue for workload didn't exist or not active; ignored for now"
  could also be logged the ClusterQueue does not exist. (#3605, @7h3-3mp7y-m4n)
- Fix preemption when using Hierarchical Cohorts by considering as preemption candidates workloads
  from ClusterQueues located further in the hierarchy tree than direct siblings. (#3691, @gabesaba)
- Fix running Job when parallelism < completions, before the fix the replacement pods for the successfully
  completed Pods were not ungated. (#3559, @mimowo)
- Fix scheduling in TAS by considering tolerations specified in the ResourceFlavor. (#3723, @mimowo)
- Fix scheduling of workload which does not include the toleration for the taint in ResourceFlavor's spec.nodeTaints,
  if the toleration is specified on the ResourceFlavor itself. (#3722, @PBundyra)
- Fix the bug which prevented the use of MultiKueue if there is a CRD which is not installed
  and removed from the list of enabled integrations. (#3603, @mszadkow)
- Fix the flow of deactivation for workloads due to rejected AdmissionChecks. 
  Now, all AdmissionChecks are reset back to the Pending state on eviction (and deactivation in particular), 
  and so an admin can easily re-activate such a workload manually without tweaking the checks. (#3350, @KPostOffice)
- Fixed rolling update for StatefulSet integration (#3684, @mbobrovskyi)
- Make topology levels immutable to prevent issues with inconsistent state of the TAS cache. (#3641, @mbobrovskyi)
- TAS: Fixed bug that doesn't allow to update cache on delete Topology. (#3615, @mbobrovskyi)

### Other (Cleanup or Flake)

- Eliminate webhook validation in case Pod integration is used on 1.26 or earlier versions of Kubernetes. (#3247, @vladikkuzn)
- Replace deprecated gcr.io/kubebuilder/kube-rbac-proxy with registry.k8s.io/kubebuilder/kube-rbac-proxy. (#3747, @mbobrovskyi)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-26T08:28:02Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-26T12:25:17Z

we have the release candidate: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.0-rc.1
cc @mwielgus @mwysokin @dgrove-oss

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T11:49:52Z

FYI: the PRs I would like to still include:
- https://github.com/kubernetes-sigs/kueue/pull/3770
- https://github.com/kubernetes-sigs/kueue/pull/3805
- https://github.com/kubernetes-sigs/kueue/pull/3803

We could do one more RC4 to allow testing targeted on the specific version, preferably today. Depending on the test results we would then aim EOW.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-11T14:19:42Z

For #3805 happy to commit to get this in for v0.10.0. Thank you for including it!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T19:33:30Z

We have RC4: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.0-rc.4. We are aiming for the full release EOW, but it might be Monday.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T14:05:03Z

tweaked release-notes for https://github.com/kubernetes-sigs/kueue/pull/3673  and https://github.com/kubernetes-sigs/kueue/pull/3610

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T10:31:59Z

Updated the release notes, the diff is added notes for #3729, #3605, and #3835

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T12:40:27Z

```
> docker run --rm -it registry.k8s.io/kueue/kueue:v0.10.0 
{"level":"info","ts":"2024-12-16T12:39:47.151270558Z","logger":"setup","caller":"kueue/main.go:141","msg":"Initializing","gitVersion":"v0.10.0","gitCommit":"5ff057f44cca5e3ba68e69a20da1bad6cc4974a2"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-08T15:05:58Z

/close
We already have the release: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.0

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-08T15:06:04Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3646#issuecomment-2577900058):

>/close
>We already have the release: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.0


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
