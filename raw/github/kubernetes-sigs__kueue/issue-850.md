# Issue #850: Release v0.3.2

**Summary**: Release v0.3.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/850

**Last updated**: 2023-06-13T15:40:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-13T14:07:01Z
- **Updated**: 2023-06-13T15:40:32Z
- **Closed**: 2023-06-13T15:34:01Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 1

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal.
  At least two for minor or major releases. At least one for a patch release.
- [x] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date #851
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
      to production: https://github.com/kubernetes/k8s.io/pull/5406
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.3.2
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`. Link: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/yiL9P2vXXhI
- [x] Update `README.md`, `CHANGELOG`, `site/content/en/installation`, `charts/kueue/Chart.yaml` (`appVersion`) and `chats/kueue/values.yaml` (`controllerManager.manager.image.tag`) in `main` branch: #853


## Changelog

```markdown
Changes since `v0.3.1`:

### Bug or Regression

- Add permission to update frameworkjob status. (#798, @tenzen-y)
- Fix a bug where a child batch/job of an unmanaged parent (doesn't have queue name) was being suspended. (#839, @tenzen-y)
- Fix panic in cluster queue if resources and coveredResources do not have the same length. (#799, @kannon92)
- Fix: Potential over-admission within cohort when borrowing. (#822, @trasc)
- Fixed preemption to prefer preempting workloads that were more recently admitted. (#845, @stuton)
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-13T14:07:24Z

/assign @tenzen-y @alculquicondor
