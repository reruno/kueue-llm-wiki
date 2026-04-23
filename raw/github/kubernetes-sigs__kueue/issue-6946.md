# Issue #6946: Release v0.12.10

**Summary**: Release v0.12.10

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6946

**Last updated**: 2025-09-30T16:14:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-22T13:28:16Z
- **Updated**: 2025-09-30T16:14:41Z
- **Closed**: 2025-09-30T16:14:39Z
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
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #7086 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8579
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.10 
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7090
  - [ ] Cherry-pick the pull request onto the `website` branch
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
Changes since `v0.12.9`:

## Changes by Kind

### Bug or Regression

- FS: Validate FairSharing.Weight against small values which lose precision (0 < value <= 10^-9) (#7007, @gabesaba)
- Fix the bug for the StatefulSet integration which would occasionally cause a StatefulSet
  to be stuck without workload after renaming the "queue-name" label. (#7038, @IrvingMg)
- Fix the bug that a workload going repeatedly via the preemption and re-admission cycle would accumulate the
  "Previously" prefix in the condition message, eg: "Previously: Previously: Previously: Preempted to accommodate a workload ...". (#6875, @amy)
- Fixed bug where internal cert manager assumed that the helm installation name was kueue. (#6916, @cmtly)
- Helm: Fixed bug where webhook configurations assumed a helm install name as "kueue". (#6923, @cmtly)
- Pod-integration now correctly handles pods stuck in the Terminating state within pod groups, preventing them from being counted as active and avoiding blocked quota release. (#6893, @ichekrygin)

```

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-23T18:34:47Z

The suspense! What is being proposed for 0.12.10?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T00:50:05Z

> The suspense! What is being proposed for 0.12.10?

Recently, we fixed some of the scheduling bugs and Helm deployment configuration bugs.
This patch version will have those fixes.

Based on the discussion with @mimowo, we will release these patches on the same date as v0.14.0.

Note: this is a final patch version for v0.12.x.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T16:00:50Z

Sanity checks:
```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.10 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.10
Digest: sha256:94ee9e5b5e34bdfc3a11564a2dd4fd91357053738857a1bd39630fb788f66b16
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.12.10'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.12.10'
        image: "registry.k8s.io/kueue/kueue:v0.12.10"
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.12.10
v0.12.10: Pulling from kueue/kueue
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
5664b15f108b: Already exists 
045fc1c20da8: Already exists 
4aa0ea1413d3: Already exists 
da7816fa955e: Already exists 
ddf74a63f7d8: Already exists 
acb4434060f4: Pull complete 
Digest: sha256:c293932347fa83efff0b6083e0282fe8159f49e8e82862dd1f25b7f1614f8b6d
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.12.10
{"level":"info","ts":"2025-09-30T15:59:41.646354221Z","logger":"setup","caller":"kueue/main.go:474","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-09-30T15:59:41.646522421Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.12.10","gitCommit":"bd167035c5e4a42529e44d6447dae003116ecd13"}
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.12.10
v0.12.10: Pulling from kueue/kueueviz-backend
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
5664b15f108b: Already exists 
045fc1c20da8: Already exists 
4aa0ea1413d3: Already exists 
da7816fa955e: Already exists 
ddf74a63f7d8: Already exists 
336ff00283c4: Pull complete 
Digest: sha256:02e888fae01b2c8b469e167903593f7db9dd924bfbf366286b9fe8a271d6a820
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.12.10
2025/09/30 16:00:06 Starting pprof server on :6060
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.12.10
v0.12.10: Pulling from kueue/kueueviz-frontend
d107e437f729: Already exists 
23418204b321: Already exists 
8544b3c3f2fc: Already exists 
ae0081685b50: Already exists 
1ab59cb3b5b2: Already exists 
a14dbb5d23ce: Already exists 
54c632f0e2c7: Pull complete 
cdcc3fef7b70: Pull complete 
1e3e5e7da8ff: Pull complete 
4f4fb700ef54: Pull complete 
Digest: sha256:1e956e8a28a7977b3e2efebe87c2e7ed009ebf9cfc0b8b81ce63728f692b0fa2
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.12.10

```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T16:14:35Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-30T16:14:41Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6946#issuecomment-3352913603):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
