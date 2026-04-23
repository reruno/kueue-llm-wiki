# Issue #3950: Release v0.10.1

**Summary**: Release v0.10.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3950

**Last updated**: 2025-01-20T12:28:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-09T10:56:38Z
- **Updated**: 2025-01-20T12:28:21Z
- **Closed**: 2025-01-20T12:28:19Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 7

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal.
  At least two for minor or major releases. At least one for a patch release.
- [ ] Verify that the changelog in this issue and the CHANGELOG folder is up-to-date
  - [x] Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes.
    Example: `release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""`
- [ ] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [ ] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [ ] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: #4011
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
      via UI or `gh release --repo kubernetes-sigs/kueue upload <tag> artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: kubernetes/k8s.io#7696
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.10.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: #4018
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release:
        <!-- example presubmit: https://github.com/kubernetes/test-infra/pull/33107 -->
        <!-- example periodic: https://github.com/kubernetes/test-infra/pull/33833 -->


## Changelog

```markdown
Changes since `v0.10.0`:

## Changes by Kind

### Bug or Regression

- Disable the unnecessary Validating Admission Policy for the visibility server, and drop the associated RBAC permissions to make the server minimal. This also prevents periodic error logging on clusters above Kubernetes 1.29+. (#3946, @varshaprasad96)
- Fix building TAS assignments for workloads with multiple PodSets (eg. JobSet or kubeflow Jobs). The assignment was computed independently for the PodSets which could result in conflicts rendering the pods unschedulable by the kube-scheduler. (#3970, @kerthcet)
- Fix populating the LocalQueue metrics: `kueue_local_queue_resource_usage` and `kueue_local_queue_resource_reservation`. (#3990, @mykysha)
- Fix the bug that prevented scaling StatefulSets which aren't managed by Kueue when the "statefulset" integration is enabled. (#3998, @mbobrovskyi)
- Fix the permission bug which prevented adding the `kueue.x-k8s.io/resource-in-use` finalizer to the Topology objects, resulting in repeatedly logged errors. (#3911, @kerthcet)
- Fixes a bug in 0.10.0 which resulted in the kueue manager configuration not being logged. (#3877, @dgrove-oss)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-09T11:05:58Z

I would like to yet wait to include https://github.com/kubernetes-sigs/kueue/pull/3937, and aim for the release next week. 

Let me know if there are other important bug fixes we need to include.

/cc @tenzen-y @dgrove-oss @varshaprasad96 @mwielgus @mwysokin @kannon92

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-09T11:47:21Z

LGTM

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-09T14:28:18Z

lgtm

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-16T08:50:28Z

We aim for release tomorrow along with 0.9.3

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-20T11:08:43Z

The image runs:
```
> docker run --rm registry.k8s.io/kueue/kueue:v0.10.1 
{"level":"info","ts":"2025-01-20T11:07:07.890029293Z","logger":"setup","caller":"kueue/main.go:423","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8080\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-01-20T11:07:07.890305343Z","logger":"setup","caller":"kueue/main.go:141","msg":"Initializing","gitVersion":"v0.10.1","gitCommit":"404a0cd659b2331b232cf5ddf93a1b67d5cc146c"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-20T12:28:14Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-20T12:28:20Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3950#issuecomment-2602299026):

>/close 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
