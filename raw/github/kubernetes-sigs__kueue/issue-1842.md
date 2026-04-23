# Issue #1842: Release v0.6.1

**Summary**: Release v0.6.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1842

**Last updated**: 2024-03-15T12:17:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-03-14T16:25:21Z
- **Updated**: 2024-03-15T12:17:12Z
- **Closed**: 2024-03-15T12:17:10Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

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
  - [x] Submit a pull request with the changes: #1847
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
      to production: https://github.com/kubernetes/k8s.io/pull/6578
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.6.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/gHCQETA8x2s
- [x] Update the below files with respective values in `main` branch :
  - Latest version in `README.md`
  - Release notes in the `CHANGELOG`
  - `version` in `site/config.toml`
  - `appVersion` in `charts/kueue/Chart.yaml`
  - `last-updated`, `last-reviewed`, `commit-hash`, `project-release`, and `distribution-points` in `SECURITY-INSIGHTS.yaml`
  - https://github.com/kubernetes-sigs/kueue/pull/1848
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
Changes Since `v0.6.0`:

### Feature

- Added MultiKueue worker connection monitoring and reconnect. (#1809, @trasc)
- The Failed pods in a pod-group are finalized once a replacement pods are created. (#1801, @trasc)

### Bug or Regression

- Exclude Pod labels, preemptionPolicy and container images when determining whether pods in a pod group have the same shape. (#1760, @alculquicondor)
- Fix incorrect quota management when lendingLimit enabled in preemption (#1826, @kerthcet, @B1F030)
- Fix the configuration for the number of reconcilers for the Pod integration. It was only reconciling one group at a time. (#1837, @alculquicondor)
- Kueue visibility API is no longer installed by default. Users can install it via helm or applying the visibility-api.yaml artifact. (#1764, @trasc)
- WaitForPodsReady: Fix a bug that the requeueState isn't reset. (#1843, @tenzen-y)

### Other (Cleanup or Flake)

- Avoid API calls for admission attempts when Workload already has condition Admitted=false (#1845, @alculquicondor)
- Skip requeueing of Workloads when there is a status update for a ClusterQueue, saving on API calls for Workloads that were already attempted for admission. (#1832, @alculquicondor)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T16:32:16Z

@mimowo @alculquicondor Please let me know if there is any possible issues we should include in this release.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-14T17:48:17Z

Just https://github.com/kubernetes-sigs/kueue/pull/1845

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T17:57:38Z

~~#1846 should be included in this.~~

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-14T18:00:55Z

#1846 does not affect 0.6, right?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T18:02:00Z

> #1846 does not affect 0.6, right?

Yes, that's right. I found it by @astefanutti's comment.

https://github.com/kubernetes-sigs/kueue/pull/1846#issuecomment-1998026703

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-14T19:04:26Z

PTAL at release notes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T19:10:16Z

> PTAL at release notes.

I removed unnecessary spaces from release notes.
Could you perform a command to get the release note again?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-14T19:16:48Z

It looks like there was only one. Updated. And #1847 as well.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T19:17:16Z

> It looks like there was only one. Updated. And #1847 as well.

LGTM!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-15T12:17:06Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-15T12:17:11Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1842#issuecomment-1999545050):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
