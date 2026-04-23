# Issue #3916: Support linux/arm64 on Kueue visibility

**Summary**: Support linux/arm64 on Kueue visibility

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3916

**Last updated**: 2025-01-14T21:10:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-01-02T02:11:07Z
- **Updated**: 2025-01-14T21:10:46Z
- **Closed**: 2025-01-14T21:10:43Z
- **Labels**: `kind/feature`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to support the linux/arm64 on the Kueue visibility image.

https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L358-L360

**Why is this needed**:
The current build system supports only the linux/amd64 platform.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-02T02:11:27Z

cc: @mbobrovskyi

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-01-03T15:29:03Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-14T13:47:24Z

@tenzen-y @KPostOffice 

I take another look for this issue and found that we already support `linux/arm64` you can check it for example [here](https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-backend/sha256:83b0e6afbf409c6d1659fbf4349dd6f7938fb3b0b770fd6d50edcf9d580f0681;tab=manifest?inv=1&invt=Abm08g).

The `kueue-viz-image` target https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L358-L360 is using just for test to do not build all platforms. For test it's enough to have only `linux/amd64`

For build and push we are using `kueue-viz-image-push` target.

https://github.com/kubernetes-sigs/kueue/blob/b35ed012bee655264e6329b17c18fd756a08a4a7/Makefile#L31
https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L354-L356
https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/cloudbuild.yaml#L14

Please let me know if I missed something.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-01-14T18:34:53Z

@mbobrovskyi Yeah, this makes sense. I will close my PR

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-14T21:10:37Z

> [@tenzen-y](https://github.com/tenzen-y) [@KPostOffice](https://github.com/KPostOffice)
> 
> I take another look for this issue and found that we already support `linux/arm64` you can check it for example [here](https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-backend/sha256:83b0e6afbf409c6d1659fbf4349dd6f7938fb3b0b770fd6d50edcf9d580f0681;tab=manifest?inv=1&invt=Abm08g).
> 
> The `kueue-viz-image` target
> 
> [kueue/Makefile](https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L358-L360)
> 
> Lines 358 to 360 in [24dffe8](/kubernetes-sigs/kueue/commit/24dffe8373d700b65cae25d9276ad70c9e02252a)
> 
>  # Build a docker local us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue-viz image 
>  .PHONY: kueue-viz-image 
>  kueue-viz-image: VIZ_PLATFORMS=linux/amd64 
> is using just for test to do not build all platforms. For test it's enough to have only `linux/amd64`
> For build and push we are using `kueue-viz-image-push` target.
> 
> [kueue/Makefile](https://github.com/kubernetes-sigs/kueue/blob/b35ed012bee655264e6329b17c18fd756a08a4a7/Makefile#L31)
> 
> Line 31 in [b35ed01](/kubernetes-sigs/kueue/commit/b35ed012bee655264e6329b17c18fd756a08a4a7)
> 
>  VIZ_PLATFORMS ?= linux/amd64,linux/arm64,linux/s390x,linux/ppc64le 
> 
> [kueue/Makefile](https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L354-L356)
> 
> Lines 354 to 356 in [24dffe8](/kubernetes-sigs/kueue/commit/24dffe8373d700b65cae25d9276ad70c9e02252a)
> 
>  .PHONY: kueue-viz-image-push 
>  kueue-viz-image-push: PUSH=--push 
>  kueue-viz-image-push: kueue-viz-image-build 
> 
> [kueue/cloudbuild.yaml](https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/cloudbuild.yaml#L14)
> 
> Line 14 in [24dffe8](/kubernetes-sigs/kueue/commit/24dffe8373d700b65cae25d9276ad70c9e02252a)
> 
>  - kueue-viz-image-push 
> Please let me know if I missed something.

Oh, that is correct. Thank you for checking that.

Frontend: https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-frontend/sha256:7e1eb2a1841dcc6383d2877113568b5de9ce3723b9b193975a838997f36bce4d;tab=manifest?inv=1&invt=Abm2tA
Backend: https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-backend/sha256:24a3a99b59681f52909d289b0fb15004931bbdc12325673779b3b78e639ae467;tab=manifest?inv=1&invt=Abm2tA

@KPostOffice Thank you for helping!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-14T21:10:43Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3916#issuecomment-2591109245):

>> [@tenzen-y](https://github.com/tenzen-y) [@KPostOffice](https://github.com/KPostOffice)
>> 
>> I take another look for this issue and found that we already support `linux/arm64` you can check it for example [here](https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-backend/sha256:83b0e6afbf409c6d1659fbf4349dd6f7938fb3b0b770fd6d50edcf9d580f0681;tab=manifest?inv=1&invt=Abm08g).
>> 
>> The `kueue-viz-image` target
>> 
>> [kueue/Makefile](https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L358-L360)
>> 
>> Lines 358 to 360 in [24dffe8](/kubernetes-sigs/kueue/commit/24dffe8373d700b65cae25d9276ad70c9e02252a)
>> 
>>  # Build a docker local us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue-viz image 
>>  .PHONY: kueue-viz-image 
>>  kueue-viz-image: VIZ_PLATFORMS=linux/amd64 
>> is using just for test to do not build all platforms. For test it's enough to have only `linux/amd64`
>> For build and push we are using `kueue-viz-image-push` target.
>> 
>> [kueue/Makefile](https://github.com/kubernetes-sigs/kueue/blob/b35ed012bee655264e6329b17c18fd756a08a4a7/Makefile#L31)
>> 
>> Line 31 in [b35ed01](/kubernetes-sigs/kueue/commit/b35ed012bee655264e6329b17c18fd756a08a4a7)
>> 
>>  VIZ_PLATFORMS ?= linux/amd64,linux/arm64,linux/s390x,linux/ppc64le 
>> 
>> [kueue/Makefile](https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/Makefile#L354-L356)
>> 
>> Lines 354 to 356 in [24dffe8](/kubernetes-sigs/kueue/commit/24dffe8373d700b65cae25d9276ad70c9e02252a)
>> 
>>  .PHONY: kueue-viz-image-push 
>>  kueue-viz-image-push: PUSH=--push 
>>  kueue-viz-image-push: kueue-viz-image-build 
>> 
>> [kueue/cloudbuild.yaml](https://github.com/kubernetes-sigs/kueue/blob/24dffe8373d700b65cae25d9276ad70c9e02252a/cloudbuild.yaml#L14)
>> 
>> Line 14 in [24dffe8](/kubernetes-sigs/kueue/commit/24dffe8373d700b65cae25d9276ad70c9e02252a)
>> 
>>  - kueue-viz-image-push 
>> Please let me know if I missed something.
>
>Oh, that is correct. Thank you for checking that.
>
>Frontend: https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-frontend/sha256:7e1eb2a1841dcc6383d2877113568b5de9ce3723b9b193975a838997f36bce4d;tab=manifest?inv=1&invt=Abm2tA
>Backend: https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/kueue/kueue-viz-backend/sha256:24a3a99b59681f52909d289b0fb15004931bbdc12325673779b3b78e639ae467;tab=manifest?inv=1&invt=Abm2tA
>
>@KPostOffice Thank you for helping!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
