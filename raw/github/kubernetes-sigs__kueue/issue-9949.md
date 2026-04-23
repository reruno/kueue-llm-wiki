# Issue #9949: Release v0.16.4

**Summary**: Release v0.16.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9949

**Last updated**: 2026-03-19T16:59:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-17T16:24:15Z
- **Updated**: 2026-03-19T16:59:34Z
- **Closed**: 2026-03-19T16:59:32Z
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
  - [x] Run `./hack/releasing/sync-notes.sh $VERSION` to generate and publish the release notes
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Ensure there are no unstaged changes in your directory (the script adds everything)
  - [x] Run `./hack/releasing/prepare_pull.sh --target release $VERSION`
  - [x] Wait for this PR to merge #10015 <!-- example #211 #214 -->
- [x] An OWNER creates a signed tag
  - [x] pull the release branch after PR from previous step merged
  - [x] run
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
      To perform this step, you need [a PGP key registered on github](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys).
- [x] An OWNER pushes the tag with
      `git push upstream $VERSION`
  - Triggers prow to build and publish a staging container image
      `us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:$VERSION`
- [x] An OWNER [prepares a draft release](https://github.com/kubernetes-sigs/kueue/releases)
  - [x] Create the draft release pointing out to the created tag.
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts in the `artifacts` folder.
  - [x] Upload the files in the `artifacts` folder to the draft release - either
      via UI or `gh release --repo kubernetes-sigs/kueue upload $VERSION artifacts/*`.
- [x] Promote images and Helm Charts to production:
  - [x] Run `./hack/releasing/wait_for_images.sh $VERSION` to await for the staging images.
  - [x] Run `./hack/releasing/promote_pull.sh $VERSION` to submit the promotion PR
  - [x] Wait for the PR to be merged kubernetes/k8s.io#9250 <!-- example kubernetes/k8s.io#7899 -->
  - [x] Run: `./hack/releasing/wait_for_images.sh --prod $VERSION` to verify that the promoted images are available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.16.4
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] for each release:
    - [ ] update the changelog <!-- example #9578 -->
  - [x] for only the latest release:
    - [x] Run `./hack/releasing/prepare_pull.sh --target main $VERSION`
    - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/10022
    - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/fVIG5cvba1U
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
Changes since `v0.16.3`:

## Changes by Kind

### Feature

- Helm: Allow setting log level (#9944, @gabesaba)
- TAS: Extend the support for handling NoSchedule taints when the TASReplaceNodeOnNodeTaints feature gate is enabled. (#10003, @j-skiba)
- VisibilityOnDemand: Introduce a new Kueue deployment argument, --visibility-server-port, which allows passing custom port when starting the visibility server. (#9976, @Nilsachy)

### Bug or Regression

- LWS integration: Fixed a bug that the `kueue.x-k8s.io/job-uid` label was not set on the workloads. (#10010, @mbobrovskyi)
- MultiKueue: Enable AllowWatchBookmarks for remote client watches to prevent idle watch connections from being terminated by HTTP proxies with idle timeouts (e.g., Cloudflare 524 errors). (#9990, @trilamsr)
- Scheduling: fix the issue that scheduler could indefinitely try re-queueing a workload which was once 
  inadmissible, but is admissible after an update. The issue affected workloads which don't specify 
  resource requests explicitly, but rely on defaulting based on limits. (#9913, @mimowo)
- Scheduling: fixed SchedulingEquivalenceHashing so equivalent workloads that become inadmissible through
  the preemption path with no candidates are also covered by the mechanism. 
  
  As a safety measure while the broader fix is validated, the beta SchedulingEquivalenceHashing feature gate
  is temporarily disabled by default. (#10007, @mimowo)
- StatefulSet integration: Fixed a bug that the `kueue.x-k8s.io/job-uid` label was not set on the workloads. (#9902, @mbobrovskyi)
- TAS: Fixed a bug where pods could become stuck in a `Pending` state during node replacement.
  This may occur when a node gets tainted or `NotReady` after the topology assignment phase, but before
  the pods are ungated. (#9978, @j-skiba)
- TAS: fix the bug that workloads which only specify resource limits, without requests, are not able to perform 
  the second-pass scheduling correctly, responsible for NodeHotSwap and ProvisioningRequests. (#9947, @mimowo)
- VisibilityOnDemand: Fix non-deterministic workload ordering with UsageBasedAdmissionFairSharing enabled. (#9955, @sohankunkerkar)

### Other (Cleanup or Flake)

- Restore the FlavorFungibilityImplicitPreferenceDefault feature gate. (#9991, @mimowo)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-19T13:51:37Z

LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T13:55:14Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-19T15:25:14Z

```shell
./hack/releasing/wait_for_images.sh --prod v0.16.4
Images:

  Checking if "registry.k8s.io/kueue/kueue:v0.16.4" is available.
    ✅ Image "registry.k8s.io/kueue/kueue@sha256:dd67ad37e1f960277cfada27d3a144b73c8edcf7ad679ad62eb723262b4d793d" is available.
    sha256:dd67ad37e1f960277cfada27d3a144b73c8edcf7ad679ad62eb723262b4d793d

  Checking if "registry.k8s.io/kueue/kueueviz-backend:v0.16.4" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-backend@sha256:f8384086781302301ba754c56d83f76a072081108aa9e68dbe67446d31a59ede" is available.
    sha256:f8384086781302301ba754c56d83f76a072081108aa9e68dbe67446d31a59ede

  Checking if "registry.k8s.io/kueue/kueueviz-frontend:v0.16.4" is available.
    ✅ Image "registry.k8s.io/kueue/kueueviz-frontend@sha256:08f7fc756d1f6ee086174fe3a78122064cee23717d5af47f5fb070a64fbdd1b7" is available.
    sha256:08f7fc756d1f6ee086174fe3a78122064cee23717d5af47f5fb070a64fbdd1b7

  Checking if "registry.k8s.io/kueue/kueue-populator:v0.16.4" is available.
    ✅ Image "registry.k8s.io/kueue/kueue-populator@sha256:84388c8288ae5d2fcbb2f6c8c309d8c8c2ee847f6814cadc40ed1b82f0c39718" is available.
    sha256:84388c8288ae5d2fcbb2f6c8c309d8c8c2ee847f6814cadc40ed1b82f0c39718

Charts:

  Checking if "registry.k8s.io/kueue/charts/kueue:0.16.4" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue@sha256:1a03273bdc7530c73db49cb926696c8020581d04aec72493e67c05bba71b6b31" is available.
    sha256:1a03273bdc7530c73db49cb926696c8020581d04aec72493e67c05bba71b6b31

  Checking if "registry.k8s.io/kueue/charts/kueue-populator:0.16.4" is available.
    ✅ Image "registry.k8s.io/kueue/charts/kueue-populator@sha256:da5b6311d2f3329a0849727ffe9b1f83a10d8e324b968caf075fb7c0931cbdba" is available.
    sha256:da5b6311d2f3329a0849727ffe9b1f83a10d8e324b968caf075fb7c0931cbdba
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-19T16:59:27Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T16:59:34Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9949#issuecomment-4091701278):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
