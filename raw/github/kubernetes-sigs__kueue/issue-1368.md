# Issue #1368: Release v0.5.1

**Summary**: Release v0.5.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1368

**Last updated**: 2023-11-29T15:40:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-11-27T10:51:32Z
- **Updated**: 2023-11-29T15:40:19Z
- **Closed**: 2023-11-29T01:27:49Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 6

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal.
  At least two for minor or major releases. At least one for a patch release.
- [x] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date
  - [x] Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes.
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2`
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] an OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update `README.md`, `CHANGELOG`, `charts/kueue/Chart.yaml` (`appVersion`) and `charts/kueue/values.yaml` (`controllerManager.manager.image.tag`) in the release branch: #1374
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
      updating `k8s.gcr.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/6131
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.5.1
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`. Link: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/1hholD9XBa0
- [x] Update `README.md`, `CHANGELOG`, `site/config.toml`, `charts/kueue/Chart.yaml` (`appVersion`) and `charts/kueue/values.yaml` (`controllerManager.manager.image.tag`) in `main` branch: https://github.com/kubernetes-sigs/kueue/pull/1375
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
Changes since `v0.5.0`:

### Bug or Regression

- Fix client-go libraries bug that can not operate clusterScoped resources like ClusterQueue and ResourceFlavor. (#1294, @tenzen-y)
- Fixed fungiblity policy `whenCanPreempt: Preempt`. The admission should happen in the flavor for which preemptions were issued. (#1332, @alculquicondor)
- Fix a bug that plain pods managed by kueue will remain a terminating condition forever. (#1342, @tenzen-y)
- Fix fungibility policy `Preempt` where it was not able to utilize the next flavor if preemption was not possible. (#1366, @alculquicondor, @KunWuLuan)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-27T10:51:44Z

cc: @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-27T11:01:16Z

We need to wait to cut a patch release until https://github.com/kubernetes-sigs/kueue/pull/1366 is merged.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-28T15:23:40Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-29T01:27:45Z

Thanks @alculquicondor!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-11-29T01:27:50Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1368#issuecomment-1831046712):

>Thanks @alculquicondor!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-29T15:40:18Z

/close
