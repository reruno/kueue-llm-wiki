# Issue #9965: Helm chart: Support custom cert-manager Issuer/ClusterIssuer

**Summary**: Helm chart: Support custom cert-manager Issuer/ClusterIssuer

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9965

**Last updated**: 2026-03-31T04:52:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-17T20:04:09Z
- **Updated**: 2026-03-31T04:52:15Z
- **Closed**: 2026-03-31T04:52:15Z
- **Labels**: `help wanted`
- **Assignees**: [@MatteoFari](https://github.com/MatteoFari)
- **Comments**: 5

## Description

### What would you like to be added?

When `enableCertManager: true` is set in the Helm chart, the chart always creates a self-signed `Issuer` and hardcodes the `issuerRef` in all three `Certificate` resources (webhook, visibility server, metrics). There is no way to reference a pre-existing `Issuer` or `ClusterIssuer`.

Many organizations manage certificates centrally using a shared `ClusterIssuer` backed by an internal CA, HashiCorp Vault, AWS PCA, or similar. Currently, the only workaround is to fork the chart or use a Helm post-renderer to patch the generated resources.

### Proposed change

Add an optional `certManager.issuerRef` value that, when set, is used in place of the auto-generated self-signed issuer. When not set, the current behavior is preserved.

**values.yaml:**

```yaml
enableCertManager: false
certManager:
  # -- Override the default self-signed issuer. When set, the chart
  #    skips creating its own Issuer and uses this reference instead.
  # issuerRef:
  #   name: "my-cluster-issuer"
  #   kind: "ClusterIssuer"
  #   group: "cert-manager.io"
```

**Template logic (certificate.yaml and others):**

```yaml
{{- if .Values.enableCertManager }}
{{- if not .Values.certManager.issuerRef }}
# Only create the self-signed Issuer when no custom issuerRef is provided
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: '{{ include "kueue.fullname" . }}-selfsigned-issuer'
  namespace: '{{ .Release.Namespace }}'
spec:
  selfSigned: {}
{{- end }}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: '{{ include "kueue.fullname" . }}-serving-cert'
  namespace: '{{ .Release.Namespace }}'
spec:
  dnsNames:
    - '{{ include "kueue.fullname" . }}-webhook-service.{{ .Release.Namespace }}.svc'
    - '{{ include "kueue.fullname" . }}-webhook-service.{{ .Release.Namespace }}.svc.{{ .Values.kubernetesClusterDomain }}'
  issuerRef:
    {{- if .Values.certManager.issuerRef }}
    {{- toYaml .Values.certManager.issuerRef | nindent 4 }}
    {{- else }}
    kind: Issuer
    name: '{{ include "kueue.fullname" . }}-selfsigned-issuer'
    {{- end }}
  secretName: '{{ include "kueue.fullname" . }}-webhook-server-cert'
{{- end }}
```

The same pattern would apply to `certificate-visibility-server.yaml` and `certificate-metrics.yaml`.

### Why is this needed?

- Self-signed certificates are often not acceptable in production environments with strict PKI requirements.
- Users who already have a cert-manager `ClusterIssuer` configured should be able to reuse it without forking the chart.
- This is a non-breaking, additive change — the default behavior remains unchanged.

### Prior art

Other Kubernetes Helm charts already support this pattern:

- **kube-prometheus-stack**: Supports an optional [`issuerRef`](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/templates/prometheus-operator/certmanager.yaml) under `prometheusOperator.admissionWebhooks.certManager`. When set, the chart skips self-signed issuer creation and uses the provided reference. ([values.yaml](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml), [related issue](https://github.com/prometheus-community/helm-charts/issues/6017))

- **Rancher**: Supports custom issuers via [`ingress.tls.source`](https://github.com/rancher/server-chart/blob/master/rancher/templates/ingress.yaml) and `ingress.tls.issuerName`, allowing users to specify a `ClusterIssuer` or namespace-scoped `Issuer`. ([related issue](https://github.com/rancher/rancher/issues/16178))

### Related issues

- #6152 — Kueue Controller-Manager and client certs provided by apiserver (related but focuses on trusting external CAs rather than configuring the issuer)

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-17T20:04:56Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-17T20:04:59Z

@kannon92: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9965):

>/help 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-18T18:05:08Z

@MatteoFari

if you comment on here you can assign this to yourself.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-18T18:05:16Z

https://github.com/kubernetes-sigs/kueue/pull/9984

### Comment by [@MatteoFari](https://github.com/MatteoFari) — 2026-03-19T08:52:29Z

Alright @kannon92 lmk if improvements are needed.
/assign
