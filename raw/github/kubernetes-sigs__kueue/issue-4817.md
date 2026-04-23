# Issue #4817: Release v0.11.2

**Summary**: Release v0.11.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4817

**Last updated**: 2025-03-28T19:39:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-28T12:48:12Z
- **Updated**: 2025-03-28T19:39:47Z
- **Closed**: 2025-03-28T19:29:35Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

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
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4826
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
      to production: https://github.com/kubernetes/k8s.io/pull/7949
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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4827
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://mail.google.com/mail/u/1/?ogbl#inbox/FMfcgzQZTqCVRFRpBnbKxPHsCXZbKgzj
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release:
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch:
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.11.1`:

## Changes by Kind

### Bug or Regression

- Fix bug which resulted in under-utilization of the resources in a Cohort.
  Now, when a ClusterQueue is configured with `preemption.reclaimWithinCohort: Any`,
  its resources can be lent out more freely, as we are certain that we can reclaim
  them later. Please see PR for detailed description of scenario. (#4822, @gabesaba)
- PodSetTopologyRequests are now configured only when TopologyAwareScheduling feature gate is enabled. (#4797, @mykysha)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T12:50:18Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T16:38:08Z

I took this release, and @mimowo is responsible for 0.10 patch release

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-28T17:00:36Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T18:14:04Z

```shell
$ docker run -it registry.k8s.io/kueue/kueue:v0.11.2
...
Digest: sha256:516dbe9dfba224936b1a9f01fd93f0d4a17de7284b4751803ac065a48b0d37c7
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.11.2 
...
{"level":"info","ts":"2025-03-28T18:13:00.509748179Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.11.2","gitCommit":"d8e79897435977b72338cd4f6f8e5cfc4eb87865"}
$
$ helm template oci://registry.k8s.io/kueue/charts/kueue --version 0.11.2 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.11.2
Digest: sha256:02c4857f5c83cdb1274c8ab9f07f7c6f5e3eb6d2041228dbcfedd27ce76f863a
        image: "registry.k8s.io/kueue/kueue:v0.11.2"
```
