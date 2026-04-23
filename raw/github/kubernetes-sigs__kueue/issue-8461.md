# Issue #8461: Release v0.14.8

**Summary**: Release v0.14.8

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8461

**Last updated**: 2026-01-20T16:36:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-08T07:39:04Z
- **Updated**: 2026-01-20T16:36:43Z
- **Closed**: 2026-01-20T16:36:43Z
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
  - [x] Submit a pull request with the changes: #8699 <!-- example #211 #214 -->
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
      to production: <!-- K8S_IO_PULL --> https://github.com/kubernetes/k8s.io/pull/8968
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.8
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/8704
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/gbgoxJlnsZg
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
Changes since `v0.14.7`:

## Changes by Kind

### Deprecation

- LWS: disable testing the mutating of the `kueue.x-k8s.io/workloadpriorityclass` label as the functionality is broken on
  Kueue 0.14 with Kubernetes 1.35+. 
  
  If you are using this functionality, please migrate to use Kueue 0.15+. (#8541, @mimowo)

### Feature

- CLI: Support "kwl" and "kueueworkload" as a shortname for Kueue Workloads. (#8473, @kannon92)

### Bug or Regression

- Add lws editer and viewer roles to kustomize and helm (#8554, @kannon92)
- Fix ClusterQueue deletion getting stuck when pending workloads are deleted after being assumed by the scheduler (#8552, @sohankunkerkar)
- HC: Avoid redundant requeuing of inadmissible workloads when multiple ClusterQueues in the same cohort hierarchy are processed. (#8512, @sohankunkerkar)
- Integrations based on Pods: skip using finalizers on the Pods created and managed by integrations. 
  
  In particular we skip setting finalizers for Pods managed by the built in Serving Workloads  Deployments,
  StatefulSets, and LeaderWorkerSets.
  
  This improves performance of suspending the workloads, and fixes occasional race conditions when a StatefulSet
  could get stuck when deactivating and re-activating in a short interval. (#8568, @mbobrovskyi)
- JobFramework: Fixed a bug that allowed a deactivated workload to be activated. (#8445, @chengjoey)
- Kubeflow TrainJob v2: fix the bug to prevent duplicate pod template overrides when starting the Job is retried. (#8488, @j-skiba)
- LeaderWorkerSet: Fixed a bug that prevented deleting the workload when the LeaderWorkerSet was scaled down. (#8672, @mbobrovskyi)
- MultiKueue now waits for WorkloadAdmitted (instead of QuotaReserved) before deleting workloads from non-selected worker clusters. To revert to the previous behavior, disable the `MultiKueueWaitForWorkloadAdmitted` feature gate. (#8601, @IrvingMg)
- MultiKueue: fix the eviction when initiated by the manager cluster (due to eg. Preemption or WairForPodsReady timeout). (#8403, @mbobrovskyi)
- ProvisioningRequest: Fixed a bug that prevented events from being updated when the AdmissionCheck state changed. (#8405, @mbobrovskyi)
- TAS: Fix a bug that MPIJob with runLauncherAsWorker Pod indexes are not correctly evaluated during rank-based ordering assignments. (#8662, @tenzen-y)
- TAS: Fixed an issue where workloads could remain in the second-pass scheduling queue (used for integration
  or TAS with ProvisioningRequests, and for TAS Node Hot Swap) even if they no longer require to be in the queue. (#8431, @skools-here)
- TAS: fix TAS resource flavor controller to extract only scheduling-relevant node updates to prevent unnecessary reconciliation. (#8454, @Ladicle)
- TAS: significantly improves scheduling performance by replacing Pod listing with an event-driven
  cache for non-TAS Pods, thereby avoiding expensive DeepCopy operations during each scheduling cycle. (#8484, @gabesaba)

```

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-20T13:33:07Z

/lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T13:37:21Z

Release note lgtm

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-20T14:23:19Z

release note lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T15:43:31Z

I verified.

```shell
$ docker run -it registry.k8s.io/kueue/kueue:v0.14.8                                                                                                                               
Unable to find image 'registry.k8s.io/kueue/kueue:v0.14.8' locally
v0.14.8: Pulling from kueue/kueue
eefa8204a60a: Pull complete 
Digest: sha256:1916f41164061e86bd320fb429e5d24fe185ec49fe891bfc256368fb77e8dec9
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.8
...
{"level":"info","ts":"2026-01-20T15:42:03.527809263Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.8","gitCommit":"2f2a452481b23fd664e4133ad51de1caa1d49c3a","buildDate":"2026-01-20T14:46:21Z"}

$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.8 | grep registry.k8s.io                                          
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.8
Digest: sha256:948dc2b7cf9a68b5d0411448fc1dbe32e6761746dce2b1f3306c8d3cdd4bea52
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.8'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.8'
        image: "registry.k8s.io/kueue/kueue:v0.14.8"

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.8                                                                                                     
v0.14.8: Pulling from kueue/kueueviz-backend
7a8849c059b4: Pull complete 
Digest: sha256:6c55a21ad6f83d5e878d1fdd8ad5cee84eb576814210497b33e4faa6635b2a30
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.8

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.8                                                                                                    
v0.14.8: Pulling from kueue/kueueviz-frontend
...
Digest: sha256:3202e5d16988fbe5886162735f7404759f3d92a6f449b7774a7886647f407c2c
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.8
```
