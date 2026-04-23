# Issue #5192: Webhook name collision causes cert problems

**Summary**: Webhook name collision causes cert problems

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5192

**Last updated**: 2025-05-13T13:31:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@andrew0li](https://github.com/andrew0li)
- **Created**: 2025-05-07T18:36:45Z
- **Updated**: 2025-05-13T13:31:20Z
- **Closed**: 2025-05-13T13:27:43Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

I'm using Kueue with LeaderWorkerSet and kept getting a webhook TLS error:

```
failed calling webhook \"vleaderworkerset.kb.io\": failed to call webhook: Post \"https://lws-webhook-service.namespace.svc:443/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset?timeout=10s\": tls: failed to verify certificate: x509: certificate is valid for kueue-webhook-service.namespace.svc, not lws-webhook-service.namespace.svc
```

It seems like because both Kueue and LWS use `mleaderworkset.kb.io` as the MutatingWebhookConfiguration name, that some `caBundle` confusion is happening, and the LWS webhook gets Kueue's webhook `caBundle`? I'm pretty inexperienced with this so very likely I missed some configuration somewhere, since I'd expect since Kueue has explicit integration that things should work out of the box.

**What you expected to happen**:

I expect things to work with self-signed certs without cert-manager out of the box.

**How to reproduce it (as minimally and precisely as possible)**:

Use internal cert management for both LWS and Kueue (i.e. `enableCertManager: false`)

**Anything else we need to know?**:

Is there extra configuration I need to do besides enabling the integration to use LWS with Kueue? If so it should be documented because I couldn't find anything. The current workaround I have is renaming Kueue's `mleaderworkerset.kb.io` to something else, though this seems like 1. either should already be in Kueue's integration if it's correct or 2. is brittle/incorrect.

**Environment**: 
- Kubernetes version (use `kubectl version`): v1.31.7
- Kueue version (use `git describe --tags --dirty --always`): 0.11.4 via Helm
- Cloud provider or hardware configuration: AKS
- OS (e.g: `cat /etc/os-release`): Ubuntu
- Kernel (e.g. `uname -a`):
- Install tools: Helm
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-08T04:26:32Z

@andrew0li We have E2E testing in a real k8s cluster, and we do not see the errors.
I guess your configuration does not seem correct. Could you check if the internal certmanagement is enabled (https://github.com/kubernetes-sigs/kueue/blob/9d2919ea7b682a9e22b185347d286fe7e82591d4/charts/kueue/values.yaml#L100-L101) and if kueue-controller-manager is running?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-08T07:08:56Z

> I'm using Kueue with LeaderWorkerSet and kept getting a webhook TLS error:

When does the error manifest, when creating LWS objects? 

Also, does it reject the creation or it is just logged, and one of the webhooks is skipped?

### Comment by [@andrew0li](https://github.com/andrew0li) — 2025-05-11T19:01:38Z

@tenzen-y @mimowo I've been trying to reproduce this but it seems like this only occurs when I try to deploy helm charts that deploy LWS as part of the chart. If I am creating LWS directly (through `controller-runtime`) the workload is admitted just fine. I have

```
internalCertManagement
  enable: true
```
and I see separate `lws-webhook-server-cert` and `kueue-wehbook-server-cert` secrets. It seems like a race condition though since it only happens *most* of the time. If I try to install enough times, the webhooks pass (or at least don't error in a noticeable way). Also, sometimes it'll error on the validating webhook as well:

```
Error: INSTALLATION FAILED: 1 error occurred:
        * Internal error occurred: failed calling webhook "vleaderworkerset.kb.io": failed to call webhook: Post "https://lws-webhook-service.namespace.svc:443/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset?timeout=10s": tls: failed to verify certificate: x509: certificate is valid for kueue-webhook-service.namespace.svc, not lws-webhook-service.namespace.svc
```

Since it seems like it'll be pretty difficult to reproduce on your sides, do you have any ideas of what I should look into? Any tips on cert management I can look into to debug this further myself?

### Comment by [@andrew0li](https://github.com/andrew0li) — 2025-05-12T14:09:03Z

@mimowo Doing some more investigation and when creating a plain LWS repeatedly I get the same flakiness issue where the apiserver seems to be confusing webhook servers/certs:

```
$ k apply -f out.yaml
Error from server (InternalError): error when creating "out.yaml": Internal error occurred: failed calling webhook "vleaderworkerset.kb.io": failed to call webhook: Post "https://lws-webhook-service.namespace.svc:443/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset?timeout=10s": tls: failed to verify certificate: x509: certificate is valid for kueue-webhook-service.namespace.svc, not lws-webhook-service.namespace.svc
$ k apply -f out.yaml
Error from server (InternalError): error when creating "out.yaml": Internal error occurred: failed calling webhook "vleaderworkerset.kb.io": failed to call webhook: Post "https://lws-webhook-service.namespace.svc:443/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset?timeout=10s": tls: failed to verify certificate: x509: certificate is valid for kueue-webhook-service.namespace.svc, not lws-webhook-service.namespace.svc
$ k apply -f out.yaml
leaderworkerset.leaderworkerset.x-k8s.io/lws-test-2 created
```

Actually, changing the webhook names also didn't help... so probably not a collision issue
```
Error: 1 error occurred:
	* Internal error occurred: failed calling webhook "vxleaderworkerset.kb.io": failed to call webhook: Post "https://lws-webhook-service.namespace.svc:443/validate-leaderworkerset-x-k8s-io-v1-leaderworkerset?timeout=10s": tls: failed to verify certificate: x509: certificate is valid for kueue-webhook-service.namespace.svc, not lws-webhook-service.namespace.svc
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-12T18:37:00Z

@andrew0li I'm not sure about this issue. 

Let's start with a sanity check: Are you installing both controllers into the same namespace or different? I'm wondering maybe both controllers save their secrets in the same place. This could explain why it is flake - it is only a problem if both controllers concurrently (roughly at the same time) write / read the secret.

### Comment by [@andrew0li](https://github.com/andrew0li) — 2025-05-12T18:44:36Z

@mimowo I suspected the same. They are in the same namespace but I see two secrets, `lws-webhook-server-cert` and `kueue-webhook-server-cert` which makes sense because I have internal cert management enabled for both. I also checked the certs inside the secrets: they have the correct CAs and SANs (`kueue-ca` and `lws-ca` with different service names for SANs). I'm going to try a clean install with default as well.

Also worth noting I tried using `cert-manager`, but I get "signed by unknown CA" errors when I setup a self-signed issuer and issue separate certs/add inject-ca-from annotation for both services.

### Comment by [@andrew0li](https://github.com/andrew0li) — 2025-05-12T19:12:36Z

Seems like its an issue with webhook cleanup when Kueue is uninstalled. I am able to reproduce this on a plain Kind install with 1 control plane/2 workers:

1. Install LWS v0.1.0 via Helm (no custom values) into a namespace (I called it `system`)
2. Install Kueue with Helm with the following values into that same namespace. 
```
nameOverride: kueue
fullnameOverride: kueue # since webhook/secret names are hardcoded
managerConfig:
  controllerManagerConfigYaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8443
    # enableClusterQueueResources: true
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: c1f6bfd2.kueue.x-k8s.io
    controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 50
      burst: 100
    #pprofBindAddress: :8083
    waitForPodsReady:
      enable: true
      timeout: 5m
      recoveryTimeout: 3m
      blockAdmission: false
      requeuingStrategy:
        timestamp: Eviction
    #    backoffLimitCount: null # null indicates infinite requeuing
    #    backoffBaseSeconds: 60
    #    backoffMaxSeconds: 3600
    #manageJobsWithoutQueueName: true
    internalCertManagement:
      enable: true
    managedJobsNamespaceSelector:
      matchExpressions:
       - key: kubernetes.io/metadata.name
         operator: NotIn
         values: [ kube-system, system ] # same namespace as LWS/Kueue
    integrations:
      frameworks:
      - "batch/job"
      - "kubeflow.org/mpijob"
      - "jobset.x-k8s.io/jobset"
      - "pod"
    #  - "deployment" (requires enabling pod integration)
    #  - "statefulset" (requires enabling pod integration)
      - "leaderworkerset.x-k8s.io/leaderworkerset"
    #fairSharing:
    #  enable: true
    #  preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
    #resources:
    #  excludeResourcePrefixes: []
    # transformations:
    # - input: nvidia.com/mig-4g.5gb
    #   strategy: Replace | Retain
    #   outputs:
    #     example.com/accelerator-memory: 5Gi
    #     example.com/accelerator-gpc: 4
```
3. Uninstall and reinstall Kueue into the same namespace, i.e. `system`.

Now when creating a LWS (without specifying a queue name), after a few attempts I get:

```
$ kubectl create -f out.yaml
Error from server (InternalError): error when creating "out.yaml": Internal error occurred: failed calling webhook "mleaderworkerset.kb.io": failed to call webhook: Post "https://lws-webhook-service.system.svc:443/mutate-leaderworkerset-x-k8s-io-v1-leaderworkerset?timeout=10s": tls: failed to verify certificate: x509: certificate is valid for kueue-webhook-service.system.svc, not lws-webhook-service.system.svc
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-13T09:52:02Z

Ah, I suspect that because the two services are in the same namespace, then the endpoint picks up pods created by both services. This would explain flakiness due to load balancer. Check if you have only one entry here, as below, or two because the endpoints match both kueue and lws services.

```
> k get endpoints -nkueue-system kueue-webhook-service  
NAME                    ENDPOINTS          AGE
kueue-webhook-service   10.244.1.71:9443   15h
```

### Comment by [@andrew0li](https://github.com/andrew0li) — 2025-05-13T13:20:14Z

You are an absolute lifesaver @mimowo it looks like LWS service selector was not specific enough and was selecting both LWS and Kueue controllers:

```
Name:                     lws-webhook-service
Namespace:                system
Labels:                   app.kubernetes.io/instance=webhook-service
                          app.kubernetes.io/managed-by=Helm
                          app.kubernetes.io/name=lws
                          app.kubernetes.io/version=v0.5.1
                          helm.sh/chart=lws-0.1.0
Annotations:              meta.helm.sh/release-name: lws
                          meta.helm.sh/release-namespace: system
Selector:                 control-plane=controller-manager
```

In general are these controllers meant to live in separate namespaces? I'm trying to package an entire stack into one namespace so all my control plane components are in one namespace (i.e. easier for packages like Kueue to ignore just one or two namespaces), but should I split them up?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-13T13:27:56Z

> In general are these controllers meant to live in separate namespaces?

not really. It should be possible to place them in the same namespace too. However, this was my suspicion as a potential place to look for a bug, because this is something we are not testing in our CI.

> Selector:                 control-plane=controller-manager

Yes, this looks like the root cause, I think it should be fixed in LWS.

For comparison the selector in Kueue is specific:

`k get service/kueue-webhook-service -nkueue-system -oyaml` returns:
```yaml
  selector:
    app.kubernetes.io/instance: kueue
    app.kubernetes.io/name: kueue
    control-plane: controller-manager
```
while `k get service/lws-webhook-service -nlws-system -oyaml` for 0.6.1:
```yaml
  selector:
    control-plane: controller-manager
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-13T13:31:18Z

I have opened https://github.com/kubernetes-sigs/lws/issues/528 in LWS.
cc @kannon92  @ahg-g 

I think we can close it in Kueue.
/close
