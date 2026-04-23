# Issue #1382: FIPS compliance for Kueue

**Summary**: FIPS compliance for Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1382

**Last updated**: 2023-12-05T19:56:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@anishasthana](https://github.com/anishasthana)
- **Created**: 2023-11-29T18:10:45Z
- **Updated**: 2023-12-05T19:56:04Z
- **Closed**: 2023-12-04T18:13:01Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

## Description

The Kueue image is currently not FIPS compliant, which makes it such that it is unusable in some high security environments.

https://github.com/openshift/check-payload is one tool that can be used to check FIPS compliance.
On running with the latest v0.5.0 image from registry.k8s.io, I'm seeing the following output:

```
I1128 09:15:37.540149 3979546 scan.go:325] "scanning failed" image="registry.k8s.io/kueue/kueue:v0.5.0" path="/manager" error="go binary is not CGO_ENABLED" component="" tag="" rpm="" status="failed"
---- Failure Report
+-----------------+------------------------------+------------------------------------+
| EXECUTABLE NAME | STATUS                       | IMAGE                              |
+-----------------+------------------------------+------------------------------------+
|                 | openssl library not present  | registry.k8s.io/kueue/kueue:v0.5.0 |
| /manager        | go binary is not CGO_ENABLED | registry.k8s.io/kueue/kueue:v0.5.0 |
+-----------------+------------------------------+------------------------------------+
F1128 09:15:37.609754 3979546 main.go:259] Error: run failed
```

The fix for this would boil down to two things:
1) Use a different base image for the last layer. I see that https://github.com/kubernetes-sigs/kueue/blob/main/Makefile#L54-L55 is parametrized, so it'd be relatively easy to build a different image if desired.
2) Use CGO_ENABLED when compiling the binary: We would need to update https://github.com/kubernetes-sigs/kueue/blob/main/Dockerfile#L20 to set it to 1.

Of the above two changes, I think `2)` would be great to implement (or parametrize, if we don't want to use CGO_ENABLED).

For context...

`CGO_Enabled=1` tells the compiler that it's okay to build code that's written in C using the C compiler, and bits written in C usually call functions provided by libc and possibly other libraries. when it's enabled, the "cgo" build tag is set, and when it's set, the source code for the standard library's crypto package calls out to openssl for some things where, if it weren't set, it would fall back to using logic written in Go. that's not the way most of the standard library works, though, and for the crypto package it's mainly about having a FIPS-validated library do the heavy lifting if it's an available option.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-29T18:23:50Z

Thanks for the report!

I don't have any concerns about the recommendations, but some comments for each topic:

1. What is a recommended image to use?
2. We just inherited the CGO_ENABLED setting from kubebuilder and never touched it.

### Comment by [@anishasthana](https://github.com/anishasthana) — 2023-11-29T19:03:34Z

1. Most of the projects I'm familiar with use variations of `ubi-minimal`, KubeRay, for an example: https://github.com/ray-project/kuberay/blob/master/ray-operator/Dockerfile#L21. 
2. I'm happy to raise a PR updating this if you'd be open to it! (Sounds like you are)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-29T19:05:20Z

What is in that image that makes it FIPS compliant? I would prefer we use images from the registry.k8s.io

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2023-11-29T19:21:41Z

FIPS compliance is typically something your vendor would certify with their distro.

The main kubernetes project (https://github.com/kubernetes/kubernetes) does not build CGO (except kubelet) or openssl linked binaries (none of them) and scanning for openssl in the image is a pretty inaccurate compliance check anyhow.

Kubernetes projects are typically built with distroless to minimize maintainer time spent patching CVEs and produce small images.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2023-11-29T19:25:53Z

> CGO_Enabled=1 tells the compiler that it's okay to build code that's written in C using the C compiler, and bits written in C usually call functions provided by libc and possibly other libraries. when it's enabled, the "cgo" build tag is set, and when it's set, the source code for the standard library's crypto package calls out to openssl for some things where, if it weren't set, it would fall back to using logic written in Go. that's not the way most of the standard library works, though, and for the crypto package it's mainly about having a FIPS-validated library do the heavy lifting if it's an available option.

I think you're confusing `GOEXPERIMENT=boringcrypto` (formerly the custom goboring toolchain) and  `CGO_ENABLED=1`, CGO means that go will use the C standard library for certain things and permit user packages to use CGO for linking to C code. `CGO_ENABLED=1` does not enable different crypto code directly (though boringcrypto uses CGO), that would be the boringcrypto experiment (which also uses boringSSL, not openSSL ...).

boringcrypto mode is non-standard with tradeoffs and again we don't build the standard core project builds this way.

EDIT: https://github.com/microsoft/go-crypto-openssl exists but requires a custom forked go toolchain.

### Comment by [@anishasthana](https://github.com/anishasthana) — 2023-11-30T10:48:21Z

Thanks for the information @BenTheElder! I wasn't familiar with how the standard core projects operator -- your justifications make sense! We can close this issue out -- carrying downstream specific patches for the Makefile/Dockerfile would cover us as well.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-30T13:30:04Z

@anishasthana I'm ok adding any parameterization in the Makefile that you could need. CGO_ENABLED is the only one missing, IIUC.

### Comment by [@anishasthana](https://github.com/anishasthana) — 2023-12-01T12:03:34Z

@alculquicondor I've opened the PR at #1391

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-01T15:19:36Z

awesome
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-01T15:19:41Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1382#issuecomment-1836294451):

>awesome
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2023-12-05T19:56:03Z

LGTM :-)
