# Issue #3441: Release v0.8.3

**Summary**: Release v0.8.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3441

**Last updated**: 2024-11-05T16:02:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-11-05T00:17:51Z
- **Updated**: 2024-11-05T16:02:49Z
- **Closed**: 2024-11-05T11:19:52Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 12

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
- [x] For major or minor releases (v$MAJ.$MIN.0), create a new release branch.
  - [x] An OWNER creates a vanilla release branch with
        `git branch release-$MAJ.$MIN main`
  - [x] An OWNER pushes the new release branch with
        `git push release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/3442
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
      via UI or `gh release upload <tag> artifacts/*`.
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io),
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7483
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.3
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: <!-- example #3007 -->
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.
    - [x] https://groups.google.com/u/1/g/kubernetes-sig-scheduling/c/uGTo75AhpjI
    - [x] https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/vahsy2zziS8
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits jobs for the next patch release:
        <!-- example https://github.com/kubernetes/test-infra/pull/33107 -->


## Changelog

```markdown
Changes since `v0.8.2`:

## Changes by Kind

### Bug or Regression

- Workload is requeued with all AdmissionChecks set to Pending if there was an AdmissionCheck in Retry state. (#3323, @PBundyra)
- Account for NumOfHosts when calculating PodSet assignments for RayJob and RayCluster (#3384, @andrewsykim)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T00:19:24Z

As @andrewsykim mentioned in https://github.com/kubernetes-sigs/kueue/pull/3384#issuecomment-2455952955, it seems that I forgot to include the KubeRay NumOfHosts fixes...

So, let us do an additional patch release.

cc : @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T00:21:12Z

It seems that some of the fixes are not included...

https://github.com/kubernetes-sigs/kueue/compare/v0.8.2...release-0.8

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-11-05T01:45:40Z

thank you @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T05:46:53Z

Thank you! LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T06:41:46Z

Tag final confirmation:

```shell
$ git log v0.8.3 --oneline 
982a9f33 (HEAD, tag: v0.8.3, upstream/release-0.8) Prepare v0.8.3 (#3442)
aa89cdb5 (release-0.8) Prepare release v0.8.2 (#3433)
fd60db57 Remove WithName() on BaseWebhook. (#3415)
4adebae9 [KubeRay] Support NumOfHosts when calculating PodSet assignments (#3386) (#3408)
59f6a906 Cleanup debug log in provisioning integration tests (#3407)
9e7a61ba Reset all Ready and Ready AdmissionChecks on Eviction as Pending (#3323) (#3395)
73e2a4ce Force status field ownership by core Kueue to fix the MultiKueue integration (#3396)
916dfde1 Automated cherry pick of #3132: Drop remove operations from webhook patches (#3358)
[...]
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T06:44:03Z

+1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T06:46:23Z

Here is the git differences between pushed v0.8.3 and v0.8.2: https://github.com/kubernetes-sigs/kueue/compare/v0.8.2...v0.8.3

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T06:49:53Z

lgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T08:46:30Z

```shell
$ docker pull registry.k8s.io/kueue/kueue:v0.8.3
v0.8.3: Pulling from kueue/kueue
3697361640de: Download complete 
Digest: sha256:bce25ee1315d46f94a84697002397f666f4619a623513d669285dd541bc59956
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.8.3
registry.k8s.io/kueue/kueue:v0.8.3

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview registry.k8s.io/kueue/kueue:v0.8.3
$ kubectl get pod -n kueue-system kueue-controller-manager-6bb64cc786-fqv5k -ojsonpath='{.spec.containers[0].image}{"\n"}'
registry.k8s.io/kueue/kueue:v0.8.3
$ kubectl get pod -n kueue-system 
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-6bb64cc786-fqv5k   2/2     Running   0          59s
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T11:19:48Z

All tasks are completed.
@andrewsykim Again, thank you for reporting this!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T11:19:53Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3441#issuecomment-2456906688):

>All tasks are completed.
>@andrewsykim Again, thank you for reporting this!
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-11-05T16:02:48Z

thank you @tenzen-y for the quick fix!
