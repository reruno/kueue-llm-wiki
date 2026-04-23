# Issue #9379: Release v0.15.5

**Summary**: Release v0.15.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9379

**Last updated**: 2026-02-27T14:46:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-19T18:39:12Z
- **Updated**: 2026-02-27T14:46:56Z
- **Closed**: 2026-02-27T14:46:54Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 5

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
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Run `./hack/releasing/prepare_pull.sh --target release $VERSION`
  - [x] Wait for this PR to merge #9568 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/9159
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`. May use `./hack/releasing/promote_pull.sh`
  - [x] Wait for the PR to be merged
  - [x] Verify that the image is available `./hack/releasing/wait_for_images.sh --prod $VERSION`
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Run `./hack/releasing/prepare_pull.sh --target main $VERSION`
  - [x] Submit a pull request with the changes: <!-- example #3007 -->
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
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
Changes since `v0.15.4`:

## Changes by Kind

### Feature

- KueueViz Helm: Add podSecurityContext and containerSecurityContext configuration options to KueueViz Helm chart for restricted pod security profile compliance (#9320, @ziadmoubayed)
- Observability: Increased the maximum finite bucket boundary for admission_wait_time_seconds histogram from ~2.84 hours to ~11.3 hours for better observability of long queue times. (#9530, @mukund-wayve)
- TAS: Introduce the TASReplaceNodeOnNodeTaints feature gate (alpha) to allow TAS workloads to be evicted or replaced when a node is tainted with NoExecute. (#9441, @j-skiba)

### Bug or Regression

- ElasticJobs: fix the temporary double-counting of quota during workload replacement. 
  In particular it was causing double-counting of quota requests for unchanged PodSets. (#9365, @benkermani)
- FairSharing: workloads fitting within their ClusterQueue's nominal quota are now preferred over workloads that require borrowing, preventing heavy borrowing on one flavor from deprioritizing a CQ's nominal entitlement on another flavor. (#9533, @mukund-wayve)
- Fix non-deterministic workload ordering in ClusterQueue by adding UID tie-breaker to queue ordering function. (#9164, @sohankunkerkar)
- Fix serverName substitution in kustomize prometheus ServiceMonitor TLS patch for cert-manager deployments. (#9190, @IrvingMg)
- Fixed invalid field name in the `ClusterQueue` printer columns. The "Cohort" column will now correctly display the assigned cohort in kubectl, k9s, and other UI tools instead of being blank. (#9447, @polinasand)
- Fixed the bug that prevented managing workloads with duplicated environment variable names in initContainers. This issue manifested when creating the Workload via the API. (#9127, @monabil08)
- LeaderWorkerSet: fix an occasional race condition resulting in workload deletion getting stuck during scale down. (#9135, @PannagaRao)
- MultiKueue: Fix a bug that the remote Job object was occasionally left by MultiKueue GC, 
  even when the corresponding Job object on the management cluster was deleted.
  This issue was observed for LeaderWorkerSet. (#9309, @sohankunkerkar)
- Scheduling: Fix the bug where inadmissible workloads would be re-queued too frequently at scale.
  This resulted in excessive processing, lock contention, and starvation of workloads deeper in the queue.
  The fix is to throttle the process with a batch period of 1s per CQ or Cohort. (#9232, @gabesaba)
- TAS: Fix a bug that LeaderWorkerSet with multiple PodTemplates (`.spec.leaderWorkerTemplate.leaderTemplate` and `.spec.leaderWorkerTemplate.workerTemplate`), Pod indexes are not correctly evaluated during rank-based ordering assignments. (#9369, @tenzen-y)
- TAS: fix a bug where NodeHotSwap may assign a Pod, based on rank-ordering, to a node which is already
  occupied by another running Pod. (#9283, @j-skiba)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T10:50:25Z

+1 on this release.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-27T10:52:31Z

release lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T13:36:07Z

```shell
Images:

  Checking if "registry.k8s.io/kueue/kueue:v0.15.5" is available.
    ✅ Image "registry.k8s.io/kueue/kueue@sha256:02b71e21f648d06108b904c6a3926066745df747e7b4fb48e1275a0148f9e62a" is available.
    sha256:02b71e21f648d06108b904c6a3926066745df747e7b4fb48e1275a0148f9e62a

  Checking if "registry.k8s.io/kueue/kueueviz-backend:v0.15.5" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-backend@sha256:e9ae34674e79266a663ff8b66f4f8abf0da1ef888e7c6a4b771ece418c1920ba" is available.
    sha256:e9ae34674e79266a663ff8b66f4f8abf0da1ef888e7c6a4b771ece418c1920ba

  Checking if "registry.k8s.io/kueue/kueueviz-frontend:v0.15.5" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-frontend@sha256:95b4635af74681bb2607a1a19e9bccd375cc64b8d38a795a392e0d57fdd40f43" is available.
    sha256:95b4635af74681bb2607a1a19e9bccd375cc64b8d38a795a392e0d57fdd40f43

  Checking if "registry.k8s.io/kueue/kueue-populator:v0.15.5" is available.
    ✅ Image "registry.k8s.io/kueue/kueue-populator@sha256:c5318e7694a2b4bda2bdae876def835d916c8cd5eb48273f63ec893275e935d3" is available.
    sha256:c5318e7694a2b4bda2bdae876def835d916c8cd5eb48273f63ec893275e935d3

Charts:

  Checking if "registry.k8s.io/kueue/charts/kueue:0.15.5" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue@sha256:47fb3ce654f3a1012aff4a41a7af97c36d612b1c3c53e534366121aafc890a5c" is available.
    sha256:47fb3ce654f3a1012aff4a41a7af97c36d612b1c3c53e534366121aafc890a5c

  Checking if "registry.k8s.io/kueue/charts/kueue-populator:0.15.5" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue-populator@sha256:429714e7bdd93ad41ec0fdfc49f992b8df7349800114238307a0fbcc4095c386" is available.
    sha256:429714e7bdd93ad41ec0fdfc49f992b8df7349800114238307a0fbcc4095c386
```

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-27T14:46:49Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-27T14:46:55Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9379#issuecomment-3973336524):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
