# Issue #3873: Publish the debug:main image

**Summary**: Publish the debug:main image

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3873

**Last updated**: 2025-01-08T09:34:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-17T08:11:25Z
- **Updated**: 2025-01-08T09:34:31Z
- **Closed**: 2025-01-08T09:34:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The debug:main image is missing in the repo: https://us-central1-docker.pkg.dev/k8s-staging-images/kueue/debug

**Why is this needed**:

To make the [dump_cache.sh](https://github.com/kubernetes-sigs/kueue/blob/main/hack/dump_cache.sh) script work OOTB as it references the debug:main image.

## Discussion

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-12-17T08:33:07Z

/assign
