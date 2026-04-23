# Issue #418: Webhook failure when trying to install dev kueue into Kind

**Summary**: Webhook failure when trying to install dev kueue into Kind

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/418

**Last updated**: 2022-10-13T22:22:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-10-13T12:29:47Z
- **Updated**: 2022-10-13T22:22:03Z
- **Closed**: 2022-10-13T22:22:03Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Hello, I’m going to work on the e2e tests for kueue.  I am running into some trouble trying to build from source and running the sample files.


**What you expected to happen**:
I can build kueue, install the CRD/Controller and then be able to install CQ and workloads without any errors.

**How to reproduce it (as minimally and precisely as possible)**:
So I have a kind cluster and then I run
`make`
`make deploy`
`make run`

`kubectl apply -f config/samples/single-clusterqueue-setup.yaml`

**Anything else we need to know?**:

```
kubectl create -f config/samples/single-clusterqueue-setup.yaml 
Error from server (InternalError): error when creating "config/samples/single-clusterqueue-setup.yaml": Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "[https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1alpha2-resourceflavor?timeout=10s](https://kueue-webhook-service.kueue-system.svc/mutate-kueue-x-k8s-io-v1alpha2-resourceflavor?timeout=10s)": dial tcp 10.96.95.201:443: connect: connection refused
Error from server (InternalError): error when creating "config/samples/single-clusterqueue-setup.yaml": Internal error occurred: failed calling webhook "mclusterqueue.kb.io": failed to call webhook: Post "[https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1alpha2-clusterqueue?timeout=10s](https://kueue-webhook-service.kueue-system.svc/mutate-kueue-x-k8s-io-v1alpha2-clusterqueue?timeout=10s)": dial tcp 10.96.95.201:443: connect: connection refused
```

All other tests pass: unit, integration.  

**Environment**:
- Kubernetes version (use `kubectl version`): Client Version: v1.24.1
- Kueue version (use `git describe --tags --dirty --always`): latest
- Cloud provider or hardware configuration: NA
- OS (e.g: `cat /etc/os-release`): ec2-linux
- Kernel (e.g. `uname -a`):

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-13T13:41:50Z

Is the controller running? I wonder whether you missed uploading the images to the kind cluster.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-13T13:44:05Z

Nvm my question about uploading the image. By default the Makefile uses k8s staging gcr.

Still, my first guess would be that the controller is not actually running, for some reason.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-10-13T13:46:20Z

Probably, [this doc](https://github.com/kubernetes-sigs/kueue/blob/main/docs/setup/install.md#build-and-install-from-source) will help you.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-13T15:03:35Z

> Nvm my question about uploading the image. By default the Makefile uses k8s staging gcr.
> 
> Still, my first guess would be that the controller is not actually running, for some reason.

You are correct.

```
  Normal   BackOff  87s (x265 over 61m)  kubelet  Back-off pulling image "gcr.io/k8s-staging-kueue/kueue:81a6305-dirty"
```
Any ideas why this fails?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-13T15:16:39Z

The tag `81a6305-dirty` is not something that is available in `k8s-staging-kueue`. `-dirty` means that you have uncommitted changes. But in general `k8s-staging-kueue` only contains the commits that are already merged.

E2E tests need to run before merge, so the appropriate thing to do is to build the image locally and upload it to the kind cluster https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-13T22:22:03Z

@alculquicondor and @tenzen-y: Thank you both for your help.  

It turns out my machine had some problems with buildx and once I resolved that, I was able to figure out the issue.  

On amazon linux, I ran into this [issue](https://github.com/docker/buildx/issues/226) when trying to run docker buildx.  Once I applied the patch they suggest, I was able to figure out the issue.  

1) I need to change the ImagePullPolicy if I load my image onto kind.

I will go ahead and close.
