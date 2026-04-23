# Issue #2231: Release v0.6.3

**Summary**: Release v0.6.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2231

**Last updated**: 2024-05-29T12:13:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-20T07:20:04Z
- **Updated**: 2024-05-29T12:13:17Z
- **Closed**: 2024-05-29T00:27:42Z
- **Labels**: _none_
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@ahg-g](https://github.com/ahg-g), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

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
  - [x] Submit a pull request with the changes: #2292
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
      updating `registry.k8s.io/images/k8s-staging-kueue/images.yaml` to
      [promote the container images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#image-promoter)
      to production: https://github.com/kubernetes/k8s.io/pull/6846
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.6.3
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   <!--Link: example https://groups.google.com/a/kubernetes.io/g/wg-batch/c/-gZOrSnwDV4 -->
- [x] Update the below files with respective values in `main` branch :
  - Latest version in `README.md`
  - Release notes in the `CHANGELOG`
  - `version` in `site/config.toml`
  - `appVersion` in `charts/kueue/Chart.yaml`
  - `last-updated`, `last-reviewed`, `commit-hash`, `project-release`, and `distribution-points` in `SECURITY-INSIGHTS.yaml`
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v0.$(($MAJ+1)).0-devel; git tag $DEVEL main && git push $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->


## Changelog

```markdown

Changes since `v0.6.2`:

### Feature

- Improve the kubectl output for workloads using admission checks. (#2014, @vladikkuzn)

### Bug or Regression

- Change the default pprof port to 8083 to fix a bug that causes conflicting listening ports between pprof and the visibility server. (#2232, @amy)
- Check the containers limits for used resources in provisioning admission check controller and include them in the ProvisioningRequest as requests (#2293, @trasc)
- Consider deleted pods without `spec.nodeName` inactive and subject for pod replacement. (#2217, @trasc)
- Fix a bug that causes the reactivated Workload to be immediately deactivated even though it doesn't exceed the backoffLimit. (#2220, @tenzen-y)
- Fix a bug that the ".waitForPodsReady.requeuingStrategy.backoffLimitCount" is ignored when the ".waitForPodsReady.requeuingStrategy.timestamp" is not set. (#2224, @tenzen-y)
- Fix chart values configuration for the number of reconcilers for the Pod integration. (#2050, @alculquicondor)
- Fix handling of eviction in StrictFIFO to ensure the evicted workload is in the head.
  Previously, in case of priority-based preemption, it was possible that the lower-priority
  workload might get admitted while the higher priority workload is being evicted. (#2081, @mimowo)
- Fix preemption algorithm to reduce the number of preemptions within a ClusterQueue when reclamation is not possible, and when using .preemption.borrowWithinCohort (#2111, @alculquicondor)
- Fix support for MPIJobs when using a ProvisioningRequest engine that applies updates only to worker templates. (#2281, @trasc)
- Fix support for jobset v0.5.x (#2271, @alculquicondor)
- Fix the resource requests computation taking into account sidecar containers. (#2159, @IrvingMg)
- Helm Chart: Fix a bug that the kueue does not work with the cert-manager. (#2098, @EladDolev)
- HelmChart: Fix a bug that the `integrations.podOptions.namespaceSelector` is not propagated. (#2095, @EladDolev)
- JobFramework: The eviction by inactivation mechanism was moved to the workload controller.
  
  This fixes a problem where pod groups would remain with condition QuotaReserved set to True when replacement pods are missing. (#2229, @mbobrovskyi)
- Make the defaults for PodsReadyTimeout backoff more practical, as for the original values
  the couple of first requeues made the impression as immediate on users (below 10s, which 
  is negligible to the wait time spent waiting for PodsReady). 
  
  The defaults values for the formula to determine the exponential back are changed as follows:
  - base `1s -> 10s`
  - exponent: `1.41284738 -> 2`
  So, now the consecutive times to requeue a workload are: 10s, 20s, 40s, ... (#2033, @mimowo)
- MultiKueue: Fix a bug that could delay the joining clusters when it's MultiKueueCluster is created. (#2167, @trasc)
- Prevent Pod from being deleted when admitted via ProvisioningRequest that has pod updates on tolerations (#2262, @vladikkuzn)
- Use PATCH updates for pods. This fixes support for Pods when using the latest features in Kubernetes v1.29 (#2089, @mbobrovskyi)

### Other (Cleanup or Flake)

- Correctly log workload status for workloads with quota reserved, but awaiting for admission checks. (#2080, @mimowo)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-20T07:26:31Z

- [x] #2174 
- [x] #2213 
- [x] #2222 
- [x] #2225 
- [x] #2243
- [x] #2226 
- [x] #2271
- [x] #2260
- [ ] ~~#2227~~
- [x] #2278

We need to complete all the tasks below before releasing the new patch.
@alculquicondor @mimowo Any other wish list?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T08:08:55Z

I'm thinking about including https://github.com/kubernetes-sigs/kueue/issues/2216 as a nice-to-have.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-20T08:11:14Z

> I'm thinking about including #2216 as a nice-to-have.

Isn't that not a bug? Basically, we used to cherry pick only bug fixes to patch version, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T08:25:14Z

Ah, sure!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T17:58:13Z

I added #2271 and #2260 to the list

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-27T21:46:56Z

I updated the release notes.
I think we can leave #2227 for the next patch release.

I'm validating something for #2278, but if it works, we can include it in the release.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-28T04:27:32Z

> I think we can leave https://github.com/kubernetes-sigs/kueue/issues/2227 for the next patch release.

I agree with you. We can say #2227 is an enhancement request to support elastic JobSet.

> I'm validating something for https://github.com/kubernetes-sigs/kueue/issues/2278, but if it works, we can include it in the release.

Thank you for sharing your progress. So, after #2278 is resolved, we can release a patch release.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-28T14:21:48Z

It doesn't work, I'll leave #2278 for the next patch release.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-28T18:22:07Z

I ended up including #2278

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-29T00:27:39Z

I sent an announcement email to sig-scheduling and wg-batch google groups.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-29T00:27:43Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2231#issuecomment-2136310526):

>I sent an announcement email to sig-scheduling and wg-batch google groups.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
