# Issue #6256: The clientConnection.qps can not disable client side rate limiter

**Summary**: The clientConnection.qps can not disable client side rate limiter

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6256

**Last updated**: 2025-07-30T17:56:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-07-29T15:00:24Z
- **Updated**: 2025-07-30T17:56:28Z
- **Closed**: 2025-07-30T17:56:28Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The clientConnection.qps field does not allow for disabling the client-side rate limiter with `qps: -1`.

https://github.com/kubernetes-sigs/kueue/blob/dfa2f5dde84b254a2b61d0020bc7acf94cb1023f/config/components/manager/controller_manager_config.yaml#L23

```shell
E0729 14:48:33.970633       1 leaderelection.go:429] Failed to update lock optimistically: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline, falling back to slow path
E0729 14:48:33.970789       1 leaderelection.go:436] error retrieving resource lock kueue-system/c1f6bfd2.kueue.x-k8s.io: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline
E0729 14:48:35.971351       1 leaderelection.go:429] Failed to update lock optimistically: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline, falling back to slow path
```

**What you expected to happen**:

We can disable the client-side rate limit by the `clientConnection.qps: -1`.

**How to reproduce it (as minimally and precisely as possible)**:

Deploying the kueue-controller-maanger with the following Configuration:

```
apiVersion: config.kueue.x-k8s.io/v1beta1
kind: Configuration
...
clientConnection:
  qps: -1
...
```

**Anything else we need to know?**:

The rest config allows to disable that with `-1` value as we confirmed the following comment:

```go
	// QPS indicates the maximum QPS to the master from this client.
	// If it's zero, the created RESTClient will use DefaultQPS: 5
	//
	// Setting this to a negative value will disable client-side ratelimiting
	// unless `Ratelimiter` is also set.
	QPS float32
```

https://github.com/kubernetes/client-go/blob/f78361a6474daec710d27e65e341613b4ae31413/rest/config.go#L117-L122

