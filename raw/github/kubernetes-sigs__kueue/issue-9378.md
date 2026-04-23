# Issue #9378: Release v0.16.2

**Summary**: Release v0.16.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9378

**Last updated**: 2026-02-27T15:24:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-19T18:38:36Z
- **Updated**: 2026-02-27T15:24:01Z
- **Closed**: 2026-02-27T15:24:00Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 6

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
- [ ] Update the release branch:
  - [x] Run `./hack/releasing/prepare_pull.sh --target release $VERSION`
  - [x] Wait for this PR to merge #9567 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/9157
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`. May use `./hack/releasing/promote_pull.sh`
  - [x] Wait for the PR to be merged
  - [x] Verify that the image is available `./hack/releasing/wait_for_images.sh --prod $VERSION`
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.16.2
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Run `./hack/releasing/prepare_pull.sh --target main $VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/9574
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
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
Changes since `v0.16.1`:

## Changes by Kind

### Feature

- KueueViz Helm: Add podSecurityContext and containerSecurityContext configuration options to KueueViz Helm chart for restricted pod security profile compliance (#9319, @ziadmoubayed)
- Observability: Increased the maximum finite bucket boundary for admission_wait_time_seconds histogram from ~2.84 hours to ~11.3 hours for better observability of long queue times. (#9507, @mukund-wayve)

### Bug or Regression

- ElasticJobs: fix the temporary double-counting of quota during workload replacement. 
  In particular it was causing double-counting of quota requests for unchanged PodSets. (#9364, @benkermani)
- FairSharing: workloads fitting within their ClusterQueue's nominal quota are now preferred over workloads that require borrowing, preventing heavy borrowing on one flavor from deprioritizing a CQ's nominal entitlement on another flavor. (#9532, @mukund-wayve)
- Fix non-deterministic workload ordering in ClusterQueue by adding UID tie-breaker to queue ordering function. (#9140, @sohankunkerkar)
- Fix serverName substitution in kustomize prometheus ServiceMonitor TLS patch for cert-manager deployments. (#9188, @IrvingMg)
- Fixed invalid field name in the `ClusterQueue` printer columns. The "Cohort" column will now correctly display the assigned cohort in kubectl, k9s, and other UI tools instead of being blank. (#9422, @polinasand)
- Fixed the bug that prevented managing workloads with duplicated environment variable names in initContainers. This issue manifested when creating the Workload via the API. (#9126, @monabil08)
- FlavorFungability: fix the bug that the semantics for the `flavorFungability.preference` enum values
  (ie. PreemptionOverBorrowing and BorrowingOverPreemption) were swapped. (#9486, @tenzen-y)
- LeaderWorkerSet: fix an occasional race condition resulting in workload deletion getting stuck during scale down. (#9135, @PannagaRao)
- MultiKueue: Fix a bug that the remote Job object was occasionally left by MultiKueue GC, 
  even when the corresponding Job object on the management cluster was deleted.
  This issue was observed for LeaderWorkerSet. (#9310, @sohankunkerkar)
- MultiKueue: for the StatefulSet integration copy the entire StatefulSet onto the worker clusters. This allows
  for proper management (and replacements) of Pods on the worker clusters. (#9539, @IrvingMg)
- Observability: Fix missing "replica-role" in the logs from the NonTasUsageReconciler. (#9456, @IrvingMg)
- Observability: Fix the stale "replica-role" value in scheduler logs after leader election. (#9431, @IrvingMg)
- Scheduling: Fix the bug where inadmissible workloads would be re-queued too frequently at scale.
  This resulted in excessive processing, lock contention, and starvation of workloads deeper in the queue.
  The fix is to throttle the process with a batch period of 1s per CQ or Cohort. (#9490, @gabesaba)
- TAS: Fix a bug that LeaderWorkerSet with multiple PodTemplates (`.spec.leaderWorkerTemplate.leaderTemplate` and `.spec.leaderWorkerTemplate.workerTemplate`), Pod indexes are not correctly evaluated during rank-based ordering assignments. (#9368, @tenzen-y)
- TAS: fix a bug where NodeHotSwap may assign a Pod, based on rank-ordering, to a node which is already
  occupied by another running Pod. (#9282, @j-skiba)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T11:24:14Z

The release is planned for tomorrow. We would like to include these two bugfixes:
- https://github.com/kubernetes-sigs/kueue/pull/9463
- https://github.com/kubernetes-sigs/kueue/pull/9232

cc @tenzen-y @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T10:50:36Z

+1 on this release.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-27T10:52:22Z

release lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T13:33:52Z

```shell
./hack/releasing/wait_for_images.sh --prod v0.16.2
Images:

  Checking if "registry.k8s.io/kueue/kueue:v0.16.2" is available.
    ✅ Image "registry.k8s.io/kueue/kueue@sha256:3a03b59b3165fc71bc174960976a6bdd3962d797dc2f295ab0c438f55f60cce7" is available.
    sha256:3a03b59b3165fc71bc174960976a6bdd3962d797dc2f295ab0c438f55f60cce7

  Checking if "registry.k8s.io/kueue/kueueviz-backend:v0.16.2" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-backend@sha256:f44b8165b56449d56a2dd24999b0f56ef849735f90533ad188fe4ffaa5528819" is available.
    sha256:f44b8165b56449d56a2dd24999b0f56ef849735f90533ad188fe4ffaa5528819

  Checking if "registry.k8s.io/kueue/kueueviz-frontend:v0.16.2" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-frontend@sha256:6ce11577e4d14c348805bec1ef5c92611dae41ae5ae6b858f17bf8f53b6d4f72" is available.
    sha256:6ce11577e4d14c348805bec1ef5c92611dae41ae5ae6b858f17bf8f53b6d4f72

  Checking if "registry.k8s.io/kueue/kueue-populator:v0.16.2" is available.
    ✅ Image "registry.k8s.io/kueue/kueue-populator@sha256:9758cdde886dcd8defc478cf311cd7ade15fb8c81ed6ef3db25e8f5c2ca7cd18" is available.
    sha256:9758cdde886dcd8defc478cf311cd7ade15fb8c81ed6ef3db25e8f5c2ca7cd18

Charts:

  Checking if "registry.k8s.io/kueue/charts/kueue:0.16.2" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue@sha256:4e0427987bb17d0a7cd74ba83ef6e637aa8b58a860f4821dfcd332a5f0d8f997" is available.
    sha256:4e0427987bb17d0a7cd74ba83ef6e637aa8b58a860f4821dfcd332a5f0d8f997

  Checking if "registry.k8s.io/kueue/charts/kueue-populator:0.16.2" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue-populator@sha256:69a8ba09149a41706637c3a9d075053984f4be923a8ef8c67bb8fdaac943ce5f" is available.
    sha256:69a8ba09149a41706637c3a9d075053984f4be923a8ef8c67bb8fdaac943ce5f
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T15:23:55Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-27T15:24:01Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9378#issuecomment-3973530447):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
