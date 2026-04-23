# Issue #6878: How to calculate custom resources for a `ClusterQueue`?

**Summary**: How to calculate custom resources for a `ClusterQueue`?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6878

**Last updated**: 2025-12-19T01:59:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@calvin0327](https://github.com/calvin0327)
- **Created**: 2025-09-17T07:32:00Z
- **Updated**: 2025-12-19T01:59:49Z
- **Closed**: 2025-12-19T01:59:49Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 14

## Description

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->

I have configured some custom resources in the `ClusterQueue`, e.g `nvidia.com/gpu` and `nvidia.com/gpumem`:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: default-queue
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources:
    - nvidia.com/gpu
    - nvidia.com/gpumem
    flavors:
    - name: hami-flavor
      resources:
      - name: nvidia.com/gpu
        nominalQuota: 2
      - name: nvidia.com/gpumem
        nominalQuota: 2048
```

And I apply a deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-burn
  namespace: kueue-test
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  replicas: 1
  selector:
    matchLabels:
      app-name: gpu-burn
  template:
    metadata:
      labels:
        app-name: gpu-burn
    spec:
      containers:
      - args:
        - while :; do /app/gpu_burn 300 || true; sleep 300; done
        command:
        - /bin/sh
        - -lc
        image: oguzpastirmaci/gpu-burn:latest
        imagePullPolicy: IfNotPresent
        name: main
        resources:
          limits:
            nvidia.com/gpu: "2"
            nvidia.com/gpumem: "1024"
          requests:
            nvidia.com/gpu: "2"
            nvidia.com/gpumem: "1024"
```

My expected result: This workload consumes 2 GPUs and 2 multiplied by 1024 of gpu memory（2048）, with no resources remaining in this ClusterQueue.

But the current result is: there is still 1024 GPU memory remaining in the ClusterQueue. This is because only a subtraction operation is performed on each individual resource.

What can I do now to meet my requirements? Thank you all very much for your help.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-17T07:41:37Z

In clusterQueue, you have 2048, while the deployment has 1024 with one replica. Since 1 replica * 1024 = 1024, this appears correct.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T07:45:07Z

Yes, this is WAI for resources in Kueue. Could you just say in your workload?

```yaml
        resources:
          requests:
            nvidia.com/gpu: "2"
            nvidia.com/gpumem: "2048"
```

### Comment by [@calvin0327](https://github.com/calvin0327) — 2025-09-17T07:47:10Z

@mbobrovskyi Thank you for your reply. 

 In HAMi, `nvidia.com/gpumem` represents that 1024 MB of GPU memory is allocated per GPU. If `nvidia.com/gpu` is set to 2, it means a total of 2 * 1024 = 2048 MB of GPU memory is allocated.

### Comment by [@calvin0327](https://github.com/calvin0327) — 2025-09-17T07:55:37Z

> Yes, this is WAI for resources in Kueue. Could you just say in your workload?
> 
>         resources:
>           requests:
>             nvidia.com/gpu: "2"
>             nvidia.com/gpumem: "2048"

@mimowo If resources are requested in this way, it means the workload requires a total of 2 * 2048 = 4096 MB of GPU memory in HAMi，I'm wondering how I can implement such a requirement in Kueue so that HAMi can use Kueue seamlessly.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T07:55:51Z

I see, so if you set `nvidia.com/gpumem: "2048"` then quota will behave ok, but the Pod will remain Pending because kube-scheduler (or its GPU plugin) will not find a single GPU with 2048.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T07:58:38Z

Maybe (brainstoriming) there should be 3 resources:
```
        nvidia.com/gpu: "2"
        nvidia.com/gpumem: "1024" // used by the driver per GPU
        gpumem-total: "2048" // used by Kueue quota management
```
but I'm not totally sure, maybe COnfigurableResourceTransformations could also be helpful. cc @dgrove-oss

### Comment by [@calvin0327](https://github.com/calvin0327) — 2025-09-17T08:02:37Z

> I see, so if you set `nvidia.com/gpumem: "2048"` then quota will behave ok, but the Pod will remain Pending because kube-scheduler (or its GPU plugin) will not find a single GPU with 2048.

Yes, Yes, therefore, I want the quota deduction to be calculated as follows: `nvidia.com/gpumem` = `nvidia.com/gpu` * `nvidia.com/gpumem`

### Comment by [@calvin0327](https://github.com/calvin0327) — 2025-09-17T08:03:05Z

> Maybe (brainstoriming) there should be 3 resources:
> 
> ```
>         nvidia.com/gpu: "2"
>         nvidia.com/gpumem: "1024" // used by the driver per GPU
>         gpumem-total: "2048" // used by Kueue quota management
> ```
> 
> but I'm not totally sure, maybe COnfigurableResourceTransformations could also be helpful. cc [@dgrove-oss](https://github.com/dgrove-oss)

@mimowo Thanks.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-18T14:59:52Z

It would be worth updating the resource transformation KEP first.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T16:12:27Z

Hello, just to clarify:

```yaml
requests:
  nvidia.com/gpu: "2"
  nvidia.com/gpumem: "1024"
```

It seems like in this case we have a “special” interpretation of the requested quantities. Normally, resource requests are taken at face value. For example, the snippet above would usually be read as,

* `nvidia.com/gpu: "2"`
* `nvidia.com/gpumem: "1024"`

But here, for `nvidia`, it sounds like we’re applying a custom interpretation:

* `nvidia.com/gpu: "2"`
* `nvidia.com/gpumem: "2048"` (calculated as `1024 * 2 GPUs`)

Am I understanding correctly that the proposal is to introduce a codified relationship between these values, so that the requested amount is derived rather than used directly? If so, I worry it could feel a bit opaque or confusing to users.

If that’s not the case, where would this transformation logic live? I’d assume the same challenge would appear outside of Kueue, for example in `ResourceQuota`.

Finally, just brainstorming, would it make sense to introduce a distinct resource to represent the “transformed” value? For example:

```yaml
nvidia.com/gpu: "2"
nvidia.com/gpumem: "1024"        # optional
nvidia.com/gpumem-total: "2048"  # used by Kueue quota management
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T16:43:06Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-18T19:25:20Z

/remove-lifecycle stale

This is tracked for 0.16
@mimowo Is anyone actively working on this?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-18T19:55:11Z

> /remove-lifecycle stale
> 
> This is tracked for 0.16 [@mimowo](https://github.com/mimowo) Is anyone actively working on this?

https://github.com/kubernetes-sigs/kueue/pull/7599

I think this may be done actually.

cc @calvin0327

### Comment by [@calvin0327](https://github.com/calvin0327) — 2025-12-19T01:59:44Z

https://github.com/kubernetes-sigs/kueue/pull/7599

@kannon92 Yes, It’s done, I close it.
