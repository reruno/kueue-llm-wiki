# Issue #197: Release v0.1.0

**Summary**: Release v0.1.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/197

**Last updated**: 2022-04-12T20:21:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-04-08T20:19:01Z
- **Updated**: 2022-04-12T20:21:40Z
- **Closed**: 2022-04-12T20:21:40Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 10

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
      Submit a PR against the release branch: #211
- [x] An OWNER prepares a draft release
  - [x] Create a draft release at [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
  - [x] Write the change log into the draft release.
  - [x] Run
      `make artifacts IMAGE_REGISTRY=k8s.gcr.io/kueue GIT_TAG=$VERSION`
      to generate the artifacts and upload the files in the `artifacts` folder
      to the draft release.
- [x] An OWNER runs
     `git tag -s $VERSION`
      and inserts the changelog into the tag description.
- [x] An OWNER pushes the tag with
      `git push $VERSION`
  - Triggers prow to build and publish a staging container image
      `gcr.io/k8s-staging-kueue/kueue:$VERSION`
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io), updating `k8s.gcr.io/images/k8s-staging-kueue/images.yaml` to [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter) to production.
- [x] Wait for the PR to be merged and verify that the image `k8s.gcr.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
- [x] Add a link to the tagged release in this issue https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`
- [x] Add a link to the release announcement in this issue https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4
- [x] For a major or minor release, update `docs/setup/install.md` in `main` branch.
  - [x] Update references on deployment yamls.
  - [x] Wait for the PR to be merged #215
- [x] For a major release, create an unannotated _devel_ tag in the `main` branch, on the first commit that gets merged after the release branch has been created (presumably the README update commit above), and, push the tag:
      `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
      This ensures that the devel builds on the `main` branch will have a meaningful version number.
- [x] Close this issue



## Changelog


First release of Kueue, a Kubernetes native set of APIs and controllers for job queueing.

The release includes:
- The API group `kueue.x-k8s.io/v1alpha1` that includes the ClusterQueue, Queue, ResourceFlavor and Workload APIs.
- A set of controllers that support quota-based job queuing, with:
  - Resource sharing: unused resources can be borrowed to other tenants.
  - Resource flavors and fungibility:  you can define multiple flavors or variants of a resource. Jobs are assigned to flavors that are still available.
  - Two queueing strategies: `StrictFIFO` and `BestEffortFIFO`.
- Support for the Kubernetes `batch/v1.Job` API.
- The Workload API abstraction allows you to integrate a third-party job API with Kueue.
- Documentation available at https://sigs.k8s.io/kueue/docs

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-11T13:03:16Z

PIN this one, now that the umbrella is complete

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-12T17:18:57Z

Let's start. Can OWNERS +1?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-04-12T17:27:53Z

+1

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-12T17:31:46Z

/lgtm

### Comment by [@denkensk](https://github.com/denkensk) — 2022-04-12T17:44:51Z

/lgtm

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-12T17:54:29Z

+1

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-12T19:44:11Z

```bash
[eduardo@fedora-workstation kueue]$ skopeo list-tags docker://k8s.gcr.io/kueue/kueue
{
    "Repository": "k8s.gcr.io/kueue/kueue",
    "Tags": [
        "sha256-430bb4d26a05e4de56e3e10d8bc5ebb8de28f77d575d99a4cacc8edadcf7567b.sig",
        "v0.1",
        "v0.1.0"
    ]
}
```

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-12T19:44:42Z

Nice! congrats on the first release :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-12T20:21:30Z

Next, I'll send a PR to the template to link to sample PRs.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-12T20:21:40Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/197#issuecomment-1097178448):

>Next, I'll send a PR to the template to link to sample PRs.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
