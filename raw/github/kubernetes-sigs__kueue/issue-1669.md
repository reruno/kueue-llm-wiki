# Issue #1669: Panic validating existing cluster queues

**Summary**: Panic validating existing cluster queues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1669

**Last updated**: 2024-01-30T13:33:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-01-29T16:35:17Z
- **Updated**: 2024-01-30T13:33:47Z
- **Closed**: 2024-01-30T13:33:47Z
- **Labels**: `kind/bug`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 1

## Description

**What happened**:

With a ClusterQueue created in previous Kueue version, e.g., v0.5.0, upgrading to the latest Kueue version, leads to the ClusterQueue validation webhook panicking whenever the ClusterQueue is updated:

```
2024/01/29 16:04:41 http: panic serving 10.244.0.1:59326: runtime error: invalid memory address or nil pointer dereference
goroutine 2941 [running]:
net/http.(*conn).serve.func1()
	/usr/local/go/src/net/http/server.go:1868 +0x13d
panic({0x32b73a0?, 0x4d26160?})
	/usr/local/go/src/runtime/panic.go:920 +0x290
sigs.k8s.io/kueue/pkg/webhooks.validatePreemption(0xc000d21440, 0xc000d21cb0)
	/Users/antonin/Development/kueue/pkg/webhooks/clusterqueue_webhook.go:143 +0x153
sigs.k8s.io/kueue/pkg/webhooks.ValidateClusterQueue(0xc000f76780)
	/Users/antonin/Development/kueue/pkg/webhooks/clusterqueue_webhook.go:125 +0x5ea
sigs.k8s.io/kueue/pkg/webhooks.ValidateClusterQueueUpdate(0xc000f76780, 0xc000f76960)
	/Users/antonin/Development/kueue/pkg/webhooks/clusterqueue_webhook.go:136 +0x65
sigs.k8s.io/kueue/pkg/webhooks.(*ClusterQueueWebhook).ValidateUpdate(0x4dac380, {0x3969518, 0xc000d206f0}, {0x394a518, 0xc000f76960}, {0x394a518, 0xc000f76780})
	/Users/antonin/Development/kueue/pkg/webhooks/clusterqueue_webhook.go:105 +0x285
sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*validatorForType).Handle(_, {_, _}, {{{0xc000696d20, 0x24}, {{0xc000ea7b40, 0xe}, {0xc000ea7b18, 0x7}, {0xc000ea7b50, ...}}, ...}})
	/Users/antonin/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.3/pkg/webhook/admission/validator_custom.go:102 +0xa44
sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*Webhook).Handle(_, {_, _}, {{{0xc000696d20, 0x24}, {{0xc000ea7b40, 0xe}, {0xc000ea7b18, 0x7}, {0xc000ea7b50, ...}}, ...}})
	/Users/antonin/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.3/pkg/webhook/admission/webhook.go:169 +0x224
sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*Webhook).ServeHTTP(0xc00031d3b0, {0x7f9b8f2ae670, 0xc0003ed9f0}, 0xc001188b00)
	/Users/antonin/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.3/pkg/webhook/admission/http.go:98 +0xd18
github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerInFlight.func1({0x7f9b8f2ae670, 0xc0003ed9f0}, 0xc001188b00)
	/Users/antonin/go/pkg/mod/github.com/prometheus/client_golang@v1.18.0/prometheus/promhttp/instrument_server.go:60 +0x13c
net/http.HandlerFunc.ServeHTTP(0xc000d12660, {0x7f9b8f2ae670, 0xc0003ed9f0}, 0xc001188b00)
	/usr/local/go/src/net/http/server.go:2136 +0x3a
github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerCounter.func1({0x3959b40, 0xc000bd2460}, 0xc001188b00)
	/Users/antonin/go/pkg/mod/github.com/prometheus/client_golang@v1.18.0/prometheus/promhttp/instrument_server.go:147 +0xf5
net/http.HandlerFunc.ServeHTTP(0xc000d13cb0, {0x3959b40, 0xc000bd2460}, 0xc001188b00)
	/usr/local/go/src/net/http/server.go:2136 +0x3a
github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerDuration.func2({0x3959b40, 0xc000bd2460}, 0xc001188b00)
	/Users/antonin/go/pkg/mod/github.com/prometheus/client_golang@v1.18.0/prometheus/promhttp/instrument_server.go:109 +0xd6
net/http.HandlerFunc.ServeHTTP(0xc000d99e00, {0x3959b40, 0xc000bd2460}, 0xc001188b00)
	/usr/local/go/src/net/http/server.go:2136 +0x3a
net/http.(*ServeMux).ServeHTTP(0xc000b1cec0, {0x3959b40, 0xc000bd2460}, 0xc001188b00)
	/usr/local/go/src/net/http/server.go:2514 +0x194
net/http.serverHandler.ServeHTTP({0xc000b4e0f0}, {0x3959b40, 0xc000bd2460}, 0xc001188b00)
	/usr/local/go/src/net/http/server.go:2938 +0x257
net/http.(*conn).serve(0xc0011de1b0, {0x3969550, 0xc0003ed900})
	/usr/local/go/src/net/http/server.go:2009 +0x1a59
created by net/http.(*Server).Serve in goroutine 543
	/usr/local/go/src/net/http/server.go:3086 +0xa65
{"level":"error","ts":"2024-01-29T16:04:41.779475135Z","caller":"controller/controller.go:329","msg":"Reconciler error","controller":"clusterqueue","controllerGroup":"kueue.x-k8s.io","controllerKind":"ClusterQueue","ClusterQueue":{"name":"cluster-queue"},"namespace":"","name":"cluster-queue","reconcileID":"98f10824-4769-41aa-ab79-7ce7000cdd2d","error":"Internal error occurred: failed calling webhook \"vclusterqueue.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-clusterqueue?timeout=10s\": EOF","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/Users/antonin/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.3/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/Users/antonin/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.3/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/Users/antonin/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.3/pkg/internal/controller/controller.go:227"}
```

The cluster queue validation webhook panics for existing resources, whose .spec.preemption.borrowWithinCohort field haven't been defaulted yet.

**What you expected to happen**:

The webhook should be backward compatible. 

**How to reproduce it (as minimally and precisely as possible)**:

* Deploy Kueue v0.5.0
* Create a ClusterQueue resource
* Upgrade Queue to v0.6.0-rc.1
* Update the ClusterQueue resource

**Anything else we need to know?**:

Relates to #1397.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.3
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-devel-213-gb7fc93f5-dirty

## Discussion

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-29T17:16:07Z

/assign
