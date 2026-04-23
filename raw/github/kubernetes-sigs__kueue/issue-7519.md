# Issue #7519: Release v0.13.9

**Summary**: Release v0.13.9

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7519

**Last updated**: 2025-11-06T13:59:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-04T08:22:58Z
- **Updated**: 2025-11-06T13:59:04Z
- **Closed**: 2025-11-06T13:59:03Z
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
  - [x] Submit a pull request with the changes: #7560 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8736
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.9
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7562
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [ ] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.13.8`:

## Changes by Kind

### Feature

- `ReclaimablePods` feature gate is introduced to enable users switching on and off the reclaimable Pods feature (#7536, @PBundyra)

### Bug or Regression

- Fix eviction of jobs with memory requests in decimal format (#7557, @brejman)
- Fix the bug for the StatefulSet integration that the scale up could get stuck if
  triggered immediately after scale down to zero. (#7499, @IrvingMg)
- MultiKueue: Remove remoteClient from clusterReconciler when kubeconfig is detected as invalid or insecure, preventing workloads from being admitted to misconfigured clusters. (#7516, @mszadkow)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-06T12:13:16Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-06T13:35:40Z

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.9 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.9
Digest: sha256:651f65de45e318c4b915dab92bfe0d1a50cd74fa9a406c0a45095b59ab09baf7
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.9'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.9'
        image: "registry.k8s.io/kueue/kueue:v0.13.9"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.9
v0.13.9: Pulling from kueue/kueue
56a7c184c825: Pull complete 
Digest: sha256:d284817aecdda9e415ffc507af67ded086c59c92cb8b1831f55b8c87d3028a51
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.13.9
...
{"level":"info","ts":"2025-11-06T13:34:29.217737091Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.9","gitCommit":"6a40455760011f0fe11a252ea40ba3a667e7039c","buildDate":"2025-11-06T12:54:00Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.9
v0.13.9: Pulling from kueue/kueueviz-backend
8d3280565b84: Pull complete 
Digest: sha256:7d4be7add03de0cb5f06d87c048c4e3cd2b21b8df37eeda443fc71394d080532
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.13.9

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.9
v0.13.9: Pulling from kueue/kueueviz-frontend
Digest: sha256:511bca1d996f8f478d089f8fc04ae890dd7ec65217e674e9e3f0773a148ca5a7
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.13.9
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-06T13:58:58Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-06T13:59:04Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7519#issuecomment-3497395977):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
