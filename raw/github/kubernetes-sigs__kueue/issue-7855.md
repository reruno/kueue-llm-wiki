# Issue #7855: Release v0.13.10

**Summary**: Release v0.13.10

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7855

**Last updated**: 2025-11-27T17:18:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T17:09:08Z
- **Updated**: 2025-11-27T17:18:47Z
- **Closed**: 2025-11-27T17:18:46Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

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
  - [x] Submit a pull request with the changes: #7963 <!-- example #211 #214 -->
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
      to production: <!-- example kubernetes/k8s.io#7899 -->
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.10
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [x] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [ ] Submit a pull request with the changes: <!-- example #3007 -->
  - [x] Cherry-pick the pull request onto the `website` branch
- [ ] For major or minor releases, merge the `main` branch into the `website` branch to publish the updated documentation.
- [x] Send an announcement email to `sig-scheduling@kubernetes.io` and `wg-batch@kubernetes.io` with the subject `[ANNOUNCE] kueue $VERSION is released`.   https://groups.google.com/u/1/a/kubernetes.io/g/wg-batch/c/YBrsePWjj18
- [ ] For a major or minor release, prepare the repo for the next version:
  - [ ] Create an unannotated _devel_ tag in the
        `main` branch, on the first commit that gets merged after the release
         branch has been created (presumably the README update commit above), and, push the tag:
        `DEVEL=v$MAJ.$(($MIN+1)).0-devel; git tag $DEVEL main && git push upstream $DEVEL`
        This ensures that the devel builds on the `main` branch will have a meaningful version number.
  - [ ] Create a milestone for the next minor release and update prow to set it automatically for new PRs:
        <!-- example https://github.com/kubernetes/test-infra/pull/30222 -->
  - [ ] Create the presubmits and the periodic jobs for the next patch release: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.13.9`:

## Changes by Kind

### Bug or Regression

- AdmissionFairSharing: Fix the bug that occasionally a workload may get admitted from a busy LocalQueue,
  bypassing the entry penalties. (#7916, @IrvingMg)
- Fix a bug that an error during workload preemption could leave the scheduler stuck without retrying. (#7817, @olekzabl)
- Fix a bug that the cohort client-go lib is for a Namespaced resource, even though the cohort is a Cluster-scoped resource. (#7801, @tenzen-y)
- Fix integration of `manageJobWithoutQueueName` and `managedJobsNamespaceSelector` with JobSet by ensuring that jobSets without a queue are  not managed by Kueue if are not selected by the  `managedJobsNamespaceSelector`. (#7761, @MaysaMacedo)
- Fix issue #6711 where an inactive workload could transiently get admitted into a queue. (#7944, @olekzabl)
- Fix the bug that the kubernetes.io/job-name label was not propagated from the k8s Job to the PodTemplate in
  the Workload object, and later to the pod template in the ProvisioningRequest. 
  
  As a consequence the ClusterAutoscaler could not properly resolve pod affinities referring to that label,
  via podAffinity.requiredDuringSchedulingIgnoredDuringExecution.labelSelector. For example, 
  such pod affinities can be used to request ClusterAutoscaler to provision a single node which is large enough
  to accommodate all Pods on a single Node.
  
  We also introduce the PropagateBatchJobLabelsToWorkload feature gate to disable the new behavior in case of 
  complications. (#7613, @yaroslava-serdiuk)
- TAS: Fix the `requiredDuringSchedulingIgnoredDuringExecution` node affinity setting being ignored in topology-aware scheduling. (#7936, @kshalot)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-25T12:42:20Z

LGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T16:37:23Z

```
❯ docker run -it registry.k8s.io/kueue/kueue:v0.13.10
{"level":"info","ts":"2025-11-27T16:35:48.115892891Z","logger":"setup","caller":"kueue/main.go:482","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwaitForPodsReady: {}\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-11-27T16:35:48.116046571Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.10","gitCommit":"ef56fd71bb83b75e8ecfe74060c8ae2796446b7d","buildDate":"2025-11-27T15:51:37Z"}
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.10
v0.13.10: Pulling from kueue/kueueviz-backend
Digest: sha256:1dc7a953cf04c48c6d019456b7aab304d7cfd2112b16f13ff7e77b956445a393
Status: Image is up to date for registry.k8s.io/kueue/kueueviz-backend:v0.13.10
2025/11/27 16:36:28 Error creating Kubernetes client: failed to load kubeconfig from /home/nonroot/.kube/config: stat /home/nonroot/.kube/config: no such file or directory
2025/11/27 16:36:28 Starting pprof server on localhost:6060
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.10
v0.13.10: Pulling from kueue/kueueviz-frontend
Digest: sha256:dce3a3e693c350baccefe79f8d8817fc8cd08729f1cc9fa22f9bb04b983721d1
Status: Image is up to date for registry.k8s.io/kueue/kueueviz-frontend:v0.13.10
```
```
❯ helm template oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue --set enableKueueViz=true --version 0.13.10 | grep registry.k8s.io

Pulled: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue:0.13.10
Digest: sha256:f2095e22023e8d2b0d58e178deb2e74fe3267b28dca85b4b67c3b2b7ce349689
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.10'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.10'
        image: "registry.k8s.io/kueue/kueue:v0.13.10"

```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T17:18:42Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-27T17:18:47Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7855#issuecomment-3586846893):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
