# Issue #786: Cluster queue creation can result in a panic

**Summary**: Cluster queue creation can result in a panic

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/786

**Last updated**: 2023-05-23T19:00:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2023-05-20T14:35:06Z
- **Updated**: 2023-05-23T19:00:51Z
- **Closed**: 2023-05-23T19:00:51Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description


**What happened**:

Trying to create a cluster queue with mismatch between `coveredResources` and `flavours` results in a webhook failure.  This is not a big deal but the error is:

```
Error from server (InternalError): error when creating "example/kueue.yaml": Internal error occurred: failed calling webhook "vclusterqueue.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-clusterqueue?timeout=10s": EOF
```

Reading the logs in Kueue-Controller-Manager you can see an out-of-bounds panic:

```
2023/05/20 14:22:30 http: panic serving 172.18.0.4:44099: runtime error: index out of range [2] with length 2
goroutine 4173 [running]:
net/http.(*conn).serve.func1()
        /usr/local/go/src/net/http/server.go:1850 +0xbf
panic({0x1709c20, 0xc000c3c420})
        /usr/local/go/src/runtime/panic.go:890 +0x262
sigs.k8s.io/kueue/apis/kueue/webhooks.validateFlavorQuotas({{0xc000b37490, 0xe}, {0xc00026d400, 0x3, 0x4}}, {0xc0005d0e80, 0x2, 0x40d71f?}, 0xc00014bbf0)
        /workspace/apis/kueue/webhooks/clusterqueue_webhook.go:163 +0x990
sigs.k8s.io/kueue/apis/kueue/webhooks.validateResourceGroups({0xc000530a80, 0x1, 0xc0007ee558?}, 0xc00014b9e0)
        /workspace/apis/kueue/webhooks/clusterqueue_webhook.go:144 +0x811
sigs.k8s.io/kueue/apis/kueue/webhooks.ValidateClusterQueue(0xc0006ddd40)
        /workspace/apis/kueue/webhooks/clusterqueue_webhook.go:108 +0x1e5
sigs.k8s.io/kueue/apis/kueue/webhooks.(*ClusterQueueWebhook).ValidateCreate(0xc0007741b0?, {0x1a6bef8?, 0xc00014b860?}, {0x1a5db30?, 0xc0006ddd40})
        /workspace/apis/kueue/webhooks/clusterqueue_webhook.go:81 +0x1a5
sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*validatorForType).Handle(_, {_, _}, {{{0xc0007741b0, 0x24}, {{0xc000b36fb0, 0xe}, {0xc000b36fc0, 0x7}, {0xc000b37060, ...}}, ...}})
```

**What you expected to happen**:

I would expect an error during validation. 

 
**How to reproduce it (as minimally and precisely as possible)**:

Case 1 (flavor exists but not in coveredResources)

```yamll
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
      - name: "ephemeral-storage"
        nominalQuota: 10Gi
```

**Anything else we need to know?**:

If you have covered resources specified but not a match in flavors you do get a webhook validation error.  

```
: admission webhook "vclusterqueue.kb.io" denied the request: spec.resourceGroups[0].flavors[0].resources: Invalid value: must have the same number of resources as the coveredResources
```

**Environment**:
- Kubernetes version (use `kubectl version`): 1.23
- Kueue version (use `git describe --tags --dirty --always`): 0.3.1 (manifest)
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
