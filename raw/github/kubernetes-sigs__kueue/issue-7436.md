# Issue #7436: Release v0.13.8

**Summary**: Release v0.13.8

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7436

**Last updated**: 2025-10-30T16:04:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-30T07:59:51Z
- **Updated**: 2025-10-30T16:04:20Z
- **Closed**: 2025-10-30T16:04:20Z
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
  - [x] Submit a pull request with the changes: #7456 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8712
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.8
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7458
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
Changes since `v0.13.7`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- MultiKueue: validate remote client kubeconfigs and reject insecure kubeconfigs by default; add feature gate MultiKueueAllowInsecureKubeconfigs to temporarily allow insecure kubeconfigs until v0.17.0.
  
  if you are using MultiKueue kubeconfigs which are not passing the new validation please
  enable the `MultiKueueAllowInsecureKubeconfigs` feature gate and let us know so that we can re-consider
  the deprecation plans for the feature gate. (#7453, @mszadkow)
 
## Changes by Kind

### Bug or Regression

- Fix a bug where a workload would not get requeued after eviction due to failed hotswap. (#7380, @pajakd)
- Fix the kueue-controller-manager startup failures.
  
  This fixed the Kueue CrashLoopBackOff due to the log message: "Unable to setup indexes","error":"could not setup multikueue indexer: setting index on workloads admission checks: indexer conflict. (#7441, @IrvingMg)
- Fixed the bug that prevented managing workloads with duplicated environment variable names in containers. This issue manifested when creating the Workload via the API. (#7442, @mbobrovskyi)
- Services: fix the setting of the `app.kubernetes.io/component` label to discriminate between different service components within Kueue as follows:
  - controller-manager-metrics-service for kueue-controller-manager-metrics-service 
  - visibility-service for kueue-visibility-server
  - webhook-service for kueue-webhook-service (#7451, @rphillips)
- TAS: Increase the number of Topology levels limitations for localqueue and workloads to 16 (#7428, @kannon92)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-30T08:39:57Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-30T15:50:28Z

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.8 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.8
Digest: sha256:48d1a26721e6a16e5df6c073659857573d7b00b56ee75f621667f1fe4cc5725b
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.8'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.8'
        image: "registry.k8s.io/kueue/kueue:v0.13.8"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.8
v0.13.8: Pulling from kueue/kueue
fff64682f1ae: Pull complete 
Digest: sha256:0c3e90ac613efba7ff8bd22ff5a0007e8e1652744f57e8a9a3eb75b10ce6a1da
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.13.8
...
{"level":"info","ts":"2025-10-30T15:48:36.409081127Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.8","gitCommit":"65cf90a97a02d8bd0c0262543e7fec4ffdd8421d","buildDate":"2025-10-30T15:21:24Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.8
v0.13.8: Pulling from kueue/kueueviz-backend
34e6148fb5ef: Pull complete 
Digest: sha256:e965aa11ad799bd232d679b63712a56b95484cf568029e2961d4b3aa48e74596
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.13.8

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.8
v0.13.8: Pulling from kueue/kueueviz-frontend
Digest: sha256:1197ebd69cc17708893a6878dd3d7d4a1a8f0e4a9f0d290643033c05b8a46753
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.13.8
```
