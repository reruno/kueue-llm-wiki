# Issue #3259: Cannot find CA bundle to use for Prometheus scraper with TLS verification enabled.

**Summary**: Cannot find CA bundle to use for Prometheus scraper with TLS verification enabled.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3259

**Last updated**: 2025-05-09T10:58:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rvasahu-amazon](https://github.com/rvasahu-amazon)
- **Created**: 2024-10-17T21:11:47Z
- **Updated**: 2025-05-09T10:58:41Z
- **Closed**: 2025-05-09T10:58:29Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 16

## Description

Hi, hope you're well.

I'm trying to set up a Prometheus scraper to access the Kueue metrics endpoint.

```
---
# create configmap for prometheus scrape config
apiVersion: v1
data:
  # prometheus config
  prometheus.yaml: |
    global:
      scrape_interval: 1m
      scrape_timeout: 10s
    scrape_configs:
    - job_name: 'kueue_metrics'
      scheme: https
      tls_config:
        insecure_skip_verify: false
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
...
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring-ns
```

Since this needs to be productionised, ideally we'd like `insecure_skip_verify` under `tls_config` to be false. I understand that the scraper would need a CA bundle corresponding to the CA that was used to create the self-signed cert for TLS handshake. There isn't much Kueue documentation I can find on this, so I'm having trouble determining how to find and use this cert.

I have a couple questions:
1. Is there a CA bundle somewhere that would contain a cert for the metrics endpoint? I could then presumably mount and use the bundle. Alternatively, how should I get a cert for subject `kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local`?
2. Is it possible that using TLS verification for accessing the metrics endpoint is not a supported use-case? For example, I can see [this](https://github.com/kubernetes-sigs/kueue/blob/587a6fc6f87072685ae7a64d6652b713fa78d790/charts/kueue/templates/prometheus/monitor.yaml#L15) service monitor does not use TLS verification:

```
...
spec:
  endpoints:
  - bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
    path: /metrics
    port: https
    scheme: https
    tlsConfig:
      insecureSkipVerify: true
...
```

I would appreciate your insight. Thanks in advance for your help, much appreciated.

## Discussion

### Comment by [@rvasahu-amazon](https://github.com/rvasahu-amazon) — 2024-10-17T21:29:02Z

I wanted to add some details about what I've done to look into this so far without cluttering the main body of the issue.

My current understanding is (and please correct me if I'm wrong):
1. The cluster default certificate authority is not used by Kueue (so `ca.crt` at the same location as `token` doesn't work). 
2. Kueue has an internal CA that is used for the webhook service, which can be disabled and replaced by an external one if need be. However this is not the CA used for the prometheus metrics server. 
3. Instead, there is separate one used for `kueue-controller-manager`, including the pod and metrics service.

On those first two points, I checked this by curling the metrics endpoint from within my cluster. This is relevant in that if a cert I use to manually curl the endpoint works, the prometheus scraper is able to use that same cert.

Skipping verification worked for viewing metrics, which is what's expected:
```
% curl -i https://kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local:8443/metrics -H "Authorization: Bearer $TOKEN" -k
# metrics outputted
```

However, when attempting to use certs, I was not able to do so:

```
% curl -i https://kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local:8443/metrics -H "Authorization: Bearer $TOKEN" --cacert /path/to/some/cert.crt
curl: (60) SSL certificate problem: self-signed certificate in certificate chain

```

I used the cluster default `ca.crt` and the webhook service `.crt`, TLS handshake failed in both cases. 

For point 3, what I then tried is getting the full certificate chain from the server:

```
% openssl s_client -connect kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local:8443 -showcerts
```

I used the first cert in the chain to try and curl the endpoint. At this point, TLS handshake succeeded, but there was a hostname mismatch:

```
...
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
...
* Server certificate:
*  subject: CN=kueue-controller-manager-684c94f946-wt9gf@1727221200
*  start date: Sep 24 22:39:59 2024 GMT
*  expire date: Sep 24 22:39:59 2025 GMT
*  subjectAltName does not match kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local
* SSL: no alternative certificate subject name matches target host name 'kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local'
* Closing connection
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (OUT), TLS alert, close notify (256):
curl: (60) SSL: no alternative certificate subject name matches target host name 'kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local'
...
```

I surmise that there must be a CA bundle that was issued by the same CA, and this bundle would have a cert for `kueue-controller-manager-metrics-service.kueue-system.svc.cluster.local`.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-18T06:52:40Z

Thank you for the summary. It will be very useful for investigation. 

I'm not yet familiar with this, and it might be chellanging given we are two weeks from the planned 0.9 release, but maybe @tenzen-y or @alculquicondor already have some relevant knowledge here. 

Also, as a pointer you may check how Kueue is setup with Prometheus in this project which is our go to setup: https://github.com/GoogleCloudPlatform/ai-on-gke, the best-practices section. Maybe it solves the issue you mention, but I'm not sure..
cc @mbobrovskyi

### Comment by [@sky333999](https://github.com/sky333999) — 2024-10-18T07:00:26Z

Looks like even the referenced project uses `insecureSkipVerify: true` as per [this](https://github.com/GoogleCloudPlatform/ai-on-gke/blob/0400243c87aff3dd71ab614920e6c87318738eee/best-practices/gke-batch-refarch/02_platform/monitoring/kueue-service-monitoring.yaml#L15).

I see there's an opt-in for cert-manager with the webhook server but the visibility server seems to only use self signed certs with no configuration exposed - any reason for the diff in approaches?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-18T12:23:15Z

We have mainly tested self-signed certificates. The reason for this was simplicity of the deployment and lack of user demand.
If you manage to get it working, we would be happy to review guides and changes, for example, to support cert-manager in the visibility API.

### Comment by [@rvasahu-amazon](https://github.com/rvasahu-amazon) — 2024-10-21T15:57:03Z

Hi @alculquicondor @mimowo,

Thanks for the information, this is much appreciated. Unfortunately we don't have bandwidth to take this up right now. We can try looking into this later, and we'll make sure to share updates when we do. In the meantime, we will go ahead with self-signed certs.

If it isn't too much trouble, I have one more question. How easy would it be for a third party to spoof a Kueue self-signed cert? Is there any security testing done along these lines?

Thanks once again.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-21T16:06:55Z

We haven't conducted such testing.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T08:30:43Z

IIUC this PR will open the possibility of using cert-manager for metrics: https://github.com/kubernetes-sigs/kueue/pull/3760, looking at the example project in kubebuilder using the new controller-runtime mechanism: https://github.com/kubernetes-sigs/kubebuilder/blob/e07823e33190b4d3b9339a8273183187b9b50535/testdata/project-v4/cmd/main.go#L129-L133. I think we would need to set the parameters based on some Kueue configuration. Added also a comment to x-ref the discussions: https://github.com/kubernetes-sigs/kueue/pull/3760#discussion_r1886374650

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-03T19:30:54Z

> IIUC this PR will open the possibility of using cert-manager for metrics: #3760, looking at the example project in kubebuilder using the new controller-runtime mechanism: https://github.com/kubernetes-sigs/kubebuilder/blob/e07823e33190b4d3b9339a8273183187b9b50535/testdata/project-v4/cmd/main.go#L129-L133. I think we would need to set the parameters based on some Kueue configuration. Added also a comment to x-ref the discussions: [#3760 (comment)](https://github.com/kubernetes-sigs/kueue/pull/3760#discussion_r1886374650)

Could we open a dedicated issue, and setting the [`metricsServer` options](https://github.com/kubernetes-sigs/kubebuilder/blob/e07823e33190b4d3b9339a8273183187b9b50535/testdata/project-v4/cmd/main.go#L129-L133) based on the [`internalCertManagement.enable`](https://github.com/kubernetes-sigs/kueue/blob/604f460a059f3e0ba8e1854feb78ca594e15228e/config/components/manager/controller_manager_config.yaml#L39-L40) parameter?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-07T10:25:27Z

> Could we open a dedicated issue, and setting the metricsServer options based on the internalCertManagement.enable parameter?

Sounds reasonable, so we would extend the `internalCertManagement` with the `metricsServer` field which would contain configuration for the metricsServer options?

Any particular reason for a dedicated issue rather than reusing this one? I'm fine either way.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T20:57:56Z

> Sounds reasonable, so we would extend the internalCertManagement with the metricsServer field which would contain configuration for the metricsServer options?

I imagined that we specify following metrics server options when the `internalCertManagement.enable: false`. So, I did not indicate the Kueue Config API. WDYT?

https://github.com/kubernetes-sigs/kubebuilder/blob/e07823e33190b4d3b9339a8273183187b9b50535/testdata/project-v4/cmd/main.go#L129-L133

> Any particular reason for a dedicated issue rather than reusing this one? I'm fine either way.

I do not have a stronger opinion of that. So, I'm ok with either issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-09T08:51:00Z

> I imagined that we specify following metrics server options when the internalCertManagement.enable: false. So, I did not indicate the Kueue Config API. WDYT?

Hm, interesting, so when the user sets `internalCertManagement.enable: false` you just "uncomment" the metrics server options. 

This could work, but I would like to first understand the following:
1. IIUC the `internalCertManagement` is currently used for webhooks server, so it would create a coupling for the certs management between the webhooks and metrics servers, right? Meaning we cannot use internal certs manager for webhook and external for metrics server, or vice versa - maybe that is ok to reduce the configuration burden.
2. Do you know if we currently support external certs for webhooks when `internalCertManagement.enable: false`, or then the endpoint is unprotected at all?
3. IIUC conceptually there are 3 states: use internal certs manager, use external certs, and don't protect the endpoint at all. So bool might not be enough, unless we only support the first two options.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-09T09:42:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-09T10:39:20Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-09T10:58:24Z

/close
I believe this is already addressed by https://github.com/kubernetes-sigs/kueue/issues/4377.

Feel free to re-open if there are still some gaps.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-09T10:58:30Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3259#issuecomment-2866118686):

>/close
>I believe this is already addressed by https://github.com/kubernetes-sigs/kueue/issues/4377.
>
>Feel free to re-open if there are still some gaps.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-09T10:58:40Z

cc @kannon92
