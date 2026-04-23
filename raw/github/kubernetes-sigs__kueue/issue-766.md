# Issue #766: Release v0.3.1

**Summary**: Release v0.3.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/766

**Last updated**: 2023-06-13T15:05:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-11T17:29:16Z
- **Updated**: 2023-06-13T15:05:30Z
- **Closed**: 2023-05-16T19:11:38Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 3

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [ ] All [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal
- [x] Verify that the changelog in this issue and CHANGELOG (#773) is up-to-date
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
      to production: https://github.com/kubernetes/k8s.io/pull/5288
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
- [x] Add a link to the tagged release in this issue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.3.1
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`
- [x] Add a link to the release announcement in this issue: https://groups.google.com/g/kubernetes-sig-scheduling/c/8gYCrI-MqGU
- [x] For a major or minor release, update `README.md`, `docs/setup/install.md`, `charts/kueue/Chart.yaml` (`appVersion`) and `chats/kueue/values.yaml` (`controllerManager.manager.image.tag`) in `main` branch: #774


## Changelog

```
- Fix a bug that the validation webhook doesn't validate the queue name set as a label when creating MPIJob. #711
- Fix a bug that updates a queue name in workloads with an empty value when using framework jobs that use batch/job internally, such as MPIJob. #713
- Fix a bug in which borrowed values are set to a non-zero value even though the ClusterQueue doesn't belong to a cohort. #759 
- Fix: Enforce borrowed=0 if ClusterQueue doesn't belong to a cohort. #761
- Fixed adding suspend=true job/mpijob by the default webhook. #765
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-11T17:30:18Z

Waiting on an integration test for #758

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-11T17:31:00Z

/assign
/cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-11T17:36:13Z

Thank you for creating this!
