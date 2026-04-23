# Issue #8137: Release v0.14.6

**Summary**: Release v0.14.6

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8137

**Last updated**: 2025-12-12T16:03:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-08T18:46:23Z
- **Updated**: 2025-12-12T16:03:29Z
- **Closed**: 2025-12-12T16:03:27Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
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
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #8213 <!-- example #211 #214 -->
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
      to production: <!-- K8S_IO_PULL --> https://github.com/kubernetes/k8s.io/pull/8864
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.6
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/8219
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/C0Yd77fYWhQ
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
Changes since `v0.14.5`:

## Changes by Kind

### Feature

- TAS: extend the information in condition messages and events about nodes excluded from calculating the
  assignment due to various recognized reasons like: taints, node affinity, node resource constraints. (#8169, @sohankunkerkar)

### Bug or Regression

- Fix `TrainJob` controller not correctly setting the `PodSet` count value based on `numNodes` for the expected number of training nodes. (#8146, @kaisoz)
- Fix a performance bug as some "read-only" functions would be taking unnecessary "write" lock. (#8182, @ErikJiang)
- Fix the race condition bug where the kueue_pending_workloads metric may not be updated to 0 after the last 
  workload is admitted and there are no new workloads incoming. (#8048, @Singularity23x0)
- Fixed the following bugs for the StatefulSet integration by ensuring the Workload object
  has the ownerReference to the StatefulSet:
  1. Kueue doesn't keep the StatefulSet as deactivated
  2. Kueue marks the Workload as Finished if all StatefulSet's Pods are deleted
  3. changing the "queue-name" label could occasionally result in the StatefulSet getting stuck (#8104, @mbobrovskyi)
- TAS: Fix handling of admission for workloads using the LeastFreeCapacity algorithm when the  "unconstrained"
  mode is used. In that case scheduling would fail if there is at least one node in the cluster which does not have
  enough capacity to accommodate at least one Pod. (#8171, @PBundyra)
- TAS: fix bug that when TopologyAwareScheduling is disabled, but there is a ResourceFlavor configured with topologyName, then preemptions fail with "workload requires Topology, but there is no TAS cache information". (#8196, @zhifei92)

### Other (Cleanup or Flake)

- Add safe-guard to protect against re-evaluating Finished workloads by scheduler which caused a bug. (#8199, @mimowo)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T07:20:00Z

I would like to still include fix for https://github.com/kubernetes-sigs/kueue/issues/8157

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-10T07:35:10Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-11T14:07:01Z

LGTM on release notes.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T14:19:43Z

We moved the release for tomorrow to also try accomodating https://github.com/kubernetes-sigs/kueue/pull/8186

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-12T15:52:54Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.6 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.6
Digest: sha256:fa72a11dd450b50ba79dd904a8d65357c27cca0fc4cc58340abf686f573cb27b
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.6'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.6'
        image: "registry.k8s.io/kueue/kueue:v0.14.6"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.14.6
v0.14.6: Pulling from kueue/kueue
db9a5bd824a5: Pull complete 
Digest: sha256:96b2925e7df7d54d001bfdd108ad13c56a84c5f319ef20452b052dbb5f932e31
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.6
...
{"level":"info","ts":"2025-12-12T15:52:00.116111798Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.6","gitCommit":"72b6a37d91805a8b19dda93d9cdc00eae3394bf6","buildDate":"2025-12-12T14:35:23Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.6
v0.14.6: Pulling from kueue/kueueviz-backend
f83cd42c8d66: Pull complete 
Digest: sha256:7bf718336df2fd508a3354f8e6a82eda2d3d315ce36b592fa659c9018bd7abe2
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.6

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.6
v0.14.6: Pulling from kueue/kueueviz-frontend
...
Digest: sha256:9e037c188f403a9818aa5a9aa52e8505a60bffba5e29f3ce31b22bb62218a96a
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.6
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-12T16:03:21Z

Done.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-12T16:03:28Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8137#issuecomment-3647181587):

>Done.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
