# Issue #1539: Release v0.5.2

**Summary**: Release v0.5.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1539

**Last updated**: 2024-01-18T22:50:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-01-02T19:51:13Z
- **Updated**: 2024-01-18T22:50:53Z
- **Closed**: 2024-01-18T22:50:51Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
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
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2`
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] an OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update `README.md`, `CHANGELOG`, `charts/kueue/Chart.yaml` (`appVersion`) and `charts/kueue/values.yaml` (`controllerManager.manager.image.tag`) in the release branch: #1610
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
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/6292
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] Update the below files with respective values in `main` branch : 
  - Latest version in `README.md`
  - Release notes in the `CHANGELOG`
  - `version` in `site/config.toml`
  - `appVersion` in `charts/kueue/Chart.yaml` 
  - `last-updated`, `last-reviewed`, `commit-hash`, `project-release`, and `distribution-points` in `SECURITY-INSIGHTS.yaml`
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
Changes since `v0.5.1`:

### Bug or Regression

- Add Missing RBAC on integration finalizers sub-resources (#1486, @astefanutti)
- Added event for QuotaReserved and fixed event for Admitted to trigger when admission checks complete (#1436, @trasc)
- Avoid recreating a Workload for a finished Job and finalize a job when the workload is declared finished. (#1572, @alculquicondor)
- Fix a bug in the pod integration where a Workload can be left with a finalizer when a pod is not found. (#1524, @achernevskii)
- Remove finalizer from Workloads that are orphaned (have no owners). (#1523, @achernevskii, @woehrl01, @trasc)
- Add Mutating WebhookConfigurations for the AdmissionCheck, RayJob, and JobSet to helm charts (#1570, @B1F030)
- Add Validating/Mutating WebhookConfigurations for the KubeflowJobs like PyTorchJob (#1462, @tenzen-y)
- Add events for transitions of the provisioning AdmissionCheck (#1394, @stuton)
- Support for retry of provisioning request. (#1595, @mimowo)
- Webhooks are served in non-leading replicas (#1511, @astefanutti)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T19:51:24Z

cc @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-04T09:11:56Z

We're waiting for https://github.com/kubernetes-sigs/kueue/pull/1523.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-11T13:34:59Z

Also, we're waiting for #1567.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-15T16:31:53Z

All waiting PRs were done.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-15T18:58:04Z

I want to add #1585

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-16T04:59:47Z

> I want to add #1585

It makes sense.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-18T18:42:42Z

All required PRs are completed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-18T19:16:20Z

I updated the release-note.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-18T19:25:22Z

Release notes LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-18T22:50:48Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-18T22:50:52Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1539#issuecomment-1899344662):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
