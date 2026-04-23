# Issue #7856: Release v0.14.5

**Summary**: Release v0.14.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7856

**Last updated**: 2025-11-27T18:13:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T17:09:25Z
- **Updated**: 2025-11-27T18:13:43Z
- **Closed**: 2025-11-27T18:13:43Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

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
  - [x] Submit a pull request with the changes: #7965 <!-- example #211 #214 -->
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
      to production: kubernetes/k8s.io#8811 <!-- example kubernetes/k8s.io#7899 -->
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.5
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7970
  - [x] Cherry-pick the pull request onto the `website` branch https://github.com/kubernetes-sigs/kueue/pull/7972
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/YBrsePWjj18
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
Changes since `v0.14.4`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- TAS: It supports the Kubeflow TrainJob.
  
  You should update Kubeflow Trainer to v2.1.0 at least when using Trainer v2. (#7755, @IrvingMg)
 
## Changes by Kind

### Bug or Regression

- AdmissionFairSharing: Fix the bug that occasionally a workload may get admitted from a busy LocalQueue,
  bypassing the entry penalties. (#7914, @IrvingMg)
- Fix a bug that an error during workload preemption could leave the scheduler stuck without retrying. (#7818, @olekzabl)
- Fix a bug that the cohort client-go lib is for a Namespaced resource, even though the cohort is a Cluster-scoped resource. (#7802, @tenzen-y)
- Fix integration of `manageJobWithoutQueueName` and `managedJobsNamespaceSelector` with JobSet by ensuring that jobSets without a queue are  not managed by Kueue if are not selected by the  `managedJobsNamespaceSelector`. (#7762, @MaysaMacedo)
- Fix issue #6711 where an inactive workload could transiently get admitted into a queue. (#7939, @olekzabl)
- Fix the bug that a workload which was deactivated by setting the `spec.active=false` would not have the 
  `wl.Status.RequeueState` cleared. (#7768, @sohankunkerkar)
- Fix the bug that the kubernetes.io/job-name label was not propagated from the k8s Job to the PodTemplate in
  the Workload object, and later to the pod template in the ProvisioningRequest. 
  
  As a consequence the ClusterAutoscaler could not properly resolve pod affinities referring to that label,
  via podAffinity.requiredDuringSchedulingIgnoredDuringExecution.labelSelector. For example, 
  such pod affinities can be used to request ClusterAutoscaler to provision a single node which is large enough
  to accommodate all Pods on a single Node.
  
  We also introduce the PropagateBatchJobLabelsToWorkload feature gate to disable the new behavior in case of 
  complications. (#7613, @yaroslava-serdiuk)
- Fix the race condition which could result that the Kueue scheduler occasionally does not record the reason
  for admission failure of a workload if the workload was modified in the meanwhile by another controller. (#7884, @mbobrovskyi)
- TAS: Fix the `requiredDuringSchedulingIgnoredDuringExecution` node affinity setting being ignored in topology-aware scheduling. (#7937, @kshalot)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-25T12:42:34Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T16:42:52Z

I confirmed the promoted image works well.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.5 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.5
Digest: sha256:1ffede210ca2ccb64ecb2899402e135d390240d167222e192f9986b36d370b49
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.5'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.5'
        image: "registry.k8s.io/kueue/kueue:v0.14.5"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.14.5
v0.14.5: Pulling from kueue/kueue
d11a3e6388cc: Pull complete 
Digest: sha256:6f8528d7184e2116046f9ab5382017499f7edaf4f49fdcd15b1cdb8716c1ba0e
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.5
...
{"level":"info","ts":"2025-11-27T16:41:50.163172801Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.5","gitCommit":"7481f8e1854ab4f819ba6f91f1468dd81d0b1670","buildDate":"2025-11-27T16:03:30Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.5
v0.14.5: Pulling from kueue/kueueviz-backend
58925a977976: Pull complete 
Digest: sha256:bd82e4fd5d42b167744275f4adf54fd585c7c55e9f4577f24313ea832cdf328d
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.5

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.5
v0.14.5: Pulling from kueue/kueueviz-frontend
...
Digest: sha256:4dfbabeca194b7e6542fe0dfb1bd29897bc515abfb6eeae727710b08894aa3ba
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.5
```
