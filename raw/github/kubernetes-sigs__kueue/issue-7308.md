# Issue #7308: Release v0.13.7

**Summary**: Release v0.13.7

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7308

**Last updated**: 2025-10-23T12:21:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-17T08:38:20Z
- **Updated**: 2025-10-23T12:21:06Z
- **Closed**: 2025-10-23T12:21:06Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

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
  - [x] Submit a pull request with the changes: #7357 <!-- example #211 #214 -->
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
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.7
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7360
  - [ ] Cherry-pick the pull request onto the `website` branch
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
  - [ ] Create the presubmits and the periodic jobs for the next patch release: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34561 -->
  - [ ] Drop CI Jobs for testing the out-of-support branch: <!-- CI_PULL -->
        <!-- example: https://github.com/kubernetes/test-infra/pull/34562 -->


## Changelog

```markdown
Changes since `v0.13.6`:

## Changes by Kind

### Feature

- JobFramework: Introduce an optional interface for custom Jobs, called JobWithCustomWorkloadActivation, which can be used to deactivate or active a custom CRD workload. (#7199, @tg123)

### Bug or Regression

- Fix existing workloads not being re-evaluated when new clusters are added to MultiKueueConfig. Previously, only newly created workloads would see updated cluster lists. (#7351, @mimowo)
- Fix handling of RayJobs which specify the spec.clusterSelector and the "queue-name" label for Kueue. These jobs should be ignored by kueue as they are being submitted to a RayCluster which is where the resources are being used and was likely already admitted by kueue. No need to double admit.
  Fix on a panic on kueue managed jobs if spec.rayClusterSpec wasn't specified. (#7257, @laurafitzgerald)
- Fixed a bug that Kueue would keep sending empty updates to a Workload, along with sending the "UpdatedWorkload" event, even if the Workload didn't change. This would happen for Workloads using any other mechanism for setting
  the priority than the WorkloadPriorityClass, eg. for Workloads for PodGroups. (#7306, @mbobrovskyi)
- MultiKueue x ElasticJobs: fix webhook validation bug which prevented scale up operation when any other
  than the default "AllAtOnce" MultiKueue dispatcher was used. (#7333, @mszadkow)
- Visibility API: Fix a bug that the Config clientConnection is not respected in the visibility server. (#7224, @tenzen-y)

### Other (Cleanup or Flake)

- Improve the messages presented to the user in scheduling events, by clarifying the reason for "insufficient quota"
  in case of workloads with multiple PodSets. 
  
  Example:
  - before: "insufficient quota for resource-type in flavor example-flavor, request > maximum capacity (24 > 16)"
  - after: "insufficient quota for resource-type in flavor example-flavor, previously considered podsets requests (16) + current podset request (8) > maximum capacity (16)" (#7294, @iomarsayed)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T10:32:42Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T11:53:29Z

sanity testing:

```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.13.7 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.13.7
Digest: sha256:0794e2b8361456855ca5a5cfa43785ede62a358ae472a2bf2609610ce386f2da
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.13.7'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.13.7'
        image: "registry.k8s.io/kueue/kueue:v0.13.7"
```

```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.13.7
v0.13.7: Pulling from kueue/kueue
Digest: sha256:e2e99e1cb062daf9bef0a37a5f6761a18398565de903dd58709e5639c341032b
Status: Image is up to date for registry.k8s.io/kueue/kueue:v0.13.7
{"level":"info","ts":"2025-10-23T11:52:32.152880884Z","logger":"setup","caller":"kueue/main.go:482","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwaitForPodsReady: {}\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-10-23T11:52:32.153188364Z","logger":"setup","caller":"kueue/main.go:147","msg":"Initializing","gitVersion":"v0.13.7","gitCommit":"e2c7413d7c767c549db725302a4a5a77926a3650","buildDate":"2025-10-23T11:16:11Z"}
```

```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.13.7
v0.13.7: Pulling from kueue/kueueviz-backend
Digest: sha256:779422b82ce9c704c3fe731d440b6fb11cdc854855e6a7cd86f70242e7a9b1ee
Status: Image is up to date for registry.k8s.io/kueue/kueueviz-backend:v0.13.7
2025/10/23 11:52:56 Starting pprof server on localhost:6060
```

```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.13.7
v0.13.7: Pulling from kueue/kueueviz-frontend
Digest: sha256:c13a0993ca2eb87c2545711d8bafacc55efd3e635c9699c3cf4d0f2c4fd903f3
Status: Image is up to date for registry.k8s.io/kueue/kueueviz-frontend:v0.13.7
```
