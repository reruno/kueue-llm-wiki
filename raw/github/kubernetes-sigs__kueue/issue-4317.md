# Issue #4317: Release v0.9.4

**Summary**: Release v0.9.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4317

**Last updated**: 2025-02-25T16:33:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-19T12:58:51Z
- **Updated**: 2025-02-25T16:33:30Z
- **Closed**: 2025-02-25T16:28:01Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 8

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
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4397
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
- [x] Submit a PR against [k8s.io](https://github.com/kubernetes/k8s.io) to 
      [promote the container images and Helm Chart](https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/7830
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
  - [x] Update `registry.k8s.io/images/charts/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.4
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/4400
  - [x] Cherry-pick the pull request onto the `website` branch: https://github.com/kubernetes-sigs/kueue/pull/4402
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/a/kubernetes.io/g/wg-batch/c/aR4DAb7Nvkc/m/MAaLmvvgAwAJ
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
Changes since `v0.9.3`:

## Changes by Kind

### Bug or Regression

- Add missing external types to apply configurations (#4202, @astefanutti)
- Disable the StatefulSet webhook in the kube-system and kueue-system namespaces by default. 
  This aligns the default StatefulSet webhook configuration with the Pod and Deployment configurations. (#4161, @@dgrove-oss)
- Fix a bug is incorrect field path in inadmissible reasons and messages when Pod resources requests do not satisfy LimitRange constraints. (#4290, @tenzen-y)
- Fix a bug is incorrect field path in inadmissible reasons and messages when container requests exceed limits (#4246, @tenzen-y)
- Fix a bug that allowed unsupported changes to some PodSpec fields which were resulting in the StatefulSet getting stuck on Pods with schedulingGates. 
  
  The validation blocks mutating the following Pod spec fields: `nodeSelector`, `affinity`, `tolerations`, `runtimeClassName`, `priority`, `topologySpreadConstraints`, `overhead`, `resourceClaims`, plus container (and init container) fields: `ports` and `resources.requests`. 
  
  Mutating other fields, such as container image, command or args, remains allowed and supported. (#4154, @mbobrovskyi)
- Fix a bug that doesn't allow Kueue to delete Pods after a StatefulSet is deleted. (#4206, @mbobrovskyi)
- Fix a bug that prevented tracking some of the controller-runtime metrics in Prometheus. (#4227, @tenzen-y)
- Fix a bug truncating AdmissionCheck condition message at `1024` characters when creation of the associated ProvisioningRequest or PodTemplate fails. 
  Instead, use the `32*1024` characters limit as for condition messages. (#4195, @mbobrovskyi)
- Fix the bug that prevented Kueue from updating the AdmissionCheck state in the Workload status on a ProvisioningRequest creation error. (#4118, @mbobrovskyi)
- Helm: Fix the unspecified LeaderElection Role and Rolebinding namespaces (#4386, @eric-higgins-ai)
- MultiKueue: Do not update the status of the Job on the management cluster while the Job is suspended. This is updated  for jobs represented by JobSet, Kubeflow Jobs and MPIJob. (#4085, @IrvingMg)
- Propagate the top-level setting of the `kueue.x-k8s.io/priority-class` label to the PodTemplate for
  Deployments and StatefulSets. This way the Workload Priority class is no longer ignored by the workloads. (#4036, @Abirdcfly)
- TAS: Fix a bug that unschedulable nodes (".spec.unschedulable=true") are counted as allocatable capacities (#4209, @tenzen-y)
- TAS: Fixed a bug that allows to create a JobSet with both kueue.x-k8s.io/podset-required-topology and kueue.x-k8s.io/podset-preferred-topology annotations set on the PodTemplate. (#4156, @mbobrovskyi)

### Other (Cleanup or Flake)

- Renamed Log key from "attemptCount" to "schedulingCycleCount". This key tracks how many scheduling cycles we have done since starting Kueue. (#4241, @tenzen-y)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T13:24:31Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T13:24:44Z

Waiting for cherry-picking of https://github.com/kubernetes-sigs/kueue/pull/4271

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T13:26:05Z

Similarly as for [v0.10.2](https://github.com/kubernetes-sigs/kueue/issues/4318) we are aiming for Friday.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T18:04:44Z

> Waiting for cherry-picking of [#4271](https://github.com/kubernetes-sigs/kueue/pull/4271)

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/4322#discussion_r1961715047, we decided not to cherry-pick #4271 to release-0.9 since 0.9 and main have so many conflicts.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T14:52:34Z

I confirmed the latest release note is the truly latest: https://www.diffchecker.com/ql2pXxzr/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T16:10:47Z

I confirmed the promoted images in the following:

```shell
$ docker run registry.k8s.io/kueue/kueue:v0.9.4
Unable to find image 'registry.k8s.io/kueue/kueue:v0.9.4' locally
v0.9.4: Pulling from kueue/kueue
Digest: sha256:b67819360cbb3e22bd6699e3f41198eb110796aed9ed8b7460ce284dfe2634be
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.9.4
{"level":"info","ts":"2025-02-25T16:08:43.563102879Z","logger":"setup","caller":"kueue/main.go:122","msg":"Initializing","gitVersion":"v0.9.4","gitCommit":"74e8b6b0d07e5aae5e07e49ff6a3361f8ef2eb30"}

$ helm template oci://registry.k8s.io/charts/kueue --version v0.9.4 | grep registry.k8s.io/kueue/kueue:v0.9.4
Pulled: registry.k8s.io/charts/kueue:v0.9.4
Digest: sha256:bc238183a94983d85483dcb028f2c6dbffe5dee8d9f2b46988680049eb708df9
        image: "registry.k8s.io/kueue/kueue:v0.9.4"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-25T16:27:56Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-25T16:28:02Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4317#issuecomment-2682577959):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
