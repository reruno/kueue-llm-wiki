# Issue #6291: Release v0.13.1

**Summary**: Release v0.13.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6291

**Last updated**: 2025-08-01T18:01:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-07-30T14:27:47Z
- **Updated**: 2025-08-01T18:01:05Z
- **Closed**: 2025-08-01T18:01:05Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 3

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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6370
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
      to production: https://github.com/kubernetes/k8s.io/pull/8357
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6371
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/sig-scheduling/c/MnfZLNpZ6MU
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release:
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch:
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.13.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- Rename kueue-metrics-certs to kueue-metrics-cert cert-manager.io/v1 Certificate name in cert-manager manifests when installing Kueue using the Kustomize configuration.
  
  If you're using cert-manager and have deployed Kueue using the Kustomize configuration, you must delete the existing kueue-metrics-certs cert-manager.io/v1 Certificate before applying the new changes to avoid conflicts. (#6362, @mbobrovskyi)
 
## Changes by Kind

### Bug or Regression

- Fix accounting for the `evicted_workloads_once_total` metric:
  - the metric wasn't incremented for workloads evicted due to stopped LocalQueue (LocalQueueStopped reason)
  - the reason used for the metric was "Deactivated" for workloads deactivated by users and Kueue, now the reason label can have the following values: Deactivated, DeactivatedDueToAdmissionCheck, DeactivatedDueToMaximumExecutionTimeExceeded, DeactivatedDueToRequeuingLimitExceeded. This approach aligns the metric with `evicted_workloads_total`.
  - the metric was incremented during preemption before the preemption request was issued. Thus, it could be incorrectly over-counted in case of the preemption request failure.
  - the metric was not incremented for workload evicted due to NodeFailures (TAS)
  
  The existing and introduced DeactivatedDueToXYZ reason label values will be replaced by the single "Deactivated" reason label value and underlying_cause in the future release. (#6360, @mimowo)
- Fix the bug for the ElasticJobsViaWorkloadSlices feature where in case of Job resize followed by eviction
  of the "old" workload, the newly created workload could get admitted along with the "old" workload.
  The two workloads would overcommit the quota. (#6257, @ichekrygin)
- Fix the bug which could occasionally cause workloads evicted by the built-in AdmissionChecks
  (ProvisioningRequest and MultiKueue) to get stuck in the evicted state which didn't allow re-scheduling.
  This could happen when the AdmissionCheck controller would trigger eviction by setting the
  Admission check state to "Retry". (#6299, @mimowo)
- Fixed a bug that prevented adding the kueue- prefix to the secretName field in cert-manager manifests when installing Kueue using the Kustomize configuration. (#6343, @mbobrovskyi)
- ProvisioningRequest: Fix a bug that Kueue didn't recreate the next ProvisioningRequest instance after the
  second (and consecutive) failed attempt. (#6329, @PBundyra)
- Support disabling client-side ratelimiting in Config API clientConnection.qps with a negative value (e.g., -1) (#6305, @tenzen-y)
- TAS: Fix a bug that the node failure controller tries to re-schedule Pods on the failure node even after the Node is recovered and reappears (#6347, @pajakd)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T14:36:02Z

We decided to release this patch version ~~by bypassing our patch version release policy~~ to fix the https://github.com/kubernetes-sigs/kueue/pull/6283 critical built-in AdmissionChecks rollback problem in case of Eviction.

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T16:07:00Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-01T17:14:27Z

I confirmed the release images:

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.1 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.1
Digest: sha256:4da30458c39432acd8eb5e0a2013af518919f982c52512d12e177148596be7e0
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.1'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.1'
        image: "registry.k8s.io/kueue/kueue:v0.13.1"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.1
v0.13.1: Pulling from kueue/kueue
...
Digest: sha256:f77326c7250c01a5389aa857a89e5ad69fc5700b811cea1c108c3da66b516091
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.13.1
...
{"level":"info","ts":"2025-08-01T17:13:07.77085767Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.1","gitCommit":"81236abed536034d41156c5af20d614590f82935","buildDate":"2025-08-01T16:42:19Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.1
v0.13.1: Pulling from kueue/kueueviz-backend
...
Digest: sha256:5b53f49eb3535d727dce53a1f519662f0541d6bb274e75800c710a6d162fc281
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.13.1

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.1
v0.13.1: Pulling from kueue/kueueviz-frontend
...
Digest: sha256:114509dbf11606de789fe9b86a1a31288baa4bcbd97d70342a74e9af490c2d03
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.13.1
```
