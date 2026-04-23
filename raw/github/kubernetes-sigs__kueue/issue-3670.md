# Issue #3670: Release v0.9.2

**Summary**: Release v0.9.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3670

**Last updated**: 2024-12-16T13:15:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-11-27T15:42:50Z
- **Updated**: 2024-12-16T13:15:42Z
- **Closed**: 2024-12-16T13:15:40Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
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
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""`
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/3862
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
      to production: https://github.com/kubernetes/k8s.io/pull/7614
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.2
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/3865
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.
  - [x] sig-scheduling@kubernetes.io: 
  - [x] wg-batch@kubernetes.io: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/kVEbjJiH_kA/m/l1AEoHRiBQAJ
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
## Changes by Kind

### Bug or Regression

- Added validation for Deployment queue-name to fail fast (#3580, @mbobrovskyi)
- Added validation for StatefulSet queue-name to fail fast. (#3585, @mbobrovskyi)
- Fix a bug which occasionally prevented updates to the PodTemplate of the Job on the management cluster
  when starting a Job (e.g. updating nodeSelectors), when using `MultiKueueBatchJobWithManagedBy` enabled. (#3731, @IrvingMg)
- Fix dropping of reconcile requests for non-leading replica, which was resulting in workloads
  getting stuck pending after the rolling restart of Kueue. (#3613, @mimowo)
- Fix memory leak due to workload entries left in MultiKueue cache. The leak affects the 0.9.0 and 0.9.1 
  releases which enable MultiKueue by default, even if MultiKueue is not explicitly used on the cluster. (#3843, @mimowo)
- Fix misleading log messages from workload_controller indicating not existing LocalQueue or
  Cluster Queue. For example "LocalQueue for workload didn't exist or not active; ignored for now"
  could also be logged the ClusterQueue does not exist. (#3832, @PBundyra)
- Fix preemption when using Hierarchical Cohorts by considering as preemption candidates workloads
  from ClusterQueues located further in the hierarchy tree than direct siblings. (#3705, @gabesaba)
- Fix scheduling of workload which does not include the toleration for the taint in ResourceFlavor's spec.nodeTaints,
  if the toleration is specified on the ResourceFlavor itself. (#3724, @PBundyra)
- Fix the bug which prevented the use of MultiKueue if there is a CRD which is not installed
  and removed from the list of enabled integrations. (#3631, @mszadkow)
- TAS: Fixed bug that doesn't allow to update cache on delete Topology. (#3655, @mbobrovskyi)
- TAS: The CQ referencing a Topology is deactivated if the topology does not exist. (#3819, @mimowo)

### Other (Cleanup or Flake)

- Replace deprecated gcr.io/kubebuilder/kube-rbac-proxy with registry.k8s.io/kubebuilder/kube-rbac-proxy. (#3749, @mbobrovskyi)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T15:43:33Z

This will be released as a patch version for December.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T15:43:39Z

cc: @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T16:16:15Z

+1, please generate the release notes already, we can update them on the release date

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-28T16:48:42Z

> +1, please generate the release notes already, we can update them on the release date

Yes, sure

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-28T16:58:25Z

> +1, please generate the release notes already, we can update them on the release date

Done.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-16T12:25:20Z

```shell
$ docker run --rm -it registry.k8s.io/kueue/kueue:v0.9.2 
Unable to find image 'registry.k8s.io/kueue/kueue:v0.9.2' locally
v0.9.2: Pulling from kueue/kueue
a91f6df36242: Download complete 
Digest: sha256:949b1562ee5e68c1cbab7c8508467713f0389d1c44d50d024749703c48ea5068
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.9.2
{"level":"info","ts":"2024-12-16T12:23:57.557624967Z","logger":"setup","caller":"kueue/main.go:122","msg":"Initializing","gitVersion":"v0.9.2","gitCommit":"174aaa75c252f3785b424e877186cd42263b2314"}
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-16T13:15:34Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-16T13:15:41Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3670#issuecomment-2545606978):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
