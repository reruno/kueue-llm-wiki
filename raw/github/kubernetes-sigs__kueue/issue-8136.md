# Issue #8136: Release v0.15.1

**Summary**: Release v0.15.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8136

**Last updated**: 2025-12-12T16:03:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-08T18:46:05Z
- **Updated**: 2025-12-12T16:03:40Z
- **Closed**: 2025-12-12T16:03:36Z
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
  - [x] Submit a pull request with the changes: #8214 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8863
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes:  https://github.com/kubernetes-sigs/kueue/pull/8215
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/C0Yd77fYWhQ
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
Changes since `v0.15.0`:

## Changes by Kind

### Feature

- TAS: extend the information in condition messages and events about nodes excluded from calculating the
  assignment due to various recognized reasons like: taints, node affinity, node resource constraints. (#8132, @sohankunkerkar)

### Bug or Regression

- Fix `TrainJob` controller not correctly setting the `PodSet` count value based on `numNodes` for the expected number of training nodes. (#8145, @kaisoz)
- Fix a performance bug as some "read-only" functions would be taking unnecessary "write" lock. (#8183, @ErikJiang)
- Fix the race condition bug where the kueue_pending_workloads metric may not be updated to 0 after the last 
  workload is admitted and there are no new workloads incoming. (#8049, @Singularity23x0)
- Fixed a bug that Kueue's scheduler would re-evaluate and update already finished workloads, significantly
  impacting overall scheduling throughput. This re-evaluation of a finished workload would be triggered when:
  1. Kueue is restarted
  2. There is any event related to LimitRange or RuntimeClass instances referenced by the workload (#8198, @mimowo)
- Fixed the following bugs for the StatefulSet integration by ensuring the Workload object
  has the ownerReference to the StatefulSet:
  1. Kueue doesn't keep the StatefulSet as deactivated
  2. Kueue marks the Workload as Finished if all StatefulSet's Pods are deleted
  3. changing the "queue-name" label could occasionally result in the StatefulSet getting stuck (#8105, @mbobrovskyi)
- MultiKueue via ClusterProfile: Fix the panic if the configuration for ClusterProfiles wasn't not provided in the configMap. (#8097, @mszadkow)
- TAS: Fix handling of admission for workloads using the LeastFreeCapacity algorithm when the  "unconstrained"
  mode is used. In that case scheduling would fail if there is at least one node in the cluster which does not have
  enough capacity to accommodate at least one Pod. (#8172, @PBundyra)
- TAS: fix bug that when TopologyAwareScheduling is disabled, but there is a ResourceFlavor configured with topologyName, then preemptions fail with "workload requires Topology, but there is no TAS cache information". (#8195, @zhifei92)

### Other (Cleanup or Flake)

- Fix: Removed outdated comments incorrectly stating that deployment, statefulset, and leaderworkerset integrations require pod integration to be enabled. (#8054, @IrvingMg)

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T07:19:56Z

I would like to still include fix for https://github.com/kubernetes-sigs/kueue/issues/8157

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-10T07:35:01Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-11T14:06:58Z

LGTM on release notes.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T14:19:47Z

We moved the release for tomorrow to also try accomodating https://github.com/kubernetes-sigs/kueue/pull/8186

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T15:53:33Z

Sanity checks 
```
❯ docker run -it registry.k8s.io/kueue/kueue:v0.15.1
{"level":"info","ts":"2025-12-12T15:50:40.734184709Z","logger":"setup","caller":"kueue/main.go:529","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta2\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-12-12T15:50:40.734364509Z","logger":"setup","caller":"kueue/main.go:158","msg":"Initializing","gitVersion":"v0.15.1","gitCommit":"84809c4a9f7ed5d83fdd7837f8ca0642881df846","buildDate":"2025-12-12T14:59:38Z"}
```
```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.15.1 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.15.1
Digest: sha256:8c582f600942bfc84c7d403ec9dc42fe575dc7f619f83b1152f131b682441f64
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.15.1'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.15.1'
        image: "registry.k8s.io/kueue/kueue:v0.15.1"
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.15.1
v0.15.1: Pulling from kueue/kueueviz-backend
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
52630fc75a18: Already exists 
dd64bf2dd177: Already exists 
4aa0ea1413d3: Already exists 
dcaa5a89b0cc: Already exists 
069d1e267530: Already exists 
6f00bfb1be55: Pull complete 
Digest: sha256:d17dca6361bed979bd6c7971c450352677b5034076506361a470dac9505b08bb
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.15.1
2025/12/12 15:51:34 Starting pprof server on localhost:6060
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.15.1
v0.15.1: Pulling from kueue/kueueviz-frontend
ae4ce04d0e1c: Already exists 
49b012f11eec: Pull complete 
c76df6f1197c: Pull complete 
46902bf66eda: Pull complete 
502d91eda693: Pull complete 
04ea45d7e8d4: Pull complete 
bab9ab7563ab: Pull complete 
5e61ea1593e5: Pull complete 
5b7851b2cd8d: Pull complete 
4f4fb700ef54: Pull complete 
Digest: sha256:65b336f9aba90c5b0335632d4f2579b555bed6caf5a04f34aa677a5fd21791e2
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.15.1
```
```
❯ docker run -it registry.k8s.io/kueue/kueue-populator:v0.15.1
Unable to find image 'registry.k8s.io/kueue/kueue-populator:v0.15.1' locally
v0.15.1: Pulling from kueue/kueue-populator
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
52630fc75a18: Already exists 
dd64bf2dd177: Already exists 
4aa0ea1413d3: Already exists 
dcaa5a89b0cc: Already exists 
069d1e267530: Already exists 
cb4a20f2a949: Pull complete 
Digest: sha256:64b0a1eac7e0544794e741343c9c1a3ee0ec943ab0e2259d14b7fec3e7f7eb96
Status: Downloaded newer image for registry.k8s.io/kueue/kueue-populator:v0.15.1
```

```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue-populator --version 0.15.1 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue-populator:0.15.1
Digest: sha256:89265fa8c56d7d17bade152dd98788bb17cc8f1c7244915de454f13bbe1d8339
        image: "registry.k8s.io/kueue/kueue-populator:v0.15.1"
```
