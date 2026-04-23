# Issue #7186: Release v0.14.1

**Summary**: Release v0.14.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7186

**Last updated**: 2025-10-08T11:36:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-07T09:36:19Z
- **Updated**: 2025-10-08T11:36:20Z
- **Closed**: 2025-10-08T11:36:19Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 5

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
  - [x] Submit a pull request with the changes: #7204 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8614
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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7205
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/ma0qKPtWjyU/m/OB39_v5gBQAJ
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
Changes since `v0.14.0`:

## Changes by Kind

### Bug or Regression

- Add rbac for train job for kueue-batch-admin and kueue-batch-user (#7198, @kannon92)
- Fix invalid annotations path being reported in `JobSet` topology validations. (#7191, @kshalot)
- Fix malformed annotations paths being reported for `RayJob` and `RayCluster` head group specs. (#7185, @kshalot)
- With BestEffortFIFO enabled, we will keep attempting to schedule a workload as long as
  it is waiting for preemption targets to complete. This fixes a bugs where an inadmissible
  workload went back to head of queue, in front of the preempting workload, allowing
  preempted workloads to reschedule (#7197, @gabesaba)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T09:54:07Z

I have prepared the release issue, but we are yet waiting for https://github.com/kubernetes-sigs/kueue/pull/7157

cc @tenzen-y @gabesaba @amy @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-07T12:14:55Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-08T10:26:24Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.1 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.1
Digest: sha256:b146879997b68f355b730da28413adb3fba1343d352f3dda4f9956b3a3bcd3ce
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.1'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.1'
        image: "registry.k8s.io/kueue/kueue:v0.14.1"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.14.1
v0.14.1: Pulling from kueue/kueue
ffcc74278c73: Pull complete 
Digest: sha256:f5e75ceaa689176fbbc8cedaf77e85adf339a2cefb11cf913e29b72126d25537
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.1
...
{"level":"info","ts":"2025-10-08T10:25:31.133089377Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.1","gitCommit":"bcdc1e482ba64f56fee107a1e5a27646825ab9e6","buildDate":"2025-10-08T09:40:15Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.1
v0.14.1: Pulling from kueue/kueueviz-backend
e3687565fdde: Pull complete 
Digest: sha256:5e3a9289da6e485e5f02ae84eb38eb69aacdfbe3044d0f1192d17d2e13651167
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.1

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.1
v0.14.1: Pulling from kueue/kueueviz-frontend
Digest: sha256:d0407e793f356f8272d077421e267c5a4cba267a6a362ce39ee25f14af525ccc
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.1

```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-08T11:36:14Z

DONE
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-08T11:36:20Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7186#issuecomment-3381107708):

>DONE
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
