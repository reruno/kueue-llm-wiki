# Issue #1256: Release v0.5.0

**Summary**: Release v0.5.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1256

**Last updated**: 2023-10-26T19:43:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-25T16:46:24Z
- **Updated**: 2023-10-26T19:43:17Z
- **Closed**: 2023-10-26T19:43:16Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 6

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
- [x] Update `README.md`, `CHANGELOG`, `charts/kueue/Chart.yaml` (`appVersion`) and `charts/kueue/values.yaml` (`controllerManager.manager.image.tag`) in the release branch: #1260
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
      updating `k8s.gcr.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/6022
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.5.0
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`. Link: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/07kedHB6J9o
- [x] Update `README.md`, `CHANGELOG`, `site/config.toml`, `charts/kueue/Chart.yaml` (`appVersion`) and `charts/kueue/values.yaml` (`controllerManager.manager.image.tag`) in `main` branch: #1262
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        https://github.com/kubernetes/test-infra/pull/31128


## Changelog

```markdown

Changes since `v0.4.0`:

## Changes by Kind

### Feature

- A mechanism for AdmissionChecks to provide labels, annotations, tolerations and node selectors to the pod templates when starting a job (#1180, @mimowo)
- A reference standalone controller that can be used to support plain Pods using taints and tolerations, which can be used in Kubernetes versions that don't support scheduling gates. (#1111, @nstogner)
- Add Active condition to AdmissionChecks (#1193, @trasc)
- Add optional cluster queue resource quota and usage metrics. (#982, @trasc)
- Add support for AdmissionChecks, a mechanism for internal or external components to influence whether a Workload can be admitted. (#1045, @trasc)
- Add support for single plain Pods. (#1072, @achernevskii)
- Add support for workload Priority (#1081, @Gekko0114)
- Add tolerations to ResourceFlavor. Kueue injects these tolerations to the jobs that are assigned to the flavor when admitted. (#1248, @trasc)
- Added pprof endpoints for profiling (#978, @stuton)
- Allow the admission of multiple workloads within one scheduling cycle while borrowing. (#1039, @trasc)
- An option to synchronize batch/job.completions with parallelism in case of partial admission (#971, @trasc)
- Expose cluster queue information about pending workloads (#1069, @stuton)
- Expose probe configurations to helm chart (#986, @yyzxw)
- Graduate Partial admission to Beta. (#1221, @trasc)
- Integrate with Cluster Autoscaler's ProvisioningRequest via two stage admission (#1154, @trasc)
- Manage cluster queue active state based on admission checks life cycle. (#1079, @trasc)
- Metrics for usage and reservations in ClusterQueues and LocalQueues. (#1206, @trasc)
- Options to allow workloads to borrow quota or preempt other workloads before trying the next flavor in the list (#849, @KunWuLuan)
- Support kubeflow.org/mxjob (#1183, @tenzen-y)
- Support kubeflow.org/paddlejob (#1142, @tenzen-y)
- Support kubeflow.org/pytorchjob (#995, @tenzen-y)
- Support kubeflow.org/tfjob (#1068, @tenzen-y)
- Support kubeflow.org/xgboostjob (#1114, @tenzen-y)
- Workload objects have the label `kueue.x-k8s.io/job-uid` where the value matches the uid of the parent job, whether that's a Job, MPIJob, RayJob, JobSet (#1032, @achernevskii)

### Bug or Regression

- Adjust resources (based on LimitRanges, PodOverhead and resource limits) on existing Workloads when a LocalQueue is created (#1197, @alculquicondor)
- Ensure the ClusterQueue status is updated as the number of pending workloads changes. (#1135, @mimowo)
- Fix resuming of RayJob after preempted. (#1156, @kerthcet)
- Fixed missing create verb for webhook (#1035, @stuton)
- Fixed scheduler to only allow one admission or preemption per cycle within a cohort that has ClusterQueues borrowing quota (#1023, @alculquicondor)
- Helm: Enable the JobSet integration by default (#1184, @tenzen-y)
- Improve job controller to be resilient to API failures during preemption (#1005, @alculquicondor)
- Prevent workloads in ClusterQueue with StrictFIFO from blocking higher priority workloads in other ClusterQueues in the same cohort that require preemption (#1024, @alculquicondor)
- Terminate Kueue when there is an internal failure during setup, so that it can be retried. (#1077, @alculquicondor)

### Other (Cleanup or Flake)

- Add client-go library for AdmissionCheck (#1104, @tenzen-y)
- Add mergeStrategy:merge to all conditions of API objects (#1089, @alculquicondor)
- Update ray-operator to v0.6.0 (#1231, @lowang-bh)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-25T16:47:20Z

LGTM

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-25T17:54:12Z

Release notes are up-to-date now. PTAL

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-10-25T18:04:03Z

lgtm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-25T21:57:46Z

Just missing https://github.com/kubernetes/test-infra/pull/31128 to merge

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-26T19:43:12Z

:rocket: 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-26T19:43:16Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1256#issuecomment-1781792463):

>:rocket: 
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
