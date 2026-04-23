# Issue #6625: Release v0.12.8

**Summary**: Release v0.12.8

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6625

**Last updated**: 2025-08-22T13:26:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-20T09:01:43Z
- **Updated**: 2025-08-22T13:26:59Z
- **Closed**: 2025-08-22T13:26:58Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
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
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6647
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
      to production: https://github.com/kubernetes/k8s.io/pull/8434
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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6650
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/VWp8ywN47pw/m/5dadEUhHAQAJ
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
Changes since `v0.12.7`:

## Changes by Kind

### Bug or Regression

- FS: Fixing a bug where a preemptor ClusterQueue was unable to reclaim its nominal quota when the preemptee ClusterQueue can borrow a large number of resources from the parent ClusterQueue / Cohort (#6619, @pajakd)
- TAS: Fix a bug where new Workloads starve, caused by inadmissible workloads frequently requeueing due to unrelated Node LastHeartbeatTime update events. (#6636, @utam0k)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-20T09:04:20Z

We want to deliver https://github.com/kubernetes-sigs/kueue/pull/6617 and https://github.com/kubernetes-sigs/kueue/pull/6570. Now we are waiting for https://github.com/kubernetes-sigs/kueue/pull/6570.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-20T09:16:03Z

cc @mimowo @gabesaba @mwysokin @pajakd @PBundyra @amy @rajatphull @utam0k

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-20T13:11:08Z

/lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-20T13:13:59Z

Michal is OOO until the end of this month. LGTM for others (@tenzen-y and @gabesaba).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-20T13:15:23Z

We are aiming for 22nd August. > @utam0k

### Comment by [@utam0k](https://github.com/utam0k) — 2025-08-20T21:47:54Z

> We are aiming for 22nd August. > @utam0k 
> 

I will give you my PR revision by the end of the day.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T13:34:03Z

Thank you to everyone. Now, all required PRs have been merged for this release.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T16:30:30Z

I updated the release note.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-22T13:02:27Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.8 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.8
Digest: sha256:598e49c3ee17827a06052abe7bc2a9933dca731049b52c2c9c05e4ac5eb31a56
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.12.8'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.12.8'
        image: "registry.k8s.io/kueue/kueue:v0.12.8"
$
$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.12.8
v0.12.8: Pulling from kueue/kueue
03db832fd5aa: Pull complete 
Digest: sha256:35fd0b59acf868fd999342aeda972a6f4290d60706c7e8136832dad77e9ac357
...
{"level":"info","ts":"2025-08-22T12:59:10.321237672Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.12.8","gitCommit":"3c650fa2adb5817cf6ccc9d705a0eff73f04299f"}
$
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.12.8
v0.12.8: Pulling from kueue/kueueviz-backend
a09248112c15: Pull complete 
Digest: sha256:770989a553db42ae485d389ee6e6aae557d965d64f9669d31a3142e77ebd6fd4
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.12.8
$
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.12.8
v0.12.8: Pulling from kueue/kueueviz-frontend
Digest: sha256:16b9f965de006fc2f34eba34167a57a8f1d7bdb7083ea521f4a26e461676f5e7
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.12.8
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-22T13:26:54Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-22T13:26:59Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6625#issuecomment-3214383415):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