But the RateLimiter that the manager uses in [main.go](https://github.com/kubernetes-sigs/kueue/blob/dfa2f5dde84b254a2b61d0020bc7acf94cb1023f/cmd/kueue/main.go#L191) does not allow us that.

So, I would like to use the `kubeConfig.QPS = -1` instead of `kubeConfig.RateLimiter = flowcontrol.NewTokenBucketRateLimiter(QPS, Burst)` when the specified qps is -1.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T15:05:13Z

In my cluster, all API requests are fully controlled by API Priority and Fairness features (a.k.a. Server Side Rate Limiter), dynamically.
So, I would like to disable the client-side rate limiter and avoid managing the static qps and burst parameters.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T16:16:34Z

As I went through the previous issues, I found https://github.com/kubernetes-sigs/kueue/issues/2423.
And the #2433 was a valid issue only when the controller-runtime is <= 0.20: https://github.com/kubernetes-sigs/controller-runtime/blob/v0.20.2/pkg/client/config/config.go#L95-L120

Since 0.21, the controller-runtime stop to override the QPS and Burst: https://github.com/kubernetes-sigs/controller-runtime/commit/ab40409635dc0c91781f575a87c64a579680be95

So, we could migrate from RateLimiter to QPS and Burst in our config setup at main.go.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T16:16:40Z

cc @gabesaba @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T15:41:59Z

@tenzen-y I understand the proposal to enable disabling the rate limited (main issue objective), but I don't understand how this is related to making the rate limiter per type vs global (last comment), can you clarify / rephrase?

In particular IIUC https://github.com/kubernetes-sigs/kueue/pull/2462 introduced single rate limitter across all types. Do you intend to change that, or keep?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T15:58:44Z

Before controller-runtime v0.20 (<= 0.20), the qps and burst are overwritten with static values by controller-runtime (https://github.com/kubernetes-sigs/controller-runtime/blob/v0.20.2/pkg/client/config/config.go#L95-L120).

So, we changed the qps and burst specification way with `kubeConfig.RateLimiter = flowcontrol.NewTokenBucketRateLimiter(QPS, Burst)`, IIUC.

After controller-runtime v0.21, the client side rate limiter is disabled by default: https://github.com/kubernetes-sigs/controller-runtime/commit/ab40409635dc0c91781f575a87c64a579680be95

So, my proposal is the following way:

(a. Keeping client side rate limit when they do not specify anything

1. Changing the KubeConfig generation with the following:

```go
if *cfg.ClientConnection.QPS != -1 {
  kubeConfig.RateLimiter = flowcontrol.NewTokenBucketRateLimiter(*cfg.ClientConnection.QPS, int(*cfg.ClientConnection.Burst))
}
```

(b. If they do not specify anything, kueue disables client side rate limiter

1 Changing the KubeConfig generation with the following:

```go
if cfg.ClientConnection.QPS != nil || cfg.ClientConnection.Burst != nil {
  kubeConfig.RateLimiter = flowcontrol.NewTokenBucketRateLimiter(*cfg.ClientConnection.QPS, int(*cfg.ClientConnection.Burst))
}
```

2 Removing the following defaulting:

https://github.com/kubernetes-sigs/kueue/blob/3263c4fbf52a4132893ee8b6f4bb738f380addb5/apis/config/v1beta1/defaults.go#L94-L95

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T16:00:23Z

We can select (a. or (b. approach.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T16:21:28Z

I see, so IIUC there are essentially 2 options:
1. keep the defaulting, but assume QPS=-1 means disable rate limiter
2. drop the defaulting and assume if QPS or Burst are unspecified then disable rate limiter

I think long term might be desired, but (1.) seems safer for existing environments. We can always follow up with dropping of the defaults later.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T16:30:51Z

> I see, so IIUC there are essentially 2 options:
> 
> 1. keep the defaulting, but assume QPS=-1 means disable rate limiter
> 2. drop the defaulting and assume if QPS or Burst are unspecified then disable rate limiter
> 
> I think long term might be desired, but (1.) seems safer for existing environments. We can always follow up with dropping of the defaults later.

That makes sense. But, in case of v0.12, we use the controller-runtime v0.20.

https://github.com/kubernetes-sigs/kueue/blob/b4306accba45a46b19c1aecc014de269dfeb9e13/go.mod#L37

So, in v0.12, we need to do the following instead of (a. approach since the controller-runtime v0.20 does not disable the client side rate limiter by default: 

```go
if *cfg.ClientConnection.QPS == -1 {
  kubeConfig.QPS = *cfg.ClientConnection.QPS
} else {
  kubeConfig.RateLimiter = flowcontrol.NewTokenBucketRateLimiter(*cfg.ClientConnection.QPS, int(*cfg.ClientConnection.Burst))
}
```

@mimowo is this acceptable for you?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T16:34:01Z

> @mimowo is this acceptable for you?

yes, but should also update comments to the QPS config indicating that -1 means disabled rate limiter. 

IIUC in the past the behaviour was "undefined" as we relied on controller-runtime defaulting rather than specified the semantic in Kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T16:36:33Z

> > [@mimowo](https://github.com/mimowo) is this acceptable for you?
> 
> yes, but should also update comments to the QPS config indicating that -1 means disabled rate limiter.

Yes, we should update the API comment.

> IIUC in the past the behaviour was "undefined" as we relied on controller-runtime defaulting rather than specified the semantic in Kueue.

If users do not specify clientConnection, Kueue mutates default values to those: https://github.com/kubernetes-sigs/kueue/blob/3263c4fbf52a4132893ee8b6f4bb738f380addb5/apis/config/v1beta1/defaults.go#L94-L95

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T16:39:29Z

> If users do not specify clientConnection, Kueue mutates default values to those:

Yes, I meant if the user specifies to -1.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T16:42:06Z

> > If users do not specify clientConnection, Kueue mutates default values to those:
> 
> Yes, I meant if the user specifies to -1.

Yes, that's right. Specifying -1 means relying on the controller-runtime. And the Kueue will fail starting up.

`Failed to update lock optimistically: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline, falling back to slow pat`

```shell
E0729 14:48:33.970633       1 leaderelection.go:429] Failed to update lock optimistically: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline, falling back to slow path
E0729 14:48:33.970789       1 leaderelection.go:436] error retrieving resource lock kueue-system/c1f6bfd2.kueue.x-k8s.io: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline
E0729 14:48:35.971351       1 leaderelection.go:429] Failed to update lock optimistically: client rate limiter Wait returned an error: rate: Wait(n=1) would exceed context deadline, falling back to slow path
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T16:43:49Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T16:44:25Z

Cool, in that case I think we can handle this even as a small cherrypickable feature or bug, because the change of semantics for -1 would not work anyway

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-30T16:45:44Z

> Cool, in that case I think we can handle this even as a small cherrypickable feature or bug, because the change of semantics for -1 would not work anyway

Yes, that's why I reported this as a bug.
