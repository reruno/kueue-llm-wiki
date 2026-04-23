# Issue #6771: Release v0.12.9

**Summary**: Release v0.12.9

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6771

**Last updated**: 2025-09-12T17:18:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-09T12:54:53Z
- **Updated**: 2025-09-12T17:18:59Z
- **Closed**: 2025-09-12T17:18:58Z
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
  - [x] Submit a pull request with the changes: #6809 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8501
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [ ] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6810
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/_NriWvkbEdk
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
Changes since `v0.12.8`:

## Changes by Kind

### Bug or Regression

- FS: Fix the algorithm bug for identifying preemption candidates, as it could return a different
  set of preemption target workloads (pseudo random) in consecutive attempts in tie-break scenarios,
  resulting in excessive preemptions. (#6800, @PBundyra)
- Fix the validation messages when attempting to remove the queue-name label from a Deployment or StatefulSet. (#6716, @Panlq)
- Helm: Fixed a bug preventing Kueue from starting after installing via Helm with a release name other than "kueue" (#6802, @mbobrovskyi)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T14:55:38Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T16:50:38Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.9 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.9
Digest: sha256:fb73258b3c6a90066b1aa5ebacc7605f664a57832653afe01c21843008ebda92
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.12.9'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.12.9'
        image: "registry.k8s.io/kueue/kueue:v0.12.9"
$
$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.12.9
v0.12.9: Pulling from kueue/kueue
Digest: sha256:8d5ae2102d99e7e802629271ec69ee70abd6b86cde70bab2448ced2f3637431e
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.12.9
...
{"level":"info","ts":"2025-09-12T16:49:11.626197543Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.12.9","gitCommit":"01e95a1a078404353f8c978bdd8274e2c850ce97"}
$
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.12.9
v0.12.9: Pulling from kueue/kueueviz-backend
Digest: sha256:6564442552cf7622d590156a195ac36f59516ab9750adee000f209ee64e4f098
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.12.9
$
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.12.9
v0.12.9: Pulling from kueue/kueueviz-frontend
Digest: sha256:d2653026766f5e2f4a2aad0559b0bd48518ee8b0fb4b5157c870d8f949eb3d12
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.12.9
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T17:18:54Z

Closing as done.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-12T17:18:59Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6771#issuecomment-3286223651):

>Closing as done.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
