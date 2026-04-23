# Issue #5886: Release v0.13.0

**Summary**: Release v0.13.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5886

**Last updated**: 2025-07-29T15:53:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-07T07:48:17Z
- **Updated**: 2025-07-29T15:53:27Z
- **Closed**: 2025-07-29T15:53:26Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 24

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
        `git push upstream release-$MAJ.$MIN`
- [x] Update the release branch:
  - [x] Update `RELEASE_BRANCH` and `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Update the `CHANGELOG`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/6213
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
      to production: https://github.com/kubernetes/k8s.io/pull/8336
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: <!-- example https://github.com/kubernetes-sigs/kueue/releases/tag/v0.1.0 -->
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: <!-- example #3007 -->
  - [x] Cherry-pick the pull request onto the `website` branch
- [x] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.  https://groups.google.com/a/kubernetes.io/g/wg-batch/c/B3W40Dtt8fg/m/pOAbQMChAAAJ
- [x] For a major or minor release, prepare the repo for the next version:
  - [x] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [x] Create a milestone for the next minor release and update prow to set it automatically for new PRs: https://github.com/kubernetes/test-infra/pull/35236
  - [x] Create the presubmits and the periodic jobs for the next patch release: https://github.com/kubernetes/test-infra/pull/35237
  - [x] Drop CI Jobs for testing the out-of-support branch: https://github.com/kubernetes/test-infra/pull/35237


## Changelog

```markdown

