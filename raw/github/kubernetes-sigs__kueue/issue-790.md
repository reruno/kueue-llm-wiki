# Issue #790: Failed to run sleep image in arm64 machine

**Summary**: Failed to run sleep image in arm64 machine

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/790

**Last updated**: 2023-05-22T11:43:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@hwdef](https://github.com/hwdef)
- **Created**: 2023-05-22T06:56:38Z
- **Updated**: 2023-05-22T11:43:40Z
- **Closed**: 2023-05-22T11:43:39Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I created sample-job for test, but it returns an error, I think `gcr.io/k8s-staging-perf-tests/sleep:v0.0.3` image does not support arm64 platform

<img width="434" alt="image" src="https://github.com/kubernetes-sigs/kueue/assets/13084946/d721996b-6c87-4148-9880-584c670cbc24">


**What you expected to happen**:

Successfully run the test job

**How to reproduce it (as minimally and precisely as possible)**:

```
kubectl create -f config/samples/sample-job.yaml
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-22T07:12:55Z

@hwdef Thank you for creating this report!

Yes, the image doesn't support arm64.
However, the image isn't maintained by this repository.

```json
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 1756,
      "digest": "sha256:99c52edc38d9087e4af9cc6f2093209835b82d2ab6b95edb4210e366d3f4d08f"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 803833,
         "digest": "sha256:2df365faf0e3007f983fadd7a65ba51d41b488eb2ed8fc70f4bf97043cfea560"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 1124619,
         "digest": "sha256:87f257c18949b274e781d7c05d3977426633cfd0f0d7f7dbdf32ddacae5675b1"
      }
   ]
}
```

https://console.cloud.google.com/gcr/images/k8s-staging-perf-tests/global/sleep@sha256:00ae8e01dd4439edfb7eb9f1960ac28eba16e952956320cce7f2ac08e3446e6b/details?tab=pull

@kerthcet @alculquicondor @ahg-g @denkensk Do you know where this image is maintained?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-22T09:46:54Z

You can refer to https://github.com/kubernetes/perf-tests/blob/master/util-images/sleep/Dockerfile

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-22T09:50:56Z

Feel free to close this.
/remove-kind bug
/kind support

### Comment by [@hwdef](https://github.com/hwdef) — 2023-05-22T10:16:37Z

I think the solution is to upload an arm64 version of the image to this image registry. I don’t know who has this permission

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-22T11:39:38Z

@hwdef Can you create an issue at https://github.com/kubernetes/perf-tests/issues, as this repo doesn't maintain that image?

### Comment by [@hwdef](https://github.com/hwdef) — 2023-05-22T11:42:25Z

> @hwdef Can you create an issue at https://github.com/kubernetes/perf-tests/issues, as this repo doesn't maintain that image?

sure

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-22T11:43:36Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-22T11:43:40Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/790#issuecomment-1557069241):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
