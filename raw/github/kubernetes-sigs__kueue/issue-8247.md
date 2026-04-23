# Issue #8247: Release v0.15.2

**Summary**: Release v0.15.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8247

**Last updated**: 2025-12-19T16:12:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-15T16:41:46Z
- **Updated**: 2025-12-19T16:12:23Z
- **Closed**: 2025-12-19T16:12:23Z
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
  - [x] Submit a pull request with the changes: #8359 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8894
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.2
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/8360
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.  https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/GMFs6YCRk1M
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
Changes since `v0.15.1`:

## Changes by Kind

### Feature

- Ray: Support RayJob InTreeAutoscaling by using the ElasticJobsViaWorkloadSlices feature. (#8284, @hiboyang)

### Bug or Regression

- Kubeflow TrainJob v2: fix the bug to prevent duplicate pod template overrides when starting the Job is retried. (#8271, @j-skiba)
- MultiKueue: Fixed status sync for CRD-based jobs (JobSet, Kubeflow, Ray, etc.) that was blocked while the local job was suspended. (#8344, @IrvingMg)
- MultiKueue: fix the bug that for Pod integration the AdmissionCheck status would be kept Pending indefinitely,
  even when the Pods are already running.
  
  The analogous fix is also done for the batch/Job when the MultiKueueBatchJobWithManagedBy feature gate  is disabled. (#8288, @IrvingMg)
- Scheduling: fix a bug that evictions submitted by scheduler (preemptions and eviction due to TAS NodeHotSwap failing)
  could result in conflict in case of concurrent workload modification by another controller.
  This could lead to indefinite failing requests sent by scheduler in some scenarios when eviction is initiated by
  TAS NodeHotSwap. (#8313, @mbobrovskyi)
- TAS NodeHotSwap: fixed the bug that allows workload to requeue by scheduler even if already deleted on TAS NodeHotSwap eviction. (#8310, @mbobrovskyi)
- TAS: fix a performance bug that continues reconciles of TAS ResourceFlavor (and related ClusterQueues) 
  were triggered by updates to Nodes' heartbeat times. (#8355, @PBundyra)
- TAS: fixed performance issue due to unncessary (empty) request by TopologyUngater (#8333, @mbobrovskyi)

### Other (Cleanup or Flake)

- Improve error messages for validation errors regarding WorkloadPriorityClass changes in workloads. (#8352, @olekzabl)
- MultiKueue: improve the MultiKueueCluster reconciler to skip attempting to reconcile and throw errors
  when the corresponding Secret or ClusterProfile objects don't exist. The reconcile will be triggered on 
  creation of the objects. (#8290, @mszadkow)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T16:42:44Z

We are aiming to include fix for https://github.com/kubernetes-sigs/kueue/issues/8245

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-19T10:17:01Z

LGTM

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-19T10:17:29Z

LGTM as well

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-19T11:27:11Z

Verifications:

```shell
$ docker run -it registry.k8s.io/kueue/kueue:v0.15.2
Unable to find image 'registry.k8s.io/kueue/kueue:v0.15.2' locally
v0.15.2: Pulling from kueue/kueue
9fd17edf5ad2: Pull complete 
Digest: sha256:004603d048d4d36aad75c6f9bc4c63b7ed5811605a8b3b0981dfa1bb175f8c68
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.15.2
...
{"level":"info","ts":"2025-12-19T11:25:25.128858958Z","logger":"setup","caller":"kueue/main.go:158","msg":"Initializing","gitVersion":"v0.15.2","gitCommit":"3790e86359efacde36b9fc2722e84f496a06d8fc","buildDate":"2025-12-19T10:53:08Z"}

$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.15.2 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.15.2
Digest: sha256:7d8561f974a68965c51861ec308def52714e1bd99178c9f3d6013f489b7c8940
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.15.2'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.15.2'
        image: "registry.k8s.io/kueue/kueue:v0.15.2"

$ helm template oci://registry.k8s.io/kueue/charts/kueue-populator --version 0.15.2 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue-populator:0.15.2
Digest: sha256:8b6eb63e2b69445942be8e4103b2d8eaacf8e6cae4599300d7669d2d1da0ca79
        image: "registry.k8s.io/kueue/kueue-populator:v0.15.2"
      image: registry.k8s.io/kubectl:v1.33.6
      image: registry.k8s.io/kubectl:v1.33.6
      image: registry.k8s.io/kubectl:v1.33.6
      image: registry.k8s.io/kubectl:v1.33.6
      image: registry.k8s.io/kubectl:v1.33.6
        image: registry.k8s.io/kubectl:v1.33.6

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.15.2
v0.15.2: Pulling from kueue/kueueviz-backend
79e1c5f2f727: Pull complete 
Digest: sha256:1e36def768cfb1f245a3cac43b06ef6f221d7ac03dc8967a70a121658ee4961f
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.15.2

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.15.2
v0.15.2: Pulling from kueue/kueueviz-frontend
Digest: sha256:118beeaddb0a6d690577e0a94ad04dfaafcdb868396e8cabb0191ac9eaa1cdfb
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.15.2

$ docker run -it registry.k8s.io/kueue/kueue-populator:v0.15.2
Unable to find image 'registry.k8s.io/kueue/kueue-populator:v0.15.2' locally
v0.15.2: Pulling from kueue/kueue-populator
951d158d6f9f: Pull complete 
Digest: sha256:4e0269dbfcf4bfd5e89c1c70d7d99b5b8572f1fc5f9ee6af8c541a9eeb84c41c
Status: Downloaded newer image for registry.k8s.io/kueue/kueue-populator:v0.15.2
```
