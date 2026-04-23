# Issue #3521: Release v0.9.1

**Summary**: Release v0.9.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3521

**Last updated**: 2024-11-18T12:43:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-13T10:06:16Z
- **Updated**: 2024-11-18T12:43:32Z
- **Closed**: 2024-11-18T12:43:30Z
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
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/3567
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
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7530
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/3573
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`. 
  - [x] wg-batch: https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/2uHG0Usmk7k
  - [x] sig-scheduling: https://groups.google.com/u/1/g/kubernetes-sig-scheduling/c/k7TH7s9zGGw
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits jobs for the next patch release:
        <!-- example https://github.com/kubernetes/test-infra/pull/33107 -->


## Changelog

```markdown

Changes since `v0.9.0`:

## Changes by Kind

### Bug or Regression

- Change, and in some scenarios fix, the status message displayed to user when a workload doesn't fit in available capacity. (#3549, @gabesaba)
- Determine borrowing more accurately, allowing preempting workloads which fit in nominal quota to schedule faster (#3550, @gabesaba)
- Fix accounting for usage coming from TAS workloads using multiple resources. The usage was multiplied
  by the number of resources requested by a workload, which could result in under-utilization of the cluster.
  It also manifested itself in the message in the workload status which could contain negative numbers. (#3513, @mimowo)
- Fix computing the topology assignment for workloads using multiple PodSets requesting the same
  topology. In particular, it was possible for the set of topology domains in the assignment to be empty,
  and as a consequence the pods would remain gated forever as the TopologyUngater would not have
  topology assignment information. (#3524, @mimowo)
- Fix running Job when parallelism < completions, before the fix the replacement pods for the successfully
  completed Pods were not ungated. (#3561, @mimowo)
- Fix the flow of deactivation for workloads due to rejected AdmissionChecks. 
  Now, all AdmissionChecks are reset back to the Pending state on eviction (and deactivation in particular), 
  and so an admin can easily re-activate such a workload manually without tweaking the checks. (#3518, @KPostOffice)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-13T10:10:32Z

cc @tenzen-y @PBundyra , I also want to include https://github.com/kubernetes-sigs/kueue/pull/3514. 

The tentative release date is 14 Nov.

and possibly https://github.com/kubernetes-sigs/kueue/pull/3518 (but I consider it nice-to-have which could go in 0.9.2 imo).

cc @dgrove-oss @KPostOffice @mwysokin 

Let me know if you are aware of other pending fixes which would be good to include.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-13T16:40:23Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-18T10:09:57Z

```shell
$ git logs --oneline
c6c50ba5 (HEAD, upstream/release-0.9) Prepare release 0.9.1 (#3567)
829c055e TAS: fix scenario when parallelism < completions (#3561)
a9f24ae7 Prioritize Workload which fits in its CQ's Nominal Capacity (#3550)
c370b164 Refactor FlavorAssigner (#3549)
abe6931e Automated cherry pick of #3350: reset admission check after deactivation (#3518)
324f6e5f Automated cherry pick of #3514: TAS: fix computing assignment when multiple PodSets (#3524)
1b5192c1 TAS: fix accounting for usage from TAS workloads using multiple resources (#3513)
365b780a [release-0.9] Update release-notes with upgrading steps to 0.9.x (#3511)
6437d26d Fix readme repo and tag for manager image (#3463)
30ed8afb Rename JobWithValidation to JobWithCustomValidation. (#3464)
d3b8af0f (tag: v0.9.0) Prepare release v0.9.0 (#3458)
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T12:43:26Z

/close
As the release is out

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-18T12:43:31Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3521#issuecomment-2482938421):

>/close
>As the release is out


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
