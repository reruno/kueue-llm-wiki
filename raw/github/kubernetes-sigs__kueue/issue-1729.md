# Issue #1729: Release v0.6.0

**Summary**: Release v0.6.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1729

**Last updated**: 2024-02-15T16:10:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-13T19:17:38Z
- **Updated**: 2024-02-15T16:10:57Z
- **Closed**: 2024-02-15T16:10:54Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 3

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal.
  At least two for minor or major releases. At least one for a patch release.
- [x] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date
  - [x] Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes.
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2`
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] an OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update `README.md`, `CHANGELOG`, `charts/kueue/Chart.yaml` (`appVersion`) and `charts/kueue/values.yaml` (`controllerManager.manager.image.tag`) in the release branch: #1733
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
      to production: https://github.com/kubernetes/k8s.io/pull/6432
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.6.0
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/LmtqKhEBGj4
- [x] Update the below files with respective values in `main` branch : #1736
  - Latest version in `README.md`
  - Release notes in the `CHANGELOG`
  - `version` in `site/config.toml`
  - `appVersion` in `charts/kueue/Chart.yaml`
  - `last-updated`, `last-reviewed`, `commit-hash`, `project-release`, and `distribution-points` in `SECURITY-INSIGHTS.yaml`
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/31985


## Changelog

```markdown
Changes since `v0.5.0`:

### API Change

