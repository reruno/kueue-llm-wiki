# Issue #4997: Release v0.10.5

**Summary**: Release v0.10.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4997

**Last updated**: 2025-04-24T20:16:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-16T08:33:09Z
- **Updated**: 2025-04-24T20:16:50Z
- **Closed**: 2025-04-24T20:15:05Z
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
  - [x] Submit a pull request with the changes: 
      - https://github.com/kubernetes-sigs/kueue/pull/5089
      - https://github.com/kubernetes-sigs/kueue/pull/5093
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
      to production: https://github.com/kubernetes/k8s.io/pull/8036
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.5
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5111
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/ED_MzPin1Mw/m/ShupNEszDwAJ
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
Changes since `v0.10.4`:

## Changes by Kind

### Bug or Regression

- TAS: Add support for Node Selectors. (#5087, @mwysokin)
- Fix LocalQueue's status message to reference LocalQueue, rather than ClusterQueue, when its status is Ready (#4957, @PBundyra)
- Fix RBAC configuration for the Topology API to allow reading and editing by the service accounts using the Kueue Batch Admin role. (#4865, @KPostOffice)
- Fix a bug which caused Kueue's Scheduler to build invalid SSA patch in some scenarios when  using
  admission checks. This patch would be rejected with the following error message: 
  Workload.kueue.x-k8s.io "job-xxxxxx" is invalid: [admissionChecks[0].lastTransitionTime: Required value (#5088, @alexeldeib)
- Fix bug which resulted in under-utilization of the resources in a Cohort.
  Now, when a ClusterQueue is configured with `preemption.reclaimWithinCohort: Any`,
  its resources can be lent out more freely, as we are certain that we can reclaim
  them later. Please see PR #4813 for detailed description of scenario. (#4823, @gabesaba)
- Fixed bug that allow to create Topology without levels. (#5018, @mbobrovskyi)
- Helm: fix ServiceMonitor selecting the wrong service. This previously led to missing Kueue metrics, even with `enablePrometheus` set to `true`. (#5084, @j-vizcaino)
- PodSetTopologyRequests are now configured only when TopologyAwareScheduling feature gate is enabled. (#4840, @mykysha)
- Revert making ClusterQueue.Preemption.BorrowWithinCohort as no-op when used with FairSharing, by reverting
  https://github.com/kubernetes-sigs/kueue/pull/4165, which was done to prevent infinite-preemption loops as
  described in https://github.com/kubernetes-sigs/kueue/issues/3779. However, it causes issues with upgrading for
  users who use that combination. This configuration remains deprecated and can be removed without any notice
  in future releases, so please consider alternatives. (#4819, @mimowo)
- TAS: Fix bug where scheduling panics when the workload using TopologyAwareScheduling has container request value specified as zero. (#4976, @qti-haeyoon)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-16T08:36:38Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T11:36:35Z

We are targeting 23rd April

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T20:05:50Z

```
> docker run -it registry.k8s.io/kueue/kueue:v0.10.5
{"level":"info","ts":"2025-04-24T20:04:53.702969818Z","logger":"setup","caller":"kueue/main.go:423","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8080\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-04-24T20:04:53.703165849Z","logger":"setup","caller":"kueue/main.go:141","msg":"Initializing","gitVersion":"v0.10.5","gitCommit":"c08d20e834572329eb6f68cfa51bd10d0035b5d9"}
```

```
> helm template oci://registry.k8s.io/kueue/charts/kueue --version 0.10.5 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.10.5
        image: "registry.k8s.io/kueue/kueue:v0.10.5"
        image: "registry.k8s.io/kubebuilder/kube-rbac-proxy:v0.16.0"
```
