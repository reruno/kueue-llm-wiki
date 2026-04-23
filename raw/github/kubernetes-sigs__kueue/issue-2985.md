# Issue #2985: Release v0.8.1

**Summary**: Release v0.8.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2985

**Last updated**: 2024-09-06T15:13:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-04T17:49:51Z
- **Updated**: 2024-09-06T15:13:29Z
- **Closed**: 2024-09-06T15:13:26Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
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
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #2997 
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
      `us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:$VERSION`
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: kubernetes/k8s.io#7267
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] Update the below files with respective values in `main` branch :
  - Latest version in `README.md`
  - Latest version in `cmd/experimental/kjobctl/docs/installation.md`
  - Release notes in the `CHANGELOG`
  - `version` in `site/hugo.toml`
  - `appVersion` in `charts/kueue/Chart.yaml`
  - `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [x] Create the presubmits jobs for the next patch release:
        <!-- example https://github.com/kubernetes/test-infra/pull/33107 -->


## Changelog

```markdown
Changes since `v0.8.0`:

### Feature

- Add gauge metric admission_cycle_preemption_skips that reports the number of Workloads in a ClusterQueue
  that got preemptions candidates, but had to be skipped in the last cycle. (#2942, @alculquicondor)
- Publish images via artifact registry (#2832, @alculquicondor)

### Bug or Regression

- CLI: Support `-` and `.` in the resource flavor name on `create cq` (#2706, @trasc)
- Detect and enable support for job CRDs installed after Kueue starts. (#2991, @ChristianZaccaria)
- Fix over-admission after deleting resources from borrowing ClusterQueue. (#2879, @mbobrovskyi)
- Fix support for kuberay 1.2.x (#2983, @mbobrovskyi)
- Helm: Fix a bug for "unclosed action error". (#2688, @mbobrovskyi)
- Prevent infinite preemption loop when PrioritySortingWithinCohort=false
  is used together with borrowWithinCohort. (#2831, @mimowo)
- Support for helm charts in the us-central1-docker.pkg.dev/k8s-staging-images/charts repository (#2834, @IrvingMg)
- Update Flavor selection logic to prefer Flavors which allow reclamation of lent nominal quota, over Flavors which require preempting workloads within the ClusterQueue. This matches the behavior in the single Flavor case. (#2829, @gabesaba)
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-04T18:17:44Z

Replace @k8s-infra-cherrypick-robot for the original authors.

Other than that, LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-04T19:32:19Z

LGTM

Remaining TODO: https://github.com/kubernetes-sigs/kueue/pull/2574

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-05T15:05:34Z

@tenzen-y @alculquicondor I have updated the release notes after https://github.com/kubernetes-sigs/kueue/pull/2574 got merged, PTAL

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-05T16:22:42Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-05T19:03:41Z

LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T15:13:22Z

/close
@tenzen-y @alculquicondor Thank you for giving me the opportunity to do the release, and guiding me in the process!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-06T15:13:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2985#issuecomment-2334277098):

>/close
>@tenzen-y @alculquicondor Thank you for giving me the opportunity to do the release, and guiding me in the process!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