- A `stopPolicy` field in the ClusterQueue allows to hold or drain a ClusterQueue (#1299, @trasc)
- Add a lendingLimit field in ClusterQueue's quotas, to allow restricting how much of the unused resources by the ClusterQueue can be borrowed by other ClusterQueues in the cohort.
  In other words, this allows a quota equal to `nominal-lendingLimit` to be exclusively used by the ClusterQueue. (#1385, @B1F030)
- Add validation for clusterQueue: when cohort is empty, borrowingLimit must be nil. (#1525, @B1F030)
- Allow decrease reclaimable pods to 0 for suspended job (#1277, @yaroslava-serdiuk)
- MultiKueue: Add Path location type for cluster KubeConfigs. (#1640, @trasc)
- MultiKueue: Add garbage collection of deleted Workloads. (#1643, @trasc)
- MultiKueue: Multi cluster job dispatching for k8s Job. This doesn't include support for live status updates. (#1313, @trasc)
- Support for a mechanism to suspend a running Job without requeueing (#1252, @vicentefb)
- Support for preemption while borrowing (#1397, @mimowo)
- The leaderElection field in the Configuration API is now defaulted.
  Leader election is now enabled by default. (#1598, @astefanutti)
- Visibility API: Add an endpoint that allows a user to fetch information about pending workloads and their position in LocalQueue. (#1365, @PBundyra)
- Visibility API: Introduce an on-demand API endpoint for fetching pending workloads in a ClusterQueue. (#1251, @PBundyra)
- Visibility API: extend the information returned for the pending workloads in a ClusterQueue, including the workload position in the queue. (#1362, @PBundyra)
- WaitForPodsReady: Add a config field to allow admins to configure the timestamp used when sorting workloads that were evicted due to their Pods not becoming ready on time. (#1542, @nstogner)
- WaitForPodsReady: Support a backoff re-queueing mechanism with configurable limit. (#1709, @tenzen-y)

### Feature

- Add Prebuilt Workload support for JobSets. (#1575, @trasc)
- Add events for transitions of the provisioning AdmissionCheck (#1271, @stuton)
- Add prebuilt workload support for batch/job. (#1358, @trasc)
- Add support for groups of plain Pods. (#1319, @achernevskii)
- Allow configuring featureGates on helm charts. (#1314, @B1F030)
- At log level 6, the usage of ClusterQueues and cohorts is included in logs.
  
  The status of the internal cache and queues is also logged on demand when a SIGUSR2 is sent to kueue, regardless of the log level. (#1528, @alculquicondor)
- Changing tolerations in an inadmissible job triggers an admission retry with the updated tolerations. (#1304, @stuton)
- Increase the default number of reconcilers for Pod and Workload objects to 5, each. (#1589, @alculquicondor)
- Jobs preserve their position in the queue if the number of pods change before being admitted (#1223, @yaroslava-serdiuk)
- Make the image build setting CGO_ENABLED configurable (#1391, @anishasthana)
- MultiKueue: Add live status updates for multikueue JobSets (#1668, @trasc)
- MultiKueue: Support for JobSets. (#1606, @trasc)
- Support RayCluster as a queue-able workload in Kueue (#1520, @vicentefb)
- Support for retry of provisioning request.
  
  When `ProvisioningACC` is enabled, and there are existing ProvisioningRequests, they are going to be recreated.
  This may cause job evictions for some long-running jobs which were using the ProvisioningRequests. (#1351, @mimowo)
- The image gcr.io/k8s-staging-kueue/debug:main, along with the script ./hack/dump_cache.sh can be used to trigger a dump of the internal cache into the logs. (#1541, @alculquicondor)
- The priority sorting within the cohort could be disabled by setting the feature gate PrioritySortingWithinCohort to false (#1406, @yaroslava-serdiuk)
- Visibility API: Add HA support. (#1554, @astefanutti)

### Bug or Regression

- Add Missing RBAC on finalizer sub-resources for job integrations. (#1486, @astefanutti)
- Add Mutating WebhookConfigurations for the AdmissionCheck, RayJob, and JobSet to helm charts (#1567, @B1F030)
- Add Validating/Mutating WebhookConfigurations for the KubeflowJobs like PyTorchJob (#1460, @tenzen-y)
- Added event for QuotaReserved and fixed event for Admitted to trigger when admission checks complete (#1436, @trasc)
- Avoid finished Workloads from blocking quota after a Kueue restart (#1689, @trasc)
- Avoid recreating a Workload for a finished Job and finalize a job when the workload is declared finished. (#1383, @achernevskii)
- Do not (re)create ProvReq if the state of admission check is Ready (#1617, @mimowo)
- Fix Kueue crashing at the log level 6 when re-admitting workloads (#1644, @mimowo)
- Fix a bug in the pod integration that unexpected errors will occur when the pod isn't found (#1512, @achernevskii)
- Fix a bug that plain pods managed by kueue will remain in a terminating state, due to a finalizer (#1342, @tenzen-y)
- Fix client-go libraries bug that can not operate clusterScoped resources like ClusterQueue and ResourceFlavor. (#1294, @tenzen-y)
- Fix fungibility policy `Preempt` where it was not able to utilize the next flavor if preemption was not possible. (#1366, @alculquicondor)
- Fix handling of preemption within a cohort when there is no borrowingLimit. In that case,
  during preemption, the permitted resources to borrow were calculated as if borrowingLimit=0, instead of unlimited.
  
  As a consequence, when using `reclaimWithinCohort`, it was possible that a workload, scheduled to ClusterQueue with no borrowingLimit, would preempt more workloads than needed, even though it could fit by borrowing. (#1561, @mimowo)
- Fix the synchronization of the admission check state based on recreated ProvisioningRequest (#1585, @mimowo)
- Fixed fungibility policy `whenCanPreempt: Preempt`. The admission should happen in the flavor for which preemptions were issued. (#1332, @alculquicondor)
- Kueue replicas are advertised as Ready only once the webhooks are functional.
  
  This allows users to wait with the first requests until the Kueue deployment is available, so that the 
  early requests don't fail. (#1676, @mimowo)
- Pending workload from StrictFIFO ClusterQueue doesn't block borrowing from other ClusterQueues (#1399, @yaroslava-serdiuk)
- Remove deleted pending workloads from the cache (#1679, @astefanutti)
- Remove finalizer from Workloads that are orphaned (have no owners). (#1523, @achernevskii)
- Trigger an eviction for an admitted Job after an admission check changed state to Rejected. (#1562, @trasc)
- Webhooks are served in non-leading replicas (#1509, @astefanutti)

### Other (Cleanup or Flake)

- Expose utilization functions to setup jobframework reconcilers and webhooks (#1630, @tenzen-y)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-13T19:19:56Z

LGTM
I'm looking forward to the new minor release!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-15T16:10:50Z

All tasks done.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-15T16:10:55Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1729#issuecomment-1946435138):

>All tasks done.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
