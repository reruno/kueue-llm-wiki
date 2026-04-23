# Issue #352: Release v0.2.1

**Summary**: Release v0.2.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/352

**Last updated**: 2022-08-26T14:58:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-24T17:16:43Z
- **Updated**: 2022-08-26T14:58:46Z
- **Closed**: 2022-08-26T14:58:46Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 12

## Description

## Release Checklist

- [x] All [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal
- [x] Verify that the changelog in this issue is up-to-date
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] an OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update things like README, deployment templates, docs, configuration, test/e2e flags.
      Submit a PR against the release branch: #357
- [x] An OWNER [prepares a draft release](https://github.com/kubernetes-sigs/kueue/releases)
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts and upload the files in the `artifacts` folder
      to the draft release.
- [x] An OWNER creates a signed tag running
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
      To perform this step, you need [a PGP key registered on github](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys).
- [x] An OWNER pushes the tag with
      `git push $VERSION`
  - Triggers prow to build and publish a staging container image
      `gcr.io/k8s-staging-kueue/kueue:$VERSION`
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io), 
      updating `k8s.gcr.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: kubernetes/k8s.io#4142
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
- [x] Add a link to the tagged release in this issue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.2.0
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`
- [x] Add a link to the release announcement in this issue: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/7Ayju9Lfg2s
- [x] For a major or minor release, update `README.md` and `docs/setup/install.md`
      in `main` branch: #359 >
- [x] For a major or minor release, create an unannotated _devel_ tag in the
      `main` branch, on the first commit that gets merged after the release
       branch has been created (presumably the README update commit above), and, push the tag:
      `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
      This ensures that the devel builds on the `main` branch will have a meaningful version number.
- [x] Close this issue


## Changelog

```md
Changes since `v0.1.0`:

### Features

- Upgrade the API version from v1alpha1 to v1alpha2. v1alpha1 is no longer supported.
  v1alpha2 includes the following changes:
  - Rename Queue to LocalQueue.
  - Remove ResourceFlavor.labels. Use ResourceFlavor.metadata.labels instead.
- Add webhooks to validate and to add defaults to all kueue APIs.
- Add internal cert manager to serve webhooks with TLS.
- Use finalizers to prevent ClusterQueues and ResourceFlavors in use from being
  deleted prematurely.
- Support [codependent resources](/docs/concepts/cluster_queue.md#codepedent-resources)
  by assigning the same flavor to codependent resources in a pod set.
- Support [pod overhead](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-overhead/)
  in Workload pod sets.
- Set requests to limits if requests are not set in a Workload pod set,
  matching [internal defaulting for k8s Pods](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#resources).
- Add [prometheus metrics](/docs/reference/metrics.md) to monitor health of
  the system and the status of ClusterQueues.
- Use Server Side Apply for Workload admission to reduce API conflicts.

### Bug fixes

- Fix bug that caused Workloads that don't match the ClusterQueue's
  namespaceSelector to block other Workloads in StrictFIFO ClusterQueues.
- Fix the number of pending workloads in BestEffortFIFO ClusterQueues status.
- Fix a bug in BestEffortFIFO ClusterQueues where a workload might not be
  retried after a transient error.
- Fix requeuing an out-of-date workload when failed to admit it.
- Fix a bug in BestEffortFIFO ClusterQueues where inadmissible workloads
  were not removed from the ClusterQueue when removing the corresponding Queue.
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T17:17:20Z

Let's start by collecting LGTMs. We are waiting on #351 to merge.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-24T20:07:43Z

/lgtm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T21:26:10Z

All PRs are merged now

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T21:26:34Z

oh, forgot to cc @kerthcet

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T23:28:00Z

Maybe 
- Features:
    1. Support SSA in workload Admission.
    2. Support finalizers to clusterQueue and resourceFlavor
    3. Support internal cert management rather than introducing a third-party one like cert-manger

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T23:29:26Z

Others LGTM.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-25T14:52:08Z

I wasn't sure if those were user-visible enough, but opened a PR nevertheless #354

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-25T19:37:59Z

Back to ready :)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-08-25T20:03:08Z

/lgtm

### Comment by [@denkensk](https://github.com/denkensk) — 2022-08-25T23:51:23Z

/lgtm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-26T14:58:35Z

/close
Release steps completed

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-26T14:58:46Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/352#issuecomment-1228602267):

>/close
>Release steps completed


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
