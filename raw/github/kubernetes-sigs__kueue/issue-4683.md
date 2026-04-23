# Issue #4683: Release v0.9.5

**Summary**: Release v0.9.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4683

**Last updated**: 2025-03-19T15:46:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-19T09:57:15Z
- **Updated**: 2025-03-19T15:46:46Z
- **Closed**: 2025-03-19T15:46:45Z
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
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4688
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
      via UI or `gh release --repo kubernetes-sigs/kueue upload <tag> artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to 
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7898
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.5
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4691
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/GwLeBu7U6E4/m/P3xgDNJkBAAJ
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release:
        <!-- example presubmit: https://github.com/kubernetes/test-infra/pull/33107 -->
        <!-- example periodic: https://github.com/kubernetes/test-infra/pull/33833 -->


## Changelog

```markdown
Changes since `v0.9.4`:

## Changes by Kind

### Bug or Regression

- Fixes a bug that would result in default values not being properly set on creation for enabled integrations whose API was not available when the Kueue controller started. (#4559, @dgrove-oss)
- Helm: Fixed a bug that prometheus namespace is enforced with namespace the same as kueue-controller-manager (#4488, @kannon92)
- TAS: Fix a bug that TopolologyUngator cound not be triggered the leader change when enabled HA mode (#4657, @tenzen-y)
- Update FairSharing to be incompatible with ClusterQueue.Preemption.BorrowWithinCohort. Using these parameters together is a no-op, and will be validated against in future releases. This change fixes an edge case which triggered an infinite preemption loop when these two parameters were combined. (#4165, @gabesaba)

### Other (Cleanup or Flake)

- Publish helm charts to the Kueue staging repository `http://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts`, 
  so that they can be promoted to the permanent location under `registry.k8s.io/kueue/charts`. (#4685, @mimowo)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T10:04:38Z

We aim for the patch release today to test the new helm publication & promotion procedure: https://github.com/kubernetes-sigs/kueue/pull/4680 before 0.11.0

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T12:05:22Z

cc @tenzen-y @kannon92 @dgrove-oss @mwysokin @gabesaba @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-19T12:48:45Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-19T12:48:55Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-19T14:21:44Z

Manager

```shell
$ docker run -it registry.k8s.io/kueue/kueue:v0.9.5
...
{"level":"info","ts":"2025-03-19T14:19:20.408315261Z","logger":"setup","caller":"kueue/main.go:122","msg":"Initializing","gitVersion":"v0.9.5","gitCommit":"12d520ce0dfea38f0a3ee55a630c7e26b0e5b517"}
```

Charts

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --version 0.9.5 | grep registry.k8s.io/kueue/kueue:v0.9.5
Pulled: registry.k8s.io/kueue/charts/kueue:0.9.5
Digest: sha256:80591f127d58324a4a82967d3657237f1496f586d48580b74282bd83fa4747d3
        image: "registry.k8s.io/kueue/kueue:v0.9.5"
$ helm show chart oci://registry.k8s.io/kueue/charts/kueue --version ^0.9
Pulled: registry.k8s.io/kueue/charts/kueue:0.9.5
Digest: sha256:80591f127d58324a4a82967d3657237f1496f586d48580b74282bd83fa4747d3
apiVersion: v2
appVersion: v0.9.5
description: Kueue is a set of APIs and controller for job queueing. It is a job-level
  manager that decides when a job should be admitted to start (as in pods can be created)
  and when it should stop (as in active pods should be deleted).
name: kueue
type: application
version: v0.9.5
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-19T15:46:40Z

Released: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.5

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T15:46:46Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4683#issuecomment-2737140631):

>Released: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.5
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
