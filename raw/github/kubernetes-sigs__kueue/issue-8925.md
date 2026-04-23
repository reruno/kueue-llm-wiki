# Issue #8925: upgrade tests are failing when the staging image expires

**Summary**: upgrade tests are failing when the staging image expires

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8925

**Last updated**: 2026-02-13T04:18:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-02T08:53:57Z
- **Updated**: 2026-02-13T04:18:00Z
- **Closed**: 2026-02-13T04:18:00Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description


**What happened**:

Upgrade tests are failing as the 0.14.4 image is removed from staging now.

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8923/pull-kueue-test-e2e-upgrade-main/2018242645490405376
```
application/vnd.oci.image.manifest.v1+json sha256:f605cf0694c5bda65a9794dd8b612f3a00a7d15ac4b9c946ba42eed7190f4a0e
Importing	elapsed: 4.4 s	total:   0.0 B	(0.0 B/s)	
Loading image 'us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.14.4' to cluster 'kind'
  Loading image to node: kind-worker2
Error response from daemon: reference does not exist
ctr: unrecognized image format
Failed to load image 'us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.14.4' to node 'kind-worker2'
Set the current-context in a kubeconfig file.
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T08:27:22Z

We have a quick fix, but we still need someone to take care of it properly.

I think two things should happen:
1. we use the released version for the "base" version for the upgrade rather than staging image
2. we need some process to bump the upgradeFrom around releasing. There is no point testing upgrade from 0.14.x forever. I think we should be testing upgrade from N-2 essentially. So, when we are about to release 0.17 we should update the upgrade version from to 0.15.x. Maybe we could add it as a step in the release process (one of the first steps). I think it makes sense to bump it before doing the "prepare" PR, wdyt?

cc @gabesaba @tenzen-y @sohankunkerkar
