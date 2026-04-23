# Issue #5381: Release v0.12.1

**Summary**: Release v0.12.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5381

**Last updated**: 2025-05-28T10:24:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-27T16:12:26Z
- **Updated**: 2025-05-28T10:24:43Z
- **Closed**: 2025-05-28T10:24:43Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 5

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
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5389
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
      to production: https://github.com/kubernetes/k8s.io/pull/8144
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.12.1
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [x] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [x] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/5394
  - [x] Cherry-pick the pull request onto the `website` branch: https://github.com/kubernetes-sigs/kueue/pull/5399
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
Changes since `v0.12.0`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- Move the API Priority and Fairness configuration for the visibility endpoint to a separate manifest file.
  This fixes the installation issues on GKE.

  If you relied on the configuration in 0.12.0, then consider installing it as opt-in from
  the visibility-apf.yaml manifest. (#5380, @mbobrovskyi)
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-27T16:13:05Z

As I discussed with @mimowo, we decided to cut a patch version for https://github.com/kubernetes-sigs/kueue/issues/5374

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-28T07:04:02Z

@tenzen-y I have updated the changelong. I had to manually adjust the entry because the release-notes script tries to pick up the note from the reverted PR. I think we fixed it for the author, but it remains an issue for retrieving the release-note itself.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-28T07:07:34Z

> [@tenzen-y](https://github.com/tenzen-y) I have updated the changelong. I had to manually adjust the entry because the release-notes script tries to pick up the note from the reverted PR. I think we fixed it for the author, but it remains an issue for retrieving the release-note itself.

LGTM, thanks.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-28T07:25:00Z

I tested the installation from the tip of the release branch and it worked:
```
> kubectl apply --server-side -k "github.com/kubernetes-sigs/kueue/config/default?ref=release-0.12"

namespace/kueue-system serverside-applied
customresourcedefinition.apiextensions.k8s.io/admissionchecks.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/clusterqueues.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/cohorts.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/localqueues.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/multikueueclusters.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/multikueueconfigs.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/provisioningrequestconfigs.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/resourceflavors.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/topologies.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/workloadpriorityclasses.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/workloads.kueue.x-k8s.io serverside-applied
serviceaccount/kueue-controller-manager serverside-applied
role.rbac.authorization.k8s.io/kueue-leader-election-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-batch-admin-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-batch-user-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-clusterqueue-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-clusterqueue-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-jaxjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-jaxjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-job-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-job-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-jobset-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-jobset-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-localqueue-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-localqueue-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-manager-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-metrics-auth-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-metrics-reader serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-mpijob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-mpijob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-paddlejob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-paddlejob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pending-workloads-cq-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pending-workloads-lq-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pytorchjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pytorchjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-raycluster-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-raycluster-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-rayjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-rayjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-resourceflavor-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-resourceflavor-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-tfjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-tfjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-topology-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-topology-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-workload-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-workload-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-xgboostjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-xgboostjob-viewer-role serverside-applied
rolebinding.rbac.authorization.k8s.io/kueue-visibility-server-auth-reader serverside-applied
rolebinding.rbac.authorization.k8s.io/kueue-leader-election-rolebinding serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/kueue-manager-rolebinding serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/kueue-metrics-auth-rolebinding serverside-applied
configmap/kueue-manager-config serverside-applied
secret/kueue-webhook-server-cert serverside-applied
service/kueue-controller-manager-metrics-service serverside-applied
service/kueue-visibility-server serverside-applied
service/kueue-webhook-service serverside-applied
deployment.apps/kueue-controller-manager serverside-applied
apiservice.apiregistration.k8s.io/v1beta1.visibility.kueue.x-k8s.io serverside-applied
mutatingwebhookconfiguration.admissionregistration.k8s.io/kueue-mutating-webhook-configuration serverside-applied
validatingwebhookconfiguration.admissionregistration.k8s.io/kueue-validating-webhook-configuration serverside-applied
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-28T08:50:03Z

sanity check
```
> docker run --rm registry.k8s.io/kueue/kueue:v0.12.1
{"level":"info","ts":"2025-05-28T08:49:07.664223157Z","logger":"setup","caller":"kueue/main.go:468","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-05-28T08:49:07.664422137Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v20250528-v0.12.1","gitCommit":"cc50889928b4bcef0fdf932b7208f5f5aaf23f6c"}
```
helm
```
> helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.12.1 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.12.1
          image: 'registry.k8s.io/kueue/kueue/kueueviz-backend:v0.12.1'
          image: 'registry.k8s.io/kueue/kueue/kueueviz-frontend:v0.12.1'
        image: "registry.k8s.io/kueue/kueue:v0.12.1"

```
