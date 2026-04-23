# Issue #2321: How to enable fairsharing in version v0.7.0-rc.1

**Summary**: How to enable fairsharing in version v0.7.0-rc.1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2321

**Last updated**: 2024-06-25T20:31:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ssc317](https://github.com/ssc317)
- **Created**: 2024-05-29T17:55:27Z
- **Updated**: 2024-06-25T20:31:42Z
- **Closed**: 2024-06-25T20:31:40Z
- **Labels**: `kind/support`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 5

## Description

I am downloading the kueue manifest file for the version `v0.7.0-rc.1` from url:
https://github.com/kubernetes-sigs/kueue/releases/download/v0.7.0-rc.1/manifests.yaml 


And I'd like to use the fairsharing feature in it. But I got problem on how to enable it.
I found there are two places mentioned it:
1. In line 304,
```
fairSharing:
                description: |-
                  fairSharing defines the properties of the ClusterQueue when participating in fair sharing.
                  The values are only relevant if fair sharing is enabled in the Kueue configuration.
```
But this part is more like a description.
Correct me if I am wrong

2. In line 11392:
```
# fairSharing:
    #   enable: true
    #   preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
```
This part is commented by default. And it seems to have some indent issue as well.
So I uncomment it and make it in the same indent level as `podOptions` and `integrations` above.(To be noted, integrations in your file is one level higher than podOptions)
But when I deploy it to my cluster, I can no longer submit the pod to the cluster due to the following error

```
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Audit-Id': 'xxxx, 'Cache-Control': 'no-cache, private', 'Content-Type': 'application/json', 'Warning': '299 - \"Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens.\"', 'X-Kubernetes-Pf-Flowschema-Uid': 'xxxx', 'X-Kubernetes-Pf-Prioritylevel-Uid': 'xxxx', 'Date': 'Thu, 23 May 2024 18:58:01 GMT', 'Content-Length': '603'})
HTTP response body: {\"kind\":\"Status\",\"apiVersion\":\"v1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"Internal error occurred: failed calling webhook \\"mpod.kb.io\\": failed to call webhook: Post \\"[https://kueue-webhook-service.kueue-system.svc:443/mutate--v1-pod?timeout=10s](https://kueue-webhook-service.kueue-system.svc/mutate--v1-pod?timeout=10s)\\": no endpoints available for service \\"kueue-webhook-service\\"\",\"reason\":\"InternalError\",\"details\":{\"causes\":[{\"message\":\"failed calling webhook \\"mpod.kb.io\\": failed to call webhook: Post \\"[https://kueue-webhook-service.kueue-system.svc:443/mutate--v1-pod?timeout=10s](https://kueue-webhook-service.kueue-system.svc/mutate--v1-pod?timeout=10s)\\": no endpoints available for service \\"kueue-webhook-service\\"\"}]},\"code\":500}
```

Please instruct me on how to enable fair sharing in this version

## Discussion

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2024-05-30T08:18:30Z

` no endpoints available for service \\"kueue-webhook-service\\"\"` the error message indicates the kueue pod that isn't running. @ssc317

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-14T13:12:21Z

@ssc317 can you please share the output of the command: `kubectl get po -n kueue-system` ?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-17T09:26:52Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:31:36Z

I fixed the indentation in the documentation and also left an example in https://kueue.sigs.k8s.io/docs/concepts/preemption/#fair-sharing

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:31:41Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2321#issuecomment-2189915766):

>I fixed the indentation in the documentation and also left an example in https://kueue.sigs.k8s.io/docs/concepts/preemption/#fair-sharing
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
