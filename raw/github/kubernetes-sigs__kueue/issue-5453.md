# Issue #5453: Docker images no longer exist for versions before 0.10.3

**Summary**: Docker images no longer exist for versions before 0.10.3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5453

**Last updated**: 2025-06-03T03:36:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@eric-higgins-ai](https://github.com/eric-higgins-ai)
- **Created**: 2025-06-03T02:32:42Z
- **Updated**: 2025-06-03T03:36:41Z
- **Closed**: 2025-06-03T03:36:40Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:
I can no longer pull prebuilt docker images for versions <0.10.3.
```
docker pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1
Error response from daemon: manifest for us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1 not found: manifest unknown: Failed to fetch "v0.10.1"

docker pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.2
Error response from daemon: manifest for us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.2 not found: manifest unknown: Failed to fetch "v0.10.2"
```

Pulling using digest doesn't work either, so it seems the image was deleted rather than just untagged (this is the digest for v0.10.2):
```
docker pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue@sha256:3cc80f3b1588b3e7cf51634cdb73b43d73185ba7be3c3cbb3a086236b3af8292
Error response from daemon: manifest for us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue@sha256:3cc80f3b1588b3e7cf51634cdb73b43d73185ba7be3c3cbb3a086236b3af8292 not found: manifest unknown: Requested entity was not found.
```

However, pulling v0.10.3 works.

I mostly want to understand why this happened. We're relying on kueue in production so images disappearing can cause outages.

**What you expected to happen**:
Prebuilt docker images exist.

## Discussion

### Comment by [@eric-higgins-ai](https://github.com/eric-higgins-ai) — 2025-06-03T03:36:40Z

ah wait I think this is our bad. We were using a version of the helm chart off an unmerged branch, and it seems like y'all have some deployment step that replaces the staging repository with registry.k8s.io when releasing
