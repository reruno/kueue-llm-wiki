# Issue #2542: Release v0.7.1

**Summary**: Release v0.7.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2542

**Last updated**: 2024-09-06T09:28:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-07-05T18:32:10Z
- **Updated**: 2024-09-06T09:28:38Z
- **Closed**: 2024-07-08T20:03:13Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
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
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #2543
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
      to production: kubernetes/k8s.io#6956
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.7.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] Update the below files with respective values in `main` branch : #2555
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
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->


## Changelog

```markdown
Changes since `v0.7.0`:

### Feature

- Improved logging for scheduling and preemption in levels 4 and 5 (#2510, @gabesaba, @alculquicondor)
- MultiKueue: Remove remote objects synchronously when the worker cluster is reachable. (#2360, @trasc)

### Bug or Regression

- Fix check that prevents preemptions when a workload requests 0 for a resource that is at nominal or over it. (#2524, @mbobrovskyi, @alculquicondor)
- Fix for the scenario when a workload doesn't match some resource flavors due to affinity or taints
  could cause the workload to be continuously retried. (#2440, @KunWuLuan)
- Fix missing fairSharingStatus in ClusterQueue (#2432, @mbobrovskyi)
- Fix missing metric cluster_queue_status. (#2475, @mbobrovskyi)
- Fix panic that could occur when a ClusterQueue is deleted while Kueue was updating the ClusterQueue status. (#2464, @mbobrovskyi)
- Fix panic when there is not enough quota to assign flavors to a Workload in the cohort, when FairSharing is enabled. (#2449, @mbobrovskyi)
- Fix performance issue in logging when processing LocalQueues. (#2492, @alexandear)
- Fix race condition on delete workload from queue manager. (#2465, @mbobrovskyi)
- MultiKueue: Do not reject a JobSet if the corresponding cluster queue doesn't exist (#2442, @vladikkuzn)
- MultiKueue: Skip garbage collection for disconnected clients which could occasionally result in panic. (#2370, @trasc)
- Show weightedShare in ClusterQueue status.fairSharing even if the value is zero (#2522, @alculquicondor)
- Skip duplicate Tolerations when an admission check introduces a toleration that the job also set. (#2499, @trasc)
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-08T20:03:10Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-08T20:03:14Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2542#issuecomment-2215123328):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
