# Issue #3371: Release v0.8.2

**Summary**: Release v0.8.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3371

**Last updated**: 2024-11-05T07:07:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-30T07:51:23Z
- **Updated**: 2024-11-05T07:07:35Z
- **Closed**: 2024-11-04T15:52:56Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
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
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""`
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #3433
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
      via UI or `gh release upload <tag> artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7479
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.2
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: #3434
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
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
Changes since `v0.8.1`:

### Feature

- Helm: Support the topologySpreadConstraints and PodDisruptionBudget (#3282, @woehrl01)

### Bug or Regression

- Fix a bug that could delay the election of a new leader in the Kueue with multiple replicas env. (#3096, @tenzen-y)
- Fix resource consumption computation for partially admitted workloads. (#3206, @trasc)
- Fix restoring parallelism on eviction for partially admitted batch/Jobs. (#3208, @trasc)
- Fix some scenarios for partial admission which are affected by wrong calculation of resources
  used by the incoming workload which is partially admitted and preempting. (#3205, @trasc)
- Fix webook validation for batch/Job to allow partial admission of a Job to use all available resources.
  It also fixes a scenario of partial re-admission when some of the Pods are already reclaimed. (#3207, @trasc)
- Prevent job webhooks from dropping fields for newer API fields when Kueue libraries are behind the latest released CRDs. (#3358, @mbobrovskyi)
- RayJob's implementation of Finished() now inspects at JobDeploymentStatus (#3128, @andrewsykim)
- Workload is requeued with all AdmissionChecks set to Pending if there was an AdmissionCheck in Retry state. (#3323, @PBundyra)
- Account for NumOfHosts when calculating PodSet assignments for RayJob and RayCluster (#3384, @andrewsykim)

### Other (Cleanup or Flake)

- Add a jobframework.BaseWebhook that can be used for custom job integrations (#3355, @mbobrovskyi)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-30T07:53:08Z

As we discussed with @tenzen-y we seem to have enough fixes to motivate the release. We aim for 4th Nov together with 0.9.0.

cc @tenzen-y @andrewsykim @dgrove-oss @kannon92

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-30T19:59:33Z

@mimowo Could we cherry-pick https://github.com/kubernetes-sigs/kueue/pull/3354 and https://github.com/kubernetes-sigs/kueue/pull/3323? It seems that those are obviously bug fixes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-30T19:59:43Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T06:12:32Z

> @mimowo Could we cherry-pick https://github.com/kubernetes-sigs/kueue/pull/3354 and https://github.com/kubernetes-sigs/kueue/pull/3323? It seems that those are obviously bug fixes.

Yes, sure.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-31T08:45:52Z

> > @mimowo Could we cherry-pick #3354 and #3323? It seems that those are obviously bug fixes.
> 
> Yes, sure.

Thank you. Note that I think we should address this comment before cherry-picking: https://github.com/kubernetes-sigs/kueue/pull/3323#discussion_r1819460282

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-10-31T14:38:20Z

Any chance we can add https://github.com/kubernetes-sigs/kueue/pull/3384 to 0.8.2?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T14:42:01Z

I'm supportive for that, because it is a bug and limited in scope.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-31T17:04:10Z

> Any chance we can add #3384 to 0.8.2?

@andrewsykim I'm fine with including #3384 in 0.8.2. @mimowo can lead the review and merge into the release branch.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T15:26:40Z

```shell
$ docker pull registry.k8s.io/kueue/kueue:v0.8.2
v0.8.2: Pulling from kueue/kueue
0bab15eea81d: Already exists 
da7816fa955e: Already exists 
474437a9a06f: Download complete 
bfb59b82a9b6: Already exists 
a62778643d56: Already exists 
9aee425378d2: Already exists 
7c12895b777b: Already exists 
4aa0ea1413d3: Already exists 
3214acf345c0: Download complete 
8ffb3c3cf71a: Already exists 
c6b97f964990: Download complete 
5664b15f108b: Already exists 
Digest: sha256:46cf9e4b2741baa368f0b1d799f33b8f5a585f71f6b9a6bafd02768c96043f93
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.8.2
registry.k8s.io/kueue/kueue:v0.8.2

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview registry.k8s.io/kueue/kueue:v0.8.2
$ kubectl get pod -n kueue-system -w
NAME                                        READY   STATUS              RESTARTS   AGE
kueue-controller-manager-6bb7c675fd-dcthk   0/2     ContainerCreating   0          8s
kueue-controller-manager-6bb7c675fd-dcthk   1/2     Running             0          11s
kueue-controller-manager-6bb7c675fd-dcthk   2/2     Running             0          13s
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T15:52:51Z

All done. Thanks all!

https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.2

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-04T15:52:57Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3371#issuecomment-2455076469):

>All done. Thanks all!
>
>https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.2
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
