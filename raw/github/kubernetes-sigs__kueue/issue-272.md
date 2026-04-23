# Issue #272: Release v0.1.1

**Summary**: Release v0.1.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/272

**Last updated**: 2022-06-13T21:13:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-06-08T17:04:06Z
- **Updated**: 2022-06-13T21:13:33Z
- **Closed**: 2022-06-13T21:13:33Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@denkensk](https://github.com/denkensk), [@ArangoGutierrez](https://github.com/ArangoGutierrez), [@ahg-g](https://github.com/ahg-g)
- **Comments**: 23

## Description

## Release Checklist
<!--
Please do not remove items from the checklist
-->
- [x] All [OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS) must LGTM the release proposal
- [x] Verify that the changelog in this issue is up-to-date
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] an OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update things like README, deployment templates, docs, configuration, test/e2e flags.
      Submit a PR against the release branch: <!-- example #211 #214 -->
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
      to production: <!-- example kubernetes/k8s.io#3612-->
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [Github releases page](https://github.com/kubernetes-sigs/kueue/releases).
- [x] Add a link to the tagged release in this issue: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.1
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`
- [x] Add a link to the release announcement in this issue: https://groups.google.com/a/kubernetes.io/g/wg-batch/c/7Ayju9Lfg2s
- [x] For a major or minor release, update `README.md` and `docs/setup/install.md`
      in `main` branch: <!-- example #215 -->
- [x] For a major or minor release, create an unannotated _devel_ tag in the
      `main` branch, on the first commit that gets merged after the release
       branch has been created (presumably the README update commit above), and, push the tag:
      `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
      This ensures that the devel builds on the `main` branch will have a meaningful version number.
- [x] Close this issue


## Changelog

- Fixed number of pending workloads in a BestEffortFIFO ClusterQueue.
- Fixed bug in a BestEffortFIFO ClusterQueue where a workload might not be
  retried after a transient error.
- Fixed requeuing an out-of-date workload when failed to admit it.
- Fixed bug in a BestEffortFIFO ClusterQueue where unadmissible workloads
  were not removed from the ClusterQueue when removing the corresponding Queue.

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-08T17:12:12Z

Changelog ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-08T17:13:22Z

The PRs haven't merged yet. I will add the changelog in a bit.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-08T18:11:49Z

Bugfixes are always welcomed! 

/lgtm

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-08T19:41:19Z

- https://github.com/kubernetes-sigs/kueue/pull/271
- https://github.com/kubernetes-sigs/kueue/pull/273
- https://github.com/kubernetes-sigs/kueue/pull/274
- https://github.com/kubernetes-sigs/kueue/pull/275
/lgtm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-08T19:54:30Z

and #273

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-09T03:43:40Z

https://github.com/kubernetes-sigs/kueue/pull/245 and https://github.com/kubernetes-sigs/kueue/pull/248 ?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-09T12:41:54Z

I think #245 is a good candidate for cherry-picking

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-09T13:07:57Z

yeah, they would be great. Can you create the cherry-picks, @kerthcet? please include a release note.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-09T14:38:41Z

Both 245 and 248 or only 245 as @ArangoGutierrez suggested, I think both of them would be great.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-09T15:16:30Z

both make sense

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-09T18:07:44Z

I think we are all set with cherry-picks.

@ahg-g @denkensk any concerns with the release?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-10T17:00:19Z

/woof

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-06-10T17:00:20Z

@ArangoGutierrez: [![dog image](https://random.dog/d034bd3f-4f5a-4d45-92b8-0bc8c314022a.jpg)](https://random.dog/d034bd3f-4f5a-4d45-92b8-0bc8c314022a.jpg)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/272#issuecomment-1152560619):

>/woof


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-10T17:00:29Z

@ahg-g @denkensk

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-13T10:43:38Z

where can one look at the list of cherrypicked PRs for this release?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-13T10:48:25Z

list by @ArangoGutierrez https://github.com/kubernetes-sigs/kueue/issues/272#issuecomment-1150326419

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-13T12:38:02Z

/lgtm

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-13T20:19:11Z

Merged!!! woof woof
/woof

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-06-13T20:19:13Z

@ArangoGutierrez: [![dog image](https://random.dog/19059-18910-199.jpg)](https://random.dog/19059-18910-199.jpg)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/272#issuecomment-1154388633):

>Merged!!! woof woof
>/woof 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-13T20:21:25Z

I still can't pull the image though

```
docker pull registry.k8s.io/kueue/kueue:v0.1.1
```

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-13T20:23:25Z

uh it's taking some time 
```bash
[eduardo@fedora-workstation render]$ skopeo list-tags docker://registry.k8s.io/kueue/kueue
{
    "Repository": "registry.k8s.io/kueue/kueue",
    "Tags": [
        "sha256-430bb4d26a05e4de56e3e10d8bc5ebb8de28f77d575d99a4cacc8edadcf7567b.sig",
        "v0.1",
        "v0.1.0"
    ]
}
```

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-13T20:41:56Z

```bash
[eduardo@fedora-workstation render]$ skopeo list-tags docker://gcr.io/k8s-staging-kueue/kueue |grep v0.1
        "v0.1.0",
        "v0.1.1",
        "v20220412-v0.1.0",
        "v20220412-v0.1.0-2-ge422ffe",
        "v20220608-v0.1.0-4-g19f2bf5",
        "v20220609-v0.1.0-10-g1be9e66",
        "v20220609-v0.1.0-6-g89df4c6",
        "v20220609-v0.1.0-8-g3b6f8df",
        "v20220609-v0.1.1"
```

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-06-13T20:42:08Z

weird... never saw it taking so much time
