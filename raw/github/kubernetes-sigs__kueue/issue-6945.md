# Issue #6945: Release v0.13.5

**Summary**: Release v0.13.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6945

**Last updated**: 2025-09-30T16:04:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-22T13:27:45Z
- **Updated**: 2025-09-30T16:04:27Z
- **Closed**: 2025-09-30T16:04:26Z
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
  - [x] Submit a pull request with the changes: #7087 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8577
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.5
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7089
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/wY3ATFcS6i8
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
Changes since `v0.13.4`:

## Changes by Kind

### Feature

- KueueViz: Enhancing the following endpoint customizations and optimizations:
  - The frontend and backend ingress no longer have hardcoded NGINX annotations. You can now set your own annotations in Helm’s values.yaml using kueueViz.backend.ingress.annotations and kueueViz.frontend.ingress.annotations
  - The Ingress resources for KueueViz frontend and backend no longer require hardcoded TLS. You can now choose to use HTTP only by not providing kueueViz.backend.ingress.tlsSecretName and kueueViz.frontend.ingress.tlsSecretName
  - You can set environment variables like KUEUEVIZ_ALLOWED_ORIGINS directly from values.yaml using kueueViz.backend.env (#6934, @Smuger)

### Bug or Regression

- ElasticJobs: workloads correctly trigger workload preemption in response to a scale-up event. (#6973, @ichekrygin)
- FS: Fix the following FairSharing bugs:
  - Incorrect DominantResourceShare caused by rounding (large quotas or high FairSharing weight)
  - Preemption loop caused by zero FairSharing weight (#6994, @gabesaba)
- FS: Validate FairSharing.Weight against small values which lose precision (0 < value <= 10^-9) (#7008, @gabesaba)
- Fix bug in workload usage removal simulation that results in inaccurate flavor assignment (#7084, @gabesaba)
- Fix the bug for the StatefulSet integration which would occasionally cause a StatefulSet
  to be stuck without workload after renaming the "queue-name" label. (#7037, @IrvingMg)
- Fix the bug that a workload going repeatedly via the preemption and re-admission cycle would accumulate the
  "Previously" prefix in the condition message, eg: "Previously: Previously: Previously: Preempted to accommodate a workload ...". (#6874, @amy)
- HC: When multiple borrowing flavors are available, prefer the flavor which
  results in borrowing more locally (closer to the ClusterQueue, further from the root Cohort).
  
  This fixes the scenario where a flavor would be selected which required borrowing
  from the root Cohort in one flavor, while in a second flavor, quota was
  available from the nearest parent Cohort. (#7042, @gabesaba)
- Helm: Fix a bug where the internal cert manager assumed that the helm installation name is 'kueue'. (#6917, @cmtly)
- Helm: Fixed bug where webhook configurations assumed a helm install name as "kueue". (#6924, @cmtly)
- Pod-integration now correctly handles pods stuck in the Terminating state within pod groups, preventing them from being counted as active and avoiding blocked quota release. (#6892, @ichekrygin)
- TAS: Fix the scenario when Node Hot Swap cannot find a replacement. In particular, if slices are used
  they could result in generating invalid assignment, resulting in panic from TopologyUngater.
  Now, such a workload is evicted. (#6927, @mbobrovskyi)
- TAS: Node Hot Swap allows replacing a node for workloads using PodSet slices, 
  ie. when the `kueue.x-k8s.io/podset-slice-size` annotation is used. (#6989, @pajakd)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T14:34:09Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T15:50:05Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.5 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.5
Digest: sha256:d226e27bf82fe900ea25fef83553d6ec372fd3877bf581d197316f4809860697
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.5'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.5'
        image: "registry.k8s.io/kueue/kueue:v0.13.5"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.5
v0.13.5: Pulling from kueue/kueue
43b543d4eebe: Pull complete 
Digest: sha256:57e0f857f8442ce861f0b47e02d756be5c3a537ea3020d4917f6ad4fcc5342fd
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.13.5
...
{"level":"info","ts":"2025-09-30T15:49:16.884023095Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.5","gitCommit":"438e12ca8f1773073250bd2e028f63333f908a31","buildDate":"2025-09-30T15:21:47Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.5
v0.13.5: Pulling from kueue/kueueviz-backend
7ebd34214649: Pull complete 
Digest: sha256:0185907d716405a29296a00386a9d225c88d0700b3887dbea20ea72793396a00
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.13.5

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.5
v0.13.5: Pulling from kueue/kueueviz-frontend
Digest: sha256:c17223241102eb6b29f3d15dda281cd9c71fa25221e216312f6aa1b293615efc
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.13.5
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T16:04:21Z

Closing this as released.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-30T16:04:27Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6945#issuecomment-3352880808):

>Closing this as released.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
