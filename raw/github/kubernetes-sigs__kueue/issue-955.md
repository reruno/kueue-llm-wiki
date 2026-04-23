# Issue #955: Release v0.4.0

**Summary**: Release v0.4.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/955

**Last updated**: 2023-07-07T15:15:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-06T14:37:21Z
- **Updated**: 2023-07-07T15:15:10Z
- **Closed**: 2023-07-07T15:15:08Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 8

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
- [x] For major or minor releases, update things like README, deployment templates, docs, configuration, test/e2e flags.
      Submit a PR against the release branch: #958
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
      to production: https://github.com/kubernetes/k8s.io/pull/5526
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.4.0
- [x] For a major or minor release, merge the documentation from the `website-release-x.y` into `main`.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`. Link: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/B22sfn6_-mA
- [x] Update `README.md`, `CHANGELOG`, `site/content/en/installation`, `charts/kueue/Chart.yaml` (`appVersion`) and `chats/kueue/values.yaml` (`controllerManager.manager.image.tag`) in `main` branch: #960
- [x] For a major or minor release, create an unannotated _devel_ tag in the
      `main` branch, on the first commit that gets merged after the release
       branch has been created (presumably the README update commit above), and, push the tag:
      `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
      This ensures that the devel builds on the `main` branch will have a meaningful version number.


## Changelog

```markdown
Changes since `v0.3.0`:

### API Change

- Report resource usage in LocalQueue. (#737, @tenzen-y)

### Feature

- Add client-go libraries. (#789, @tenzen-y)
- Add support for Kuberay's RayJobs. (#667, @trasc)
- Add support for dynamic reclaim in the JobSet integration. (#901, @trasc)
- Add support for partial workload admission (#771, @trasc)
- Add the support for dynamic resources reclaim. (#756, @trasc)
- Allow scheduler to admit more jobs when the head job have not reached the PodReady=true status. (#708, @KunWuLuan)
- Allow specifying the manager pod and container security context instead of hardcoded values (#878, @bh-tt)
- Feature gates for alpha/experimental features is introduced to Kueue Project. (#788, @kerthcet)
- Ignoring integrations if crd wasn't installed otherwise all integrations are enabled by default (#883, @stuton)
- Integrate JobSet into kueue (#762, @mcariatm)

### Bug or Regression

- Add permission to update frameworkjob status. (#797, @tenzen-y)
- Fix a bug that updates events for clusterQueues are created endlessly. (#907, @tenzen-y)
- Fix a bug where a child batch/job of an unmanaged parent (doesn't have queue name) was being suspended. (#835, @tenzen-y)
- Fix panic in cluster queue if resources and coveredResources do not have the same length. (#787, @kannon92)
- Fix: Enforce borrowed=0 if ClusterQueue doesn't belong to a cohort. (#759, @tenzen-y)
- Fix: Potential over-admission within cohort when borrowing. (#805, @trasc)
- Fixed preemption to prefer preempting workloads that were more recently admitted. (#843, @stuton)
- Fixed the suspend=true add to the job/mpijob by the default webhook has not taken effect. (#758, @fjding)

### Other (Cleanup or Flake)

- Add validation for child jobs without ownerReference. (#865, @tenzen-y)
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-06T14:38:44Z

cc @tenzen-y @kerthcet

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-06T14:40:36Z

LGTM

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-06T15:18:09Z

Great! 🎉🎉🎉

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-07-07T02:37:51Z

Looks good to me!

### Comment by [@denkensk](https://github.com/denkensk) — 2023-07-07T02:43:48Z

LGTM 👍🏻

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-07T13:37:12Z

added release notes

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-07T15:15:04Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-07T15:15:09Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/955#issuecomment-1625565325):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
