# Issue #4330: ServiceMonitor TLS Verification Failure: Missing IP SAN in Self-Signed Certificate

**Summary**: ServiceMonitor TLS Verification Failure: Missing IP SAN in Self-Signed Certificate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4330

**Last updated**: 2025-11-22T08:04:23Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@sbathgate](https://github.com/sbathgate)
- **Created**: 2025-02-19T19:05:38Z
- **Updated**: 2025-11-22T08:04:23Z
- **Closed**: 2025-11-22T08:04:22Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Prometheus was unable to scrape the kueue controller-manager's metrics endpoint due to a TLS certificate verification error. The self-signed certificate used by the built-in certs did not include the IP address in its SANs, resulting in the error:  
```
tls: failed to verify certificate: x509: cannot validate certificate for xxx.xxx.xxx.xxx because it doesn’t contain any IP SANs
```
**What you expected to happen**:
The ServiceMonitor should successfully scrape the metrics endpoint over HTTPS, and Prometheus should display the metrics as "up" without any TLS errors.

**How to reproduce it (as minimally and precisely as possible)**:

1. Deploy the kueue controller-manager using the built-in self-signed certificates (not using cert-manager) and enablePrometheus.
```yaml
enablePrometheus: true
enableCertManager: false
```

3.	Observe that Prometheus logs show a TLS error similar to:
```
Get "https://xxx.xxx.xxx.xxx:8443/metrics": tls: failed to verify certificate: x509: cannot validate certificate for xxx.xxx.xxx.xxx because it doesn't contain any IP SANs
```

**Anything else we need to know?**:
The issue was resolved by specifying a serverName in the tlsConfig section of the ServiceMonitor. The serverName value must match the Common Name (or one of the SANs) on the self-signed certificate. The updated ServiceMonitor configuration could be achieved as shown below:
```
spec:
  endpoints:
  - bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
    path: /metrics
    port: https
    scheme: https
    tlsConfig:
      insecureSkipVerify: true
      serverName: {{ include "kueue.fullname" . }}-controller-manager-metrics-service.{{ .Release.Namespace }}.svc
```
By adding the serverName field, Prometheus now verifies the certificate against the expected hostname rather than the IP address, which resolved the TLS error.

**Environment**:
	•	Kubernetes version (use kubectl version): 1.27.10
	•	Kueue version (use git describe --tags --dirty --always): v0.10.1
	•	Cloud provider or hardware configuration: OpenStack Ussuri
	•	OS (e.g: cat /etc/os-release): AlmaLinux8

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-23T20:06:28Z

Wow! Thank you the report and the recommended fix.

Would you be interested in contributing a patch for this?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-24T07:26:23Z

+1, IIUC, we should start by adjusting the config, [`config/components/prometheus/monitor.yaml`](https://github.com/kubernetes-sigs/kueue/blob/04609d6e1b76af93529101802180b60df0b1ff41/config/components/prometheus/monitor.yaml#L14). Then, the yaml for the chart is derived by `./hack/update-helm.sh` which may require an adjustment too.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-25T07:53:55Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-25T00:05:51Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-25T06:23:24Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-23T06:36:55Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T07:34:57Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-22T08:04:17Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-22T08:04:23Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4330#issuecomment-3566016643):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
