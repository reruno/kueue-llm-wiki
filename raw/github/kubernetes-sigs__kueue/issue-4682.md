# Issue #4682: Release v0.10.3

**Summary**: Release v0.10.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4682

**Last updated**: 2025-03-19T15:48:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-19T09:55:05Z
- **Updated**: 2025-03-19T15:48:00Z
- **Closed**: 2025-03-19T15:47:57Z
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
        `git push release-$MAJ.$MIN`
- [ ] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes:  https://github.com/kubernetes-sigs/kueue/pull/4689
- [x] An OWNER creates a signed tag running
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
      To perform this step, you need [a PGP key registered on github](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys).
- [x] An OWNER pushes the tag with
      `git push upstream $VERSION`
  - Triggers prow to build and publish a staging container image
      `us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:$VERSION`
- [ ] An OWNER [prepares a draft release](https://github.com/kubernetes-sigs/kueue/releases)
  - [x] Create the draft release poiting out to the created tag.
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts in the `artifacts` folder.
  - [x] Upload the files in the `artifacts` folder to the draft release - either
      via UI or `gh release --repo kubernetes-sigs/kueue upload <tag> artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to 
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7899
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
  - [ ] Update `registry.k8s.io/images/charts/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.3
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4693
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release:
        <!-- example presubmit: https://github.com/kubernetes/test-infra/pull/33107 -->
        <!-- example periodic: https://github.com/kubernetes/test-infra/pull/33833 -->


## Changelog

```markdown
Changes since `v0.10.2`:

## Changes by Kind

### Bug or Regression

- Fixes a bug that would result in default values not being properly set on creation for enabled integrations whose API was not available when the Kueue controller started. (#4557, @dgrove-oss)
- Helm: Fixed a bug that prometheus namespace is enforced with namespace the same as kueue-controller-manager (#4487, @kannon92)
- TAS: Do not ignore the TAS annotation if set on the template for the Ray submitter Job. (#4502, @mszadkow)
- TAS: Fix a bug that TopolologyUngator cound not be triggered the leader change when enabled HA mode (#4656, @tenzen-y)
- Update FairSharing to be incompatible with ClusterQueue.Preemption.BorrowWithinCohort. Using these parameters together is a no-op, and will be validated against in future releases. This change fixes an edge case which triggered an infinite preemption loop when these two parameters were combined. (#4165, @gabesaba)

### Other (Cleanup or Flake)

- Publish helm charts to the Kueue staging repository `http://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts`, 
  so that they can be promoted to the permanent location under `registry.k8s.io/kueue/charts`. (#4684, @mimowo)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T10:04:23Z

We aim for the patch release today to test the new helm publication & promotion procedure: https://github.com/kubernetes-sigs/kueue/pull/4680 before 0.11.0

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T12:05:27Z

cc @tenzen-y @kannon92 @dgrove-oss @mwysokin @gabesaba @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-19T12:54:38Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T14:26:56Z

```
> docker run -it registry.k8s.io/kueue/kueue:v0.10.3
{"level":"info","ts":"2025-03-19T14:26:02.282174344Z","logger":"setup","caller":"kueue/main.go:423","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8080\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-03-19T14:26:02.282336134Z","logger":"setup","caller":"kueue/main.go:141","msg":"Initializing","gitVersion":"v0.10.3","gitCommit":"c79419eb5b3b0021621805a73bec2ff58c398d8b"}
```
helm
```
> helm template oci://registry.k8s.io/kueue/charts/kueue --version 0.10.3 | grep registry.k8s.io/kueue/kueue:v0.10.3
        image: "registry.k8s.io/kueue/kueue:v0.10.3"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T15:47:53Z

Released: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.3

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T15:47:59Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4682#issuecomment-2737144688):

>Released: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.3
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
