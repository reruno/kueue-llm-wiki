# Issue #8248: Release v0.14.7

**Summary**: Release v0.14.7

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8248

**Last updated**: 2025-12-19T12:15:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-15T16:42:00Z
- **Updated**: 2025-12-19T12:15:10Z
- **Closed**: 2025-12-19T12:15:10Z
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
- [ ] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date
  - [ ] Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes.
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""`
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #8361 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8895 <!-- example kubernetes/k8s.io#7899 -->
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.7
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/8363
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/GMFs6YCRk1M
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
Changes since `v0.14.6`:

## Changes by Kind

### Feature

- Ray: Support RayJob InTreeAutoscaling by using the ElasticJobsViaWorkloadSlices feature. (#8282, @hiboyang)

### Bug or Regression

- MultiKueue: Fixed status sync for CRD-based jobs (JobSet, Kubeflow, Ray, etc.) that was blocked while the local job was suspended. (#8346, @IrvingMg)
- MultiKueue: fix the bug that for Pod integration the AdmissionCheck status would be kept Pending indefinitely,
  even when the Pods are already running.
  
  The analogous fix is also done for the batch/Job when the MultiKueueBatchJobWithManagedBy feature gate  is disabled. (#8293, @IrvingMg)
- Scheduling: fix a bug that evictions submitted by scheduler (preemptions and eviction due to TAS NodeHotSwap failing)
  could result in conflict in case of concurrent workload modification by another controller.
  This could lead to indefinite failing requests sent by scheduler in some scenarios when eviction is initiated by
  TAS NodeHotSwap. (#8314, @mbobrovskyi)
- TAS NodeHotSwap: fixed the bug that allows workload to requeue by scheduler even if already deleted on TAS NodeHotSwap eviction. (#8306, @mbobrovskyi)
- TAS: fix a performance bug that continues reconciles of TAS ResourceFlavor (and related ClusterQueues) 
  were triggered by updates to Nodes' heartbeat times. (#8356, @PBundyra)
- TAS: fixed performance issue due to unncessary (empty) request by TopologyUngater (#8337, @mbobrovskyi)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T16:42:55Z

We are aiming to include fix for https://github.com/kubernetes-sigs/kueue/issues/8245

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-19T10:17:12Z

LGTM

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-19T11:38:18Z

Image verification:
```
docker run -it registry.k8s.io/kueue/kueue:v0.14.7                                                                                                                               
Unable to find image 'registry.k8s.io/kueue/kueue:v0.14.7' locally
v0.14.7: Pulling from kueue/kueue
Digest: sha256:cfa11e1ae40098b32fbda81a54a725271d720c77e701274c1390854229a9b5b6
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.14.7

helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.7 | grep registry.k8s.io                                          
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.7
Digest: sha256:9ea3dbec55b747b025a84a889cfc563e7a84034a5cfa31a0294ee91790fd30fe
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.7'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.7'
        image: "registry.k8s.io/kueue/kueue:v0.14.7"

docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.7                                                                                                     
v0.14.7: Pulling from kueue/kueueviz-backend
Digest: sha256:21f7d7fd8dc9e691a3d62c9fb1aa311df9005eabe4ed5bb52ee251c29df0f439
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.7
2025/12/19 11:36:34 Starting pprof server on localhost:6060
2025/12/19 11:36:34 Error creating Kubernetes client: failed to load kubeconfig from /home/nonroot/.kube/config: stat /home/nonroot/.kube/config: no such file or directory

docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.7                                                                                                    
v0.14.7: Pulling from kueue/kueueviz-frontend
Digest: sha256:a296b1dfabd41f980fce540c4da810036190cb76f249a2583dd8ac41486417a4
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.7
