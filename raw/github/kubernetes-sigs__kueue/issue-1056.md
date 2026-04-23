# Issue #1056: Release v0.4.1

**Summary**: Release v0.4.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1056

**Last updated**: 2023-08-15T14:01:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-14T20:27:48Z
- **Updated**: 2023-08-15T14:01:09Z
- **Closed**: 2023-08-15T13:59:22Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 2

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
      to production: https://github.com/kubernetes/k8s.io/pull/5721
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.4.1
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`. Link: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/vQld0eIC8mg
- [x] Update `README.md`, `CHANGELOG`, `site/content/en/installation`, `charts/kueue/Chart.yaml` (`appVersion`) and `chats/kueue/values.yaml` (`controllerManager.manager.image.tag`) in `main` branch: #1058


## Changelog

```markdown
### Bug or Regression

- Fixed missing create verb for webhook (#1053, @stuton )
- Fixed scheduler to only allow one admission or preemption per cycle within a cohort that has ClusterQueues borrowing quota (#1029, @alculquicondor)
- Prevent workloads in ClusterQueue with StrictFIFO from blocking higher priority workloads in other ClusterQueues in the same cohort that require preemption (#1030, @alculquicondor)
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-14T20:29:22Z

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-15T04:54:59Z

It looks good to me! Thanks!
