# Issue #7307: Release v0.14.2

**Summary**: Release v0.14.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7307

**Last updated**: 2025-10-23T13:44:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-17T08:37:54Z
- **Updated**: 2025-10-23T13:44:04Z
- **Closed**: 2025-10-23T13:44:03Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

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
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #7358 <!-- example #211 #214 -->
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
      via UI or `gh release --repo kubernetes-sigs/kueue upload $VERSION artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/8689
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7359
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/CAfc6j9uQZQ
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.14.1`:

## Changes by Kind

### Feature

- JobFramework: Introduce an optional interface for custom Jobs, called JobWithCustomWorkloadActivation, which can be used to deactivate or active a custom CRD workload. (#7286, @tg123)

### Bug or Regression

- Fix existing workloads not being re-evaluated when new clusters are added to MultiKueueConfig. Previously, only newly created workloads would see updated cluster lists. (#7349, @mimowo)
- Fix handling of RayJobs which specify the spec.clusterSelector and the "queue-name" label for Kueue. These jobs should be ignored by kueue as they are being submitted to a RayCluster which is where the resources are being used and was likely already admitted by kueue. No need to double admit.
  Fix on a panic on kueue managed jobs if spec.rayClusterSpec wasn't specified. (#7258, @laurafitzgerald)
- Fixed a bug that Kueue would keep sending empty updates to a Workload, along with sending the "UpdatedWorkload" event, even if the Workload didn't change. This would happen for Workloads using any other mechanism for setting
  the priority than the WorkloadPriorityClass, eg. for Workloads for PodGroups. (#7305, @mbobrovskyi)
- MultiKueue x ElasticJobs: fix webhook validation bug which prevented scale up operation when any other
  than the default "AllAtOnce" MultiKueue dispatcher was used. (#7332, @mszadkow)
- TAS: Introduce missing validation against using incompatible `PodSet` grouping configuration in `JobSet, `MPIJob`, `LeaderWorkerSet`, `RayJob` and `RayCluster`. 
  
  Now, only groups of two `PodSet`s can be defined and one of the grouped `PodSet`s has to have only a single `Pod`.
  The `PodSet`s within a group must specify the same topology request via one of the `kueue.x-k8s.io/podset-required-topology` and `kueue.x-k8s.io/podset-preferred-topology` annotations. (#7263, @kshalot)
- Visibility API: Fix a bug that the Config clientConnection is not respected in the visibility server. (#7225, @tenzen-y)
- WorkloadRequestUseMergePatch: use "strict" mode for admission patches during scheduling which
  sends the ResourceVersion of the workload being admitted for comparing by kube-apiserver. 
  This fixes the race-condition issue that Workload conditions added concurrently by other controllers
  could be removed during scheduling. (#7279, @mszadkow)

### Other (Cleanup or Flake)

- Improve the messages presented to the user in scheduling events, by clarifying the reason for "insufficient quota"
  in case of workloads with multiple PodSets. 
  
  Example:
  - before: "insufficient quota for resource-type in flavor example-flavor, request > maximum capacity (24 > 16)"
  - after: "insufficient quota for resource-type in flavor example-flavor, previously considered podsets requests (16) + current podset request (8) > maximum capacity (16)" (#7293, @iomarsayed)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T10:13:45Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T11:53:13Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.2 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.2
Digest: sha256:45c73cd951f9d9804ae1995f12f7069050ee6e8d27650765229f9cb8dfbd5081
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.2'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.2'
        image: "registry.k8s.io/kueue/kueue:v0.14.2"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.14.2
v0.14.2: Pulling from kueue/kueue
680b0cabe91e: Pull complete 
Digest: sha256:8efdc98cef5e71198d513bcb1d072c30dd1f3114fb36d93b9b1d36819c9ebef3
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.2
...
{"level":"info","ts":"2025-10-23T11:51:53.215185966Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.2","gitCommit":"afb96efdd444eb95e357e6d6b77ce9cd2817fc91","buildDate":"2025-10-23T11:21:54Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.2
v0.14.2: Pulling from kueue/kueueviz-backend
501dd0e6e325: Pull complete 
Digest: sha256:30f10c989ed422038e69dacfd4a25dd51913a23037d3007edd58e4fbce4c5640
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.2

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.2
v0.14.2: Pulling from kueue/kueueviz-frontend
Digest: sha256:479273576fedde053c00dd6849cc30c51c3218abd56b716dc372d701598dbbab
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.2
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T13:43:57Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-23T13:44:04Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7307#issuecomment-3437098402):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
