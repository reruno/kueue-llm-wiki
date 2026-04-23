# Issue #5884: Release v0.12.4

**Summary**: Release v0.12.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5884

**Last updated**: 2025-07-09T17:01:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-07T07:40:59Z
- **Updated**: 2025-07-09T17:01:02Z
- **Closed**: 2025-07-09T17:01:02Z
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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5911
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
      to production: https://github.com/kubernetes/k8s.io/pull/8284
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.4
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5918
  - [x] Cherry-pick the pull request onto the `website` branch: https://github.com/kubernetes-sigs/kueue/pull/5922
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
Changes since `v0.12.3`:

## Changes by Kind

### Feature

- Helm: support for specifying nodeSelector and tolerations for all Kueue components (#5869, @zmalik)

### Bug or Regression

- Fix a bug where the GroupKindConcurrency in Kueue Config is not propagated to the controllers (#5826, @tenzen-y)
- TAS: Fix a bug for the incompatible NodeFailureController name with Prometheus (#5824, @tenzen-y)
- TAS: Fix a bug that Kueue unintentionally gives up a workload scheduling in LeastFreeCapacity if there is at least one unmatched domain. (#5804, @PBundyra)
- TAS: Fix a bug that the tas-node-failure-controller unexpectedly is started under the HA mode even though the replica is not the leader. (#5851, @tenzen-y)
- TAS: Fix the bug when Kueue crashes if the preemption target, due to quota, is using a node which is already deleted. (#5843, @mimowo)

### Other (Cleanup or Flake)

- KueueViz: reduce the image size from 1.14 GB to 267MB, resulting in faster pull and shorter startup time. (#5875, @mbobrovskyi)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-07T07:42:18Z

We are aiming for Wednesday - 9th July

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-07T07:42:25Z

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T15:02:46Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T16:05:29Z

sanity checks
```
> helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.4 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.4
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.12.4'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.12.4'
        image: "registry.k8s.io/kueue/kueue:v0.12.4"
```
```
> docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.12.4
v0.12.4: Pulling from kueue/kueue
Digest: sha256:65b9f620c8eb993bba609e6e3463726de078adbd3eaa0382f6f7952d807f3b74
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.12.4
{"level":"info","ts":"2025-07-09T16:05:12.892772484Z","logger":"setup","caller":"kueue/main.go:468","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-07-09T16:05:12.892979444Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.12.4","gitCommit":"ab6a91294a318ed6bf6f7d33862320445e0424a0"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T17:00:56Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-09T17:01:02Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5884#issuecomment-3053368946):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