Changes since `v0.12.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- Helm: 
  
  - Fixed KueueViz installation when enableKueueViz=true is used with default values for the image specifying parameters.
  - Split the image specifying parameters into separate repository and tag, both for KueueViz backend and frontend. 
  
  If you are using Helm charts and installing KueueViz using custom images,
  then you need to specify them by kueueViz.backend.image.repository, kueueViz.backend.image.tag, 
  kueueViz.fontend.image.repository and kueueViz.frontend.image.tag parameters. (#5400, @mbobrovskyi)
 - ProvisioningRequest: Kueue now supports and manages ProvisioningRequests in v1 rather than v1beta1. 
  
  if you are using ProvisioningRequests with ClusterAutoscaler
  ensure that your ClusterAutoscaler supports the v1 API (1.31.1+). (#4444, @kannon92)
 - TAS: Drop support for MostFreeCapacity mode
  
  The `TASProfileMostFreeCapacity` feature gate is no longer available.
  If you specify that, you must remove it from the `.featureGates` in your Kueue Config or kueue-controller-manager command-line flag, `--feature-gates`. (#5536, @lchrzaszcz)
 - The API Priority and Fairness configuration for the visibility endpoint is installed by default.
  
  If your cluster is using k8s 1.28 or older, you will need to either update your version of k8s (to 1.29+) or remove the  FlowSchema and PriorityLevelConfiguration from the installation manifests of Kueue. (#5043, @mbobrovskyi)

## Upgrading steps

### 1. Backup Cohort Resources (skip if you are not using Cohorts API):

kubectl get cohorts.kueue.x-k8s.io -o yaml > cohorts.yaml


### 2. Update apiVersion in Backup File (skip if you are not using Cohort API):
Replace `v1alpha1` with `v1beta1` in `cohorts.yaml` for all resources:

sed -i -e 's/v1alpha1/v1beta1/g' cohorts.yaml
sed -i -e 's/^    parent: \(\S*\)$/    parentName: \1/' cohorts.yaml

### 3. Delete old CRDs:

kubectl delete crd cohorts.kueue.x-k8s.io


### 4. Install Kueue v0.13.x:
Follow the instruction [here](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version) to install.

### 5. Restore Cohorts Resources (skip if you are not using Cohorts API):

kubectl apply -f cohorts.yaml


## Changes by Kind

### Deprecation

- Promote Cohort CRD version to v1beta1
  
  The Cohort CRD `v1alpha1` is no longer supported.
  The `.spec.parent` in Cohort `v1alpha1` was replaced with `.spec.parentName` in Cohort `v1beta1`. (#5595, @tenzen-y)

### Feature

- AFS: Introduce the "entry penalty" for newly admitted workloads in a LQ. 
  This mechanism is designed to prevent exploiting a flaw in the previous design which allowed
  to submit and get admitted multiple workloads from a single LQ before their usage would be
  accounted by the admission fair sharing mechanism. (#5933, @IrvingMg)
- AFS: preemption candidates are now ordered within ClusterQueue with respect to LQ's usage. 
  The ordering of candidates coming from other ClusterQueues is unchanged. (#5632, @PBundyra)
- Adds the `pods_ready_to_evicted_time_seconds` metric that measures the time between workload's start,
  based on the PodsReady condition, and its eviction. (#5923, @amy)
- Flavor Fungibility: Introduces a new mode which allows to prefer preemption over borrowing when choosing a flavor. 
  In this mode the preference is decided based on FavorFungibilityStrategy. This behavior is behind the 
  FlavorFungibilityImplicitPreferenceDefault Alpha feature gate (disabled by default). (#6132, @pajakd)
- Graduate ManagedJobNamespaceSelector to GA (#5987, @kannon92)
- Helm: Allow setting the controller-manager's Pod `PriorityClassName` (#5631, @kaisoz)
- Helm: introduce new parameters to configure KueueViz installation:
  - kueueViz.backend.ingress and kueueViz.frontend.ingress to configure ingress
  - kueueViz.imagePullSecrets and kueueViz.priorityClassName (#5815, @btwseeu78)
- Helm: support for specifying nodeSelector and tolerations for all Kueue components (#5820, @zmalik)
- Introduce the ManagedJobsNamespaceSelectorAlwaysRespected feature, which allows you to manage Jobs in the managed namespaces. Even if the Jobs have queue name label, this feature ignore those Jobs when the deployed namespaces are not managed by Kueue (#5638, @PannagaRao)
- KueueViz: Add View YAML (#5992, @samzong)
- Kueue_controller_version prometheus metric, that specifies the Git commit ID used to compile Kueue controller (#5846, @rsevilla87)
- MultiKueue: Introduce the Dispatcher API which allows to provide an external dispatcher for nominating
  a subset of worker clusters for workload admission, instead of all clusters.
  
  The name of the dispatcher, either internal or external, is specified in the global config map under the
  `multikueue.dispatcherName` field. The following internal dispatchers are supported:
  - kueue.x-k8s.io/multikueue-dispatcher-all-at-once - nominates all clusters at once (default, used if the name is not specified)
  - kueue.x-k8s.io/multikueue-dispatcher-incremental - nominates clusters incrementally in constant time intervals
  
  **Important**: the current implementation requires implementations of external dispatchers to use 
  `kueue-admission` as the field manager when patching the status.nominatedClusterNames field. (#5782, @mszadkow)
- Promoted ObjectRetentionPolicies to Beta. (#6209, @mykysha)
- Support for Elastic (Dynamically Sized Jobs) in Alpha as designed in [KEP-77](https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs). 
  The implementation supports resizing (scale up and down) of batch/v1.Job and is behind the Alpha 
  `ElasticJobsViaWorkloadSlices` feature gate. Jobs which are subject to resizing need to have the
  `kueue.x-k8s.io/elastic-job` annotation added at creation time. (#5510, @ichekrygin)
- Support for Kubernetes 1.33 (#5123, @mbobrovskyi)
- TAS: Add FailFast on Node's failure handling mode (#5861, @PBundyra)
- TAS: Co-locate leader and workers in a single replica in LeaderWorkerSet (#5845, @lchrzaszcz)
- TAS: Increase the maximal number of Topology Levels (`.spec.levels`) from 8 to 16. (#5635, @sohankunkerkar)
- TAS: Introduce a mode for triggering node replacement as soon as the workload's Pods are terminating
  on the node which is not ready. This behavior is behind the ReplaceNodeOnPodTermination Alpha feature gate
  (disabled by default). (#5931, @pajakd)
- TAS: Introduce two-level scheduling (#5353, @lchrzaszcz)

### Bug or Regression

- Emit the Workload event indicating eviction when LocalQueue is stopped (#5984, @amy)
- Fix a bug that would allow a user to bypass localQueueDefaulting. (#5451, @dgrove-oss)
- Fix a bug where the GroupKindConcurrency in Kueue Config is not propagated to the controllers (#5818, @tenzen-y)
- Fix incorrect workload admission after CQ is deleted in a cohort reducing the amount of available quota. The culprit of the issue was that the cached amount of quota was not updated on CQ deletion. (#5985, @amy)
- Fix the bug that Kueue, upon startup, would incorrectly admit and then immediately deactivate
  already deactivated Workloads.
  
  This bug also prevented the ObjectRetentionPolicies feature from deleting Workloads
  that were deactivated by Kueue before the feature was enabled. (#5625, @mbobrovskyi)
- Fix the bug that the webhook certificate setting under `controllerManager.webhook.certDir` was ignored by the internal cert manager, effectively always defaulting to /tmp/k8s-webhook-server/serving-certs. (#5432, @ichekrygin)
- Fixed bug that doesn't allow Kueue to admit Workload after queue-name label set. (#5047, @mbobrovskyi)
- HC: Add Cohort Go client library (#5597, @tenzen-y)
- Helm: Fix a templating bug when configuring managedJobsNamespaceSelector. (#5393, @mtparet)
- MultiKueue: Fix a bug that batch/v1 Job final state is not synced from Workload cluster to Management cluster when disabling the `MultiKueueBatchJobWithManagedBy` feature gate. (#5615, @ichekrygin)
- MultiKueue: Fix the bug that Job deleted on the manager cluster didn't trigger deletion of pods on the worker cluster. (#5484, @ichekrygin)
- RBAC permissions for the Cohort API to update & read by admins are now created out of the box. (#5431, @vladikkuzn)
- TAS: Fix a bug for the incompatible NodeFailureController name with Prometheus (#5819, @tenzen-y)
- TAS: Fix a bug that Kueue unintentionally gives up a workload scheduling in LeastFreeCapacity if there is at least one unmatched domain. (#5803, @PBundyra)
- TAS: Fix a bug that LeastFreeCapacity Algorithm does not respect level ordering (#5464, @tenzen-y)
- TAS: Fix a bug that the tas-node-failure-controller unexpectedly is started under the HA mode even though the replica is not the leader. (#5848, @tenzen-y)
- TAS: Fix bug which prevented admitting any workloads if the first resource flavor is reservation, and the fallback is using ProvisioningRequest. (#5426, @mimowo)
- TAS: Fix the bug when Kueue crashes if the preemption target, due to quota, is using a node which is already deleted. (#5833, @mimowo)
- TAS: fix the bug which would trigger unnecessary second pass scheduling for nodeToReplace
  in the following scenarios: 
  1. Finished workload
  2. Evicted workload
  3. node to replace is not present in the workload's TopologyAssignment domains (#5585, @mimowo)
- TAS: fix the scenario when deleted workload still lives in the cache. (#5587, @mimowo)
- Use simulation of preemption for more accurate flavor assignment. 
  In particular, in certain scenarios when preemption while borrowing is enabled, 
  the previous heuristic would wrongly state that preemption was possible. (#5529, @pajakd)
- Use simulation of preemption for more accurate flavor assignment. 
  In particular, the previous heuristic would wrongly state that preemption
  in a flavor was possible even if no preemption candidates could be found. 
  
  Additionally, in scenarios when preemption while borrowing is enabled,
  the flavor in which reclaim is possible is preferred over flavor where 
  priority-based preemption is required. This is consistent with prioritizing 
  flavors when preemption without borrowing is used. (#5698, @gabesaba)

### Other (Cleanup or Flake)

- KueueViz: reduce the image size from 1.14 GB to 267MB, resulting in faster pull and shorter startup time. (#5860, @mbobrovskyi)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-07T07:55:35Z

We are aiming to release it on July 14th, but we may consider extending the timeline for 2 weeks (see [release](https://github.com/kubernetes-sigs/kueue/blob/main/RELEASE.md#release-cycle)). 

Please prioritize reviews and remaining work for features you wish to include in 0.13, the next release is planned for mid September. 

cc @tenzen-y @alaypatel07 @ichekrygin @dgrove-oss @kannon92 @mwysokin @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-07T09:11:48Z

FYI we have RC0: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.0-rc.0 for early testers

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T08:09:11Z

FYI: I synced with @tenzen-y and we decided to move the target release date to 22 July.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T08:16:40Z

We are moving the release date to July 25th, giving a bit more time to complete the ongoing work in 0.13.

cc @ichekrygin @lchrzaszcz @mszadkow @alaypatel07

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T13:43:18Z

@tenzen-y I have updated the release notes, and added the "Upgrading steps" due to graduation of cohorts PTAL.

This is inspired by https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0

I've tested manually that without the steps upgrade breaks, and with the steps it passes successfully.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T14:12:54Z

> [@tenzen-y](https://github.com/tenzen-y) I have updated the release notes, and added the "Upgrading steps" due to graduation of cohorts PTAL.
> 
> This is inspired by https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0
> 
> I've tested manually that without the steps upgrade breaks, and with the steps it passes successfully.

Shouldn't we add `sed -i -e 's/parent/parentName/g' cohorts.yaml` step?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T14:16:46Z

Ah yes, I forgot that we also renamed the field, though 's/parent/parentName/g' is likely not speciific enough

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T14:28:02Z

@mimowo shouldn't we remove the below comment?

```
 - The API Priority and Fairness configuration for the visibility endpoint is installed by default.
  
  If your cluster is using k8s 1.28 or older, you will need to either update your version of k8s (to 1.29+) or remove the  FlowSchema and PriorityLevelConfiguration from the installation manifests of Kueue. (#5043, @mbobrovskyi)
```

Because we reverted the change in https://github.com/kubernetes-sigs/kueue/pull/5380

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T14:45:26Z

> @mimowo shouldn't we remove the below comment?

I'm ok removing the comment, it is very niche where it would be useful. Only for users on 0.12.0 or 0.12.1 upgrading to 0.13.0, and really relying on the config, which is very unlikely.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T14:48:19Z

> Shouldn't we add `sed -i -e 's/parent/parentName/g' cohorts.yaml` step?

@tenzen-y , I updated the steps with a bit more selective `sed -e 's/^    parent: \(\S*\)$/    parentName: \1/' cohorts.yaml`, wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T14:51:45Z

> > [@mimowo](https://github.com/mimowo) shouldn't we remove the below comment?
> 
> I'm ok removing the comment, it is very niche where it would be useful. Only for users on 0.12.0 or 0.12.1 upgrading to 0.13.0, and really relying on the config, which is very unlikely.

SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T14:52:17Z

> > Shouldn't we add `sed -i -e 's/parent/parentName/g' cohorts.yaml` step?
> 
> [@tenzen-y](https://github.com/tenzen-y) , I updated the steps with a bit more selective `sed -e 's/^ parent: \(\S*\)$/ parentName: \1/' cohorts.yaml`, wdyt?

Did that work correct? I think you forgot to add `-i` option.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T14:57:26Z

Yeah, i tested without -i so that I could iterate easily, now fixed

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T14:58:32Z

I refined release note on some PRs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T15:00:45Z

> Yeah, i tested without -i so that I could iterate easily, now fixed

Thank you, SGTM.
For more safety, I would recommend stopping ClusterQueue by stopPolicy when they upgrade the Cohort api version.
But, I don't say that we should mention the safe way since I don't know the expected migration safety level for users.

Anyway, LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T15:02:50Z

> I refined release note on some PRs.

thanks, I regenerated the notes, ptal

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T15:04:53Z

I refined https://github.com/kubernetes-sigs/kueue/pull/5632.
Could you regenerate once more?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T15:09:18Z

done

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T15:10:39Z

> done

Thank you, SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T15:13:23Z

Absolutely, LGTM on this release.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T16:37:55Z

I confirmed that.

```shell
$ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.0 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.0
Digest: sha256:86bff65a0c41cf14f66c776fa6f6719388f4a4290f3094c51baa830d28f1864e
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.0'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.0'
        image: "registry.k8s.io/kueue/kueue:v0.13.0"

$ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.0
v0.13.0: Pulling from kueue/kueue
...
Digest: sha256:c08764e4d772fc36e5b8a488a0846038aecc4d69280ab48adf4c9eed3e0d8268
Status: Downloaded newer image for registry.k8s.io/kueue/kueue:v0.13.0
...
{"level":"info","ts":"2025-07-28T16:36:10.740008252Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.0","gitCommit":"fd121ddac504bcbc824ab995fbaf027d571e26ee","buildDate":"2025-07-28T15:48:39Z"}

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.0
v0.13.0: Pulling from kueue/kueueviz-backend
...
Digest: sha256:5fcf6220773c282f7c752abcf75d99cbfb7253014546c23d41fbc1ac6020c56c
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.13.0

$ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.0
v0.13.0: Pulling from kueue/kueueviz-frontend
...
Digest: sha256:c4f9fe15030e29725e55553f0dfc3f1ab47abd66daa0ffbd06eea225e70d76fb
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.13.0
```

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-07-28T19:55:46Z

Thank you Michał & Yuki! Really awesome effort which is greatly appreciated! 🖖

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T15:53:22Z

/close
As all steps are done

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-29T15:53:26Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5886#issuecomment-3133123530):

>/close
>As all steps are done


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
