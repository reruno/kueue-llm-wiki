# Issue #5617: Release v0.11.7

**Summary**: Release v0.11.7

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5617

**Last updated**: 2025-06-24T16:38:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T08:01:15Z
- **Updated**: 2025-06-24T16:38:41Z
- **Closed**: 2025-06-24T16:38:40Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5749
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
      to production: https://github.com/kubernetes/k8s.io/pull/8228
  - [ ] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link:  https://github.com/kubernetes-sigs/kueue/releases/tag/v0.11.7
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5752
  - [x] Cherry-pick the pull request onto the `website` branch: https://github.com/kubernetes-sigs/kueue/pull/5753
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
Changes since `v0.11.6`:

## Changes by Kind

### Feature

- Allow setting the controller-manager's Pod `PriorityClassName` from the Helm chart (#5650, @kaisoz)

### Bug or Regression

- Add Cohort Go client library (#5604, @tenzen-y)
- Fix the bug that Job deleted on the manager cluster didn't trigger deletion of pods on the worker cluster. (#5608, @ichekrygin)
- Fix the bug that Kueue, upon startup, would incorrectly admit and then immediately deactivate
  already deactivated Workloads.
  
  This bug also prevented the ObjectRetentionPolicies feature from deleting Workloads
  that were deactivated by Kueue before the feature was enabled. (#5630, @mbobrovskyi)
- Fix the bug that the webhook certificate setting under `controllerManager.webhook.certDir` was ignored by the internal cert manager, effectively always defaulting to /tmp/k8s-webhook-server/serving-certs. (#5490, @ichekrygin)
- Fixed bug that doesn't allow Kueue to admit Workload after queue-name label set. (#5715, @mbobrovskyi)
- MultiKueue: Fix a bug that batch/v1 Job final state is not synced from Workload cluster to Management cluster when disabling the `MultiKueueBatchJobWithManagedBy` feature gate. (#5707, @ichekrygin)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T10:37:18Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-24T16:05:06Z

```
> docker run --rm registry.k8s.io/kueue/kueue:v0.11.7
{"level":"info","ts":"2025-06-24T16:04:31.440568821Z","logger":"setup","caller":"kueue/main.go:464","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-06-24T16:04:31.440742791Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.11.7","gitCommit":"c1f708bfa1a0bb43cd00a09149f4b3b8e93416e0"}
```

```
> helm template oci://registry.k8s.io/kueue/charts/kueue --version 0.11.7 | grep registry.k8s.io 
Pulled: registry.k8s.io/kueue/charts/kueue:0.11.7
        image: "registry.k8s.io/kueue/kueue:v0.11.7"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-24T16:38:36Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-24T16:38:41Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5617#issuecomment-3001166104):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
