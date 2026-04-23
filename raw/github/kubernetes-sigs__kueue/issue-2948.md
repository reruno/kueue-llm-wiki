# Issue #2948: Pods lose 1.31 fields during creation

**Summary**: Pods lose 1.31 fields during creation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2948

**Last updated**: 2024-09-03T17:13:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-09-01T04:16:44Z
- **Updated**: 2024-09-03T17:13:12Z
- **Closed**: 2024-09-03T17:12:38Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 13

## Description

So tonight I was working on playing around with https://github.com/kubernetes-sigs/dra-example-driver/blob/main/README.md#demo and Kueue.

All I am doing is following the demo to create a mock DRA driver.

I can run all the examples in this repo by running.

I then install kueue (0.8.0) (`kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.8.0/manifests.yaml`) and then all the examples fail due to validation of resourceClaims.

Pre install of Kueue:

```
kehannon@kehannon-thinkpadp1gen4i:~/Work/dra-example-driver$ kubectl create -f demo/gpu-test1.yaml 
namespace/gpu-test1 created
resourceclaimtemplate.resource.k8s.io/single-gpu created
pod/pod0 created
pod/pod1 created
```

Install Kueue:

```
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.8.0/manifests.yaml
```

And then I run the same example (deleted before I install Kueue).
```
kehannon@kehannon-thinkpadp1gen4i:~/Work/dra-example-driver/demo$ kubectl create -f gpu-test1.yaml 
namespace/gpu-test1 created
resourceclaimtemplate.resource.k8s.io/single-gpu created
Error from server (Invalid): error when creating "gpu-test1.yaml": Pod "pod0" is invalid: spec.resourceClaims[0]: Invalid value: core.PodResourceClaim{Name:"gpu", ResourceClaimName:(*string)(nil), ResourceClaimTemplateName:(*string)(nil)}: must specify one of: `resourceClaimName`, `resourceClaimTemplateName`
Error from server (Invalid): error when creating "gpu-test1.yaml": Pod "pod1" is invalid: spec.resourceClaims[0]: Invalid value: core.PodResourceClaim{Name:"gpu", ResourceClaimName:(*string)(nil), ResourceClaimTemplateName:(*string)(nil)}: must specify one of: `resourceClaimName`, `resourceClaimTemplateName`
```

Not really sure what is going wrong here.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-01T04:43:37Z

I even tried https://github.com/kubernetes-sigs/kueue/pull/2402 to see if maybe we were picking up old APIs somewhere in Kueue. I get the same error if I install kueue.

### Comment by [@pohly](https://github.com/pohly) — 2024-09-02T15:21:41Z

Does Kueue install a mutating pod webhook?

If yes, then it seems to strip out the fields added for DRA in 1.31 (`spec.resourceClaims[0].resourceClaimTemplateName`).

### Comment by [@pohly](https://github.com/pohly) — 2024-09-02T15:22:21Z

Rebuilding Kueue against the 1.31 client-go might fix this.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-02T16:25:34Z

Kueue does have a pod webhook but it doesn’t seem to do anything with these fields.

https://github.com/kubernetes-sigs/kueue/blob/9dad9cb894509725e911d29cff269a7b0accf072/pkg/controller/jobs/pod/pod_webhook.go#L136

I’ll see what is going on here. 

I did try building with 1.31 and that didn’t seem to fix the issue.

### Comment by [@pohly](https://github.com/pohly) — 2024-09-02T16:42:06Z

> Kueue does have a pod webhook but it doesn’t seem to do anything with these fields.

Decoding into a `v1.Pod` from Kubernetes 1.30 and encoding again drops fields from 1.31 because they are unknown.

https://github.com/kubernetes-sigs/kueue/blob/9dad9cb894509725e911d29cff269a7b0accf072/pkg/controller/jobs/pod/pod_webhook.go#L194-L195 works with `v1.Pod`, so this could very well happen.

> I did try building with 1.31 and that didn’t seem to fix the issue.

I would add log output that dumps the entire pod before/after to debug further.

Did you double-check that your modified Kueue was running in the cluster?

### Comment by [@pohly](https://github.com/pohly) — 2024-09-02T16:43:36Z

Note that the unknown fields will already have been dropped on the incoming `v1.Pod`.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-03T12:04:39Z

This sounds like the same as #2878. It's a problem coming down from controller-runtime.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-03T14:12:58Z

/retitle Pods loses 1.31 fields during creation

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-03T14:25:50Z

I'll test this again but I still saw this problem with https://github.com/kubernetes-sigs/kueue/issues/2948#issuecomment-2323165151.

I would think that if we used 1.31 apis for Kueue this would be resolved.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-03T16:13:15Z

Sounds good, please do report your findings. Make sure to use better titles than "interesting problem" :)

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-03T17:12:06Z

Okay. @pohly was correct. I was picking up the main kueue image and not the build one.

If I force kueue to use the branch image in kind, I no longer see this problem.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-03T17:12:34Z

/close

This isn't a bug but will be resolved once https://github.com/kubernetes-sigs/kueue/pull/2402 is merged.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-03T17:12:39Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2948#issuecomment-2327037779):

>/close
>
>This isn't a bug but will be resolved once #2948 is merged and released.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
