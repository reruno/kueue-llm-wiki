# Issue #5232: Release v0.10.6

**Summary**: Release v0.10.6

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5232

**Last updated**: 2025-05-26T16:30:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-12T14:32:26Z
- **Updated**: 2025-05-26T16:30:42Z
- **Closed**: 2025-05-26T16:30:41Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 7

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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5355
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
      to production: https://github.com/kubernetes/k8s.io/pull/8133
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5359
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/fExLJh9ylJQ
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
## Changes by Kind

### Bug or Regression

- Fix Kueue crash caused by race condition when deleting ClusterQueue (#5295, @gabesaba)
- Fix RayJob webhook validation when `LocalQueueDefaulting` feature is enabled. (#5073, @MaysaMacedo)
- Fix a bug where PropagateResourceRequests would always trigger an API status patch call. (#5131, @alexeldeib)
- TAS: Fix RBAC configuration for the Topology API (#5121, @qti-haeyoon)
- TAS: Fix the bug where TAS workloads may be admitted after restart of the Kueue controller. (#5335, @mimowo)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T14:33:22Z

This will be the final patch release for v0.10. We (@tenzen-y and @mimowo) are going to release this patch in the early next week.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-19T14:08:05Z

We decided to postpone the patch release for tomorrow.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-26T16:08:57Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-26T16:09:01Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5232#issuecomment-2910190889):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-26T16:15:56Z

```shell
$ docker run -it registry.k8s.io/kueue/kueue:v0.10.6
Unable to find image 'registry.k8s.io/kueue/kueue:v0.10.6' locally
v0.10.6: Pulling from kueue/kueue
Digest: sha256:8d021d06dcec794a726cc708c9be3ac49c6a575763188708e15d783aad0aeefd
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.10.6
...
{"level":"info","ts":"2025-05-26T16:13:32.2015075Z","logger":"setup","caller":"kueue/main.go:141","msg":"Initializing","gitVersion":"v0.10.6","gitCommit":"85c195852dd2fbd7d1b229735b8bf5e1d15ceaba"}
```

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --version 0.10.6 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.10.6
Digest: sha256:8f430193efbd376a69749b4131ab722eee09df8e29260e2eb89d50668698c89c
        image: "registry.k8s.io/kueue/kueue:v0.10.6"
        image: "registry.k8s.io/kubebuilder/kube-rbac-proxy:v0.16.0"
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-26T16:30:37Z

Released 🎉  https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.6

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-26T16:30:41Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5232#issuecomment-2910228178):

>Released 🎉  https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.6
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
