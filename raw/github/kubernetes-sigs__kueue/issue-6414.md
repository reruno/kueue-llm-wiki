# Issue #6414: Release v0.13.2

**Summary**: Release v0.13.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6414

**Last updated**: 2025-08-11T16:45:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-04T09:20:55Z
- **Updated**: 2025-08-11T16:45:53Z
- **Closed**: 2025-08-11T16:45:52Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@gabesaba](https://github.com/gabesaba), [@tenzen-y](https://github.com/tenzen-y)
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
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: <!-- PREPARE_PULL --> <!-- example #211 #214 -->
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
      to production: <!-- example kubernetes/k8s.io#7899 -->
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6536
  - [ ] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
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
Changes since `v0.13.1`:

## Changes by Kind

### Bug or Regression

- ElasticJobs: Fix the bug that scheduling of the Pending workloads was not triggered on scale-down of the running 
  elastic Job which could result in admitting one or more of the queued workloads. (#6407, @ichekrygin)
- Fix support for PodGroup integration used by external controllers, which determine the 
  the target LocalQueue and the group size only later. In that case the hash would not be 
  computed resulting in downstream issues for ProvisioningRequest.
  
  Now such an external controller can indicate the control over the PodGroup by adding
  the `kueue.x-k8s.io/pod-suspending-parent` annotation, and later patch the Pods by setting
  other metadata, like the kueue.x-k8s.io/queue-name label to initiate scheduling of the PodGroup. (#6461, @pawloch00)
- TAS: fix the bug that Kueue is crashing when PodSet has size 0, eg. no workers in LeaderWorkerSet instance. (#6522, @mimowo)
```

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-11T12:09:19Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T12:10:30Z

LGTM

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-11T12:33:43Z

Generated release notes:

```
release-notes --org kubernetes-sigs --repo kueue --branch release-0.13 --start-sha 81236abed536034d41156c5af20d614590f82935 --end-sha 5174e3b2c94869544f3a464f7477e1af71aa3dfd --dependencies=false --required-author=""
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T12:36:22Z

@gabesaba Could we use this form, and replace @ k8s-infra-cherrypick-robot with proper ones?

```
Changes since `v0.13.1`:
## Changes by Kind

### Bug or Regression

- ElasticJobs: Fix the bug that scheduling of the Pending workloads was not triggered on scale-down of the running 
  elastic Job which could result in admitting one or more of the queued workloads. (#6407, @k8s-infra-cherrypick-robot)
- Fix support for PodGroup integration used by external controllers, which determine the 
  the target LocalQueue and the group size only later. In that case the hash would not be 
  computed resulting in downstream issues for ProvisioningRequest.
  
  Now such an external controller can indicate the control over the PodGroup by adding
  the `kueue.x-k8s.io/pod-suspending-parent` annotation, and later patch the Pods by setting
  other metadata, like the kueue.x-k8s.io/queue-name label to initiate scheduling of the PodGroup. (#6461, @k8s-infra-cherrypick-robot)
- TAS: fix the bug that Kueue is crashing when PodSet has size 0, eg. no workers in LeaderWorkerSet instance. (#6522, @k8s-infra-cherrypick-robot)
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T12:51:41Z

Oh yes, the latest released "release-notes" script  may not yet contain these fixes: https://github.com/kubernetes/release/pulls?q=is%3Apr+author%3AIrvingMg+is%3Aclosed

So for now I compiled the script locally.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T12:55:56Z

Opened https://github.com/kubernetes/release/issues/4083 to track the release of the script

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T12:58:25Z

We can install the latest one with `GOBIN=$(pwd)/bin go install k8s.io/release/cmd/release-notes@master`.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-11T14:15:00Z

Verified images promoted
```
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.2 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.2
Digest: sha256:27b66b32722f4cfd7a08150322994f0d04c093e90349ad1881589d3567070fc7
```
```
$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.2
v0.13.2: Pulling from kueue/kueue
Digest: sha256:58f1cf049726926b62860c29f8aa2a9d6666dce0ec11d1cc7daa85043f7f3775
Status: Image is up to date for registry.k8s.io/kueue/kueue:v0.13.2
```
```
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.2
v0.13.2: Pulling from kueue/kueueviz-backend
Digest: sha256:fd371fd8e217b16144f563b7e6be3b30fbfba707bb4c97fece1b44ef39f00d49
Status: Image is up to date for registry.k8s.io/kueue/kueueviz-backend:v0.13.2
```
```
docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.2
v0.13.2: Pulling from kueue/kueueviz-frontend
Digest: sha256:5bd9700c66bf631b63e38c8e4056423a93d605135ade258743e4e950fb8d01b4
Status: Image is up to date for registry.k8s.io/kueue/kueueviz-frontend:v0.13.2

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T16:45:48Z

/close 
Just marked `Submit a pull request with the changes: Update main with release 0.13.2 #6536` and `Send an announcement email to sig-scheduling@kubernetes.io and wg-batch@kubernetes.io with the subject [ANNOUNCE] kueue $VERSION is released.`

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-11T16:45:53Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6414#issuecomment-3175855651):

>/close 
>Just marked `Submit a pull request with the changes: Update main with release 0.13.2 #6536` and `Send an announcement email to sig-scheduling@kubernetes.io and wg-batch@kubernetes.io with the subject [ANNOUNCE] kueue $VERSION is released.`


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
