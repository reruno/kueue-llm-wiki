# Issue #5616: Release v0.12.3

**Summary**: Release v0.12.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5616

**Last updated**: 2025-06-25T12:59:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T08:00:40Z
- **Updated**: 2025-06-25T12:59:51Z
- **Closed**: 2025-06-25T12:59:49Z
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
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5748
- [ ] An OWNER creates a signed tag running
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
      to production: https://github.com/kubernetes/k8s.io/pull/8227
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5750
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
  - [ ] Create the presubmits and the periodic jobs for the next patch release:
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch:
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.12.2`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- Helm: 
  
  - Fixed KueueViz installation when enableKueueViz=true is used with default values for the image specifying parameters.
  - Split the image specifying parameters into separate repository and tag, both for KueueViz backend and frontend. 
  
  If you are using Helm charts and installing KueueViz using custom images,
  then you need to specify them by kueueViz.backend.image.repository, kueueViz.backend.image.tag, 
  kueueViz.fontend.image.repository and kueueViz.frontend.image.tag parameters. (#5514, @mbobrovskyi)
 
## Changes by Kind

### Feature

- Allow setting the controller-manager's Pod `PriorityClassName` from the Helm chart (#5649, @kaisoz)

### Bug or Regression

- Add Cohort Go client library (#5603, @tenzen-y)
- Fix the bug that Job deleted on the manager cluster didn't trigger deletion of pods on the worker cluster. (#5607, @ichekrygin)
- Fix the bug that Kueue, upon startup, would incorrectly admit and then immediately deactivate
  already deactivated Workloads.
  
  This bug also prevented the ObjectRetentionPolicies feature from deleting Workloads
  that were deactivated by Kueue before the feature was enabled. (#5629, @mbobrovskyi)
- Fix the bug that the webhook certificate setting under `controllerManager.webhook.certDir` was ignored by the internal cert manager, effectively always defaulting to /tmp/k8s-webhook-server/serving-certs. (#5491, @ichekrygin)
- Fixed bug that doesn't allow Kueue to admit Workload after queue-name label set. (#5714, @mbobrovskyi)
- MultiKueue: Fix a bug that batch/v1 Job final state is not synced from Workload cluster to Management cluster when disabling the `MultiKueueBatchJobWithManagedBy` feature gate. (#5706, @ichekrygin)
- TAS: fix the bug which would trigger unnecessary second pass scheduling for nodeToReplace
  in the following scenarios: 
  1. Finished workload
  2. Evicted workload
  3. node to replace is not present in the workload's TopologyAssignment domains (#5591, @mimowo)
- TAS: fix the scenario when deleted workload still lives in the cache. (#5605, @mimowo)
- Use simulation of preemption for more accurate flavor assignment. 
  In particular, in certain scenarios when preemption while borrowing is enabled, 
  the previous heuristic would wrongly state that preemption was possible. (#5700, @gabesaba)
- Use simulation of preemption for more accurate flavor assignment. 
  In particular, the previous heuristic would wrongly state that preemption
  in a flavor was possible even if no preemption candidates could be found. 

  Additionally, in scenarios when preemption while borrowing is enabled,
  the flavor in which reclaim is possible is preferred over flavor where 
  priority-based preemption is required. This is consistent with prioritizing 
  flavors when preemption without borrowing is used. (#5740, @gabesaba)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T10:36:13Z

cc @tenzen-y @dgrove-oss @kannon92 @mwielgus @mwysokin @gabesaba 

FYI: I synced with @tenzen-y and we are aiming June 20th. Let me know if you want to include some other bugfixes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T10:37:25Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T13:51:09Z

Folks, sorry for the delay, we moved the release date for June 24.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-24T16:03:51Z

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.3 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.3
Digest: sha256:f6ecb9802e33c1f9eadf96cabac49e03d7358cad89025717fdf82e89aad559cb
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.12.3'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.12.3'
        image: "registry.k8s.io/kueue/kueue:v0.12.3"
$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.12.3
v0.12.3: Pulling from kueue/kueue
2b1ce36ead8f: Pull complete 
ddf74a63f7d8: Pull complete 
Digest: sha256:58631910025b345ffcd6aa925c25e813c6adb368ef88f5d7d67cd00acec237dc
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.12.3
...
{"level":"info","ts":"2025-06-24T16:04:31.896065675Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.12.3","gitCommit":"5e45476a20cec4eb74fe1e553a03c543bbeb8a89"}
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.12.3
v0.12.3: Pulling from kueue/kueueviz-backend
ddf74a63f7d8: Pull complete 
178b6db4e58c: Pull complete 
Digest: sha256:932603299423f0dfc8a599a3fe2ded01aed60a0e39cbd532f24cc21b66782870
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.12.3
$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.12.3
v0.12.3: Pulling from kueue/kueueviz-frontend
Digest: sha256:db90616681a2b2b8d83feccf989254c650d546ca2647076e60de814725807fe8
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.12.3
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-25T12:59:44Z

Done.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-25T12:59:51Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5616#issuecomment-3004684906):

>Done.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
