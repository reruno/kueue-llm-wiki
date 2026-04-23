# Issue #47: Enhance Makefile arguments for img building and pushing

**Summary**: Enhance Makefile arguments for img building and pushing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/47

**Last updated**: 2022-02-22T21:45:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-02-22T12:20:10Z
- **Updated**: 2022-02-22T21:45:17Z
- **Closed**: 2022-02-22T21:45:17Z
- **Labels**: `kind/feature`
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 6

## Description

Current Makefile doesn't provide flexible ways to modify how I want to build and push the image

```bash
VERSION := $(shell git describe --tags --dirty --always)
# Image URL to use all building/pushing image targets
IMAGE_BUILD_CMD ?= docker build
IMAGE_PUSH_CMD ?= docker push
IMAGE_BUILD_EXTRA_OPTS ?=
IMAGE_REGISTRY ?= k8s.gcr.io/kueue
IMAGE_NAME := controller
IMAGE_TAG_NAME ?= $(VERSION)
IMAGE_EXTRA_TAG_NAMES ?=
IMAGE_REPO ?= $(IMAGE_REGISTRY)/$(IMAGE_NAME)
IMAGE_TAG ?= $(IMAGE_REPO):$(IMAGE_TAG_NAME)
BASE_IMAGE_FULL ?= golang:1.17
```

Also in order to be more generic, rename
`docker-image` to simply `image` or `image-build` 
`docker-push` to simply `push`  or `image-push`

This provides more flexibility when developing in a non docker environment, like `buildah` , `podman` or even building the image with CI tool on `kubernetes` it self.

/kind feature

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-22T12:20:50Z

Waiting for feedback
/assign

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-22T15:23:01Z

Example implementation : https://github.com/kubernetes-sigs/node-feature-discovery/blob/master/Makefile

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T16:31:00Z

Agree, not everyone uses docker :)

Do you really need the registry? The existing `IMG` parameter already allows you to use a full path.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-22T16:32:28Z

IMG is full path, splitting it down to registry + namespace + imagename + tag, is good when developing

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-22T16:35:34Z

it works nice for use in NFD< bc we can set it to push to staging or other registries by simply editing an ENV VAR :) , but I am open to suggestion, once we agree here, I'll submit a patch

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T16:54:59Z

sounds good.

Since you have `BASE_IMAGE_FULL`, do you want to add one for the end image that is currently one of the distroless variants?
