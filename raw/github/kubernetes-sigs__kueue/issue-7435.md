# Issue #7435: Release v0.14.3

**Summary**: Release v0.14.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7435

**Last updated**: 2025-10-30T16:04:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-30T07:59:38Z
- **Updated**: 2025-10-30T16:04:03Z
- **Closed**: 2025-10-30T16:04:03Z
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
  - [x] Submit a pull request with the changes: #7454 <!-- example #211 #214 -->
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
      to production: https://github.com/kubernetes/k8s.io/pull/8713
  - [x] Update `registry.k8s.io/images/k8s-staging-kueue/images.yaml`.
- [x] Wait for the PR to be merged and verify that the image `registry.k8s.io/kueue/kueue:$VERSION` is available.
- [x] Publish the draft release prepared at the [GitHub releases page](https://github.com/kubernetes-sigs/kueue/releases).
      Link: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.3
- [x] Run the [openvex action](https://github.com/kubernetes-sigs/kueue/actions/workflows/openvex.yaml) to generate openvex data. The action will add the file to the release artifacts.
- [x] Run the [SBOM action](https://github.com/kubernetes-sigs/kueue/actions/workflows/sbom.yaml) to generate the SBOM and add it to the release.
- [ ] Update the `main` branch :
  - [ ] Update `RELEASE_VERSION` in `Makefile` and run `make prepare-release-branch`
  - [x] Release notes in the `CHANGELOG`
  - [ ] `SECURITY-INSIGHTS.yaml` values by running `make update-security-insights GIT_TAG=$VERSION`
  - [x] Submit a pull request with the changes: https://github.com/kubernetes-sigs/kueue/pull/7455
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
Changes since `v0.14.2`:

## Urgent Upgrade Notes 

### (No, really, you MUST read this before you upgrade)

- MultiKueue: validate remote client kubeconfigs and reject insecure kubeconfigs by default; add feature gate MultiKueueAllowInsecureKubeconfigs to temporarily allow insecure kubeconfigs until v0.17.0.
  
  if you are using MultiKueue kubeconfigs which are not passing the new validation please
  enable the `MultiKueueAllowInsecureKubeconfigs` feature gate and let us know so that we can re-consider
  the deprecation plans for the feature gate. (#7452, @mszadkow)
 
## Changes by Kind

### Bug or Regression

- Fix a bug where a workload would not get requeued after eviction due to failed hotswap. (#7379, @pajakd)
- Fix the kueue-controller-manager startup failures.
  
  This fixed the Kueue CrashLoopBackOff due to the log message: "Unable to setup indexes","error":"could not setup multikueue indexer: setting index on workloads admission checks: indexer conflict. (#7440, @IrvingMg)
- Fixed the bug that prevented managing workloads with duplicated environment variable names in containers. This issue manifested when creating the Workload via the API. (#7443, @mbobrovskyi)
- Increase the number of Topology levels limitations for localqueue and workloads to 16 (#7427, @kannon92)
- Services: fix the setting of the `app.kubernetes.io/component` label to discriminate between different service components within Kueue as follows:
  - controller-manager-metrics-service for kueue-controller-manager-metrics-service 
  - visibility-service for kueue-visibility-server
  - webhook-service for kueue-webhook-service (#7450, @rphillips)

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-30T08:39:09Z

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T15:55:25Z

sanity checks:

```
❯ helm template oci://registry.k8s.io/kueue/charts/kueue --set enableKueueViz=true --version 0.14.3 | grep registry.k8s.io
Pulled: registry.k8s.io/kueue/charts/kueue:0.14.3
Digest: sha256:ff8b47a3c904837bc1c7c73035269f9ecbc654b39128d5f200b3dff313c12887
          image: 'registry.k8s.io/kueue/kueueviz-backend:v0.14.3'
          image: 'registry.k8s.io/kueue/kueueviz-frontend:v0.14.3'
        image: "registry.k8s.io/kueue/kueue:v0.14.3"
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueue:v0.14.3
v0.14.3: Pulling from kueue/kueue
Digest: sha256:2c5b782a2a3954ef72576db22d6bdc752d3604d39f3be734662ab7acfa2f61dc
Status: Image is up to date for registry.k8s.io/kueue/kueue:v0.14.3
{"level":"info","ts":"2025-10-30T15:54:24.9334297Z","logger":"setup","caller":"kueue/main.go:507","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  dispatcherName: kueue.x-k8s.io/multikueue-dispatcher-all-at-once\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nwaitForPodsReady: {}\nwebhook:\n  certDir: /tmp/k8s-webhook-server/serving-certs\n  port: 9443\n"}
{"level":"info","ts":"2025-10-30T15:54:24.93358803Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"v0.14.3","gitCommit":"7c2881e3214f174897db25865e39471500ca9689","buildDate":"2025-10-30T15:24:35Z"}
```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-backend:v0.14.3
v0.14.3: Pulling from kueue/kueueviz-backend
fd4aa3667332: Already exists 
bfb59b82a9b6: Already exists 
017886f7e176: Already exists 
62de241dac5f: Already exists 
2780920e5dbf: Already exists 
7c12895b777b: Already exists 
3214acf345c0: Already exists 
5664b15f108b: Already exists 
045fc1c20da8: Already exists 
4aa0ea1413d3: Already exists 
da7816fa955e: Already exists 
ddf74a63f7d8: Already exists 
7f620af5f9d0: Pull complete 
Digest: sha256:fef57a36eaec628631fe23764adc3713251998bba3c16204d3d669cf3a4f760d
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-backend:v0.14.3
2025/10/30 15:54:49 Starting pprof server on localhost:6060

```
```
❯ docker run --pull=always -it registry.k8s.io/kueue/kueueviz-frontend:v0.14.3
v0.14.3: Pulling from kueue/kueueviz-frontend
abe1fea37542: Already exists 
f4cd9bff1825: Already exists 
665ebdb29186: Already exists 
d3fca9f43ccc: Already exists 
2ea8a20d5cb7: Already exists 
1f01a4ce38ec: Pull complete 
164941841989: Pull complete 
4f42325971fd: Pull complete 
a1f3dc343341: Pull complete 
4f4fb700ef54: Pull complete 
Digest: sha256:d8217b5eefe1b8e23cbbc9a9939800dc4ab69fb13eabc54bfc89604eb91296e8
Status: Downloaded newer image for registry.k8s.io/kueue/kueueviz-frontend:v0.14.3
```
